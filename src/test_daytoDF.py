import unittest

from need_to_test import _read_day, _get_cols, _get_lines, _get_word_order, get_df, iter_df
class TestDaytoDF(unittest.TestCase):
	def setUp(self):
		self.a = _read_day('OCRoutputIndustrial19300009-009801.day')

	def test_read_day(self):
		test_list_location = [3373,4259,1555,1678]
		b = self.a.values.tolist()
		self.assertEqual([round(i*400/1440) for i in test_list_location],[round(j) for j in b[3][0:4]])

	def test_get_cols_lines(self):
		test_col = [1,1,0,0]
		test_line = [0,0,0,0]

		c = _get_cols(self.a)
		f = _get_lines(self.a)

		d = c.values.tolist()
		g = f.values.tolist()
		h = []
		e = []
		for i in range(4):
			e.append(d[i][5])
			h.append(g[i][6])
		self.assertEqual(e,test_col)
		self.assertEqual(h,test_line)



	def test_get_word_order(self):
		pass

	
if __name__ == '__main__':
	unittest.main()
