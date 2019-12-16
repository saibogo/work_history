import unittest
from wh_app.supporting import functions
from wh_app.config_and_backup import config


class MyTestCase(unittest.TestCase):
    def test_num_to_time1(self):
        self.assertEqual(functions.num_to_time_str(0), '00', 'num_to_str 0 -> "00" Failed')

    def test_num_to_time2(self):
        self.assertEqual(functions.num_to_time_str(2), '02', 'num_to_str 0 -> "00" Failed')

    def test_num_to_time3(self):
        self.assertEqual(functions.num_to_time_str(12), '12', 'num_to_str 0 -> "00" Failed')

    def test_str_to_str_n_1(self):
        self.assertTrue(functions.str_to_str_n("abc", 2) == 'ab\nc', 'not corrected function str_to_str_n("abc", 2)')

    def test_str_to_str_n_2(self):
        self.assertTrue(functions.str_to_str_n("abc", 3) == 'abc', 'not corrected function str_to_str_n("abc", 3)')

    def test_str_to_str_n_3(self):
        self.assertTrue(functions.str_to_str_n("abc", 4) == 'abc', 'not corrected function str_to_str_n("abc", 4)')

    def test_str_to_str_n_4(self):
        self.assertTrue(functions.str_to_str_n("abc", 0) == 'a\nb\nc', 'not corrected function str_to_str_n("abc", 0)')

    def test_full_equip_to_view1(self):
        self.assertListEqual(functions.full_equip_to_view([]), [], 'not corrected convertation [] in full_equip_view')

    def test_full_equip_to_view2(self):
        self.assertListEqual(functions.full_equip_to_view([1]), [], 'not corrected convertation [1] in full_equip_view')

    def test_full_equip_to_view3(self):
        self.assertListEqual(functions.full_equip_to_view([1, 2, 3, 4, 5, 6]),
                             ['1', '3', '4', '5', '6'],
                             'not corrected convertation [1, 2, 3, 4, 5, 6] in full_equip_view')

    def test_list_of_pages1(self):
        self.assertListEqual(functions.list_of_pages([]),
                             [1], 'Not corrected create pages list from []')

    def test_list_of_pages2(self):
        self.assertListEqual(functions.list_of_pages([i for i in range(config.max_records_in_page - 1)]),
                             [1], 'Not corrected create pages list from [1, 2, ... max_size - 1]')

    def test_list_of_pages3(self):
        self.assertListEqual(functions.list_of_pages([i for i in range(config.max_records_in_page)]),
                             [1], 'Not corrected create pages list from [1, 2, ... max_size]')

    def test_list_of_pages4(self):
        self.assertListEqual(functions.list_of_pages([i for i in range(config.max_records_in_page + 1)]),
                             [1, 2], 'Not corrected create pages list from [1, 2, ... max_size + 1]')

    def test_works_table_add_new_performer1(self):
        self.assertListEqual(functions.works_table_add_new_performer([]),
                             [], 'Not corrected convertation [] in add new performer')

    def test_works_table_add_new_performer2(self):
        self.assertListEqual(functions.works_table_add_new_performer([[]]),
                             [[]], 'Not corrected convertation [[]] in add new performer')

    def test_works_table_add_new_performer3(self):
        self.assertListEqual(functions.works_table_add_new_performer([[1, 2]]),
                             [['1', '2<a href="/add-performer-to-work/1">+</a>']],
                             'Not corrected convertation [[1, 2]] in add new performer')

    def test_works_table_add_new_performer4(self):
        self.assertListEqual(functions.works_table_add_new_performer([[1, 2, 3], [4, 5, 6]]),
                             [['1', '2', '3<a href="/add-performer-to-work/1">+</a>'],
                              ['4', '5', '6<a href="/add-performer-to-work/4">+</a>']],
                             'Not corrected convertation [[1, 2, 3], [4, 5, 6]] in add new performer')


if __name__ == '__main__':
    unittest.main()
