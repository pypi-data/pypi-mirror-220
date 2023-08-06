"""
The test of function convolution2d
"""

import unittest
import numpy as np

from src.data_management.transform_data import convolution2d


class TestWindow1dFunction(unittest.TestCase):

    def test_transpose2d(self):

        # Checks if returns correct values
        input_matrix = np.array([
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
        ])
        kernel = np.array([[0, 1], [2, 3]])

        actual_result = convolution2d(input_matrix=input_matrix, kernel=kernel)
        expected_result = np.array([
            [19, 25],
            [37, 43]])

        comparison = actual_result == expected_result
        equal_arrays = comparison.all()
        assert equal_arrays

        input_matrix = np.array([
            [0, 1, 2, 3],
            [4, 5, 6, 7],
            [8, 9, 10, 11],
            [12, 13, 14, 15],
        ])
        kernel = np.array([[0, 1], [2, 3]])

        actual_result = convolution2d(input_matrix=input_matrix, kernel=kernel)
        expected_result = np.array([
            [24, 30, 36],
            [48, 54, 60],
            [72, 78, 84]
        ])

        comparison = actual_result == expected_result
        equal_arrays = comparison.all()
        assert equal_arrays

        input_matrix = np.array([
            [0, 1, 2, 3],
            [4, 5, 6, 7],
            [8, 9, 10, 11],
            [12, 13, 14, 15],
        ])
        kernel = np.array([[0, 1], [2, 3]])
        stride = 2

        actual_result = convolution2d(input_matrix=input_matrix, kernel=kernel, stride=stride)
        expected_result = np.array([
            [24, 36],
            [72, 84]
        ])

        comparison = actual_result == expected_result
        equal_arrays = comparison.all()
        assert equal_arrays

        stride = 3
        actual_result = convolution2d(input_matrix=input_matrix, kernel=kernel, stride=stride)
        expected_result = np.array([
            [24]
        ])

        comparison = actual_result == expected_result
        equal_arrays = comparison.all()
        assert equal_arrays

if __name__ == '__main__':
    unittest.main()
