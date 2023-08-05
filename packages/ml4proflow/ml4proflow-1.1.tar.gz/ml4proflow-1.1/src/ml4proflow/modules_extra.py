from __future__ import annotations
from typing import Any, Union
from pandas import DataFrame
import time
import sys
from ml4proflow.modules import (SourceModule, ExecutableModule, SinkModule,
                                Module, DataFlowManager)


class AggregateModule(Module):
    def __init__(self, dfm: DataFlowManager, config: dict[str, Any]):
        Module.__init__(self, dfm, config)
        config.setdefault('function', 'max')
        
    def on_new_data(self,  name: str, sender: SourceModule,
                    data: DataFrame) -> None:
        data = data.agg(self.config['function'])
        self._push_data(self.config['channels_push'][0], data)

    @classmethod
    def get_module_desc(cls) -> dict[str, Union[str, list[str]]]:
        return {"name": "Aggregatuib Module",
                "categories": ["Examples"],
                "jupyter-gui-cls": "ml4proflow_jupyter.widgets.BasicWidget",
                }

class PassThroughModule(Module):
    """Pass Trough Module class
    Benchmark module that forwards the data
    Modules are scheduled at in the middle of the data processing graph.
    """
    def on_new_data(self,  name: str, sender: SourceModule,
                    data: DataFrame) -> None:
        self._push_data(self.config['channels_push'][0], data)

    @classmethod
    def get_module_desc(cls) -> dict[str, Union[str, list[str]]]:
        return {"name": "Passthrough Module",
                "categories": ["Benchmarking"],
                "jupyter-gui-cls": "ml4proflow_jupyter.widgets.BasicWidget",
                }


class RepeatingSourceModule(SourceModule, ExecutableModule):
    """Repeating Data Source Module class
    Benchmark module repeated n-times in the data processing graph
    Modules are scheduled at in the middle of the data processing graph.
    """
    def __init__(self, dfm: DataFlowManager, config: dict[str, Any]):
        config.setdefault('channels_push', ['src'])
        SourceModule.__init__(self, dfm, config)
        ExecutableModule.__init__(self, dfm, config)
        self.config.setdefault('print_lock', False)
        self.config.setdefault('data_to_push', [])
        self.config.setdefault('cache_pd', False)
        self.config.setdefault('should_record_times', True)
        self.config.setdefault('gen_meta_data', True)
        self.times: list[float] = []
        self.channel_push = self.config['channels_push'][0]
        self._current_id = 0
        if self.config['cache_pd']:
            self.data_to_push = DataFrame(data=self.config['data_to_push'])

    def execute_once(self) -> None:
        if self.config['cache_pd']:
            if self.config['gen_meta_data']:
                self.data_to_push.attrs['id'] = self._current_id
                self._current_id += 1
            if self.config['should_record_times']:
                self.times.append(time.time())
            self._push_data(self.channel_push, self.data_to_push)
        else:
            tmp = DataFrame(data=self.config['data_to_push'])
            if self.config['gen_meta_data']:
                tmp.attrs['id'] = self._current_id
                self._current_id += 1
            if self.config['should_record_times']:
                self.times.append(time.time())
            self._push_data(self.channel_push, tmp)

    def on_shutdowned(self) -> None:
        if self.config['should_record_times']:
            if self.config['print_lock']:
                self.config['print_lock'].acquire()
            print('RepeatingSourceModule:%s' % self.times)
            sys.stdout.flush()
            if self.config['print_lock']:
                self.config['print_lock'].release()


class DummyDF():
    def __init__(self, _id: int):
        self.attrs = {"id": _id}


class FakeRepeatingSourceModule(SourceModule, ExecutableModule):
    def __init__(self, dfm: DataFlowManager, config: dict[str, Any]):
        SourceModule.__init__(self, dfm, config)
        ExecutableModule.__init__(self, dfm, config)
        self.config.setdefault('print_lock', False)
        self.times: list[float] = []
        self._current_id = 0

    def execute_once(self) -> None:
        tmp = DummyDF(self._current_id)
        self._current_id += 1
        self.times.append(time.time())
        self._push_data(self.config['channels_push'][0], tmp)  # type: ignore

    def on_shutdowned(self) -> None:
        if self.config['print_lock']:
            self.config['print_lock'].acquire()
        print('FakeRepeatingSourceModule:%s' % self.times)
        sys.stdout.flush()
        if self.config['print_lock']:
            self.config['print_lock'].release()


class StatisticSinkModule(SinkModule):
    def __init__(self, dfm: DataFlowManager, config: dict[str, Any]):
        SinkModule.__init__(self, dfm, config)
        self.config.setdefault('should_record_times', True)
        self.config.setdefault('print_lock', False)
        self.times: list[float] = []
        self.ids: list[int] = []

    def on_new_data(self, name: str, sender: SourceModule,
                    data: DataFrame) -> None:
        if self.config['should_record_times']:
            self.times.append(time.time())
            self.ids.append(data.attrs.get('id', -1))

    def on_shutdowned(self) -> None:
        if self.config['should_record_times']:
            if self.config['print_lock']:
                self.config['print_lock'].acquire()
            print('StatisticSinkModule:%s:%s' % (self.times, self.ids))
            sys.stdout.flush()
            if self.config['print_lock']:
                self.config['print_lock'].release()


class PrintSinkModule(SinkModule):
    def __init__(self, dfm: DataFlowManager, config: dict[str, Any]):
        SinkModule.__init__(self, dfm, config)

    def on_new_data(self, name: str, sender: SourceModule,
                    data: DataFrame) -> None:
        print(data)
