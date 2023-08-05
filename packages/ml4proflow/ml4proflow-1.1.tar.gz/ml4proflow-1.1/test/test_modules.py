import unittest
import pandas
from ml4proflow import modules, module_finder, exceptions


class TestModulesDataFlowManager(unittest.TestCase):
    def test_create_DataFlowManager(self):
        dfm = modules.DataFlowManager()
        self.assertIsInstance(dfm, modules.DataFlowManager)


class TestModulesModule(unittest.TestCase):
    def setUp(self):
        self.dfm = modules.DataFlowManager()

    def test_create_sink_module(self):
        dut = modules.SinkModule(self.dfm, {})
        self.assertIsInstance(dut, modules.SinkModule)

    def test_create_source_module(self):
        dut = modules.SourceModule(self.dfm, {})
        self.assertIsInstance(dut, modules.SourceModule)

    def test_create_module(self):
        dut = modules.Module(self.dfm, {})
        self.assertIsInstance(dut, modules.Module)

    def test_create_module_test_receive(self):
        dut = modules.Module(self.dfm, {})
        dummy = modules.Module(self.dfm, {})
        dut.on_new_data("test", dummy, pandas.DataFrame(data=[]))

    def test_module_is_instance_of_sink_module(self):
        dut = modules.Module(self.dfm, {})
        self.assertIsInstance(dut, modules.SinkModule)

    def test_module_sink_module_double_reg(self):
        config_push = {'channels_push': ['dst']}
        config_pull = {'channels_pull': ['dst']}
        modules.SourceModule(self.dfm, config_push)
        dut1 = modules.SinkModule(self.dfm, config_pull)
        with self.assertRaises(exceptions.ModuleIsAlreadySink):
            modules.SinkModule.__init__(dut1, self.dfm, config_pull)

    def test_module_sink_module_reg_unreg_reg(self):
        modules.SourceModule(self.dfm, {'channels_push': ['dst']})
        dut1 = modules.SinkModule(self.dfm, {'channels_pull': ['dst']})
        self.dfm.unregister_sink('dst', dut1)
        modules.SinkModule.__init__(dut1, self.dfm, {'channels_pull': ['dst']})

    def test_module_channel_unreg_no_channel(self):
        dut0 = modules.SourceModule(self.dfm, {'channels_push': ['dst']})
        with self.assertRaises(exceptions.NoSuchChannel):
            self.dfm.unregister_sink('unknown', dut0)

    def test_module_channel_unreg_no_module(self):
        modules.SourceModule(self.dfm, {'channels_push': ['dst']})
        with self.assertRaises(exceptions.NoSuchModule):
            self.dfm.unregister_sink('dst', None)

    def test_module_is_instance_of_source_module(self):
        dut = modules.Module(self.dfm, {})
        self.assertIsInstance(dut, modules.SourceModule)
        test = module_finder.find_and_import_framework_modules()
        print([*test.values()])

    def test_create_empty_DataFlowGraph(self):
        dut_dfg = modules.DataFlowGraph(self.dfm, {})
        self.assertIsInstance(dut_dfg, modules.DataFlowGraph)

    def test_create_no_modules_DataFlowGraph(self):
        dut_dfg = modules.DataFlowGraph(self.dfm, {'modules': []})
        self.assertIsInstance(dut_dfg, modules.DataFlowGraph)

    def test_create_no_modules_DataFlowGraph_shutdown(self):
        dut_dfg = modules.DataFlowGraph(self.dfm, {'modules': []})
        self.assertIsInstance(dut_dfg, modules.DataFlowGraph)
        dut_dfg.shutdown()

    def test_create_DataFlowGraph_no_such_module(self):
        dfg_desc = [{
            "module_ident": "ml4proflow.modules.NoModule",
            "module_config": {}
            }]
        with self.assertRaises(exceptions.NoSuchModule):
            modules.DataFlowGraph(self.dfm, {'modules': dfg_desc})


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
