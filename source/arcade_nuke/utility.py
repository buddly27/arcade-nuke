# :coding: utf-8

import math


class Vector(object):
    """Representation of a Vector."""

    def __init__(self, x, y):
        """Initialize vector.

        :param x: Initial projected value on the X axis.

        :param y: Initial projected value on the Y axis.


        """
        self._value = (x, y)

    def __repr__(self):
        """Display representation of vector"""
        return "<Vector(x={},y={})>".format(self._value[0], self._value[1])

    def __add__(self, other):
        """Addition with vector.

        :param other: Instance of :class:`Vector` or scalar.

        :return: Instance of :class:`Vector`.

        """
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        return Vector(self.x + other, self.y + other)

    def __iadd__(self, other):
        """In-place addition with vector.

        :param other: Instance of :class:`Vector` or scalar.

        :return: Instance of :class:`Vector`.

        """
        self._value = (self + other)._value
        return self

    def __sub__(self, other):
        """Subtraction with vector.

        :param other: Instance of :class:`Vector` or scalar.

        :return: Instance of :class:`Vector`.

        """
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)
        return Vector(self.x - other, self.y - other)

    def __isub__(self, other):
        """In-place subtraction with vector.

        :param other: Instance of :class:`Vector` or scalar.

        :return: Instance of :class:`Vector`.

        """
        self._value = (self - other)._value
        return self

    def __mul__(self, other):
        """Multiplication with vector.

        :param other: Instance of :class:`Vector` or scalar.

        :return: Instance of :class:`Vector`.

        """
        if isinstance(other, Vector):
            return Vector(self.x * other.x, self.y * other.y)
        return Vector(self.x * other, self.y * other)

    def __imul__(self, other):
        """In-place multiplication with vector.

        :param other: Instance of :class:`Vector` or scalar.

        :return: Instance of :class:`Vector`.

        """
        self._value = (self * other)._value
        return self

    def __div__(self, other):
        """Division with vector.

        :param other: Instance of :class:`Vector` or scalar.

        :return: Instance of :class:`Vector`.

        """
        if isinstance(other, Vector):
            return Vector(self.x / other.x, self.y / other.y)
        return Vector(self.x / other, self.y / other)

    def __idiv__(self, other):
        """In-place division with vector.

        :param other: Instance of :class:`Vector` or scalar.

        :return: Instance of :class:`Vector`.

        """
        self._value = (self / other)._value
        return self

    def __iter__(self):
        """Iterate though vector values.

        :return: Iterator.

        """
        return iter(self._value)

    def __abs__(self):
        """Length of the vector

        :return: Floating value.

        """
        return math.sqrt(sum(v * v for v in list(self)))

    @property
    def x(self):
        """Projected value on the X axis.

        :return: Integer value.

        """
        return self._value[0]

    @property
    def y(self):
        """Projected value on the Y axis.

        :return: Integer value.

        """
        return self._value[1]

    def dot(self, other):
        """Return the dot product of two vectors.

        :param other: Instance of :class:`Vector`.

        :return: Floating value.

        """
        return sum(v * w for v, w in zip(self, other))

    def unit_vector(self):
        """Return unit vector.

        :return: Instance of :class:`Vector`.

        """
        return self / abs(self)
