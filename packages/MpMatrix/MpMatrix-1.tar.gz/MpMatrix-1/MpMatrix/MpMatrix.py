"""
This file contains code for the library "MpMatrix".
Author: GlobalCreativeApkDev
"""


# Importing necessary libraries.


import sys
import os
import copy
from mpmath import *
mp.pretty = True


# Creating static function to check whether an object is a number or not


def is_number(obj: object) -> bool:
    try:
        mpf(str(obj))
        return True
    except ValueError:
        return False


# Creating static function to check whether the MpMatrix initialisation is valid or not.


def is_valid(a_list: list) -> bool:
    default_length: int = -1  # initial value
    for i in range(len(a_list)):
        if not isinstance(a_list[i], list):
            return False

        if i > 0:
            if len(a_list[i]) != default_length:
                return False
        else:
            default_length = len(a_list[i])

        for k in a_list[i]:
            if not is_number(k):
                return False

    return True


# Creating necessary classes.


class MpMatrix:
    """
    This class contains attributes of a matrix containing mpf objects.
    """

    def __init__(self, numbers):
        # type: (list) -> None
        if not is_valid(numbers):
            raise Exception("Invalid MpMatrix!")
        self.__numbers: list = numbers

    def __str__(self):
        # type: () -> str
        return str(self.__numbers)

    def get_dimensions(self):
        # type: () -> list
        return [len(self.__numbers), len(self.__numbers[0])]

    def __add__(self, other):
        # type: (object) -> MpMatrix
        new_nums: list = []  # initial value
        for row in range(self.get_dimensions()[0]):
            curr: list = []
            for col in range(self.get_dimensions()[1]):
                curr.append(0)

            new_nums.append(curr)

        if isinstance(other, MpMatrix):
            for row in range(self.get_dimensions()[0]):
                for col in range(self.get_dimensions()[1]):
                    new_nums[row][col] = mpf(self.__numbers[row][col]) + mpf(other.__numbers[row][col])

            return MpMatrix(new_nums)

        else:
            raise TypeError("Unsupported operand type '+' for type 'MpMatrix' with '" +
                            str(type(other)) + "'!")

    def __sub__(self, other):
        # type: (object) -> MpMatrix
        new_nums: list = []  # initial value
        for row in range(self.get_dimensions()[0]):
            curr: list = []
            for col in range(self.get_dimensions()[1]):
                curr.append(0)

            new_nums.append(curr)

        if isinstance(other, MpMatrix):
            for row in range(self.get_dimensions()[0]):
                for col in range(self.get_dimensions()[1]):
                    new_nums[row][col] = mpf(self.__numbers[row][col]) - mpf(other.__numbers[row][col])

            return MpMatrix(new_nums)

        else:
            raise TypeError("Unsupported operand type '-' for type 'MpMatrix' with '" +
                            str(type(other)) + "'!")

    def __mul__(self, other):
        # type: (object) -> MpMatrix
        if isinstance(other, MpMatrix):
            if self.get_dimensions()[1] != other.get_dimensions()[0]:
                raise Exception("MpMatrix dimensions mismatch for multiplication between a " +
                                str(self.get_dimensions()[0]) + " x " + str(self.get_dimensions()[1]) +
                                " matrix with a " + str(other.get_dimensions()[0]) + " x "
                                + str(other.get_dimensions()[1]) + " matrix.")
            else:
                new_nums: list = []  # initial value
                for row in range(self.get_dimensions()[0]):
                    curr: list = []
                    for col in range(other.get_dimensions()[1]):
                        curr.append(0)

                    new_nums.append(curr)

                for row in range(self.get_dimensions()[0]):
                    for col in range(other.get_dimensions()[1]):
                        new_nums[row][col] = mpf("0")  # initial value
                        for x in range(self.get_dimensions()[1]):
                            new_nums[row][col] += mpf(self.__numbers[row][x]) * mpf(other.__numbers[x][col])

                return MpMatrix(new_nums)

        elif isinstance(other, mpf) or isinstance(other, int) or isinstance(other, float):
            new_nums: list = []  # initial value
            for row in range(self.get_dimensions()[0]):
                curr: list = []
                for col in range(self.get_dimensions()[1]):
                    curr.append(0)

                new_nums.append(curr)

            for row in range(self.get_dimensions()[0]):
                for col in range(self.get_dimensions()[1]):
                    new_nums[row][col] = mpf(self.__numbers[row][col]) * mpf(other)

            return MpMatrix(new_nums)
        else:
            raise TypeError("Unsupported operand type '*' for type 'MpMatrix' with '" +
                            str(type(other)) + "'!")

    def __eq__(self, other):
        # type: (object) -> bool
        if isinstance(other, MpMatrix):
            if self.get_dimensions() != other.get_dimensions():
                return False
            else:
                for row in range(self.get_dimensions()[0]):
                    for col in range(self.get_dimensions()[1]):
                        # Ensuring there is no big difference between the values of the corresponding matrix entries
                        if mpf(self.__numbers[row][col]) - mpf(other.__numbers[row][col]) > mpf("1e-20"):
                            return False
            return True
        return False

    def clone(self):
        # type: () -> MpMatrix
        return copy.deepcopy(self)
