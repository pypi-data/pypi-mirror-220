from typing import TypeVar, Generic, Optional, Union

from ronds_sdk.transforms.core import Windowing
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ronds_sdk.pipeline import Pipeline, PipelineVisitor
    from ronds_sdk.pipeline import AppliedPTransform

T = TypeVar('T')


class PValue(object):
    """
    Base class for PCollection.
    主要特征:
        (1) 属于一个 Pipeline, 初始化时加入
        (2) 拥有一个 Transform 用来计算 value
        (3) 拥有一个 value, 如果 Transform执行后,该值拥有意义
    """

    def __init__(self,
                 pipeline,  # type: Pipeline
                 tag=None,  # type: Optional[str]
                 element_value=None,  # type: T
                 element_type=None,  # type: Optional[Union[type]],
                 windowing=None,  # type: Optional[Windowing]
                 is_bounded=True,
                 ):
        self.pipeline = pipeline
        self.tag = tag
        self.element_value = element_value
        self.element_type = element_type
        # The AppliedPTransform instance for the application of the PTransform
        # generating this PValue. The field gets initialized when a transform
        # gets applied.
        self.producer = None  # type: Optional[AppliedPTransform]
        self.consumers = list()  # type: list[AppliedPTransform]
        self.is_bounded = is_bounded
        if windowing:
            self._windowing = windowing
        self.requires_deterministic_key_coder = None

    def __str__(self):
        return self._str_internal()

    def __repr__(self):
        return '<%s at %s>' % (self._str_internal(), hex(id(self)))

    def _str_internal(self) -> str:
        return "%s[%s.%s]" % (
            self.__class__.__name__,
            self.producer.full_label if self.producer else None,
            self.tag
        )

    def apply(self, *args, **kwargs):
        """Applies a transform or callable to a PValue"""
        arg_list = list(args)
        arg_list.insert(1, self)
        return self.pipeline.apply(*arg_list, **kwargs)

    def visit(self,
              visitor,  # type: PipelineVisitor
              ):
        # type: (...) -> bool
        if visitor.visit_value(self) and self.consumers:
            for consumer in self.consumers:
                consumer.visit(visitor)
            return True
        return False

    def add_consumer(self,
                     consumer  # type: AppliedPTransform
                     ):
        self.consumers.append(consumer)


class PCollection(PValue, Generic[T]):

    def __init__(self,
                 pipeline,  # type: Pipeline
                 tag=None,  # type: Optional[str]
                 element_value=None,  # type: T
                 element_type=None,  # type: Optional[Union[type]],
                 windowing=None,  # type: Optional[Windowing]
                 is_bounded=True,
                 ):
        super(PCollection, self).__init__(pipeline, tag, element_value,
                                          element_type, windowing, is_bounded)

    def __eq__(self, other):
        if isinstance(other, PCollection):
            return self.tag == other.tag and self.producer == other.producer

    def __hash__(self):
        return hash((self.tag, self.producer))


class AsSideInput(object):
    def __init__(self, p_coll):
        # type: (PCollection) -> None
        self.pvalue = p_coll


class PBegin(PValue):
    """pipelines input 的 begin marker, 用于 create/read transforms"""
    pass


class PDone(PValue):
    """
    PDone 代表 transform 的 output,具有简单的结果, 例如 Write
    """

    def __init__(self,
                 pipeline,  # type: Pipeline
                 tag=None,  # type: Optional[str]
                 element_type=None,  # type: Optional[Union[type]],
                 windowing=None,  # type: Optional[Windowing]
                 is_bounded=True,
                 stream_writer=None,
                 ):
        super().__init__(pipeline, tag, element_type=element_type, windowing=windowing, is_bounded=is_bounded)
        self.stream_writer = stream_writer






















































