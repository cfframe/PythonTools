# plot_helper_test_case.py

import datetime
import filecmp
import numpy as np
import os
import shutil
import unittest

from pathlib import Path
from src.plot_helper import PlotHelper


class PlotHelperTestCase(unittest.TestCase):
    """Test names are generally self-explanatory and so docstrings not provided on an individual basis other
    than by exception.

    Keyword arguments:
    TestCase -- standard class required for tests based on unittest.case
    """

    def setUp(self):
        """Fixtures used by tests."""
        self.Root = Path(__file__).parent
        self.dataset_up_start = np.asarray([1, 6, 8, 9, 10, 10, 11, 10, 10])
        self.dataset_up_end = np.asarray([6, -5, 1, 1, 1, 1, 2, 2, 5])
        self.dataset_down_start = 11 - self.dataset_up_start
        self.dataset_down_end = 11 - self.dataset_up_end

    def test_legend_location_from_data(self):

        with self.subTest(self, testing_for="legend_location lower right"):
            expected = 'lower right'
            actual = PlotHelper.legend_location_from_data(self.dataset_up_start)
            self.assertEqual(actual, expected)

        with self.subTest(self, testing_for="legend_location upper right"):
            expected = 'upper right'
            actual = PlotHelper.legend_location_from_data(self.dataset_down_start)
            self.assertEqual(actual, expected)

        with self.subTest(self, testing_for="legend_location upper left"):
            expected = 'upper left'
            actual = PlotHelper.legend_location_from_data(self.dataset_up_end)
            self.assertEqual(actual, expected)

        with self.subTest(self, testing_for="legend_location lower left"):
            expected = 'lower left'
            actual = PlotHelper.legend_location_from_data(self.dataset_down_end)
            self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
