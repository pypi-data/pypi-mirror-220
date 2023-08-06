import sys
from datetime import date, datetime

from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession

import ronds_sdk.transforms.ronds as ronds
from ronds_sdk.options.pipeline_options import PipelineOptions, CassandraOptions
from ronds_sdk.pipeline import Pipeline
from ronds_sdk.tools.utils import RuleParser, ForeachBatchFunc

import findspark

from ronds_sdk.transforms.pandas.cassandra_rule import ForeachRule

findspark.init()


def mock_data():
    """离线模拟数据"""
    return [(1, 2., 'string1', date(2000, 1, 1), datetime(2000, 1, 1, 12, 0)),
            (2, 3., 'string2', date(2000, 2, 1), datetime(2000, 1, 2, 12, 0)),
            (3, 4., 'string3', date(2000, 3, 1), datetime(2000, 1, 3, 12, 0))]


def test_create():
    """创建离线数据处理流程"""
    with Pipeline() as pipeline:
        pipeline | "Create elements" >> ronds.Create(mock_data()) \
            | "Filter elements" >> ronds.Filter("_1", "_1 > '1'") \
            | "console" >> ronds.Console()


def test_socket():
    """创建实时数据流处理流程"""
    with Pipeline() as pipeline:
        pipeline | "Create Socket" >> ronds.Socket("localhost", 9999) \
            | "Filter elements" >> ronds.Filter("value", "value is not null") \
            | "console" >> ronds.Console('append')


def test_socket_multi():
    """创建实时数据流处理流程"""
    with Pipeline() as pipeline:
        p1 = pipeline | "Create Socket" >> ronds.Socket("localhost", 9999)
        p2 = p1 | "Filter elements" >> ronds.Filter("value", "value is not null")
        p3 = p1 | "Filter elements 2" >> ronds.Filter("value", "value ='spark'")
        p2 | "console" >> ronds.Console('append')
        p3 | "console 2" >> ronds.Console('append')


def test_rule_cassandra_scan_console():
    options = PipelineOptions(
        transform_package='ronds_sdk.transforms.pandas.transforms',
        # enable_executor_debug=True,
        spark_repartition_num=1,
        cassandra_window_duration=1,
        cassandra_start_datetime='2023-06-25 01:47:00',
        algorithm_path='AlgMock',
        algorithm_funcname='alg_mock.alg_mock'
    )
    with Pipeline(options=options) as p:
        p | "Rule Cassandra Scan" >> ronds.RulesCassandraScan('rule_config.json') \
            | "algorithm" >> ronds.Algorithm() \
            | "Console" >> ronds.Console()


def test_rule():
    print("test_rule path:" + str(sys.path))
    rule_parser = RuleParser('rule_config.json')
    rules = rule_parser.load()
    conf = SparkConf().setAppName("test").setMaster('local[2]')
    sc = SparkContext(conf=conf)
    df = sc.parallelize(rules)
    df.foreachPartition(prints)


def test_rule2():
    print(sys.path)
    rule_parser = RuleParser('rule_config.json')
    rules = rule_parser.load()
    spark = SparkSession.builder.master('local[2]').getOrCreate()
    df = spark.createDataFrame(rules)
    df = df.repartition(2, df.device_id)
    df.foreachPartition(prints)


def prints2(itr):
    print("prints path:" + str(sys.path))
    for r in itr:
        print(r)


def prints(itr):
    print(sys.modules.keys())
    print("prints path:" + str(sys.path))
    for_batch = ForeachBatchFunc(echo_r)
    for_rule = ForeachRule(CassandraOptions(), for_batch)
    for_rule.foreach_rules(itr)


def echo_r(df, epoch_id):
    print(epoch_id)


if __name__ == '__main__':
    # test_create()
    # test_socket()
    test_rule_cassandra_scan_console()
    # test_rule2()
    # test_rule()
