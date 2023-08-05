import unittest
import tempfile
from ml4proflow import ml4proflow_cli


class TestCli(unittest.TestCase):
    def test_create_dataflow(self):
        ml4proflow_cli.main([])

    def test_create_dataflow_w_params(self):
        conf = '{"modules": [{"module_ident": "ml4proflow.modules_extra.' \
               'RepeatingSourceModule", "module_config": {"channels_push":' \
               ' ["src"], "cache_pd": true}}]}'
        fp = tempfile.NamedTemporaryFile(delete=False, mode="w")  # TODO
        fp.write(conf)
        fp.close()
        ml4proflow_cli.main(['--graph-desc', fp.name,
                             '--process-n-times', '1',
                             '--record-times'])


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
