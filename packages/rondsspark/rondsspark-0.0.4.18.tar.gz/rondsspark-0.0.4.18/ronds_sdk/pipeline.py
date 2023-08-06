import importlib
import logging
import re
import tempfile
import time
from collections import defaultdict
from types import TracebackType
from typing import Optional, List, Union, Mapping, Dict, Set, Any, Type

import unicodedata

from ronds_sdk import error
from ronds_sdk.options.pipeline_options import PipelineOptions
from ronds_sdk.transforms import ptransform
from ronds_sdk.dataframe import pvalue

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ronds_sdk.runners.runner import PipelineRunner, PipelineResult
    from ronds_sdk.transforms.ptransform import PTransform

__all__ = ['Pipeline', 'AppliedPTransform', 'PipelineVisitor']


class Pipeline(object):
    """
    Pipeline 对象代表 DAG, 由
    :class:`ronds_sdk.dataframe.pvalue.PValue` and
    :class:`ronds_sdk.transforms.ptransform.PTransform` 组成.

    PValue 是 DAG 的 nodes, 算子 PTransform 是 DAG 的 edges.

    所有应用到 Pipeline 的 PTransform 算子必须有唯一的 full label.
    """

    def __init__(self, options=None, argv=None):
        # type: (Optional[PipelineOptions], Optional[List[str]]) -> None
        """
        初始化 Pipeline
        :param options: 运行 Pipeline 需要的参数
        :param argv: 当 options=None 时, 用于构建 options
        """
        logging.basicConfig()

        # parse PipelineOptions
        if options is not None:
            if isinstance(options, PipelineOptions):
                self._options = options
            else:
                raise ValueError(
                    'Parameter options, if specified, must be of type PipelineOptions. '
                    'Received : %r' % options)
        elif argv is not None:
            if isinstance(argv, list):
                self._options = PipelineOptions(argv)
            else:
                raise ValueError(
                    'Parameter argv, if specified, must be a list. Received : %r' %
                    argv)
        else:
            self._options = PipelineOptions([])

        self.local_tempdir = tempfile.mkdtemp(prefix='ronds-pipeline-temp')

        self.root_transform = AppliedPTransform(None, None, '', None, is_root=True)
        # Set of transform labels (full labels) applied to the pipeline.
        # If a transform is applied and the full label is already in the set
        # then the transform will have to be cloned with a new label.
        self.applied_labels = set()  # type: Set[str]
        # Create a ComponentIdMap for assigning IDs to components.
        self.component_id_map = ComponentIdMap()
        # Records whether this pipeline contains any external transforms.
        self.contain_external_transforms = False
        self.job_context = None

    @property
    def options(self):
        return self._options

    def _root_transform(self):
        # type: () -> AppliedPTransform
        """
        返回 root transform
        :return: root transform
        """
        return self.root_transform

    def run(self):
        # type: () -> PipelineResult
        from ronds_sdk.runners.spark_runner import SparkRunner
        runner = SparkRunner(self.options)
        return runner.run_pipeline(self, self._options)

    def __enter__(self):
        return self

    def __exit__(self,
                 exc_type,  # type: Optional[Type[BaseException]]
                 exc_val,  # type: Optional[BaseException]
                 exc_tb  # type: Optional[TracebackType]
                 ):
        start = time.time()
        try:
            if not exc_type:
                self.result = self.run()
                self.result.wait_until_finish()
        finally:
            end = time.time()
            logging.info('pipeline exited, cost: %s ~' % str(end - start))

    def visit(self, visitor):
        # type: (PipelineVisitor) -> None
        self._root_transform().visit(visitor, )

    def apply(self,
              transform,  # type: ptransform.PTransform
              p_valueish=None,  # type: Optional[pvalue.PValue]
              label=None  # type: Optional[str]
              ):
        # type: (...) -> pvalue.PValue
        # noinspection PyProtectedMember
        if isinstance(transform, ptransform._NamedPTransform):
            self.apply(transform.transform, p_valueish, label or transform.label)
        if not isinstance(transform, ptransform.PTransform):
            raise TypeError("Expected a PTransform object, got %s" % transform)
        full_label = label or transform.label
        if full_label in self.applied_labels:
            raise RuntimeError(
                'A transform with label "%s" already exists in the pipeline. '
                'To apply a transform with a specified label write '
                'pvalue | "label" >> transform' % full_label)
        self.applied_labels.add(full_label)

        # noinspection PyProtectedMember
        p_valueish, inputs = transform._extract_input_p_values(p_valueish)
        try:
            if not isinstance(inputs, dict):
                inputs = {str(ix): inp for (ix, inp) in enumerate(inputs)}
        except TypeError:
            raise NotImplementedError(
                'Unable to extract PValue inputs from %s; either %s does not accept '
                'inputs of this format, or it does not properly override '
                '_extract_input_p_values' % (p_valueish, transform))
        for t, leaf_input in inputs.items():
            if not isinstance(leaf_input, pvalue.PValue) or not isinstance(t, str):
                raise NotImplementedError(
                    '%s does not properly override _extract_input_p_values, '
                    'returned %s from %s' % (transform, inputs, p_valueish))
        current = AppliedPTransform(
            p_valueish.producer, transform, full_label, inputs
        )
        p_valueish.add_consumer(current)
        try:
            p_valueish_result = self.expand(transform, p_valueish, self._options)

            for tag, result in ptransform.get_named_nested_p_values(p_valueish_result):
                assert isinstance(result, pvalue.PValue)

                if result.producer is None:
                    result.producer = current

                assert isinstance(result.producer.inputs, tuple)
                base = tag
                counter = 0
                while tag in current.outputs:
                    counter += 1
                    tag = '%s_%d' % (base, counter)

                current.add_output(result, tag)
        except Exception as r:
            logging.error('unexpected error: %s' % repr(r))
            raise r
        return p_valueish_result

    @staticmethod
    def expand(transform,  # type: PTransform
               input,
               options,  # type: PipelineOptions
               ):
        # sp_transform = self.load_spark_transform(transform)
        return transform.expand(input)


class AppliedPTransform(object):
    """
    A transform node representing an instance of applying a PTransform
    """

    def __init__(self,
                 parent,  # type: Optional[AppliedPTransform]
                 transform,  # type: Optional[ptransform],
                 full_label,  # type: str
                 main_inputs,  # type: Optional[Mapping[str, Union[pvalue.PBegin, pvalue.PCollection]]]
                 environment_id=None,  # type: Optional[str]
                 annotations=None,  # type: Optional[Dict[str, bytes]]
                 is_root=False  # type: bool
                 ):
        # type: (...) -> None
        self.parent = parent
        self.transform = transform
        self.full_label = full_label
        self.main_input = dict(main_inputs or {})

        self.side_input = tuple() if transform is None else transform.side_inputs
        self.outputs = {}  # type: Dict[Union[str, int, None], pvalue.PValue]
        self.parts = []  # type: List[AppliedPTransform]
        self.environment_id = environment_id if environment_id else None  # type: Optional[str]
        self._is_root = is_root

    @property
    def inputs(self):
        # type: () -> tuple[Union[pvalue.PBegin, pvalue.PCollection]]
        return tuple(self.main_input.values())

    def is_root(self):
        # type: () -> bool
        return self._is_root

    def __repr__(self):
        # type: () -> str
        return "%s(%s, %s)" % (
            self.__class__.__name__, self.full_label, type(self.transform).__name__)

    def add_output(self,
                   output,  # type: Union[pvalue.PValue]
                   tag  # type: Union[str, int, None]
                   ):
        # (...) -> None
        if isinstance(output, pvalue.PValue):
            if tag not in self.outputs:
                self.outputs[tag] = output
            else:
                raise error.TransformError('tag[%s] has existed in outputs')
        else:
            raise TypeError("Unexpected out type: %s" % output)

    def add_part(self, part):
        # type: (AppliedPTransform) -> None
        assert isinstance(part, AppliedPTransform)
        self.parts.append(part)

    def is_composite(self):
        # type: () -> bool
        return bool(self.parts) or all(
            p_val.producer is not self for p_val in self.outputs.values()
        )

    def visit(self,
              visitor,  # type: PipelineVisitor
              ):
        # type: (...) -> None
        """Visits all nodes reachable from the current node."""
        if self._is_root and self.outputs and self.outputs['__root']:
            root = self.outputs['__root']
            assert isinstance(root, pvalue.PValue)
            for consumer in root.consumers:
                consumer.visit(visitor)
        elif visitor.visit_transform(self) and self.outputs:
            for p_value in self.outputs.values():
                assert isinstance(p_value, pvalue.PValue)
                p_value.visit(visitor)
        visitor.leave_transform(self)


class ComponentIdMap(object):
    """
    A utility for assigning unique component ids to Beam components.

    Component ID assignments are only guaranteed to be unique and consistent
    within the scope of a ComponentIdMap instance.
    """

    def __init__(self, namespace="ref"):
        self.namespace = namespace
        self._counters = defaultdict(lambda: 0)  # type:Dict[type, int]
        self._obj_to_id = {}  # type: Dict[Any, str]

    def get_or_assign(self, obj=None, obj_type=None, label=None):
        if obj not in self._obj_to_id:
            self._obj_to_id[obj] = self._unique_ref(obj, obj_type, label)
        return self._obj_to_id[obj]

    def _unique_ref(self, obj=None, obj_type=None, label=None):
        # Normalize, trim, and unify.
        prefix = self._normalize(
            "%s_%s_%s" % (self.namespace, obj_type.__name__, label or type(obj).__name__)
        )[0:100]
        self._counters[obj_type] += 1
        return '%s_%d' % (prefix, self._counters[obj_type])

    @staticmethod
    def _normalize(str_value):
        str_value = unicodedata.normalize('NFC', str_value)
        return re.sub(r'[^a-zA-Z0-9-_]+', '-', str_value)


class PipelineVisitor(object):
    """
    Visitor pattern class used to traverse a DAG of transforms
    """

    def __init__(self):
        self.stream_writers = list()
        self.module = None
        self.__trans_cache = dict()  # type: dict[PTransform, PTransform]

    def load_spark_transform(self,  # type: PipelineVisitor
                             transform,  # type: PTransform,
                             options=None,  # type: PipelineOptions
                             **kwargs,
                             ):
        # type: (...) -> PTransform
        # cache first
        if self.__trans_cache.__contains__(transform):
            return self.__trans_cache[transform]

        # create new PTransform
        if not self.module:
            self.module = importlib.import_module(self.transform_package(options))
        d = getattr(self.module, transform.__class__.__name__)
        if d:
            all_kwargs = dict()
            if 'options' in d.__dict__['__init__'].__code__.co_varnames:
                all_kwargs['options'] = options
            for key in kwargs.keys():
                if key in d.__dict__['__init__'].__code__.co_varnames:
                    all_kwargs[key] = kwargs[key]
            sp_trans = d(transform, **all_kwargs)
            self.__trans_cache[transform] = sp_trans
            return sp_trans
        else:
            raise NotImplementedError(
                "transform [%s] not implemented by Spark!" % transform.__class__.__name__)

    @staticmethod
    def transform_package(options):
        if options is None:
            raise error.PipelineError("load_spark_transform pipeline options is null!")
        return options.transform_package

    def visit_value(self, value):
        # type: (pvalue.PValue) -> bool
        """
        Callback for visiting a PValue in the pipeline DAG.
        :param value: PValue visited (typically a PCollection instance).
        :return:
        """
        return True

    def visit_transform(self, transform_node):
        # type: (AppliedPTransform) -> bool
        return True

    def leave_transform(self, transform_node):
        # type: (AppliedPTransform) -> None
        pass
