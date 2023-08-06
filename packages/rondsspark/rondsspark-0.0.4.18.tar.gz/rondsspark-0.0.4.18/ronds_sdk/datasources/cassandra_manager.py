import datetime
import logging
import uuid
from typing import Sequence, List

from cassandra.cluster import Cluster, Session, ResultSet
from ronds_sdk.options.pipeline_options import CassandraOptions
from ronds_sdk.tools.utils import Singleton

logger = logging.getLogger('executor')
logger.setLevel(logging.INFO)


class CassandraManager(metaclass=Singleton):
    """
    Cassandra 数据库的操作类, 单例
    连接到固定的一个 Cassandra 集群, 可以操作多个 keyspace
    """

    def __init__(self,
                 options,  # type: CassandraOptions
                 ):
        self.cluster = Cluster(options.cassandra_host)
        self.session_cache = dict()  # type: dict[str, Session]

    def get_session(self, keyspace):
        # type: (str) -> Session
        if not self.session_cache.__contains__(keyspace):
            self.session_cache[keyspace] = self.cluster.connect(keyspace)
        return self.session_cache.get(keyspace)

    def query(self, keyspace: str, sql: str, params: List[str]) -> ResultSet:
        result = self.get_session(keyspace).execute(sql, params)
        return result

    def execute(self, keyspace: str, sql: str, params: List[str]) -> None:
        self.get_session(keyspace).execute(sql, params)

    def __del__(self):
        try:
            self.cluster.shutdown()
            logger.info("cassandra cluster shutdown~")
        except Exception as ex:
            logger.error("CassandraManager cluster shutdown failed: %s" % ex)
            raise ex


class ProcessDataManager(metaclass=Singleton):
    """
    内置的操作工艺数据表的操作类
    """

    def __init__(self,
                 options,  # type: CassandraOptions
                 keyspace=None,  # type: str
                 ):
        self._options = options
        self._table_name = options.cassandra_table_process  # type: str
        self.cassandra_manager = CassandraManager(options)  # type: CassandraManager
        if keyspace:
            self.keyspace = keyspace
        elif options.cassandra_keyspace:
            self.keyspace = options.cassandra_keyspace

    @property
    def _get_session(self):
        return self.cassandra_manager.get_session(self.keyspace)

    @property
    def _get_window_select_prepare(self):
        return self._get_session.prepare("""SELECT id, time, value
                                            FROM %s 
                                            where id in ?
                                            AND time >= ? 
                                            AND time < ?""" % self._table_name)

    def window_select(self,
                      uid_list,  # type: Sequence[str],
                      start_time,  # type: datetime.datetime
                      end_time,  # type: datetime.datetime
                      ):
        # type:  (...) -> ResultSet
        try:
            uuid_list = [uuid.UUID(uid) for uid in uid_list]
            return self._get_session.execute(self._get_window_select_prepare, [uuid_list, start_time, end_time])
        except Exception as ex:
            logger.error('window_select failed, uid_list: %s, start_time: %s, end_time: %s, ex:\n %s' % (
                str(uid_list), start_time, end_time, str(ex)))
            raise ex
