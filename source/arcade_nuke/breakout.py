# :coding: utf-8

import nuke
from PySide2 import QtGui, QtWidgets, QtCore

import arcade_nuke.node
from arcade_nuke.node import Vector


class GameOver(Exception):
    """Exception to raise when the game is over."""


class Game(object):
    """Object managing all elements of the game.
    """

    def __init__(self):
        """Initialize the game."""
        self._timer = QtCore.QTimer()
        self._timer.setInterval(5)
        self._timer.timeout.connect(self._process)

        # Setup elements of game.
        self._setup_field()
        self._setup_brick_pattern()

        self._initialized = False

    def initialize(self):
        """Initialize the game."""
        self._field.reset()
        self._paddle.reset()
        self._ball.reset()

        for brick in self._brick_mapping.values():
            brick.reset()

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

    def _process(self):
        """Method called for each move of the game."""
        # Move the paddle according to the cursor position.
        self._paddle.move(
            y=self._field.bottom_edge - 20,
            right_edge=self._field.right_edge,
            left_edge=self._field.left_edge
        )

        # Move the ball according to its motion vector.
        self._ball.move()

        try:
            self._check_collision()

        except GameOver:
            self._ball.destroy()
            self.stop()

            self._initialized = False

    def _setup_field(self):
        """Initialize game field."""
        self._field = Field(x=0, y=0, width=47, height=30, padding=10)

        self._paddle = Paddle(
            x=self._field.center_x - Paddle.width() / 2,
            y=self._field.bottom_edge - 25,
        )

        self._ball = Ball(
            x=self._field.center_x,
            y=self._field.bottom_edge - 25
        )

    def _setup_brick_pattern(self):
        """Initialize brick patterns."""
        self._brick_mapping = {}

        # Initial top-left position.
        x = self._field.left_edge + 30
        y = self._field.top_edge + 20

        # Number of bricks on the X axis.
        width = 10

        # Padding between each brick on both axis.
        padding_h = 10
        padding_v = 8

        # Node classes to use for each line of bricks.
        node_classes = [
            "Grade", "Roto", "Glow", "AddMix", "Write", "Shuffle", "Noise"
        ]

        for y_index, node_class in enumerate(node_classes):
            for x_index in range(width):
                label = str((y_index * width) + x_index)
                brick = Brick(
                    x=x + (Brick.width() + padding_h) * x_index, y=y,
                    node_class=node_class, label=label
                )
                self._brick_mapping[label] = brick

            y += (Brick.height() + padding_v)

    def _check_collision(self):
        """Indicate whether the *ball* hit one of the game elements.
        """
        # Check collision with the wall of the field.
        if (
            self._ball.position.x > self._field.right_edge or
            self._ball.position.x < self._field.left_edge
        ):
            self._ball.motion_vector *= Vector(-1, 1)
            return

        if self._ball.position.y < self._field.top_edge:
            self._ball.motion_vector *= Vector(1, -1)
            return

        if self._ball.position.y > self._field.bottom_edge:
            raise GameOver("Failed!")

        # Check collision with the bricks.
        for label, brick in self._brick_mapping.items():
            push_vector = arcade_nuke.node.collision(self._ball, brick)
            if push_vector is not None:
                print(push_vector)

                self._ball.motion_vector *= push_vector

                # Destroy brick
                brick.destroy()
                del self._brick_mapping[label]

        # Check collision with the paddle.
        push_vector = arcade_nuke.node.collision(self._ball, self._paddle)
        if push_vector is not None:
            self._ball.motion_vector *= push_vector


class Field(object):
    """Object managing the field of the game."""

    def __init__(self, x, y, width, height, padding):
        """Initialize the field.

        :param x: Position of the left edge of the field on the X axis.

        :param y: Position of the top edge of the field on the Y axis.

        :param width: Number of dots to define the width of the field.

        :param height: Number of dots to define the height of the field.

        :param padding: Padding between each dot defining the limit of the
            field.

        """
        self._units = []

        # Units representing top wall.
        for index in range(width):
            unit = FieldUnit(x + (FieldUnit.width() + padding) * index, y)
            self._units.append(unit)

        # Units representing left wall.
        for index in range(1, height):
            unit = FieldUnit(x, y + (FieldUnit.height() + padding) * index)
            self._units.append(unit)

        # Units representing right wall.
        for index in range(1, height):
            unit = FieldUnit(
                x + (FieldUnit.width() + padding) * (width - 1),
                y + (FieldUnit.height() + padding) * index
            )
            self._units.append(unit)

        # Units representing bottom wall.
        for index in range(width):
            unit = FieldUnit(
                x + (FieldUnit.width() + padding) * index,
                y + (FieldUnit.height() + padding) * height
            )
            self._units.append(unit)

        # Compute edges.
        self._top = y + FieldUnit.height()
        self._left = x + FieldUnit.width()
        self._right = (
            x + (FieldUnit.width() + padding) * (width - 1) - FieldUnit.width()
        )
        self._bottom = (
            y + (FieldUnit.height() + padding) * height - FieldUnit.height()
        )

    def reset(self):
        """Reset field."""
        for unit in self._units:
            unit.reset()

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


class FieldUnit(arcade_nuke.node.DotNode):
    """Object managing the field unit."""

    @property
    def label(self):
        """Return label of the node."""
        return "field_unit"


class Ball(arcade_nuke.node.DotNode):
    """Object managing the ball."""

    def __init__(self, x, y):
        """Initialize the ball.

        :param x: Initial position of left corner of the node on the X axis.

        :param y: Initial position of top corner of the node on the Y axis.

        """
        super(Ball, self).__init__(x, y)
        self._motion_vector = Vector(1, -3)

    @property
    def label(self):
        """Return label of the node."""
        return "ball"

    @property
    def motion_vector(self):
        """Return motion vector of the ball."""
        return self._motion_vector

    @motion_vector.setter
    def motion_vector(self, value):
        """Return motion vector of the ball."""
        self._motion_vector = value

    def move(self):
        """Move the ball following the motion vector."""
        node = self.node()
        node.setXpos(int(round(self.position.x + self._motion_vector.x)))
        node.setYpos(int(round(self.position.y + self._motion_vector.y)))


class Paddle(arcade_nuke.node.RectangleNode):
    """Object managing the paddle."""

    @property
    def label(self):
        """Return label of the node."""
        return "paddle"

    @property
    def node_class(self):
        """Return class of the node."""
        return "Viewer"

    def move(self, y, right_edge, left_edge):
        """Move the paddle on the X axis within the limit of the field.

        Use the position of the cursor to determine the position.

        :param y: Position of the paddle on the Y axis.

        :param right_edge: Maximum position on the X axis.

        :param left_edge: Minimum position on the X axis.

        """
        cursor = QtGui.QCursor.pos()

        node = self.node()

        right_edge -= self.width()
        node.setXpos(min(max(cursor.x(), left_edge), right_edge))
        node.setYpos(y)


class Brick(arcade_nuke.node.RectangleNode):
    """Object managing a single brick."""

    def __init__(self, x, y, node_class, label):
        """Initialize the brick.

        :param x: Position of the brick on the X axis.

        :param y: Position of the brick on the Y axis.

        :param node_class: Class of the node to create to represent the brick.

        :param label: Label of the brick.

        """
        super(Brick, self).__init__(x, y)
        self._node_class = node_class
        self._label = label

    @property
    def label(self):
        """Return label of the node."""
        return "brick_{}".format(self._label)

    @property
    def node_class(self):
        """Return class of the node."""
        return self._node_class

    def create_node(self):
        """Create node."""
        node = super(Brick, self).create_node()
        node["autolabel"].setValue(self._label)
        return node
