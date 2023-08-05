import unittest
import json
import threading
from ml4proflow import modules, exceptions


class TestModulesExtraModule(unittest.TestCase):
    def setUp(self):
        self.dfm = modules.DataFlowManager()

    def test_create_dfGraph_one_source_no_channel(self):
        dfg_desc = [{
            "module_ident": "ml4proflow.modules_extra.RepeatingSourceModule",
            "module_config": {}
            }]
        dut_dfg = modules.DataFlowGraph(self.dfm, {'modules': dfg_desc})
        self.assertIsInstance(dut_dfg, modules.DataFlowGraph)

    def test_create_dfGraph_one_source(self):
        dfg_desc = [{
            "module_ident": "ml4proflow.modules_extra.RepeatingSourceModule",
            "module_config": {'channels_push': ['src']}
            }]
        dut_dfg = modules.DataFlowGraph(self.dfm, {'modules': dfg_desc})
        print(json.dumps(dut_dfg.get_config()))

    def test_create_dfGraph_one_source_push_data(self):
        dfg_desc = [{
            "module_ident": "ml4proflow.modules_extra.RepeatingSourceModule",
            "module_config": {'channels_push': ['src']}
            }]
        dut_dfg = modules.DataFlowGraph(self.dfm, {'modules': dfg_desc})
        dut_dfg.execute_once()

    def test_create_dfGraph_two_wrong_connection(self):
        dfg_desc = [{
            "module_ident": "ml4proflow.modules_extra.RepeatingSourceModule",
            "module_config": {'channels_push': ['src']}
            }, {
            "module_ident": "ml4proflow.modules_extra.PassThroughModule",
            "module_config": {
                'channels_push': ['p_out'],
                'channels_pull': ['src_wrong']
                }
            }]
        with self.assertRaises(exceptions.NoSuchChannel):
            modules.DataFlowGraph(self.dfm, {'modules': dfg_desc})

    def test_create_dfGraph_double_create_dst(self):
        """
        Note: In the future we would like to support double push but only
              one Node is allowed to create the channel
        """
        dfg_desc = [{
            "module_ident": "ml4proflow.modules_extra.RepeatingSourceModule",
            "module_config": {'channels_push': ['src']}
            }, {
            "module_ident": "ml4proflow.modules_extra.PassThroughModule",
            "module_config": {
                'channels_push': ['dst'],
                'channels_pull': ['src']
                }
            }, {
            "module_ident": "ml4proflow.modules_extra.PassThroughModule",
            "module_config": {
                'channels_push': ['dst'],
                'channels_pull': ['src']
                }
            }]
        with self.assertRaises(exceptions.ChannelAlreadyExists):
            modules.DataFlowGraph(self.dfm, {'modules': dfg_desc})

    def test_create_dfGraph_two(self):
        dfg_desc = [{
            "module_ident": "ml4proflow.modules_extra.RepeatingSourceModule",
            "module_config": {'channels_push': ['src']}
            }, {
            "module_ident": "ml4proflow.modules_extra.PassThroughModule",
            "module_config": {
                'channels_push': ['p_out'],
                'channels_pull': ['src']
                }
            }]
        dut_dfg = modules.DataFlowGraph(self.dfm, {'modules': dfg_desc})
        self.assertIsInstance(dut_dfg, modules.DataFlowGraph)

    def test_create_dfGraph_three(self):
        dfg_desc = [{
            "module_ident": "ml4proflow.modules_extra.RepeatingSourceModule",
            "module_config": {}
            }, {
            "module_ident": "ml4proflow.modules_extra.PassThroughModule",
            "module_config": {}
            }, {
            "module_ident": "ml4proflow.modules_extra.StatisticSinkModule",
            "module_config": {}
            }]
        dut_dfg = modules.DataFlowGraph(self.dfm, {'modules': dfg_desc})
        self.assertIsInstance(dut_dfg, modules.DataFlowGraph)

    def test_create_dfGraph_three_produce_no_cache(self):
        dfg_desc = [{
            "module_ident": "ml4proflow.modules_extra.RepeatingSourceModule",
            "module_config": {
                "cache_pd": False,
                'channels_push': ['src'],
                }
            }, {
            "module_ident": "ml4proflow.modules_extra.PassThroughModule",
            "module_config": {}
            }, {
            "module_ident": "ml4proflow.modules_extra.StatisticSinkModule",
            "module_config": {}
            }]
        dut_dfg = modules.DataFlowGraph(self.dfm, {'modules': dfg_desc})
        dut_dfg.execute_once()
        self.assertIsInstance(dut_dfg, modules.DataFlowGraph)

    def test_create_dfGraph_three_produce_check_lock(self):
        lock = threading.Lock()
        dfg_desc = [{
            "module_ident": "ml4proflow.modules_extra.RepeatingSourceModule",
            "module_config": {
                "cache_pd": False,
                "print_lock": lock,
                'channels_push': ['src'],
                }
            }, {
            "module_ident": "ml4proflow.modules_extra.PassThroughModule",
            "module_config": {}
            }, {
            "module_ident": "ml4proflow.modules_extra.StatisticSinkModule",
            "module_config": {}
            }]
        dut_dfg = modules.DataFlowGraph(self.dfm, {'modules': dfg_desc})
        dut_dfg.execute_once()
        dut_dfg.on_shutdowning()
        dut_dfg.on_shutdowned()
        self.assertFalse(lock.locked())

    def test_create_dfGraph_three_call_shutdown_shutdowned(self):
        dfg_desc = [{
            "module_ident": "ml4proflow.modules_extra.RepeatingSourceModule",
            "module_config": {}
            }, {
            "module_ident": "ml4proflow.modules_extra.PassThroughModule",
            "module_config": {}
            }, {
            "module_ident": "ml4proflow.modules_extra.StatisticSinkModule",
            "module_config": {}
            }]
        dut_dfg = modules.DataFlowGraph(self.dfm, {'modules': dfg_desc})
        dut_dfg.on_shutdowning()
        dut_dfg.on_shutdowned()

    def test_create_dfGraph_fake_three_call_shutdown_shutdowned(self):
        dfg_desc = [{
            "module_ident":
                "ml4proflow.modules_extra.FakeRepeatingSourceModule",
            "module_config": {}
            }, {
            "module_ident": "ml4proflow.modules_extra.PassThroughModule",
            "module_config": {}
            }, {
            "module_ident": "ml4proflow.modules_extra.StatisticSinkModule",
            "module_config": {}
            }]
        dut_dfg = modules.DataFlowGraph(self.dfm, {'modules': dfg_desc})
        dut_dfg.on_shutdowning()
        dut_dfg.on_shutdowned()

    def test_create_dfGraph_fake_one_produce(self):
        dfg_desc = [{
            "module_ident":
                "ml4proflow.modules_extra.FakeRepeatingSourceModule",
            "module_config": {
                'channels_push': ['src']
                }
            }]
        dut_dfg = modules.DataFlowGraph(self.dfm, {'modules': dfg_desc})
        dut_dfg.execute_once()

    def test_create_dfGraph_1k(self):
        push_channels = ['src']
        dfg_desc = [{
            "module_ident": "ml4proflow.modules_extra.RepeatingSourceModule",
            "module_config": {'channels_push': push_channels}
            }]
        for i in range(1000):
            pull_channels = push_channels
            push_channels = ['pass_through_%d' % i]
            dfg_desc.append({
                "module_ident": "ml4proflow.modules_extra.PassThroughModule",
                "module_config": {
                    'channels_push': push_channels,
                    'channels_pull': pull_channels
                    }
                })
        dfg_desc.append({
            "module_ident": "ml4proflow.modules_extra.StatisticSinkModule",
            "module_config": {'channels_pull': push_channels}
            })
        dut_dfg = modules.DataFlowGraph(self.dfm, {'modules': dfg_desc})
        self.assertIsInstance(dut_dfg, modules.DataFlowGraph)

    def test_create_dfGraph_1k_with_one_produce_run(self):
        push_channels = ['src']
        dfg_desc = [{
            "module_ident": "ml4proflow.modules_extra.RepeatingSourceModule",
            "module_config": {'channels_push': push_channels}
            }]
        for i in range(1000):
            pull_channels = push_channels
            push_channels = ['pass_through_%d' % i]
            dfg_desc.append({
                "module_ident": "ml4proflow.modules_extra.PassThroughModule",
                "module_config": {
                    'channels_push': push_channels,
                    'channels_pull': pull_channels
                    }
                })
        dfg_desc.append({
            "module_ident": "ml4proflow.modules_extra.StatisticSinkModule",
            "module_config": {
                'channels_pull': push_channels
                }
            })
        dut_dfg = modules.DataFlowGraph(self.dfm, {'modules': dfg_desc})
        dut_dfg.execute_once()

    def test_create_dfGraph_2_and_get_config(self):
        push_channels = ['src']
        dfg_desc = [{
            "module_ident": "ml4proflow.modules_extra.RepeatingSourceModule",
            "module_config": {
                'channels_push': push_channels
                }
            }]
        for i in range(2):
            pull_channels = push_channels
            push_channels = ['pass_through_%d' % i]
            dfg_desc.append({
                "module_ident": "ml4proflow.modules_extra.PassThroughModule",
                "module_config": {
                    'channels_push': push_channels,
                    'channels_pull': pull_channels
                    }
                })
        dfg_desc.append({
            "module_ident": "ml4proflow.modules_extra.StatisticSinkModule",
            "module_config": {
                'channels_pull': push_channels
                }
            })
        dfg_desc = {'modules': dfg_desc}
        dut_dfg = modules.DataFlowGraph(self.dfm, dfg_desc)
        config = dut_dfg.get_config()
        self.assertDictEqual(config, dfg_desc)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
