# :coding: utf-8

import abc
import uuid
import math

import nuke


class BaseNode(object):
    """Basic representation of a Nuke Node."""

    __metaclass__ = abc.ABCMeta

    def __init__(self, x, y):
        """Initialise node.

        :param x: Initial position of left corner of the node on the X axis.

        :param y: Initial position of top corner of the node on the Y axis.

        """
        self._name = "node_{}".format(uuid.uuid4().hex)
        self._position = Vector(x, y)
        self._destroyed = False

    @staticmethod
    def width():
        """Return width of the node."""
        raise NotImplemented()

    @staticmethod
    def height():
        """Return height of the node."""
        raise NotImplemented()

    @abc.abstractproperty
    def label(self):
        """Return label of the node."""

    @abc.abstractproperty
    def node_class(self):
        """Return class of the node."""

    @property
    def position(self):
        """Return current position the node."""
        node = self.node()
        return Vector(node.xpos(), node.ypos())

    @property
    def middle_position(self):
        """Return current middle position the top-left corner of the node."""
        position = self.position
        return position + Vector(self.width()/2, self.height()/2)

    def destroyed(self):
        """Indicate whether the node is destroyed."""
        return self._destroyed

    def reset(self):
        """Reset node."""
        self._destroyed = False

        node = self.node()
        node.setXpos(self._position.x)
        node.setYpos(self._position.y)

    def node(self):
        """Retrieve the the node."""
        if self._destroyed:
            raise RuntimeError(
                "Node '{}' already destroyed...".format(self.label)
            )

        node = nuke.toNode(self._name)
        if not node:
            node = self.create_node()

        return node

    def create_node(self):
        """Create node."""
        node = getattr(nuke.nodes, self.node_class)(
            name=self._name,
            xpos=self._position.x,
            ypos=self._position.y,
            hide_input=True
        )
        node["autolabel"].setValue("' '")
        return node

    def destroy(self):
        """Delete node."""
        node = self.node()
        nuke.delete(node)
        self._destroyed = True

    @abc.abstractmethod
    def projection_x(self):
        """Return minimum and maximum projection on the X axis.

        :return: Tuple containing the minimum and maximum values.

        """

    @abc.abstractmethod
    def projection_y(self):
        """Return minimum and maximum projection on the Y axis.

        :return: Tuple containing the minimum and maximum values.

        """


class DotNode(BaseNode):
    """Representation of a Dot node."""

    __metaclass__ = abc.ABCMeta

    @staticmethod
    def width():
        """Return width of the node."""
        return 11

    @staticmethod
    def height():
        """Return height of the node."""
        return 11

    @staticmethod
    def radius():
        """Return radius of node."""
        return 5.5

    @property
    def node_class(self):
        """Return class of the node."""
        return "Dot"

    def projection_x(self):
        """Return minimum and maximum projection on the X axis.

        :return: Tuple containing the minimum and maximum values.

        """
        minimum = self.middle_position.x - self.radius()
        maximum = self.middle_position.x + self.radius()
        return minimum, maximum

    def projection_y(self):
        """Return minimum and maximum projection on the Y axis.

        :return: Tuple containing the minimum and maximum values.

        """
        minimum = self.middle_position.y - self.radius()
        maximum = self.middle_position.y + self.radius()
        return minimum, maximum


class RectangleNode(BaseNode):
    """Representation of a Rectangle node."""

    __metaclass__ = abc.ABCMeta

    @staticmethod
    def width():
        """Return width of the node."""
        return 79

    @staticmethod
    def height():
        """Return height of the node."""
        return 17

    def vertices(self):
        """Return all vertices of the node as vectors."""
        return [
            self.position,
            self.position + Vector(0, self.height()),
            self.position + Vector(self.width(), self.height()),
            self.position + Vector(self.width(), 0),
        ]

    def projection_x(self):
        """Return minimum and maximum projection on the X axis.

        :return: Tuple containing the minimum and maximum values.

        """
        minimum, maximum = float("+inf"), float("-inf")
        for vertex in self.vertices():
            projection = vertex.dot(Vector(1, 0))
            minimum = min(minimum, projection)
            maximum = max(maximum, projection)

        return minimum, maximum

    def projection_y(self):
        """Return minimum and maximum projection on the Y axis.

        :return: Tuple containing the minimum and maximum values.

        """
        minimum, maximum = float("+inf"), float("-inf")
        for vertex in self.vertices():
            projection = vertex.dot(Vector(0, 1))
            minimum = min(minimum, projection)
            maximum = max(maximum, projection)

        return minimum, maximum


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


def collision(node1, node2):
    """Check collision between two nodes

    It uses a simplified implementation of the SAT Collision algorithm as
    we consider that the nodes cannot rotate.

    :param node1: Instance of :class:`arcade_nuke.node.BaseNode`.

    :param node2: Instance of :class:`arcade_nuke.node.BaseNode`.

    :return: None if no collision of Instance of :class:`Vector` representing
        the push vector.

    """
    impact_vector = Vector(0, 0)

    # Horizontal axis
    min1, max1 = node1.projection_x()
    min2, max2 = node2.projection_x()

    if not (max1 >= min2 and max2 >= min1):
        return

    x = min(max1 - min2, max2 - min1)
    impact_vector += Vector(x, 0)

    # Vertical axis
    min1, max1 = node1.projection_y()
    min2, max2 = node2.projection_y()

    if not (max1 >= min2 and max2 >= min1):
        return

    y = min(max1 - min2, max2 - min1)
    impact_vector += Vector(0, y)

    # If collision is confirmed, compute push vector.
    if impact_vector.x > impact_vector.y:
        return Vector(1, -1)
    return Vector(-1, 1)
