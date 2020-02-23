import collections
from typing import Generator
from unittest import TestCase
from osbot_utils.utils.Misc  import Misc
from osbot_utils.utils.Files import Files


class test_Misc(TestCase):

    def test_array_add(self):
        array = ['aaa']
        self.assertEqual  (Misc.array_add(array,'abc'), 'abc'       )
        self.assertIsNone (Misc.array_add(array, None)              )
        self.assertEqual  (array                      ,['aaa','abc'])

    def test_array_find(self):
        array = ['1',2,'3']
        self.assertEqual  (Misc.array_find(array, '1' ),  0)
        self.assertEqual  (Misc.array_find(array,  2  ),  1)
        self.assertEqual  (Misc.array_find(array, '3' ),  2)
        self.assertEqual  (Misc.array_find(array, 'a' ), -1)
        self.assertEqual  (Misc.array_find(array, None), -1)
        self.assertRaises (Exception, Misc.array_find, None, None)
        self.assertRaises (Exception, Misc.array_find, 'a', None)

    def test_array_get(self):
        array = ['1',2,'3']
        assert Misc.array_get(array,  0  ) == '1'
        assert Misc.array_get(array,  1  ) ==  2
        assert Misc.array_get(array,  2  ) == '3'
        assert Misc.array_get(array, -1  ) is None
        assert Misc.array_get(array,  3  ) is None
        assert Misc.array_get(array, None) is None
        assert Misc.array_get(None , None) is None

    def test_array_pop(self):
        array = ['1',2,'3']
        assert Misc.array_pop(array) == '3'
        assert Misc.array_pop(array) ==  2
        assert Misc.array_pop(array) == '1'
        assert Misc.array_pop(array) is None
        assert Misc.array_pop(None)  is None
        array = ['1', 2, '3']
        assert Misc.array_pop(array, 1) ==  2
        assert Misc.array_pop(array, 1) == '3'
        assert Misc.array_pop(array, 1) is None
        assert Misc.array_pop(array, 0) == '1'
        assert Misc.array_pop(array, 0) is None

    def test_array_pop_and_trim(self):
        array = [' 1 ',2,'3']
        assert Misc.array_pop_and_trim(array,  1  ) ==  2
        assert Misc.array_pop_and_trim(array,   1 ) == '3'
        assert Misc.array_pop_and_trim(array,   0 ) == '1'
        assert Misc.array_pop_and_trim(array, None) is None

    def test_chunks(self):
        array = ['1',2,'3',4 ,'5']
        assert list(Misc.chunks(array,  2  )) == [['1', 2    ], ['3', 4], ['5']]
        assert list(Misc.chunks(array,  3  )) == [['1', 2,'3'], [ 4 , '5'     ]]
        assert list(Misc.chunks(array,  0  )) == []
        assert list(Misc.chunks(array, None)) == []
        assert type(Misc.chunks(None , 0)).__name__ == 'generator'
        assert list(Misc.chunks(None , 0)) == []


    def test_random_filename(self):
        result = Misc.random_filename()
        assert len(result) == 14
        assert ".tmp" in result

    def test_exists(self):
        assert Files.exists(Files.current_folder()) is True
        assert Files.exists('aaaa_bbb_ccc'        ) is False
        assert Files.exists(None                  ) is False

    def test_is_number(self):
        assert Misc.is_number(123   ) is True
        assert Misc.is_number('123' ) is True
        assert Misc.is_number('abc' ) is False
        assert Misc.is_number(None  ) is False
        assert Misc.is_number([]    ) is False
