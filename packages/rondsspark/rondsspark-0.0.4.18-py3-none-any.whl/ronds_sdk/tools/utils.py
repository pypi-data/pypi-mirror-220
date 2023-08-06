import datetime
import json
from typing import Callable, List, Union

from ronds_sdk import error


class WrapperFunc(object):
    def call(self, *args, **kwargs):
        raise NotImplementedError


class ForeachBatchFunc(WrapperFunc):
    def __init__(self,
                 func,  # type: Callable
                 **kwargs
                 ):
        self._func = func
        self._kwargs = kwargs

    def call(self, *args, **kwargs):
        new_kwargs = {**self._kwargs, **kwargs}
        self._func(*args, **new_kwargs)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class RuleParser(object):

    def __init__(self,
                 rule_path,  # type: str
                 ):
        """
        从文件解析 phm 规则编辑器传入的规则配置信息, 用于从 Cassandra 根据指定规则读取测点数据;

        包含: 规则 id 列表, 读取的 Cassandra 数据表类型, 测点 id 列表等信息.

        :param rule_path:
        """
        self._rule_path = rule_path

    def load(self) -> list:
        with open(self._rule_path, 'r', encoding='utf-8') as r:
            config = r.read()
            if config is None:
                raise RuntimeError("config is None")
            return json.loads(config.strip('\t\r\n'))

    @staticmethod
    def point_ids(rule: dict) -> List[str]:
        """
        读取 rule 配置文件中的测点 id list

        :param rule: 规则配置
        :return: 测点 id list
        """
        points = rule['points']
        p_list = list()
        if points:
            for point in points:
                p_list.append(point.point_id)
        return p_list

    @staticmethod
    def datetime_format():
        return '%Y-%m-%d %H:%M:%S'


class GraphParser(object):

    def __init__(self,
                 file_path=None
                 ):
        """
        phm 规则编辑器 Cassandra, Kafka 等数据源配置信息解析

        :param file_path: 配置文件地址
        """
        self._file_path = file_path
        self.__graph_dict = None

    def load(self):
        # type: () -> dict
        with open(self._file_path, 'r', encoding='utf-8') as r:
            config = r.read()
            if config is None:
                raise RuntimeError("config is None")
            return json.loads(config.strip('\t\r\n'))

    def get_graph(self):
        # type: () -> dict
        """
        lazy create

        :return: graph dict
        """
        if self.__graph_dict is None:
            self.__graph_dict = self.load()
        return self.__graph_dict

    def _act_config(self, keys):
        # type: (set) -> dict
        """
        actConfig 节点中读取 Cassandra, Kafka 配置信息

        :param keys: 需要读取的 keys
        :return:  配置信息 dict
        """
        graph = self.get_graph()
        res_dict = dict()
        if not graph.__contains__('acts'):
            return res_dict
        acts = graph.get('acts')
        assert isinstance(acts, list)
        for act in acts:
            assert isinstance(act, dict)
            if not act.__contains__('actConfig'):
                continue
            act_config = act.get('actConfig')
            assert isinstance(act_config, dict)
            for k, v in act_config.items():
                if keys.__contains__(k):
                    res_dict[k] = v
        return res_dict

    def kafka_source_topics(self):
        # type: () -> dict
        """
        Kafka 相关的配置信息;

        包括 告警, indices指标, graph json 等 topic信息.

        :return:
        """
        # noinspection SpellCheckingInspection
        return self._act_config({'eventKafkaSource',
                                 'indiceKafkaSource',
                                 'graphKafkaSource',
                                 'exceptionKafkaSource',
                                 })

    def kafka_config(self):
        # type: () -> dict
        """
        kafka 配置信息, 默认多个 topic 的 kafka 集群的配置信息相同

        :return:
        """
        kafka_dict = self.kafka_source_topics()
        for source_name, kafka_config in kafka_dict.items():
            assert isinstance(kafka_config, dict)
            if kafka_config.__contains__('bootstraps') \
                    and kafka_config.__contains__('port'):
                return kafka_config

    def kafka_bootstraps(self):
        # type: () -> str
        kafka_config = self.kafka_config()
        return '%s:%s' % (kafka_config['bootstraps'], kafka_config['port'])

    def cassandra_sources(self):
        # type: () -> dict
        """
        Cassandra 数据源及表配置信息;

        包括 振动表, 工艺表数据 .

        :return: Cassandra 表及数据源配置信息
        """
        return self._act_config({'processCassandraSource',
                                 'vibCassandraSource',
                                 })

    # noinspection SpellCheckingInspection
    def cassandra_process_table(self):
        # type: () -> str
        source_dict = self.cassandra_sources()
        if source_dict.__contains__('processCassandraSource'):
            process_dict = source_dict.get('processCassandraSource')
            assert isinstance(process_dict, dict)
            dt_names = process_dict.get('dtnames')
            assert isinstance(dt_names, list)
            return dt_names[0]

    def cassandra_config(self):
        # type: () -> dict
        """
        Cassandra 数据源配置信息, 默认振动表, 工艺表等共用一个 Cassandra 集群;

        :return: Cassandra 配置信息
        """
        source_dict = self.cassandra_sources()
        for source_name, source_config in source_dict.items():
            assert isinstance(source_config, dict)
            if source_config.__contains__('address') \
                    and source_config.__contains__('keyspace'):
                return source_config

    def cassandra_host(self):
        # type: () -> list
        config = self.cassandra_config()
        if config.__contains__('address'):
            return [config['address']]

    def cassandra_keyspace(self):
        # type: () -> str
        config = self.cassandra_config()
        if config.__contains__('keyspace'):
            return config['keyspace']

    def window_duration(self):
        # type: () -> int
        """
        返回 Cassandra 定期扫描的窗口长度

        :return: 数据扫描的窗口长度, seconds
        """
        duration_dict = self._act_config({'window_duration'})
        if len(duration_dict) > 0:
            return int(next(iter(duration_dict.values())))
        return 300


def to_bool(v):
    # type: (Union[str, bool]) -> bool
    if v is None:
        return False
    if type(v) == bool:
        return v
    if type(v) == str:
        return v.lower() == 'true'
    return False


def date_format_str(date):
    # type: (datetime.datetime) -> str
    """
    格式化日期为字符串: %Y-%m-%d %H:%M:%S

    :param date: 日期
    :return: 格式化的日期字符串
    """
    if isinstance(date, datetime.datetime):
        return date.strftime(RuleParser.datetime_format())
    if isinstance(date, str):
        return date
    else:
        raise TypeError('expected datetime, but found %s' % type(date))


def to_dict(value):
    if isinstance(value, datetime.datetime):
        return datetime.datetime.strftime(value, '%Y-%m-%d %H:%M:%S.%f')[0:-3]
    else:
        return {k: v for k, v in value.__dict__.items() if not str(k).startswith('_')}
