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
        return 12

    @staticmethod
    def height():
        """Return height of the node."""
        return 12

    @staticmethod
    def radius():
        """Return radius of node."""
        return 6

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


class PolygonNode(BaseNode):
    """Representation of a Polygon node."""

    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def vertices(self):
        """Return all vertices of the node as vectors."""

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


class RectangleNode(PolygonNode):
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
        return [Vector(1, 0), Vector(0, 1)]

    @property
    def vertices(self):
        """Return all vertices of the node as vectors."""
        return [
            self.position,
            self.position + Vector(0, self.height()),
            self.position + Vector(self.width(), self.height()),
            self.position + Vector(self.width(), 0),
        ]


class ViewerNode(PolygonNode):
    """Representation of a Viewer node."""

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
        return [Vector(0, 1), Vector(-0.6, 1), Vector(0.6, 1)]

    @property
    def vertices(self):
        """Return all vertices of the node as vectors."""
        # The bevel is exaggerated to provide more interesting bounces.
        bevel = 15

        # Top position is shifted to the right.
        _position = self.position + Vector(bevel - 2, 0)

        return [
            _position,
            _position + Vector(-bevel, self.height() / 2),
            _position + Vector(0, self.height()),
            _position + Vector(self.width() - bevel, self.height()),
            _position + Vector(self.width(), self.height() / 2),
            _position + Vector(self.width() - bevel, 0),
        ]
