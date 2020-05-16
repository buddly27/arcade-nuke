# :coding: utf-8

import math


def collision(node1, node2):
    """Check collision between two nodes.

    :param node1: Instance of :class:`arcade_nuke.node.BaseNode`.

    :param node2: Instance of :class:`arcade_nuke.node.BaseNode`.

    :return: None if no collision of Instance of :class:`Vector` representing
        the push vector.

    """
    # Ignore if the two nodes are too far apart.
    delta = node2.middle_position - node1.middle_position
    if abs(delta) > 40:
        return

    # Check separating axis against all normals.
    normals = set(node1.normals + node2.normals)

    push_vectors = []

    for normal in normals:
        min1, max1 = node1.projection(normal)
        min2, max2 = node2.projection(normal)
        if not (max1 >= min2 and max2 >= min1):
            return

        distance = min(max2 - min1, max1 - min2)

        # If collision is confirmed, compute push vector.
        vector = normal * (distance / abs(normal) + 1)
        push_vectors.append(vector)

    # Compute the minimum push vector to determine the change in motion vector.
    push_vector = min(push_vectors, key=(lambda _vector: abs(_vector)))

    # Compute distance between two node centers.
    if delta.dot(push_vector) > 0:
        push_vector *= -1

    # Convert into a unit vector.
    return push_vector / abs(push_vector)


def bounce(motion_vector, push_vector):
    """Compute reflected vector after a collision.

    :param motion_vector: Instance of incoming :class:`Vector`.

    :param push_vector: Instance of normal push :class:`Vector` as returned by
        :func:`collision`.

    :return: Reflected instance of :class:`Vector`.

    """
    return push_vector * motion_vector.dot(push_vector) * -2 + motion_vector


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

    def __hash__(self):
        """Compute hash for vector."""
        return hash(self._value)

    def __eq__(self, other):
        """Compare with vector.

        :param other: Instance of :class:`Vector`.

        """
        return isinstance(other, Vector) and self._value == other._value

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
