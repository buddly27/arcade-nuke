# :coding: utf-8

import abc
import uuid

import nuke

from arcade_nuke.logic import Vector


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
        self._motion_vector = Vector(0, 0)

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
    def motion_vector(self):
        """Return motion vector of the node."""
        return self._motion_vector

    @motion_vector.setter
    def motion_vector(self, value):
        """Return motion vector of the node."""
        self._motion_vector = value

    @property
    def middle_position(self):
        """Return current middle position the top-left corner of the node."""
        position = self.position
        return position + Vector(self.width()/2, self.height()/2)

    @abc.abstractproperty
    def normals(self):
        """Return normals."""

    @abc.abstractmethod
    def projection(self, normal):
        """Return minimum and maximum projection on the X axis.

        :param normal: Normal vector to project onto.

        """

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


class DotNode(BaseNode):
    """Representation of a Dot node."""

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

    def label(self):
        """Return label of the node."""
        return "dot"

    @property
    def node_class(self):
        """Return class of the node."""
        return "Dot"

    @property
    def normals(self):
        """Return normals."""
        return []

    def projection(self, normal):
        """Return minimum and maximum projection on the X axis.

        :param normal: Normal vector to project onto.

        :return: Tuple containing the minimum and maximum values.

        """
        minimum, maximum = float("+inf"), float("-inf")

        for vertex in [
            self.middle_position - normal * self.radius(),
            self.middle_position + normal * self.radius()
        ]:
            projection = vertex.dot(normal)
            minimum = min(minimum, projection)
            maximum = max(maximum, projection)

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

    @property
    def normals(self):
        """Return normals."""
        return [Vector(1, 0), Vector(0, 1), Vector(-1, 0), Vector(0, -1)]

    @property
    def vertices(self):
        """Return all vertices of the node as vectors."""
        return [
            self.position,
            self.position + Vector(0, self.height()),
            self.position + Vector(self.width(), self.height()),
            self.position + Vector(self.width(), 0),
        ]

    def projection(self, normal):
        """Return minimum and maximum projection on the X axis.

        :param normal: Normal vector to project onto.

        :return: Tuple containing the minimum and maximum values.

        """
        minimum, maximum = float("+inf"), float("-inf")
        for vertex in self.vertices:
            projection = vertex.dot(normal)
            minimum = min(minimum, projection)
            maximum = max(maximum, projection)

        return minimum, maximum


class ViewerNode(BaseNode):
    """Representation of a Viewer node."""

    __metaclass__ = abc.ABCMeta

    @staticmethod
    def width():
        """Return width of the node."""
        return 83

    @staticmethod
    def height():
        """Return height of the node."""
        return 17

    @property
    def label(self):
        """Return label of the node."""
        return "viewer"

    @property
    def node_class(self):
        """Return class of the node."""
        return "Viewer"

    @property
    def normals(self):
        """Return normals."""
        return [
            Vector(0, 1), Vector(-0.5, 1), Vector(0.5, 1),
            Vector(0, -1), Vector(-0.5, -1), Vector(0.5, -1),
        ]

    @property
    def vertices(self):
        """Return all vertices of the node as vectors."""
        bevel = 15
        return [
            self.position + Vector(0, self.height() / 2),
            self.position + Vector(bevel, self.height()),
            self.position + Vector(self.width() - bevel, self.height()),
            self.position + Vector(self.width(), self.height() / 2),
            self.position + Vector(self.width() - bevel, 0),
            self.position + Vector(bevel, 0),
        ]

    def projection(self, normal):
        """Return minimum and maximum projection on the X axis.

        :param normal: Normal vector to project onto.

        :return: Tuple containing the minimum and maximum values.

        """
        minimum, maximum = float("+inf"), float("-inf")
        for vertex in self.vertices:
            projection = vertex.dot(normal)
            minimum = min(minimum, projection)
            maximum = max(maximum, projection)

        return minimum, maximum
