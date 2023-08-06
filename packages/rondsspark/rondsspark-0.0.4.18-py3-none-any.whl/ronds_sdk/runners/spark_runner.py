import logging

from pyspark.sql import SparkSession

from ronds_sdk.pipeline import PipelineVisitor
from ronds_sdk.dataframe import pvalue
from ronds_sdk.runners.runner import PipelineRunner, PipelineResult
from ronds_sdk.runners.visitors.spark_runner_visitor import SparkRunnerVisitor
from ronds_sdk.options.pipeline_options import PipelineOptions, SparkRunnerOptions

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ronds_sdk.transforms.ptransform import PTransform


class SparkRunner(PipelineRunner):

    def __init__(self,
                 options  # type: PipelineOptions
                 ):
        super(SparkRunner, self).__init__(options)
        import findspark
        findspark.init()
        self.spark_options = self.options.view_as(SparkRunnerOptions)
        self.spark = self.new_spark(self.spark_options)

    @staticmethod
    def new_spark(options):
        builder = SparkSession.builder
        logging.info("spark master url: %s" % options.spark_master_url)
        if options.spark_master_url is not None:
            builder.master(options.spark_master_url)
        return builder.getOrCreate()

    def transform_package(self):
        return self.spark_options.spark_transform_package

    def run_pipeline(self, pipeline, options):
        visitor = SparkRunnerVisitor(self.options, self.spark)
        pipeline.visit(visitor)
        stream_writers = visitor.stream_writers
        return SparkPipelineResult(stream_writers, 'STARTED')

    def apply(self,
              transform,  # type: PTransform
              input,
              options,  # type: PipelineOptions
              ):
        # sp_transform = self.load_spark_transform(transform)
        return transform.expand(input)


class SparkPipelineVisitor(PipelineVisitor):

    def visit_value(self, value):
        # type: (pvalue.PValue) -> bool
        if isinstance(value, pvalue.PDone):
            if value.stream_writer:
                self.stream_writers.append(value.stream_writer)
        return super().visit_value(value)


class SparkPipelineResult(PipelineResult):

    def __init__(self,
                 stream_writers,
                 state,
                 ):
        super(SparkPipelineResult, self).__init__(state)
        self._stream_writers = stream_writers

    def wait_until_finish(self, duration=None):
        await_list = list()
        if self._stream_writers:
            for w in self._stream_writers:
                query = w.start()
                await_list.append(query)
                logging.warning("query started, attention please ~")
        if await_list:
            for query in await_list:
                query.awaitTermination()
