import unittest
import os
from pathlib import Path
import shutil
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
from ds_capability import FeatureBuild
from ds_capability.intent.feature_build_intent import FeatureBuildIntentModel
from aistac.properties.property_manager import PropertyManager

# Pandas setup
pd.set_option('max_colwidth', 320)
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 99)
pd.set_option('expand_frame_repr', True)


class FeatureBuilderTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        # clean out any old environments
        for key in os.environ.keys():
            if key.startswith('HADRON'):
                del os.environ[key]
        # Local Domain Contract
        os.environ['HADRON_PM_PATH'] = os.path.join('working', 'contracts')
        os.environ['HADRON_PM_TYPE'] = 'parquet'
        # Local Connectivity
        os.environ['HADRON_DEFAULT_PATH'] = Path('working/data').as_posix()
        # Specialist Component
        try:
            os.makedirs(os.environ['HADRON_PM_PATH'])
        except OSError:
            pass
        try:
            os.makedirs(os.environ['HADRON_DEFAULT_PATH'])
        except OSError:
            pass
        PropertyManager._remove_all()

    def tearDown(self):
        try:
            shutil.rmtree('working')
        except OSError:
            pass

    def test_for_smoke(self):
        fb = FeatureBuild.from_memory()
        tools: FeatureBuildIntentModel = fb.tools
        tbl = tools.get_synthetic_data_types(100)
        self.assertEqual(100, tbl.num_rows)

    def test_model_sample_link(self):
        fb = FeatureBuild.from_memory()
        tools: FeatureBuildIntentModel = fb.tools
        canonical = tools.get_synthetic_data_types(10, category_encode=False)
        other = tools.get_synthetic_data_types(5, category_encode=False)
        result = tools.model_sample_link(canonical=canonical, other=other, headers=['int'], rename_map=['key'])
        self.assertCountEqual(result.column_names, canonical.column_names+['key'])
        result = tools.model_sample_link(canonical=canonical, other=other, headers=['int', 'num'], rename_map={'int': 'key', 'num': 'prob'})
        self.assertCountEqual(result.column_names, canonical.column_names + ['key', 'prob'])
        result = tools.model_sample_link(canonical=canonical, other=other, headers=['int'], rename_map=['key1'], multi_map={'key2': 'key1'})
        self.assertCountEqual(result.column_names, canonical.column_names + ['key1', 'key2'])
        self.assertTrue(result.column('key1').equals(result.column('key2')))


    def test_raise(self):
        with self.assertRaises(KeyError) as context:
            env = os.environ['NoEnvValueTest']
        self.assertTrue("'NoEnvValueTest'" in str(context.exception))


if __name__ == '__main__':
    unittest.main()
