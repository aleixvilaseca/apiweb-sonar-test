from re import T
import date_utils
import unittest

class Test_date(unittest.TestCase):
    def test_get_current_year(self):
        self.assertEqual(date_utils.get_current_year(), 2022)

    def test_substract_one_month_from_today_1(self):
        self.assertEqual(date_utils.substract_one_month_from_today('%Y-%m-%d'), '2022-01-01')

    def test_substract_one_month_from_today_2(self):
        self.assertEqual(date_utils.substract_one_month_from_today('%Y-%m-%dT00:00:00Z'), '2022-01-01T00:00:00Z')

    def test_substract_one_year_from_today(self):
        self.assertEqual(date_utils.substract_one_year_from_today('%Y-%m-%dT00:00:00Z'), '2021-02-01T00:00:00Z')

    def test_substract_n_month_from_today_1(self):
        self.assertEqual(date_utils.substract_n_months_from_today(12, '%Y-%m-%dT00:00:00Z'), '2021-02-01T00:00:00Z')

    def test_substract_n_month_from_today_2(self):
        self.assertEqual(date_utils.substract_n_months_from_today(13, '%Y-%m-%dT00:00:00Z'), '2021-01-01T00:00:00Z')

    def test_substract_n_month_from_today_3(self):
        self.assertEqual(date_utils.substract_n_months_from_today(14, '%Y-%m-%dT00:00:00Z'), '2020-12-01T00:00:00Z')

    def test_get_today_date(self):
        self.assertAlmostEquals(date_utils.get_today_date('%Y-%m-%d'), '2022-02-24')

if __name__ == '__main__':
    unittest.main()