from __future__ import annotations
from typing import Any, Union
from pandas import DataFrame
from ml4proflow import exceptions


class DataFlowManager:
    """
    Implementation Note:
    The current implementation is stack based, therefore you need to call
    ``sys.setrecursionlimit(n)`` if you need graph depths > ~1K nodes.
    """
    def __init__(self) -> None:
        self.channels: dict[str, list['SinkModule']] = {}

    def create_channel(self, channel: str) -> None:
        if channel in self.channels.keys():
            raise exceptions.ChannelAlreadyExists("Name: %s" % channel)
        self.channels[channel] = []

    def register_sink(self, channel: str, receiver: 'SinkModule') -> None:
        if channel not in self.channels.keys():
            raise exceptions.NoSuchChannel("""Target Channel: %s
            Channels: %s""" % (channel, self.channels.keys()))
        if receiver in self.channels[channel]:
            raise exceptions.ModuleIsAlreadySink("Target Channel: %s" % channel)
        self.channels[channel].append(receiver)

    def unregister_sink(self, channel: str, receiver: 'SinkModule') -> None:
        if channel not in self.channels.keys():
            raise exceptions.NoSuchChannel("Target Channel: %s" % channel)
        if receiver not in self.channels[channel]:
            raise exceptions.NoSuchModule("Target Channel: %s" % channel)
        self.channels[channel].remove(receiver)

    def new_data(self, channel: str, sender: 'SourceModule',
                 data: DataFrame) -> None:
        if channel not in self.channels.keys():
            raise exceptions.NoSuchChannel("Target Channel: %s" % channel)
        for module in self.channels[channel]:
            module.on_new_data(channel, sender, data)


class BasicModule:
    """Basic Module class
    """
    def __init__(self, dfm: DataFlowManager, config: dict[str, Any]) -> None:
        self.dfm = dfm
        self.config = config
        # (min, max, step) or [choices]
        self.config_range: dict[str, Union[tuple[float, float, float],
                                           list[Any]]] = {}
        self.config_desc: dict[str, str] = {}

    @classmethod
    def get_module_tags(cls) -> list[str]:
        return []

    @classmethod
    def get_module_desc(cls) -> dict[str, Union[str, list[str]]]:
        return {}

    @classmethod
    def get_module_ident(cls) -> str:
        return cls.get_module_path() + "." + cls.get_module_name()

    @classmethod
    def get_module_name(cls) -> str:
        return cls.__name__

    @classmethod
    def get_module_path(cls) -> str:
        return cls.__module__

    def get_config(self) -> dict[str, Any]:
        return self.config

    def update_config(self, k: str, v: Any) -> None:
        self.config[k] = v

    def get_config_desc(self) -> dict[str, str]:
        return self.config_desc

    def on_shutdowning(self) -> None:
        pass

    def on_shutdowned(self) -> None:
        pass


class ExecutableModule(BasicModule):
    def __init__(self, dfm: DataFlowManager, config: dict[str, Any]):
        BasicModule.__init__(self, dfm, config)

    def execute_once(self) -> None:
        pass


class SourceModule(BasicModule):
    """Source Module class
    Class for modules that produce data only.
    Source modules are scheduled at the beginning of the data processing graph.

    Events you need to implement:
    - ``produce_data()`` -> Produce data to be passed to a channel

    (Helper-)Methods you need to use:
    - ``_push_data()`` -> Push your results to a channel
    """
    def __init__(self, dfm: DataFlowManager, config: dict[str, Any]):
        BasicModule.__init__(self, dfm, config)
        self.config.setdefault('channels_push', [])
        self.config_desc['channels_push'] = 'Output channels of this module'
        for c in self.config['channels_push']:
            dfm.create_channel(c)

    def update_config(self, k: str, v: Any) -> None:
        # TODO: Channel cleanup!!!
        if k == 'channels_push':
            for c in v:
                try:
                    self.dfm.create_channel(c)
                except exceptions.ChannelAlreadyExists:
                    pass
        BasicModule.update_config(self, k, v)

    def _push_data(self, channel: str, data: DataFrame) -> None:
        """Helper function:
        Push "data" to a channel (inside our current dataflow graph)
        :param name: Name of the channel
        :param data: Data to push
        :return: None
        """
        # we could validate the channel name in our list (with an assert?)
        self.dfm.new_data(channel, self, data)


class SinkModule(BasicModule):
    def __init__(self, dfm: DataFlowManager, config: dict[str, Any]):
        BasicModule.__init__(self, dfm, config)
        self.config.setdefault('channels_pull', [])
        self.config_desc['channels_pull'] = 'Input channels of this module'
        for c in self.config['channels_pull']:
            dfm.register_sink(c, self)

    def update_config(self, k: str, v: Any) -> None:
        # TODO: Channel cleanup!!!
        if k == 'channels_pull':
            for c in v:
                try:
                    self.dfm.register_sink(c, self)
                except exceptions.ModuleIsAlreadySink:
                    pass
        BasicModule.update_config(self, k, v)

    def on_new_data(self, name: str, sender: SourceModule,
                    data: DataFrame) -> None:
        """Called when there is new data available ready to process
        :param name: Name of the channel
        :param sender: Name of the module that sends the data
        :param data: DataFrame to be processed
        :return:
        """
        pass


class Module(SourceModule, SinkModule):
    """Module class
    Class for modules that can receive input data and can produce output data.
    Modules are scheduled at any position of the data processing graph.

    Events you need to implement:
    - ``on_new_data()``: Your module gets new data

    (Helper-)Methods you need to use:
    - ``_push_data()`` -> Push your results to a channel
    """
    def __init__(self, dfm: DataFlowManager, config: dict[str, Any]):
        SourceModule.__init__(self, dfm, config)
        SinkModule.__init__(self, dfm, config)

    def update_config(self, k: str, v: Any) -> None:
        # TODO: this currently sets the config twice
        SourceModule.update_config(self, k, v)
        SinkModule.update_config(self, k, v)


from ml4proflow import module_finder  # noqa: E402


class DataFlowGraph(ExecutableModule):
    def __init__(self, dfm: DataFlowManager, config: dict[str, Any]):
        ExecutableModule.__init__(self, dfm, config)
        self.modules = []
        self.executable_modules = []  # type: list[ExecutableModule]
        self.config.setdefault('modules', [])
        for m_desc in self.config['modules']:
            m_class = module_finder.find_by_name(m_desc["module_ident"])
            m_inst = m_class(dfm=dfm, config=m_desc["module_config"])
            self.modules.append(m_inst)
            if issubclass(m_class, ExecutableModule):
                self.executable_modules.append(m_inst)  # type: ignore
        assert len(self.executable_modules) <= 1, \
            'DFGraph currently only supports a maximum of one producer'
        del self.config  # Delete the config cache. See get_config

    def add_module(self, module: BasicModule) -> None:
        self.modules.append(module)
        if isinstance(module, ExecutableModule):
            self.executable_modules.append(module)  # type: ignore

    def get_config(self) -> dict[str, Any]:
        """
        Implementation note:
        This module regenerates the config (it doesn't use self.config) because
        otherwise it would have to track changes of the
        embedded submodule configs.
        :return:
        """
        modules = []
        for m in self.modules:
            module_config = {"module_ident": m.get_module_ident(),
                             "module_config": m.get_config()}
            modules.append(module_config)
        return {'modules': modules}

    def execute_once(self) -> None:
        # Currently it only supports one producer node
        self.executable_modules[0].execute_once()

    def on_shutdowning(self) -> None:
        for m in self.modules:
            m.on_shutdowning()

    def on_shutdowned(self) -> None:
        for m in self.modules:
            m.on_shutdowned()

    def shutdown(self) -> None:
        self.on_shutdowning()
        self.on_shutdowned()
