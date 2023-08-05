import unittest
import pandas
from tempfile import TemporaryDirectory
from ml4proflow_mods.io.modules import DirectoryFileSourceModule, \
                                       FileSourceModule, \
                                       FileSinkModule
from ml4proflow import modules


class TestModulesModule(unittest.TestCase):
    def setUp(self):
        self.dfm = modules.DataFlowManager()

    def test_create_new_sink_module(self):
        with TemporaryDirectory() as tmp_dir:
            config = {'directory': tmp_dir, 'channels_push': ['src']}
            dut = DirectoryFileSourceModule(self.dfm, config)
            self.assertIsInstance(dut, DirectoryFileSourceModule)
            self.assertEqual(dut.get_file_count(), 0)
            self.assertEqual(dut.get_remaining_file_count(), 0)
    
    def on_new_data(self, name, sender, data):
        self.assertTrue(data.equals(self.dut_pd))
    
    def generic_test(self, ext, parser_options):
        with TemporaryDirectory() as tmp_dir:
            self.dfm.create_channel('dummy_source')
            dut_sink = FileSinkModule(self.dfm,
                                      {'channels_pull': ['dummy_source'],
                                       'write_metadata': True,
                                       'parser_options': parser_options,
                                       'file': f'{tmp_dir}/test{ext}'})
            pd = pandas.DataFrame({'test':[1,2,3,4], 'test2': [5,6,7,8]})
            self.dut_pd = pd
            self.dfm.new_data('dummy_source', None, pd)
            
            dut_source = FileSourceModule(self.dfm,
                                          {'channels_push': ['dut_source'],
                                           'read_metadata': True,
                                           'file': f'{tmp_dir}/test{ext}'})
            self.dfm.register_sink('dut_source', self)
            dut_source.execute_once()
    
    def test_write_read_file_csv(self):
        self.generic_test('.csv', {'index': False})

    def test_write_read_file_json(self):
        self.generic_test('.json', {})

    def test_write_read_file_hdf(self):
        self.generic_test('.h5', {'key':'test'})


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
