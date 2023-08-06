import importlib.machinery
import json
import logging
import sys
import time
from os.path import dirname, abspath
from typing import TYPE_CHECKING, Callable
from pathlib import Path

import pandas as pd
from pyspark.sql import DataFrame, SparkSession

from ronds_sdk import error, logger_config
from ronds_sdk.dataframe import pvalue
from ronds_sdk.datasources.kafka_manager import KafkaManager
from ronds_sdk.options.pipeline_options import SparkRunnerOptions, CassandraOptions, AlgorithmOptions, KafkaOptions
from ronds_sdk.tools.constants import JsonKey, Constant
from ronds_sdk.tools.utils import RuleParser
from ronds_sdk.transforms import ronds
from ronds_sdk.transforms.ptransform import PTransform, ForeachBatchTransform

if TYPE_CHECKING:
    from ronds_sdk.options.pipeline_options import PipelineOptions

logger_config.config()
logger = logging.getLogger('executor')


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


class RulesCassandraScan(ForeachBatchTransform):
    """
    基于配置规则信息, 定时轮询读取 Cassandra 数据, 整合成算法需要的 Graph JSON 结构, 用于后续的算法处理流程.
    """

    def __init__(self,
                 rule_load,  # type: ronds.RulesCassandraScan
                 options,  # type: PipelineOptions
                 spark=None,  # type: SparkSession
                 ):
        super(RulesCassandraScan, self).__init__()
        self._rules = rule_load.rules
        self._spark = spark
        self.__options = options

    @property
    def options(self):
        return self.__options

    def expand(self, p_begin, action_func=None):
        from ronds_sdk.transforms.pandas.cassandra_rule import ForeachRule
        foreach_rule = ForeachRule(self.options.view_as(CassandraOptions), action_func)
        if self._spark:
            repartition_num = self.options.view_as(SparkRunnerOptions).spark_repartition_num
            df = self._spark.createDataFrame(self._rules)
            df = df.repartition(repartition_num, df.assetId)
            if action_func:
                df.foreachPartition(foreach_rule.foreach_rules)
            return pvalue.PDone(p_begin.pipeline,
                                element_type=DataFrame,
                                is_bounded=True)
        else:
            df = pd.DataFrame(self._rules)
            return pvalue.PCollection(p_begin.pipeline,
                                      element_value=df,
                                      element_type=pd.DataFrame,
                                      is_bounded=True)


class Console(PTransform):

    def __init__(self,
                 console,  # type: ronds.Console
                 ):
        super(Console, self).__init__()
        self._mode = console.mode

    def expand(self, input_inputs, action_func=None):
        assert isinstance(input_inputs, pvalue.PCollection)
        df = input_inputs.element_value
        assert isinstance(df, pd.DataFrame)
        print('*' * 20)
        print(df.head(10))
        return pvalue.PDone(input_inputs.pipeline,
                            element_type=pd.DataFrame,
                            is_bounded=True)


class Algorithm(PTransform):

    def __init__(self,
                 algorithm,  # type: ronds.Algorithm
                 options,  # type: PipelineOptions
                 ):
        super(Algorithm, self).__init__()
        self._options = options.view_as(AlgorithmOptions) if options is not None \
            else AlgorithmOptions()
        self.path = algorithm.path if algorithm.path \
            else self._options.algorithm_path
        self.func_name = algorithm.func_name if algorithm.func_name \
            else self._options.algorithm_funcname
        # directory of RondsSpark/ronds_sdk/transforms/pandas
        self._base_dir = dirname(dirname(dirname(dirname(dirname(abspath(__file__))))))

        # load algorithm as module by path
        self._algorithm_func = self.__load_alg()

    @staticmethod
    def is_absolute(path: str) -> bool:
        p_obj = Path(path)
        return p_obj.is_absolute()

    @property
    def algorithm_func(self):
        return self._algorithm_func

    def __load_alg(self):
        """load algorithm by file path"""

        # load new algorithm func
        alg_absolute_path = self.path if self.is_absolute(self.path) \
            else '%s/%s' % (self._base_dir, self.path)
        if alg_absolute_path not in sys.path:
            sys.path.append(alg_absolute_path)
        func_paths = self.func_name.split('.')
        if len(func_paths) <= 1:
            raise error.TransformError("""algorithm func path expect the format: file.function_name, 
                                          but found: %s""" % self.func_name)
        model_path = '.'.join(func_paths[0:-1])
        func_name = func_paths[-1]
        loader = importlib.machinery.SourceFileLoader(model_path,
                                                      '%s/%s.py' % (alg_absolute_path, model_path))
        alg_model = loader.load_module(model_path)
        alg_func = getattr(alg_model, func_name)
        if alg_func is None:
            raise error.TransformError("""failed load algorithm """)
        return alg_func

    # noinspection SpellCheckingInspection
    def algorithm_call(self, row):
        device_id = row[JsonKey.DEVICE_ID.value]
        res_row = self.algorithm_func(row)
        if isinstance(res_row, dict):
            ret_row = res_row
        elif isinstance(res_row, str):
            ret_row = json.loads(res_row)
        else:
            raise error.TransformError('unexpected algorithm func return type: %s, value: %s'
                                       % (type(res_row), res_row))
        assert isinstance(ret_row, dict)
        if ret_row is not None and not ret_row.__contains__(JsonKey.DEVICE_ID.value):
            ret_row[JsonKey.DEVICE_ID.value] = device_id
        return ret_row

    def expand(self, input_inputs, action_func=None):
        assert isinstance(input_inputs, pvalue.PCollection)
        assert isinstance(input_inputs.element_value, pd.DataFrame)
        df = input_inputs.element_value
        if len(input_inputs.element_value) > 0:
            df_dict = input_inputs.element_value.to_dict('records')
            res_df_list = list()
            for row in df_dict:
                res_row = self.algorithm_call(row)
                res_df_list.append(res_row)
            logger.info('algorithm data: %s' % json.dumps(next(iter(res_df_list))))
            df = pd.DataFrame(res_df_list)
        assert isinstance(df, pd.DataFrame)
        return pvalue.PCollection(input_inputs.pipeline,
                                  element_value=df,
                                  element_type=pd.DataFrame,
                                  is_bounded=True)


class SendKafka(PTransform):

    def __init__(self,
                 send_kafka,  # type: ronds.SendKafka
                 options,  # type: PipelineOptions
                 ):
        super(SendKafka, self).__init__()
        self.topic = send_kafka.topic
        self.key_value_generator = send_kafka.key_value_generator
        self.kafka_manager = KafkaManager(options.view_as(KafkaOptions))  # type: KafkaManager

    def expand(self, input_inputs, action_func=None):
        assert isinstance(input_inputs, pvalue.PCollection)
        assert isinstance(input_inputs.element_value, pd.DataFrame)
        df = input_inputs.element_value
        key_values = self.key_value_generator(df)
        assert isinstance(key_values, dict)
        for key, value in key_values.items():
            self.kafka_manager.send(self.topic, key, value)
        return pvalue.PCollection(input_inputs.pipeline,
                                  element_value=df,
                                  element_type=pd.DataFrame,
                                  is_bounded=input_inputs.is_bounded)


class SendAlgJsonKafka(PTransform):

    def __init__(self,  # type: SendAlgJsonKafka
                 send_alg_json_kafka,  # type: ronds.SendAlgJsonKafka
                 options,  # type: PipelineOptions
                 ):
        """
        将算法处理之后的数据发送到 Kafka;

        包括: events 告警, indices 指标, graph json 等信息 .

        :param send_alg_json_kafka: 包含 kafka topic 等基本配置信息
        :param options: kafka 等系统配置信息
        """
        super(SendAlgJsonKafka, self).__init__()
        self.topics = send_alg_json_kafka.topics
        self.options = options
        self.kafka_manager = KafkaManager(options.view_as(KafkaOptions))  # type: KafkaManager
        # noinspection SpellCheckingInspection
        self.switch_dict = {
            'eventKafkaSource': self.send_events,
            'indiceKafkaSource': self.send_indices,
            'graphKafkaSource': self.send_graph,
            'exceptionKafkaSource': self.send_exception,
        }  # type: dict[str, Callable[[pd.DataFrame, str], None]]

    def send_events(self,
                    df,  # type: pd.DataFrame
                    topic,  # type: str
                    ):
        # type: (...) -> None
        """
        "events":
        [
            [
                {
                    "assetid": "3a..0",
                    "name": "sh_event",
                    "value": {},
                    "group": "alarm"
                }
            ]
        ]

        :param df:
        :param topic:
        :return:
        """
        if len(df) == 0 or 'events' not in df.columns:
            return None

        all_events = df['events']
        for events in all_events:
            if isinstance(events, list) and len(events) > 0:
                for in_events in events:
                    match = isinstance(in_events, list) and len(in_events) > 0
                    if not match:
                        continue
                    for event in in_events:
                        event_str = json.dumps(event)
                        logging.warning('kafka events sending, topic: %s, error: %s'
                                        % (topic, event_str))
                        self.kafka_manager.send(topic, key=None, value=event_str)

    # noinspection SpellCheckingInspection
    def send_indices(self,
                     df,  # type: pd.DataFrame
                     topic,  # type: str
                     ):
        # type: (...) -> None
        """
        "indices":
        [
            [
                {
                    "assetid": "3a00..f",
                    "meastime": "2023-05-22T14:44:00",
                    "names": [],
                    "values": [],
                    "wids": []
                }
            ]
        ]

        :param df: json DataFrame after algorithm process
        :param topic: kafka topic
        :return: kv for sending to kafka
        """
        if len(df) == 0 or 'indices' not in df.columns:
            return None

        all_indices = df['indices']
        for indices in all_indices:
            if isinstance(indices, list) and len(indices) > 0:
                for in_indices in indices:
                    match = isinstance(in_indices, list) and len(in_indices) > 0
                    if not match:
                        continue
                    for index in in_indices:
                        assert isinstance(index, dict)
                        if not index.__contains__(JsonKey.NAMES.value):
                            continue
                        msg = list()
                        asset_id = None
                        for i, name in enumerate(index[JsonKey.NAMES.value]):
                            index_value = index['values'][i]
                            if index_value is None or str.lower(index_value) == Constant.NAN.value:
                                continue
                            wid = index['wids'][i]
                            asset_id = index['assetid']
                            msg.append({
                                'assetid': asset_id,
                                'datatype': name,
                                'measdate': index['meastime'],
                                'condition': -1,
                                'measvalue': float(index_value),
                                'wid': wid,
                            })
                        if len(msg) > 0:
                            self.kafka_manager.send(topic, asset_id, json.dumps(msg))

    def send_exception(self,  # type: SendAlgJsonKafka
                       df,  # type: pd.DataFrame
                       topic,  # type: str
                       ):
        # type: (...) -> None
        if len(df) == 0 or 'exceptions' not in df.columns:
            return None
        all_ex = df['exceptions']
        if len(all_ex) == 0:
            return None
        for index, row in df.iterrows():
            json_str = row.to_json(orient='index',
                                   date_format=RuleParser.datetime_format())
            self.kafka_manager.send(topic, key=None, value=json_str)

    def send_graph(self,
                   df,  # type: pd.DataFrame
                   topic,  # type: str
                   ):
        # type: (...) -> None
        if len(df) == 0:
            return None

        for index, row in df.iterrows():
            if 'exceptions' in df.columns and len(row['exceptions']) > 0:
                continue
            # noinspection SpellCheckingInspection
            device_id = row[JsonKey.DEVICE_ID.value]
            json_str = row.to_json(orient='index',
                                   date_format=RuleParser.datetime_format())
            self.kafka_manager.send(topic, key=device_id, value=json_str)

    def expand(self, input_inputs, action_func=None):
        assert isinstance(input_inputs, pvalue.PCollection)
        assert isinstance(input_inputs.element_value, pd.DataFrame)
        df = input_inputs.element_value
        for source, kafka_config in self.topics.items():
            if not self.switch_dict.__contains__(source):
                continue
            kv_sender = self.switch_dict[source]
            for t in kafka_config['topics']:
                kv_sender(df, t)
        return pvalue.PCollection(input_inputs.pipeline,
                                  element_value=df,
                                  element_type=pd.DataFrame,
                                  is_bounded=input_inputs.is_bounded)
