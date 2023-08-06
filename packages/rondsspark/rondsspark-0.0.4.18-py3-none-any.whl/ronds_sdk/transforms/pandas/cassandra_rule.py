import datetime
import logging
import time
import traceback
from functools import lru_cache

import pandas as pd
from cassandra.cluster import ResultSet

from ronds_sdk import error, logger_config
from ronds_sdk.datasources.cassandra_manager import ProcessDataManager
from ronds_sdk.options.pipeline_options import CassandraOptions
from ronds_sdk.tools.schedule import Scheduler
from ronds_sdk.tools.utils import RuleParser, ForeachBatchFunc, WrapperFunc, date_format_str
from ronds_sdk.transforms.pandas.rule_merge_data import RuleData


logger_config.config()
logger = logging.getLogger('executor')


class DatetimeHolder(object):
    def __init__(self,
                 d_time,  # type: datetime.datetime
                 ):
        self._d_time = d_time

    def datetime(self):
        return self._d_time

    def update(self, new_d_time):
        """
        update time by new_d_time that is less or equal now(), otherwise set now()
        :param new_d_time:
        :return:
        """
        c_d_time = datetime.datetime.today()
        if new_d_time > c_d_time:
            self._d_time = c_d_time
        else:
            self._d_time = new_d_time


class ForeachRule(object):
    def __init__(self,
                 c_options,  # type: CassandraOptions
                 action_func,  # type: WrapperFunc
                 ):
        self.c_options = c_options
        self.action_func = action_func
        self.scheduler = Scheduler()

    def foreach_rules(self,
                      rules,
                      ):
        logger.info("foreach_rules started ~")
        if self.c_options.enable_executor_debug:
            # enable spark executor debug, only for test
            import pydevd_pycharm
            pydevd_pycharm.settrace('localhost', port=12345, stdoutToServer=True, stderrToServer=True)

        interval_seconds = self.c_options.cassandra_window_duration
        current_timestamp = datetime.datetime.now() \
            if self.c_options.cassandra_start_datetime is None \
            else datetime.datetime.strptime(
            self.c_options.cassandra_start_datetime, RuleParser.datetime_format()
        )
        end_datetime_holder = DatetimeHolder(current_timestamp)
        process_manager = ProcessDataManager(self.c_options)

        # iter to tuple
        rules = self.iter_to_list(rules)

        # schedule task
        self.scheduler.every(interval_seconds).seconds.do(self.rule_task,
                                                          rules=rules,
                                                          process_manager=process_manager,
                                                          end_datetime_holder=end_datetime_holder,
                                                          interval_seconds=interval_seconds,
                                                          action_func=self.action_func)
        last_ex = None
        while True:
            # noinspection PyBroadException
            try:
                logging.info("running pending ~")
                self.scheduler.run_pending()
            except error.KafkaError:
                logging.error("rule_task kafka error: \n%s" % traceback.format_exc())

            except Exception:
                logging.error("rule_task error: \n%s" % traceback.format_exc())
            finally:
                time.sleep(5)

    def rule_task(self,
                  rules,
                  process_manager,  # type: ProcessDataManager
                  end_datetime_holder,  # type: DatetimeHolder
                  interval_seconds,  # type: int
                  action_func,  # type: ForeachBatchFunc
                  ):
        end_datetime = end_datetime_holder.datetime()
        delta = datetime.timedelta(seconds=interval_seconds)
        start_datetime = end_datetime - delta
        end_datetime_str = end_datetime.strftime(RuleParser.datetime_format())
        logging.info("start_time: %s, end_time: %s" % (
            start_datetime.strftime(RuleParser.datetime_format()),
            end_datetime_str))

        # process rules
        result_list = list()
        for rule in rules:
            uid_list = self.get_point_id_list(rule)
            logging.info("uid_list size: %s" % len(uid_list))
            if len(uid_list) == 0:
                continue
            result_set = process_manager.window_select(uid_list, start_datetime, end_datetime)
            rule_data = self.transform_to_rule_data_pd(result_set, rule)
            if rule_data is not None:
                result_list.append(rule_data)
            del result_set
            info = "query end, uid_list: %s, start_datetime: %s, end_datetime: %s, results: %s" \
                   % (str(uid_list), date_format_str(start_datetime),
                      date_format_str(end_datetime), len(result_list))
            logger.info(info)
        p_dataframe = pd.DataFrame(result_list)
        action_func.call(df=p_dataframe, epoch_id=end_datetime_str)

        # update end_datetime
        end_datetime_holder.update(end_datetime + delta)

    @staticmethod
    def transform_to_rule_data_pd(process_result_set: ResultSet, rule: dict) -> dict:
        rule_data = None
        device_id = rule['assetId']
        rule_ids = rule['rules']
        for r in process_result_set:
            if r.time is None or r.value is None:
                continue
            if rule_data is None:
                rule_data = RuleData(device_id, rule_ids)
            rule_data.add_process_data(str(r.id),
                                       r.time.strftime(RuleParser.datetime_format()),
                                       r.value)
        return rule_data.get_data() if rule_data is not None else None

    @lru_cache(maxsize=100)
    def scan_cassandra(self,
                       process_manager,  # type: ProcessDataManager
                       uid_list,  # type: tuple[str]
                       start_time,  # type: datetime.datetime
                       end_time,  # type: datetime.datetime
                       ):
        #  type: (...) -> ResultSet
        """
        maybe useful but memory dangerous, for future
        :param process_manager: 工艺查询管理
        :param uid_list: 测点 id 列表
        :param start_time: 开始时间
        :param end_time: 结束时间
        :return: ResultSet
        """
        return process_manager.window_select(uid_list, start_time, end_time)

    @staticmethod
    def iter_to_list(rules):
        res_list = list()
        for r in rules:
            res_list.append(r)
        return res_list

    @staticmethod
    def get_point_id_list(rule,
                          ):
        if 'points' not in rule.__fields__:
            return None
        p_list = list()
        for point in rule.points:
            assert isinstance(point, dict)
            if not point.__contains__('pointId'):
                continue
            p_list.append(point['pointId'])
        return p_list
