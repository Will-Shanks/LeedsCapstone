import unittest

from need_to_test import _read_day, _get_cols, _get_lines, _get_word_order, get_df, iter_df
class TestDaytoDF(unittest.TestCase):
	#def setUp(self):
		#self._read_day = _read_day('OCRoutputIndustrial19300009-009801.day')

	def test_read_day(self):
		test_list_location = [3373,4259,1555,1678]
		a = _read_day('OCRoutputIndustrial19300009-009801.day')
		b = a.values.tolist()
		self.assertEqual([round(i*400/1440) for i in test_list_location],[round(j) for j in b[3][0:4]])

	def test_get_cols(self):
		pass

	def test_get_lines(self):
		pass

	def test_get_word_order(self):
		pass

	
if __name__ == '__main__':
	unittest.main()