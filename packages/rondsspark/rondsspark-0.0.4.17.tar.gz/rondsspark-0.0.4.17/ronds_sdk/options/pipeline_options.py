import argparse
from typing import Optional, Any, List, Iterable, Type, TypeVar, NoReturn

__all__ = [
    'PipelineOptions',
    'SparkRunnerOptions',
    'CassandraOptions',
    'AlgorithmOptions',
    'KafkaOptions',
]

from ronds_sdk.options.value_provider import StaticValueProvider, RuntimeValueProvider

PipelineOptionsT = TypeVar('PipelineOptionsT', bound='PipelineOptions')


class PipelineOptions(object):

    def __init__(self, flags=None, **kwargs):
        # type: (Optional[List[str]], **Any) -> None
        self._flags = flags

        parser = _RondsArgumentParser()
        for cls in type(self).mro():
            if cls == PipelineOptions:
                self.add_argparse_args(parser)
                break
            elif '_add_argparse_args' in cls.__dict__:
                cls._add_argparse_args(parser)  # type: ignore

        self._visible_options, _ = parser.parse_known_args(flags)

        self._all_options = kwargs

        for option_name in self._visible_option_list():
            # Note that options specified in kwargs will not be overwritten
            if option_name not in self._all_options:
                self._all_options[option_name] = getattr(self._visible_options, option_name)

    @classmethod
    def add_argparse_args(cls, parser):
        # type: (_RondsArgumentParser) -> None
        # Override this in subclasses to provide options.
        parser.add_argument(
            '--transform_package',
            default='ronds_sdk.transforms.spark.transforms',
            help='运行任务时, 物理执行算子的 package 路径, runner 有默认值, 一般无需修改'
        )
        parser.add_argument(
            '--enable_executor_debug',
            default=False,
            help='是否启用 Spark Executor 端的 DEBUG 功能, 仅用于测试'
        )

    def view_as(self, cls):
        # type: (Type[PipelineOptionsT]) -> PipelineOptionsT
        view: PipelineOptions = cls(self._flags)

        for option_name in view._visible_option_list():  # type: ignore
            if option_name not in self._all_options:
                self._all_options[option_name] = getattr(
                    view._visible_options, option_name)
        view._all_options = self._all_options
        return view

    def _visible_option_list(self):
        # type: () -> List[str]
        return sorted(
            option for option in dir(self._visible_options) if option[0] != '_'
        )

    def __dir__(self) -> Iterable[str]:
        return sorted(
            dir(type(self)) + list(self.__dict__) + self._visible_option_list()
        )

    def __getattr__(self, name):
        if name[:2] == name[-2:] == '__':
            return object.__getattribute__(self, name)
        elif name in self._visible_option_list():
            return self._all_options[name]
        else:
            raise AttributeError(
                "'%s' object has no attribute '%s'" % (type(self).__name__, name)
            )

    def __setattr__(self, name, value):
        if name in ('_flags', '_all_options', '_visible_options'):
            super().__setattr__(name, value)
        elif name in self._visible_option_list():
            self._all_options[name] = value
        else:
            raise AttributeError(
                "'%s' object has no attribute '%s'" % (type(self).__name__, name))

    def __str__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join(
                '%s=%s' % (option, getattr(self, option))
                for option in self._visible_option_list()
            )
        )


class _RondsArgumentParser(argparse.ArgumentParser):
    """An ArgumentParser that supports ValueProvider options.

      Example Usage::

        class TemplateUserOptions(PipelineOptions):
          @classmethod
          def _add_argparse_args(cls, parser):
            parser.add_value_provider_argument('--vp_arg1', default='start')
            parser.add_value_provider_argument('--vp_arg2')
            parser.add_argument('--non_vp_arg')

      """

    def add_value_provider_argument(self, *args, **kwargs):
        assert args != () and len(args[0]) >= 1
        if args[0][0] != '-':
            option_name = args[0]
            if kwargs.get('nargs') is None:
                kwargs['nargs'] = '?'
        else:
            option_name = [i.repalce('--', '') for i in args if i[:2] == '--'][0]
        value_type = kwargs.get('type') or str
        kwargs['type'] = _static_value_provider_of(value_type)
        default_value = kwargs.get('default')
        kwargs['default'] = RuntimeValueProvider(
            option_name=option_name,
            value_type=value_type,
            default_value=default_value
        )
        self.add_argument(*args, **kwargs)

    def error(self, message: str) -> NoReturn:
        if message.startswith('ambiguous option: '):
            return
        super().error(message)


class SparkRunnerOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):  # type: (_RondsArgumentParser) -> None
        parser.add_argument(
            '--spark_master_url',
            default=None,
        )
        parser.add_argument(
            '--spark_job_server_jar',
        )
        parser.add_argument(
            '--spark_version',
            default='3'
        )
        parser.add_argument(
            '--spark_repartition_num',
            default=2,
            help='Spark DataFrame repartition num if necessary'
        )
        parser.add_argument(
            '--spark_window_duration',
            default=5,
            help='window duration minutes'
        )


class CassandraOptions(PipelineOptions):

    # noinspection SpellCheckingInspection
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_argument(
            '--cassandra_window_duration',
            default=10,
            help='cassandra scan window duration seconds'
        )
        parser.add_argument(
            '--cassandra_host',
            default=['192.168.1.186']
        )
        parser.add_argument(
            '--cassandra_keyspace',
            default='eimp'
        )
        parser.add_argument(
            '--cassandra_table_process',
            default='processdata',
            help='table name for precess table'
        )
        parser.add_argument(
            '--cassandra_start_datetime',
            default=None
        )


class KafkaOptions(PipelineOptions):

    # noinspection SpellCheckingInspection
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_argument(
            '--kafka_bootstrap_servers',
            default=None,
            help='kafka bootstrap servers, eg. "host1:9092,host2:9092" .'
        )
        parser.add_argument(
            '--kafka_send_mock',
            default=False,
            help='if true, print messages instead of sending to Kafka cluster, for test'
        )


class AlgorithmOptions(PipelineOptions):

    # noinspection SpellCheckingInspection
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_argument(
            '--algorithm_path',
            help='Relative or absolute algorithm file path'
        )
        parser.add_argument(
            '--algorithm_funcname',
            help='algorithm function reference'
        )


def _static_value_provider_of(value_type):
    def _f(value):
        _f.__name__ = value_type.__name__
        return StaticValueProvider(value_type, value)

    return _f
