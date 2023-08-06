import logging
import time

from ronds_sdk import error
from ronds_sdk.transforms.ptransform import PTransform, ForeachBatchTransform
from ronds_sdk.dataframe import pvalue
from ronds_sdk.runners.spark_runner import SparkRunner
from pyspark.sql import DataFrame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ronds_sdk.transforms import ronds


class Sleep(PTransform):

    def __init__(self,
                 _sleep  # type: ronds.Sleep
                 ):
        super(Sleep, self).__init__()
        self._sleep = _sleep

    def expand(self, input_inputs, action_func=None):
        logging.info("start sleep~")
        time.sleep(self._sleep.seconds)
        logging.info("end sleep~")
        return input_inputs


class Create(PTransform):
    def __init__(self,
                 create,  # type: ronds.Create
                 ):
        super(Create, self).__init__()
        self.values = create.values

    def expand(self, p_begin, action_func=None):
        assert isinstance(p_begin, pvalue.PBegin)
        df = get_spark(p_begin).createDataFrame(self.values)
        return pvalue.PCollection(p_begin.pipeline,
                                  element_value=df,
                                  element_type=DataFrame,
                                  is_bounded=True)


class Socket(ForeachBatchTransform):
    def __init__(self,
                 socket,  # type: ronds.Socket
                 ):
        super(Socket, self).__init__()
        self.host = socket.host
        self.port = socket.port

    def expand(self, p_begin, action_func=None):
        assert isinstance(p_begin, pvalue.PBegin)
        df = get_spark(p_begin).readStream \
            .format("socket") \
            .option("host", self.host) \
            .option("port", self.port) \
            .load()
        if action_func:
            writer = df.writeStream.foreachBatch(action_func.call)
            return pvalue.PDone(p_begin.pipeline,
                                element_type=DataFrame,
                                is_bounded=False,
                                stream_writer=writer)
        return pvalue.PCollection(p_begin.pipeline,
                                  element_type=DataFrame,
                                  element_value=df,
                                  is_bounded=False)


class Filter(PTransform):
    def __init__(self,
                 filter_,  # type: ronds.Filter
                 ):
        super(Filter, self).__init__()
        self.where = filter_.where
        self.select_cols = filter_.select_cols

    def expand(self, input_inputs, action_func=None):
        assert isinstance(input_inputs, pvalue.PCollection)
        if input_inputs.element_value:
            df = input_inputs.element_value
            assert isinstance(df, DataFrame)
            new_df = df.select(self.select_cols).where(self.where)
            return pvalue.PCollection(input_inputs.pipeline,
                                      element_value=new_df,
                                      element_type=DataFrame,
                                      is_bounded=input_inputs.is_bounded)
        raise error.PValueError(
            "unexpected input_inputs.element_value: %s" % input_inputs.tag)


class Console(PTransform):

    def __init__(self,
                 console,  # type: ronds.Console
                 ):
        super(Console, self).__init__('Console')
        self.mode = console.mode

    def expand(self, input_inputs, action_func=None):
        assert isinstance(input_inputs, pvalue.PCollection)
        df = input_inputs.element_value
        assert isinstance(df, DataFrame)
        if not df.isStreaming:
            df.show()
            return pvalue.PDone(input_inputs.pipeline,
                                element_type=DataFrame,
                                is_bounded=True)
        else:
            query = df.writeStream \
                .outputMode(self.mode) \
                .format("console")
            return pvalue.PDone(input_inputs.pipeline,
                                element_type=DataFrame,
                                is_bounded=False,
                                stream_writer=query)


def get_spark(p_coll: pvalue.PValue):
    """
    从 runner 中 获取 SparkSession
    :param p_coll: 数据集
    :return: SparkSession
    """
    if p_coll:
        runner = p_coll.pipeline.runner
        if isinstance(runner, SparkRunner):
            return runner.spark
        raise TypeError("expect SparkRunner, but found %s " % runner)
    else:
        raise error.PValueError("get_spark, PValue is null!")
