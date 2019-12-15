import unittest
from wh_app.supporting import functions


class MyTestCase(unittest.TestCase):
    def test_num_to_time1(self):
        self.assertEqual(functions.num_to_time_str(0), '00', 'num_to_str 0 -> "00" Failed')

    def test_num_to_time2(self):
        self.assertEqual(functions.num_to_time_str(2), '02', 'num_to_str 0 -> "00" Failed')

    def test_num_to_time3(self):
        self.assertEqual(functions.num_to_time_str(12), '12', 'num_to_str 0 -> "00" Failed')


if __name__ == '__main__':
    unittest.main()
