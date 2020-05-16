# :coding: utf-8

import nuke
from PySide2 import QtGui, QtWidgets, QtCore

import arcade_nuke.base
import arcade_nuke.node
import arcade_nuke.logic


class BreakoutGame(arcade_nuke.base.BaseGame):
    """Object managing all elements of the game.
    """

    def __init__(self, generator):
        """Initialize the game.

        :param generator: Callback to draw the brick pattern.

        """
        super(BreakoutGame, self).__init__()

        # Setup elements of game.
        self._setup_field()

        # Draw brick pattern.
        self._bricks = generator(
            x=self._field.left_edge,
            y=self._field.top_edge
        )

        self._initialized = False

    def initialize(self):
        """Initialize the game."""
        super(BreakoutGame, self).initialize()

        self._field.reset()
        self._paddle.reset()
        self._ball.reset()

        for brick in self._bricks:
            brick.reset()

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

        except arcade_nuke.base.GameOver:
            self._ball.destroy()
            self.stop()
            self.signal.stopped.emit()

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
            y=self._field.bottom_edge - 40
        )

    def _check_collision(self):
        """Indicate whether the *ball* hit one of the game elements.
        """
        # Check collision with the wall of the field.
        if (
            self._ball.position.x > self._field.right_edge or
            self._ball.position.x < self._field.left_edge
        ):
            self._ball.motion_vector *= arcade_nuke.node.Vector(-1, 1)
            return

        if self._ball.position.y < self._field.top_edge:
            self._ball.motion_vector *= arcade_nuke.node.Vector(1, -1)
            return

        if self._ball.position.y > self._field.bottom_edge:
            raise arcade_nuke.base.GameOver("Failed!")

        # Check collision with the bricks.
        bricks_destroyed = 0

        for brick in self._bricks:
            if brick.destroyed():
                bricks_destroyed += 1
                continue

            push_vector = arcade_nuke.logic.collision(self._ball, brick)
            if push_vector is not None:
                self._ball.motion_vector = arcade_nuke.logic.bounce(
                    self._ball.motion_vector, push_vector
                )

                # Destroy brick
                brick.destroy()

        # Raise if all bricks are destroyed.
        if len(self._bricks) == bricks_destroyed:
            raise arcade_nuke.base.GameOver("Done!")

        # Check collision with the paddle.
        push_vector = arcade_nuke.logic.collision(self._ball, self._paddle)
        if push_vector is not None:
            self._ball.motion_vector = arcade_nuke.logic.bounce(
                self._ball.motion_vector, push_vector
            )


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
        self.motion_vector = arcade_nuke.node.Vector(1, -3)

    @property
    def label(self):
        """Return label of the node."""
        return "ball"

    def move(self):
        """Move the ball following the motion vector."""
        node = self.node()
        node.setXpos(int(round(self.position.x + self.motion_vector.x)))
        node.setYpos(int(round(self.position.y + self.motion_vector.y)))

    def reset(self):
        """Reset node."""
        super(Ball, self).reset()

        # Reset motion vector.
        self.motion_vector = arcade_nuke.node.Vector(1, -3)


class Paddle(arcade_nuke.node.ViewerNode):
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


def brick_generator1(x, y):
    """Draw first brick pattern.

    :param x: Position of the left edge of the field on the X axis.

    :param y: Position of the top edge of the field on the Y axis.

    +-----------------------------------------+
    | +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ |
    | +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ |
    | +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ |
    | +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ |
    | +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ |
    | +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ |
    | +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ |
    |                                         |
    |                                         |
    |                                         |
    |                                         |
    +-----------------------------------------+

    """
    bricks = []

    # Initialize top-left position.
    x += 30
    y += 20

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
            bricks.append(brick)

        y += (Brick.height() + padding_v)

    return bricks


def brick_generator2(x, y):
    """Draw first brick pattern.

    :param x: Position of the left edge of the field on the X axis.

    :param y: Position of the top edge of the field on the Y axis.

    +-----------------------------------------+
    |           +-+             +-+           |
    |               +-+     +-+               |
    |               +-+     +-+               |
    |           +-+ +-+ +-+ +-+ +-+           |
    |           +-+ +-+ +-+ +-+ +-+           |
    |       +-+ +-+     +-+     +-+ +-+       |
    |       +-+ +-+     +-+     +-+ +-+       |
    |   +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+   |
    |   +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+   |
    |   +-+     +-+ +-+ +-+ +-+ +-+     +-+   |
    |   +-+     +-+             +-+     +-+   |
    |   +-+     +-+             +-+     +-+   |
    |               +-+     +-+               |
    |               +-+     +-+               |
    |                                         |
    |                                         |
    |                                         |
    |                                         |
    +-----------------------------------------+

    """
    bricks = []

    # Initialize top-left position.
    x += 80
    y += 20

    # Padding between each brick on both axis.
    padding_h = 10
    padding_v = 8

    # Initialize index.
    index = 0

    # Draw antennas.
    coordinates = [(2, 0), (6, 0), (3, 1), (5, 1), (3, 2), (5, 2)]
    for index_x, index_y in coordinates:
        brick = Brick(
            x=x + (Brick.width() + padding_h) * index_x,
            y=y + (Brick.height() + padding_v) * index_y,
            node_class="Write", label=str(index)
        )
        bricks.append(brick)
        index += 1

    # Draw head.
    coordinates = [
        (2, 3), (3, 3), (4, 3), (5, 3), (6, 3),
        (2, 4), (3, 4), (4, 4), (5, 4), (6, 4),
        (1, 5), (2, 5), (4, 5), (6, 5), (7, 5),
        (1, 6), (2, 6), (4, 6), (6, 6), (7, 6),
        (0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), (8, 7),
        (0, 8), (1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8),
        (2, 9), (3, 9), (4, 9), (5, 9), (6, 9)
    ]
    for index_x, index_y in coordinates:
        brick = Brick(
            x=x + (Brick.width() + padding_h) * index_x,
            y=y + (Brick.height() + padding_v) * index_y,
            node_class="AddMix", label=str(index)
        )
        bricks.append(brick)
        index += 1

    # Draw feet.
    coordinates = [
        (0, 9), (8, 9),
        (0, 10), (2, 10), (6, 10), (8, 10),
        (0, 11), (2, 11), (6, 11), (8, 11),
        (3, 12), (5, 12),
        (3, 13), (5, 13),
    ]
    for index_x, index_y in coordinates:
        brick = Brick(
            x=x + (Brick.width() + padding_h) * index_x,
            y=y + (Brick.height() + padding_v) * index_y,
            node_class="Write", label=str(index)
        )
        bricks.append(brick)
        index += 1

    return bricks


def brick_generator3(x, y):
    """Draw first brick pattern.

    :param x: Position of the left edge of the field on the X axis.

    :param y: Position of the top edge of the field on the Y axis.

    +-----------------------------------------+
    |       +-+ +-+             +-+ +-+       |
    |   +-+ +-+ +-+ +-+     +-+ +-+ +-+ +-+   |
    |   +-+ +-+ +-+ +-+     +-+ +-+ +-+ +-+   |
    |   +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+   |
    |   +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+   |
    |   +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+   |
    |   +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+   |
    |       +-+ +-+ +-+ +-+ +-+ +-+ +-+       |
    |       +-+ +-+ +-+ +-+ +-+ +-+ +-+       |
    |           +-+ +-+ +-+ +-+ +-+           |
    |           +-+ +-+ +-+ +-+ +-+           |
    |               +-+ +-+ +-+               |
    |               +-+ +-+ +-+               |
    |                   +-+                   |
    |                                         |
    |                                         |
    |                                         |
    |                                         |
    +-----------------------------------------+

    """
    bricks = []

    # Initialize top-left position.
    x += 80
    y += 20

    # Padding between each brick on both axis.
    padding_h = 10
    padding_v = 8

    # Initialize index.
    index = 0

    coordinates = [
        (1, 0), (2, 0), (6, 0), (7, 0),
        (0, 1), (1, 1), (2, 1), (3, 1), (5, 1), (6, 1), (7, 1), (8, 1),
        (0, 2), (1, 2), (2, 2), (3, 2), (5, 2), (6, 2), (7, 2), (8, 2),
        (0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3),
        (0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4),
        (0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5),
        (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6), (8, 6),
        (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
        (1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8),
        (2, 9), (3, 9), (4, 9), (5, 9), (6, 9),
        (2, 10), (3, 10), (4, 10), (5, 10), (6, 10),
        (3, 11), (4, 11), (5, 11),
        (3, 12), (4, 12), (5, 12),
        (4, 13),
    ]

    for index_x, index_y in coordinates:
        brick = Brick(
            x=x + (Brick.width() + padding_h) * index_x,
            y=y + (Brick.height() + padding_v) * index_y,
            node_class="Shuffle", label=str(index)
        )
        bricks.append(brick)
        index += 1

    return bricks
