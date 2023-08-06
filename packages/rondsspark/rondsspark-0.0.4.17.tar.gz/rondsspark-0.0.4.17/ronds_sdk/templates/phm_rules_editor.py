import os
import sys

from ronds_sdk.tools.utils import GraphParser, RuleParser, to_bool


def run(rule_path,
        alg_path,
        alg_func,
        graph_path,
        spark_master_url=None,
        start_time=None,
        send_kafka_mock=False):
    # type: (str, str, str, str, str, str, bool) -> None
    import ronds_sdk as ronds
    sys.path.append(alg_path)
    # init params
    graph_parser = GraphParser(graph_path)
    rule_parser = RuleParser(rule_path)
    rules = rule_parser.load()
    spark_repartition_num = len(rules) if len(rules) < 1000 else 1000
    options = ronds.Options(
        enable_executor_debug=to_bool(os.getenv('EXECUTOR_DEBUG', False)),
        # spark
        transform_package='ronds_sdk.transforms.pandas.transforms',
        spark_repartition_num=spark_repartition_num,
        spark_master_url=spark_master_url,
        # algorithm
        algorithm_path=alg_path,
        algorithm_funcname=alg_func,
        # cassandra
        cassandra_window_duration=graph_parser.window_duration(),
        cassandra_start_datetime=start_time,
        cassandra_host=graph_parser.cassandra_host(),
        cassandra_keyspace=graph_parser.cassandra_keyspace(),
        cassandra_table_process=graph_parser.cassandra_process_table(),
        # kafka
        kafka_bootstrap_servers=graph_parser.kafka_bootstraps(),
        kafka_send_mock=send_kafka_mock,
    )

    # create and run pipeline
    with ronds.Pipeline(options=options) as p:
        p | 'Rule Cassandra Scan' >> ronds.RulesCassandraScan(rules) \
            | 'algorithm' >> ronds.Algorithm() \
            | 'send algorithm json kafka' >> ronds.SendAlgJsonKafka(graph_parser.kafka_source_topics())
