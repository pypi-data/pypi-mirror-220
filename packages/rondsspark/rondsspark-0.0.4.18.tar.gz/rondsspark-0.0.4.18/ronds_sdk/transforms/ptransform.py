from typing import TypeVar, Generic, Sequence, Optional, Callable, Union

from ronds_sdk import error
from ronds_sdk.dataframe import pvalue
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ronds_sdk.pipeline import Pipeline, AppliedPTransform
    from ronds_sdk.tools.utils import WrapperFunc


InputT = TypeVar('InputT')
OutputT = TypeVar('OutputT')
PTransformT = TypeVar('PTransformT', bound='PTransform')


class PTransform(object):
    # 默认, transform 不包含 side inputs
    side_inputs = ()  # type: Sequence[pvalue.AsSideInput]

    # used for nullity transforms
    pipeline = None  # type: Optional[Pipeline]

    # Default is unset
    _user_label = None  # type:  Optional[str]

    def __init__(self, label=None):
        # type:  (Optional[str]) -> None
        super().__init__()
        self.label = label

    @property
    def label(self):
        # type:  () -> str
        return self._user_label or self.default_label()

    @label.setter
    def label(self, value):
        # type: (Optional[str]) -> None
        self._user_label = value

    def default_label(self):
        # type: () -> str
        return self.__class__.__name__

    def expand(self,  # type: PTransform
               input_inputs,  # type: InputT
               action_func=None  # type: WrapperFunc
               ):
        # type: (...) -> OutputT
        if not self.validate_input_inputs(input_inputs):
            raise NotImplementedError(
                "transform not implemented: %s" % self.__class__.__name__)
        return pvalue.PCollection(input_inputs.pipeline,
                                  element_type=pvalue.PCollection,
                                  is_bounded=input_inputs.is_bounded,
                                  )

    @staticmethod
    def validate_input_inputs(input_inputs,
                              ):
        if isinstance(input_inputs, pvalue.PValue):
            return input_inputs.element_value is None
        if isinstance(input_inputs, list):
            for input in input_inputs:
                if not isinstance(input, pvalue.PValue) \
                        or input.element_value is not None:
                    return False
        if isinstance(input_inputs, dict):
            for input in input_inputs.values():
                if not isinstance(input, pvalue.PValue) \
                        or input.element_value is not None:
                    return False
        return True

    def __str__(self):
        return '<%s>' % self._str_internal()

    def __repr__(self):
        return '<%s at %s>' % (self._str_internal(), hex(id(self)))

    def _str_internal(self) -> str:
        return '%s(PTransform)%s%s%s' % (
            self.__class__.__name__,
            ' label=[%s]' % self.label if (hasattr(self, 'label') and self.label) else '',
            ' inputs=%s ' % str(self.inputs) if (hasattr(self, 'inputs') and self.inputs) else '',
            ' side_inputs=%s' % str(self.side_inputs) if self.side_inputs else ''
        )

    def __rrshift__(self, label):
        return _NamedPTransform(self, label)

    def __or__(self, right):
        """Used to compose PTransforms, e.g., ptransform1 | ptransform2."""
        if isinstance(right, PTransform):
            return _ChainedPTransform(self, right)
        return NotImplemented

    def __ror__(self, left, label):
        p_valueish, p_values = self._extract_input_p_values(left)
        if isinstance(p_values, dict):
            p_values = tuple(p_values.values())
        pipelines = [v.pipeline for v in p_values if isinstance(v, pvalue.PValue)]
        if not pipelines:
            if self.pipeline is not None:
                p = self.pipeline
            else:
                raise ValueError('"%s" requires a pipeline to be specified '
                                 'as there are no deferred inputs.' % self.label)
        else:
            p = self.pipeline or pipelines[0]
            for pp in pipelines:
                if p != pp:
                    raise ValueError(
                        'Mixing values in different pipelines is not allowed.'
                        '\n{%r} != {%r}' % (p, pp))
        # deferred = not getattr(p.runner, 'is_eager', False)
        self.pipeline = p
        result = p.apply(self, p_valueish, label)
        return result

    @staticmethod
    def extract_input_if_one_p_values(input_inputs) -> pvalue.PValue:
        """
        In most scenarios, if Collection contain one element, return the element directly
        :param input_inputs: inputs
        :return:
        """

        if isinstance(input_inputs, tuple) or isinstance(input_inputs, list):
            return input_inputs[0] if len(input_inputs) == 1 else input_inputs
        elif isinstance(input_inputs, dict):
            return next(iter(input_inputs.values())) if len(input_inputs) == 1 else input_inputs
        return input_inputs

    @staticmethod
    def extract_first_input_p_values(input_inputs) -> pvalue.PValue:
        """
        extract first input for use
        :param input_inputs: inputs
        :return: first input
        """
        if isinstance(input_inputs, tuple) or isinstance(input_inputs, list):
            return input_inputs[0]
        elif isinstance(input_inputs, dict):
            return next(iter(input_inputs.values()))
        assert isinstance(input_inputs, pvalue.PValue)
        return input_inputs

    @staticmethod
    def _extract_input_p_values(p_valueish):
        from ronds_sdk import pipeline
        if isinstance(p_valueish, pipeline.Pipeline):
            if not p_valueish.root_transform.outputs:
                p_begin = pvalue.PBegin(p_valueish)
                p_valueish.root_transform.add_output(p_begin, '__root')
            p_valueish = p_valueish.root_transform.outputs.get('__root')
        return p_valueish, {
            str(tag): value
            for (tag, value) in get_named_nested_p_values(p_valueish, as_inputs=True)
        }

    @staticmethod
    def _check_pcollection(p_coll):
        # type: (pvalue.PCollection) -> None
        if not isinstance(p_coll, pvalue.PCollection):
            raise error.TransformError('Expecting a PCollection argument.')
        if not p_coll.pipeline:
            raise error.TransformError('PCollection not part of a pipeline')


class ForeachBatchTransform(PTransform):

    def expand(self, input_inputs, action_func=None):
        raise NotImplementedError


def get_named_nested_p_values(p_valueish, as_inputs=False):
    if isinstance(p_valueish, tuple):
        fields = getattr(p_valueish, '_fields', None)
        if fields and len(fields) == len(p_valueish):
            tagged_values = zip(fields, p_valueish)
        else:
            tagged_values = enumerate(p_valueish)
    elif isinstance(p_valueish, list):
        if as_inputs:
            yield None, p_valueish
            return
        tagged_values = enumerate(p_valueish)
    elif isinstance(p_valueish, dict):
        tagged_values = p_valueish.items()
    else:
        if as_inputs or isinstance(p_valueish, pvalue.PValue):
            yield None, p_valueish
        return
    for tag, sub_value in tagged_values:
        for sub_tag, sub_sub_value in get_named_nested_p_values(
                sub_value, as_inputs=as_inputs):
            if sub_tag is None:
                yield tag, sub_sub_value
            else:
                yield '%s.%s' % (tag, sub_tag), sub_sub_value


class _NamedPTransform(PTransform):
    def __init__(self, transform, label):
        super().__init__(label)
        self.transform = transform

    def __ror__(self, p_valueish, _unused=None):
        return self.transform.__ror__(p_valueish, self.label)

    def expand(self, p_value):
        raise RuntimeError("Should never be expanded directly.")


class _ChainedPTransform(PTransform):
    def __init__(self, *parts):
        # type: (*PTransform) -> None
        super().__init__(label=self._chain_label(parts))
        self._parts = parts

    @staticmethod
    def _chain_label(parts):
        return '|'.join(p.label for p in parts)

    def __or__(self, right):
        if isinstance(right, PTransform):
            return _ChainedPTransform(*(self._parts + (right,)))
        return NotImplemented

    def expand(self, p_val):
        raise NotImplementedError
