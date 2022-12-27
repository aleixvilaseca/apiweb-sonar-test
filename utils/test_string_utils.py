from functools import reduce
import unittest
import string_utils

class Test_string(unittest.TestCase):
    def test_snake_case_1(self):
        self.assertEqual(string_utils.snake_case("HOLA QUE TAL"), "hola_que_tal")

    def test_snake_case_2(self):
        self.assertEqual(string_utils.snake_case("HOLAQUETAL"), "holaquetal")

    def test_snake_case_3(self):
        self.assertEqual(string_utils.snake_case("Hola que tal"), "hola_que_tal")


if __name__ == '__main__':
    unittest.main()