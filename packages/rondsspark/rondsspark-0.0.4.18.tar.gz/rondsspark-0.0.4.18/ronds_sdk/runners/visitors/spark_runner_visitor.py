import logging

from typing import TYPE_CHECKING, List
from ronds_sdk import error
from ronds_sdk.dataframe import pvalue
from ronds_sdk.options.pipeline_options import PipelineOptions
from ronds_sdk.tools.utils import ForeachBatchFunc
from ronds_sdk.pipeline import PipelineVisitor
from ronds_sdk.transforms.ptransform import PTransform, ForeachBatchTransform

if TYPE_CHECKING:
    from ronds_sdk.pipeline import AppliedPTransform
    from pyspark.sql import SparkSession


def foreach_batch(df,
                  epoch_id,  # type: str
                  transform_root,  # type: AppliedPTransform
                  options,  # type: PipelineOptions
                  ):
    logging.info("batch_id: %s, consumer size: %d"
                 % (epoch_id, len(transform_root.outputs)))
    for p_coll in transform_root.outputs.values():
        p_coll.element_value = df
        p_coll.tag = epoch_id
        # todo 如果包含不可序列化对象, 此处会报序列化异常
        p_coll.visit(SparkRunnerVisitor(options))


class SparkRunnerVisitor(PipelineVisitor):
    def __init__(self,
                 options,  # type: PipelineOptions
                 spark=None,  # type: SparkSession
                 ):
        super(SparkRunnerVisitor, self).__init__()
        self._options = options
        self._spark = spark

    def visit_transform(self, transform_node):
        # type: (AppliedPTransform) -> bool
        transform = transform_node.transform  # type: PTransform
        sp_transform = self.load_spark_transform(transform, self._options, spark=self._spark)
        input_or_inputs = transform.extract_input_if_one_p_values(transform_node.inputs)
        # process SourceTransform
        p_coll = transform_node.outputs.get(None)
        if isinstance(sp_transform, ForeachBatchTransform):
            p_coll.is_bounded = True
            return self.visit_foreach_batch(sp_transform, transform_node, input_or_inputs)

        # process PTransform
        sp_coll = sp_transform.expand(input_or_inputs)
        if sp_coll is None:
            raise error.TransformError('Transform [%s] expand return None error!'
                                       % sp_transform.__class__.__name__)
        assert isinstance(sp_coll, pvalue.PValue)
        p_coll.element_value = sp_coll.element_value
        first_input = transform.extract_first_input_p_values(input_or_inputs)
        p_coll.is_bounded = first_input.is_bounded
        return super().visit_transform(transform_node)

    def visit_foreach_batch(self,
                            sp_transform,  # type: PTransform
                            transform_node,  # type: AppliedPTransform
                            first_input,  # type: pvalue.PValue
                            ):
        #  type: (...) -> bool
        p_coll = sp_transform.expand(first_input,
                                     ForeachBatchFunc(foreach_batch,
                                                      transform_root=transform_node,
                                                      options=self._options))
        if isinstance(p_coll, pvalue.PDone):
            self.stream_writers.append(p_coll.stream_writer)
        else:
            raise error.TransformError(
                "PDone output of SourceTransform expected, but [%s]" % p_coll)
        return False

    @staticmethod
    def get_first_output(transform_node  # type: AppliedPTransform
                         ):
        # type: (...) -> pvalue.PValue
        if transform_node.outputs:
            return next(iter(transform_node.outputs.values()))

    @staticmethod
    def is_stream_begin(p_values: List[pvalue.PValue]):
        if p_values and len(p_values) == 1:
            return not p_values[0].is_bounded
        return False
