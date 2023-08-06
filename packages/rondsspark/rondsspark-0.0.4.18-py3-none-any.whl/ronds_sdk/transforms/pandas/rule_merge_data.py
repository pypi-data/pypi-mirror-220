from typing import Union


from ronds_sdk.tools.constants import JsonKey


# noinspection SpellCheckingInspection
class RuleData(object):

    def __init__(self,
                 device_id,  # type: str
                 rule_ids,  # type: list[str]
                 nodes=None,  # type: list
                 edges=None,  # type: list
                 datasources=None,  # type: list
                 indices=None,  # type: list
                 events=None,  # type: list
                 running_time=None,  # type: float
                 datasource_times=None,  # type: str

                 ):
        """
        根据规则读取 Cassandra 数据, 组合成算法能够识别的 JSON 格式数据
        :param nodes: 设备 DAG nodes
        :param edges: 设备 DAG edges
        :param datasources: 数据源的具体数据
        :param indices: 需要存储到 Cassandra 的数据
        :param events: 需要发送到 Kafka 告警主题的数据
        :param running_time: 运行时间
        :param datasource_times: 数据源数据批次生成 时间
        """
        self._data_dict = {
            JsonKey.DEVICE_ID.value: device_id,
            'nodes': nodes if nodes else [
                {
                    'id': device_id,
                    'name': '',
                    'group': 2,
                    'code': 139555,
                    'attributes': {
                        'entcode': 'COM'
                    }
                }
            ],
            'edges': edges if edges else [],
            'datasource': [[]] if datasources is None else datasources,
            'version': '1.0.0',
            'indices': indices if indices else [],
            'events': events if events else [],
            'runningtime': running_time if running_time else [],
            'datasourcetimes': [datasource_times] if datasource_times else [],
            'rules': rule_ids,
            'cache': {
                JsonKey.DEVICE_ID.value: device_id,
                'metadata': [],
                'buffer': ''
            },
        }
        self._data_index = dict()

    def get_data(self) -> dict:
        return self._data_dict

    def get_datasource(self) -> list:
        datasources = self._data_dict['datasource']
        assert isinstance(datasources, list)
        return datasources[0]

    def set_nodes(self, nodes: list) -> None:
        if nodes:
            self._data_dict['nodes'] = nodes

    def set_edges(self, edges: list) -> None:
        if edges:
            self._data_dict['edges'] = edges

    def add_process_data(self,  # type: RuleData
                         asset_id,  # type: str
                         c_time,  # type: str
                         value,  # type: Union[float, int]
                         data_type=106,  # type: int
                         ):
        # type: (...) -> None
        """
        添加工艺数据
        :param asset_id: 测点 id
        :param c_time: 数据产生时间
        :param value: 数据内容
        :param data_type: 数据类型, 默认工艺 data_type = 106
        :return: None
        """
        if not self._data_index.__contains__(asset_id):
            datasource = {
                'assetid': asset_id,
                'value': {
                    'channeldata': {
                        'code': '',
                        'nodetype': '',
                        'data': [],
                        'assetid': asset_id,
                        'caption': '',
                        'property': {
                            'sernortype': 0,
                            'direct': '',
                            'direction': 1
                        }
                    }
                }
            }
            self._data_index[asset_id] = datasource
            self.get_datasource().append(datasource)
        datasource = self._data_index[asset_id]
        self.fill_channel_data(data_type, asset_id, c_time, value, datasource)

    @staticmethod
    def get_data_key(*args) -> str:
        return '_'.join([str(s) for s in args])

    def fill_channel_data(self,  # type: RuleData
                          data_type,  # type: int
                          asset_id,  # type: str
                          c_time,  # type: str
                          value,  # type: float
                          datasource,  # type: dict
                          ):
        # type: (...) -> None
        """
        按照格式填充 datasource.value.chaneldata.data 的数据
        :param value: 工艺数据值
        :param c_time: 数据产生时间
        :param asset_id: 测点 id
        :param data_type: 设备类型
        :param datasource: 需要填充的 datasource
        """
        channel_data_key = self.get_data_key(asset_id, data_type)
        if not self._data_index.__contains__(channel_data_key):
            channel_data = {
                'times': [],
                'values': [],
                'datatype': data_type,
                'indexcode': -1,
                'conditions': [],
                'properties': []
            }
            self._data_index[channel_data_key] = channel_data
            datasource['value']['channeldata']['data'].append(channel_data)
        channel_data = self._data_index[channel_data_key]
        channel_data['times'].append(c_time)
        channel_data['values'].append(value)
