# :coding: utf-8

import uuid
import math

import nuke
from PySide2 import QtGui, QtWidgets, QtCore


class Game(object):
    """Object managing all elements of the game.
    """

    def __init__(self):
        """Initialize the game."""
        self._timer = QtCore.QTimer()
        self._timer.setInterval(5)
        self._timer.timeout.connect(self._play)

        self._field = None
        self._paddle = None
        self._ball = None
        self._brick_manager = None

        self._initialized = False

    def initialize(self):
        """Initialize the game."""
        # Initialize the field.
        self._field = Field(x=0, y=0, width=47, height=30, padding=10)

        # Initialize the paddle.
        self._paddle = Paddle(
            x=self._field.center_x,
            y=self._field.bottom_edge - 20,
        )

        # Initialize the ball.
        self._ball = Ball(
            x=self._paddle.x,
            y=self._paddle.y
        )

        # Initialize the brick pattern to destroy.
        self._brick_manager = BrickManager(
            x=self._field.left_edge + 30,
            y=self._field.top_edge + 20
        )

        self._initialized = True

    def start(self):
        """Start the game."""
        if not self._initialized:
            return

        self._timer.start()

    def stop(self):
        """Stop the game."""
        if not self._initialized:
            return

        self._timer.stop()

    def _play(self):
        """Method called for each move of the game."""
        # Move the paddle according to the cursor position.
        self._paddle.move(
            y=self._field.bottom_edge - 20,
            right_edge=self._field.right_edge,
            left_edge=self._field.left_edge
        )

        # Move the ball according to its motion vector.
        self._ball.move()

        # Check whether the ball hit one of the walls of the field.
        if self._field.hit_wall(self._ball):
            print("Collision with field")
            return

        # Check whether the ball hits one brick.
        elif self._brick_manager.hit_brick(self._ball):
            print("Brick destroyed!!!")
            return


class Field(object):
    """Object managing the field of the game."""

    #: Width of the Dot node representing the field units.
    DOT_WIDTH = 11

    #: Height of the Dot node representing the field units.
    DOT_HEIGHT = 11

    def __init__(self, x, y, width, height, padding):
        """Initialize the field.

        :param x: Position of the left edge of the field on the X axis.

        :param y: Position of the top edge of the field on the Y axis.

        :param width: Number of dots to define the width of the field.

        :param height: Number of dots to define the height of the field.

        :param padding: Padding between each dot defining the limit of the
            field.

        """
        self._top = y + self.DOT_HEIGHT
        self._right = (
            x + (self.DOT_WIDTH + padding) * (width - 1) - self.DOT_WIDTH
        )
        self._bottom = (
            y + (self.DOT_HEIGHT + padding) * height - self.DOT_HEIGHT
        )
        self._left = x + self.DOT_WIDTH

        # TOP
        for index in range(width):
            nuke.nodes.Dot(
                xpos=x + (self.DOT_WIDTH + padding) * index,
                ypos=y,
                hide_input=True
            )

        # LEFT
        for index in range(1, height):
            nuke.nodes.Dot(
                xpos=x,
                ypos=y + (self.DOT_WIDTH + padding) * index,
                hide_input=True
            )

        # RIGHT
        for index in range(1, height):
            nuke.nodes.Dot(
                xpos=x + (self.DOT_WIDTH + padding) * (width - 1),
                ypos=y + (self.DOT_HEIGHT + padding) * index,
                hide_input=True
            )

        # BOTTOM
        for index in range(width):
            nuke.nodes.Dot(
                xpos=x + (self.DOT_WIDTH + padding) * index,
                ypos=y + (self.DOT_HEIGHT + padding) * height,
                hide_input=True
            )

        # Zoom on the field
        nuke.zoom(0)

    @property
    def center_x(self):
        """Return the middle of the field on the X axis."""
        return int(self.left_edge + (self.right_edge - self.left_edge) / 2.0)

    @property
    def right_edge(self):
        """Return the right edge of the field."""
        return self._right

    @property
    def left_edge(self):
        """Return the left edge of the field."""
        return self._left

    @property
    def bottom_edge(self):
        """Return the bottom edge of the field."""
        return self._bottom

    @property
    def top_edge(self):
        """Return the top edge of the field."""
        return self._top

    def hit_wall(self, ball):
        """Indicate whether the *ball* hit one of the wall.

        Modify the ball direction accordingly if necessary.

        :param ball: Instance of :class:`Ball`.

        :return: Boolean value.

        """
        if ball.x > self._right or ball.x < self._left:
            ball.bounce_horizontal()
            return True

        if ball.y > self._bottom or ball.y < self._top:
            ball.bounce_vertical()
            return True

        return False


class Ball(object):
    """Object managing the ball."""

    #: Unique name of the ball.
    NAME = uuid.uuid4().hex

    #: Radius of the Dot node representing the ball.
    RADIUS = 5.5

    def __init__(self, x, y):
        """Initialize the ball.

        :param x: Initial position of the ball on the X axis.

        :param y: Initial position of the ball on the Y axis.

        """
        self._x = x
        self._y = y
        self._vector = Vector(1, -3)

        self._get_node()

    @property
    def x(self):
        """Position of the center of the ball on the X axis"""
        node = self._get_node()
        return node.xpos() + self.RADIUS

    @property
    def y(self):
        """Position of the center of the ball on the Y axis"""
        node = self._get_node()
        return node.ypos() + self.RADIUS

    def move(self):
        """Move the ball following the motion vector."""
        node = self._get_node()
        node.setXpos(int(round(self.x - self.RADIUS + self._vector.x)))
        node.setYpos(int(round(self.y - self.RADIUS + self._vector.y)))

    def bounce_horizontal(self):
        """Invert the motion vector on the horizontal axis."""
        self._vector *= Vector(-1, 1)

    def bounce_vertical(self):
        """Invert the motion vector on the vertical axis."""
        self._vector *= Vector(1, -1)

    def _get_node(self):
        """Retrieve the the node representing the ball.

        Create the ball if necessary at the initial position using its unique
        name.

        """
        node = nuke.toNode(self.NAME)

        if not node:
            node = nuke.nodes.Dot(
                name=self.NAME,
                xpos=self._x + 20,
                ypos=self._y - 20,
                hide_input=True
            )

            # Reset motion vector.
            self._vector = Vector(1, -3)

        return node


class Paddle(object):
    """Object managing the paddle."""

    #: Width of the Viewer node representing the paddle.
    WIDTH = 70

    def __init__(self, x, y):
        """Initialize the paddle.

        :param x: Initial position of the paddle on the X axis.

        :param y: Initial position of the paddle on the Y axis.

        """
        self._x = x
        self._y = y

        node = self._get_node()
        node.setXpos(self._x)
        node.setYpos(self._y)

    @property
    def x(self):
        """Position of the paddle on the X axis."""
        node = self._get_node()
        return node.xpos()

    @property
    def y(self):
        """Position of the paddle on the Y axis."""
        node = self._get_node()
        return node.ypos()

    def move(self, y, right_edge, left_edge):
        """Move the paddle on the X axis within the limit of the field.

        Use the position of the cursor to determine the position.

        :param y: Position of the paddle on the Y axis.

        :param right_edge: Maximum position on the X axis.

        :param left_edge: Minimum position on the X axis.

        """
        cursor = QtGui.QCursor.pos()

        node = self._get_node()

        right_edge -= self.WIDTH
        node.setXpos(min(max(cursor.x(), left_edge), right_edge))
        node.setYpos(y)

    def _get_node(self):
        """Retrieve the the node representing the paddle.

        Create the paddle if necessary.

        """
        nodes = nuke.allNodes("Viewer")
        if not len(nodes):
            nodes = [nuke.nodes.Viewer(xpos=self._x, ypos=self._y)]
        return nodes[0]


class BrickManager(object):
    """Object managing the brick pattern to destroy."""

    def __init__(self, x, y):
        """Initialize the brick pattern.

        :param x: Position of the left edge of the brick pattern on the X axis.

        :param y: Position of the top edge of the brick pattern on the Y axis.

        """
        # Number of bricks on the X axis.
        width = 10

        # Padding between each brick on both axis.
        padding_h = 10
        padding_v = 8

        # Node classes to use for each line of bricks.
        node_classes = [
            "Grade",
            "Roto",
            "Glow",
            "AddMix",
            "Write",
            "Shuffle",
            "Noise"
        ]

        # Mapping recording each brick per unique name.
        self._mapping = {}

        for y_index, node_class in enumerate(node_classes):
            for x_index in range(width):
                label = str((y_index * width) + x_index)
                brick = Brick(
                    x=x + (Brick.WIDTH + padding_h) * x_index,
                    y=y,
                    node_class=node_class,
                    label=label
                )
                self._mapping[label] = brick

            y += (Brick.HEIGHT + padding_v)

    def hit_brick(self, ball):
        """Indicate whether the *ball* hit one of the bricks.

        Destroy the brick and modify the ball direction accordingly if
        necessary.

        :param ball: Instance of :class:`Ball`.

        :return: Boolean value.

        """
        for label, brick in self._mapping.items():
            if brick.hit(ball):
                del self._mapping[label]
                return True

        return False


class Brick(object):
    """Object managing a single brick."""

    #: Width of the node representing the paddle.
    WIDTH = 79

    #: Height of the node representing the paddle.
    HEIGHT = 17

    def __init__(self, x, y, node_class, label):
        """Initialize the brick.

        :param x: Position of the brick on the X axis.

        :param y: Position of the brick on the Y axis.

        :param node_class: Class of the node to create to represent the brick.

        :param label: Label of the brick.

        """
        self._name = uuid.uuid4().hex
        self._node_class = node_class
        self._label = label
        self._x = x
        self._y = y

        node = self._get_node()
        self._top = node.ypos()
        self._left = node.xpos()
        self._bottom = node.ypos() + self.HEIGHT
        self._right = node.xpos() + self.WIDTH

    def hit(self, ball):
        """Indicate whether the *ball* hit the brick.

        Destroy the brick and modify the ball direction accordingly if
        necessary.

        :param ball: Instance of :class:`Ball`.

        :return: Boolean value.

        """
        node = self._get_node()

        if (
            self._right > ball.x > self._left and
            self._bottom > ball.y > self._top
        ):
            nuke.delete(node)
            ball.bounce_vertical()
            return True

        return False

    def _get_node(self):
        """Retrieve the the node representing the brick.

        Create the brick if necessary.

        """
        node = nuke.toNode(self._name)

        if not node:
            node = getattr(nuke.nodes, self._node_class)(
                name=self._name,
                xpos=self._x,
                ypos=self._y,
                hide_input=True
            )
            node["autolabel"].setValue(self._label)

        return node


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

    def dot(self, other):
        """Return the dot product of two vectors.

        :param other: Instance of :class:`Vector`.

        :return: Floating value.

        """
        return sum(v * w for v, w in zip(self, other))

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
