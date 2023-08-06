import numpy as np


def transpose2d(input_matrix: list[list[float]]) -> list:
    """
    Transpose lists values in such way:
    From: [[x1, x2, x3, ...], [y1, y2, y3, ...]]
    To: [[x1, y1], [x2, y2], [x3, y3], ...]
    :param input_matrix: list of two lists with numbers.
    :return: [[x1, y1], [x2, y2], [x3, y3], ...]
    """
    if len(input_matrix) != 2:
        raise ValueError('It must be 2D array')
    if len(input_matrix[0]) != len(input_matrix[1]):
        raise ValueError("Arrays' len should be the same")
    return [[x, y] for x, y in zip(input_matrix[0], input_matrix[1])]


def window1d(input_array: list | np.ndarray, size: int, shift: int = 1, stride: int = 1) -> list[list | np.ndarray]:
    """
    Returns a dataset of "windows"
    :param input_array: 1D list or np.ndarray
    :param size: datasets of size (or possibly fewer if there are not enough input elements)
    :param shift: determines the number of input elements to shift between the start of each window
    :param stride: determines the stride between input elements within a window
    :return: a dataset of "windows"
    """
    x, y = 0, size*stride
    results = []
    while True:
        result = input_array[x:y:stride] if y < len(input_array) else input_array[x::stride]
        results.append(result)
        x += shift if shift > 0 else y
        y = x + size * stride
        if x >= len(input_array):
            break
    return results

def convolution2d(input_matrix: np.ndarray, kernel: np.ndarray, stride: int = 1) -> np.ndarray:
    """
    Applies a 2D convolution over an input image composed of several input planes.
    :param input_matrix: the matrix in np.ndarray format
    :param kernel: the matrix in np.ndarray format
    :param stride: the number of rows and columns traversed per slide
    :return: the matrix in np.ndarray format
    """
    input_x, input_y = input_matrix.shape
    kernel_x, kernel_y = kernel.shape
    results = []
    for x in range(0, input_x-kernel_x + 1, stride):
        result = []
        for y in range(0, input_x-kernel_y + 1, stride):
            result.append((input_matrix[x:x+kernel_x, y:y+kernel_y] * kernel).sum())
        results.append(result)
    results = np.array(results)
    return results
