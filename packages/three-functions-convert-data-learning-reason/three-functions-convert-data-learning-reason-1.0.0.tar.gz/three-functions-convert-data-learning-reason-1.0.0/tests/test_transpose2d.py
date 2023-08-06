"""
The test of Function's transpose2d
"""

import unittest

from src.data_management.transform_data import transpose2d


class TestTranspose2dFunction(unittest.TestCase):

    def test_transpose2d(self):

        # Checks if returns correct values
        input_value = [[1, 2, 3, 18, 9], [7, 5, 7, 9, 18]]
        actual_result = transpose2d(input_value)
        expected_result = [[1, 7], [2, 5], [3, 7], [18, 9], [9, 18]]
        assert actual_result == expected_result

        input_value = [[9, 14, 3, 18, 9], [3, 8, 7, 2, 1]]
        actual_result = transpose2d(input_value)
        expected_result = [[9, 3], [14, 8], [3, 7], [18, 2], [9, 1]]
        assert actual_result == expected_result

        # Checks if both elements are the same length.
        input_value = [[9, 14, 3, 18, 9], [3, 8, 7, 2]]
        with self.assertRaises(ValueError):
            transpose2d(input_value)

        # Checks if dataset has 2 elements.
        input_value = [[9, 14, 3, 18, 9]]
        with self.assertRaises(ValueError):
            transpose2d(input_value)

        # Checks if dataset has 2 elements.
        input_value = [[9, 14, 3], [18, 9, 8], [1, 3, 4]]
        with self.assertRaises(ValueError):
            transpose2d(input_value)


if __name__ == '__main__':
    unittest.main()
