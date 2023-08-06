#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass()
class Boundaries2D():
    left: str = 'zero'
    right: str = 'zero'
    top: str = 'zero'
    bottom: str = 'zero'

    def __post_init__(self):
        self.assert_both_boundaries_not_same(self.left, self.right)
        self.assert_both_boundaries_not_same(self.top, self.bottom)

    @property
    def dictionary(self):
        return {
            'left': self.left,
            'right': self.right,
            'top': self.top,
            'bottom': self.bottom
        }

    @property
    def x_symmetry(self):
        if self.left == 'symmetric' or self.right == 'symmetric':
            return 'symmetric'
        elif self.left == 'anti-symmetric' or self.right == 'anti-symmetric':
            return 'anti-symmetric'
        else:
            return 'zero'

    @property
    def y_symmetry(self):
        if self.top == 'symmetric' or self.bottom == 'symmetric':
            return 'symmetric'
        elif self.top == 'anti-symmetric' or self.bottom == 'anti-symmetric':
            return 'anti-symmetric'
        else:
            return 'zero'

    def assert_both_boundaries_not_same(self, boundary_0: str, boundary_1: str):
        if boundary_0 != 'zero' and boundary_1 != 'zero':
            raise ValueError("Both left and right or top and "
                              "bottom symmetry shouldn't be the same "
                              "if symmetric or anti-symmetric")


@dataclass()
class Boundaries1D():
    left: str = 'zero'
    right: str = 'zero'

    def __post_init__(self):
        self.assert_both_boundaries_not_same(self.left, self.right)

    @property
    def dictionary(self):
        return {
            'left': self.left,
            'right': self.right
        }

    @property
    def x_symmetry(self):
        if self.left == 'symmetric' or self.right == 'symmetric':
            return 'symmetric'
        elif self.left == 'anti-symmetric' or self.right == 'anti-symmetric':
            return 'anti-symmetric'
        else:
            return 'zero'

    def assert_both_boundaries_not_same(self, boundary_0: str, boundary_1: str):
        if boundary_0 != 'zero' and boundary_1 != 'zero':
            raise ValueError("Both left and right or top and "
                              "bottom symmetry shouldn't be the same "
                              "if symmetric or anti-symmetric")