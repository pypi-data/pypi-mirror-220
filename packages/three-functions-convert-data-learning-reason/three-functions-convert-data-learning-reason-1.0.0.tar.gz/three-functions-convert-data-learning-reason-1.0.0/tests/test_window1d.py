"""
The test of function window1d
"""

import unittest
import numpy as np

from src.data_management.transform_data import window1d


class TestWindow1dFunction(unittest.TestCase):

    def test_transpose2d(self):

        # Checks if returns correct values
        input_value = np.array([0, 1, 2, 3, 4, 5, 6])
        size, shift, stride = 1, 1, 1

        actual_result = window1d(input_value, size=size, shift=shift, stride=stride)
        expected_result = np.array([[0], [1], [2], [3], [4], [5], [6]])
        comparison = actual_result == expected_result
        equal_arrays = comparison.all()
        assert equal_arrays

        expected_result = np.array([[0], [1], [2], [3], [4], [5], [7]])
        comparison = actual_result == expected_result
        equal_arrays = comparison.all()
        assert not equal_arrays

        input_value = np.array([0, 1, 2, 3, 4])
        size, shift, stride = 2, 1, 1

        actual_result = window1d(input_value, size=size, shift=shift, stride=stride)
        expected_result = [[0, 1], [1, 2], [2, 3], [3, 4], [4]]

        # Checks if elements is np.ndarray format
        for result in actual_result:
            assert isinstance(result, np.ndarray)

        assert [list(result) for result in expected_result] == expected_result

        input_value = np.array([0, 1, 2, 3, 4, 5, 6])
        size, shift, stride = 2, 2, 1

        actual_result = window1d(input_value, size=size, shift=shift, stride=stride)
        expected_result = [[0, 1], [2, 3], [4, 5], [6]]

        # Checks if elements is np.ndarray format
        for result in actual_result:
            assert isinstance(result, np.ndarray)

        assert [list(result) for result in actual_result] == expected_result

        input_value = np.array([0, 1, 2, 3, 4, 5, 6])
        size, shift, stride = 2, 2, 2

        actual_result = window1d(input_value, size=size, shift=shift, stride=stride)
        expected_result = [[0, 2], [2, 4], [4, 6], [6]]

        # Checks if elements is np.ndarray format
        for result in actual_result:
            assert isinstance(result, np.ndarray)

        assert [list(result) for result in actual_result] == expected_result

        input_value = [0, 1, 2, 3, 4, 5, 6]
        size, shift, stride = 2, 2, 2

        actual_result = window1d(input_value, size=size, shift=shift, stride=stride)
        expected_result = [[0, 2], [2, 4], [4, 6], [6]]

        assert actual_result == expected_result


if __name__ == '__main__':
    unittest.main()
