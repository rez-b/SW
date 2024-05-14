import unittest
from classCompareson import Compareson

class Testcompareson(unittest.TestCase):
    """пример unit тестирования класса Compareson"""
    def setUp(self):
        self.data = [[1,2,3,4,5,6,7,8],[1,2,3,4,5,6,7,8]]
        stringCount = 2
        columnCount = 4
        self.my_compareson = Compareson(self.data[0], self.data[1], stringCount, columnCount)

    def test_get_matrix_data_sheet(self):
        self.assertEqual([[1,2,3,4],[5,6,7,8]],self.my_compareson.get_matrix_data_sheet(self.data[0]))

    def test_compare(self):
        self.assertEqual([],self.my_compareson.compare())

    def test_correct_answers_percentage(self):
        self.assertEqual(100, self.my_compareson.correct_answers_percentage())
        
unittest.main()