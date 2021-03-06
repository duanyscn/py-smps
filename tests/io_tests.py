import unittest
import smps
from smps.io import load_sample, load_file
import os

basedir = os.path.dirname(os.path.abspath(__file__))

class SetupTestCase(unittest.TestCase):
    def setUp(self):

        # Import some test data
        self.data_number = load_file(os.path.join(basedir, "datafiles/test_data_number.txt"), column=False)
        self.data_diameter = load_file(os.path.join(basedir, "datafiles/test_data_diameter.txt"), column=False)
        self.data_surface_area = load_file(os.path.join(basedir, "datafiles/test_data_surface_area.txt"), column=False)
        self.data_volume = load_file(os.path.join(basedir, "datafiles/test_data_volume.txt"), column=False)

    def tearDown(self):
        pass

    def test_load_sample(self):
        # Load the sample
        df = load_sample('boston')

        self.assertIsInstance(df, smps.io.SMPS)

    def test_load_sample_column(self):
        df = load_sample('chamber')

        self.assertIsInstance(df, smps.io.SMPS)

    def test_smps_copy(self):
        df = self.data_number

        cpy = df.copy()

        self.assertTrue(df.raw.equals(cpy.raw))

    def test_smps_calculations(self):
        s = self.data_number

        # Test the first bin of dlogdp
        self.assertEqual(len(s.dlogdp), s.bins.shape[0])
        self.assertTrue(s.dndlogdp.equals(s.raw[s.bin_labels]))

        # Make sure that dDdlogDp is correct
        _calculated = self.data_number.dddlogdp * 1e-3 # divide by 1000 to go from um to nm
        _reference = self.data_diameter.dndlogdp # nanometers

        self.assertEqual(round(_calculated.iloc[0][0], 2), round(_reference.iloc[0][0], 2))

        # Make sure that dSdlogDp is correct

    def test_datatypes(self):
        df = self.data_number

        self.assertEqual(df.raw['Median'].dtype, float)
        self.assertEqual(df.raw['Mean'].dtype, float)
        self.assertEqual(df.raw['Mode'].dtype, float)
        self.assertEqual(df.raw['GM'].dtype, float)
        self.assertEqual(df.raw['GSD'].dtype, float)
        self.assertEqual(df.raw['Total Conc.'].dtype, float)

    def test_resampling(self):
        df = self.data_number

        #self.assertIsNotNone(df.resample('5min', inplace=False))
        self.assertTrue(df.resample('5min', inplace=True))

    def test_smps_model(self):
        pass
        #model = load_sample('boston')

        # Check dlo

    def test_stats(self):
        df = self.data_number
        df2 = self.data_surface_area
        df3 = self.data_volume

        # Retrieve the stats
        stats = df.stats(weight='number')

        self.assertTrue('Total Number' in stats.columns)
        self.assertTrue('Total Surface Area' in stats.columns)
        self.assertTrue('Total Volume' in stats.columns)
        self.assertTrue('Mean' in stats.columns)

        # Make sure the GM, GSD, and Mean are all within 1% error
        def one_pct_error(x1, x2):
            diff = abs(x1 - x2) / x1

            return True if diff <= 0.01 else False

        self.assertTrue(one_pct_error(stats["GM"][0], df.scan_stats['GM'][0]))
        self.assertTrue(one_pct_error(stats["Mean"][0], df.scan_stats['Mean'][0]))
        self.assertTrue(one_pct_error(stats["GSD"][0], df.scan_stats['GSD'][0]))

        # Repeat for Surface-Area weighted Statistics
        stats = df.stats(weight='surface_area')

        self.assertTrue(one_pct_error(stats["GM"][0], df2.scan_stats['GM'][0]))
        self.assertTrue(one_pct_error(stats["Mean"][0], df2.scan_stats['Mean'][0]))
        self.assertTrue(one_pct_error(stats["GSD"][0], df2.scan_stats['GSD'][0]))

        # Repeat for Volume weighted Statistics
        stats = df.stats(weight='volume')

        self.assertTrue(one_pct_error(stats["GM"][0], df3.scan_stats['GM'][0]))
        self.assertTrue(one_pct_error(stats["Mean"][0], df3.scan_stats['Mean'][0]))
        self.assertTrue(one_pct_error(stats["GSD"][0], df3.scan_stats['GSD'][0]))
