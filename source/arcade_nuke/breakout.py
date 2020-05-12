# :coding: utf-8

import uuid

import nuke
from PySide2 import QtGui, QtWidgets, QtCore

from arcade_nuke.utility import Vector


class Game(object):
    """Object managing all elements of the game.
    """

    def __init__(self):
        """Initialize the game."""
        self._timer = QtCore.QTimer()
        self._timer.setInterval(5)
        self._timer.timeout.connect(self._play)

        # Setup elements of game.
        self._field = Field(x=0, y=0, width=47, height=30, padding=10)
        self._paddle = Paddle(
            x=self._field.center_x,
            y=self._field.bottom_edge - 20,
        )
        self._ball = Ball(
            x=self._field.center_x,
            y=self._field.bottom_edge - 25
        )
        self._brick_manager = BrickManager(
            x=self._field.left_edge + 30,
            y=self._field.top_edge + 20
        )

        self._initialized = False

    def initialize(self):
        """Initialize the game."""
        self._field.reset()
        self._paddle.reset()
        self._ball.reset()
        self._brick_manager.reset()

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

    #: Size of the Dot node representing the field units.
    UNIT = Vector(11, 11)

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
            self._units.append(
                dict(
                    name=str(uuid.uuid4()),
                    position=Vector(x + (self.UNIT.x + padding) * index, y)
                )
            )

        # Units representing left wall.
        for index in range(1, height):
            self._units.append(
                dict(
                    name=str(uuid.uuid4()),
                    position=Vector(x, y + (self.UNIT.x + padding) * index)
                )
            )

        # Units representing right wall.
        for index in range(1, height):
            self._units.append(
                dict(
                    name=str(uuid.uuid4()),
                    position=Vector(
                        x + (self.UNIT.x + padding) * (width - 1),
                        y + (self.UNIT.y + padding) * index
                    )
                )
            )

        # Units representing bottom wall.
        for index in range(width):
            self._units.append(
                dict(
                    name=str(uuid.uuid4()),
                    position=Vector(
                        x + (self.UNIT.x + padding) * index,
                        y + (self.UNIT.y + padding) * height
                    )
                )
            )

        # Compute edges.
        self._top = y + self.UNIT.y
        self._right = x + (self.UNIT.x + padding) * (width - 1) - self.UNIT.x
        self._bottom = y + (self.UNIT.y + padding) * height - self.UNIT.y
        self._left = x + self.UNIT.x

    def reset(self):
        """Reset field."""
        for unit in self._units:
            node = nuke.toNode(unit["name"])

            if not node:
                nuke.nodes.Dot(
                    name=unit["name"],
                    xpos=unit["position"].x,
                    ypos=unit["position"].y,
                    hide_input=True
                )

            else:
                node.setXpos(unit["position"].x)
                node.setYpos(unit["position"].y)

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
        if ball.position.x > self._right or ball.position.x < self._left:
            ball.motion_vector *= Vector(-1, 1)
            return True

        if ball.position.y > self._bottom or ball.position.y < self._top:
            ball.motion_vector *= Vector(1, -1)
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
        self._initial_position = Vector(x, y)
        self._motion_vector = Vector(1, -3)

    def reset(self):
        """Draw ball status."""
        node = self._get_node()
        node.setXpos(self._initial_position.x)
        node.setYpos(self._initial_position.y)

    @property
    def position(self):
        """Return the middle position the ball as a Vector."""
        node = self._get_node()
        return Vector(node.xpos(), node.ypos()) + self.RADIUS

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
        node = self._get_node()
        x = self.position.x - self.RADIUS
        y = self.position.y - self.RADIUS
        node.setXpos(int(round(x + self._motion_vector.x)))
        node.setYpos(int(round(y + self._motion_vector.y)))

    def _get_node(self):
        """Retrieve the the node representing the ball.

        Create the ball if necessary at the initial position using its unique
        name.

        """
        node = nuke.toNode(self.NAME)

        if not node:
            node = nuke.nodes.Dot(
                name=self.NAME,
                xpos=self._initial_position.x,
                ypos=self._initial_position.y,
                hide_input=True
            )

            # Reset motion vector.
            self._motion_vector = Vector(1, -3)

        return node


class Paddle(object):
    """Object managing the paddle."""

    #: Width of the Viewer node representing the paddle.
    WIDTH = 70

    #: Height of the node representing the paddle.
    HEIGHT = 17

    def __init__(self, x, y):
        """Initialize the paddle.

        :param x: Initial position of the paddle on the X axis.

        :param y: Initial position of the paddle on the Y axis.

        """
        self._position = Vector(x, y)

    def reset(self):
        """Reset paddle status."""
        node = self._get_node()
        node.setXpos(self._position.x)
        node.setYpos(self._position.y)

    @property
    def position(self):
        """Return the middle position the paddle as Vector."""
        node = self._get_node()
        position = Vector(node.xpos(), node.ypos())
        return position + Vector(self.WIDTH/2, self.HEIGHT/2)

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
            nodes = [
                nuke.nodes.Viewer(
                    xpos=self._position.x,
                    ypos=self._position.y
                )
            ]
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
                    x=x + (Brick.WIDTH + padding_h) * x_index, y=y,
                    node_class=node_class,
                    label=label
                )
                self._mapping[label] = brick

            y += (Brick.HEIGHT + padding_v)

    def reset(self):
        """Draw brick pattern status."""
        for brick in self._mapping.values():
            brick.reset()

    def hit_brick(self, ball):
        """Indicate whether the *ball* hit one of the bricks.

        Destroy the brick and modify the ball direction accordingly if
        necessary.

        :param ball: Instance of :class:`Ball`.

        :return: Boolean value.

        """
        for label, brick in self._mapping.items():
            if brick.hit(ball):
                brick.destroy()
                del self._mapping[label]
                return True

        return False


class Brick(object):
    """Object managing a single brick."""

    #: Width of the node representing the brick.
    WIDTH = 79

    #: Height of the node representing the brick.
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
        self._position = Vector(x, y)
        self._destroyed = False

    def reset(self):
        """Reset brick status."""
        self._get_node()
        self._destroyed = False

    @property
    def position(self):
        """Return the middle position the brick as Vector."""
        node = self._get_node()
        position = Vector(node.xpos(), node.ypos())
        return position + Vector(self.WIDTH/2, self.HEIGHT/2)

    def vertices(self):
        """Return all vertices of the brick as vectors."""
        top_left_position = self.position - Vector(self.WIDTH/2, self.HEIGHT/2)
        return [
            top_left_position,
            top_left_position + Vector(0, self.HEIGHT),
            top_left_position + Vector(self.WIDTH, self.HEIGHT),
            top_left_position + Vector(self.WIDTH, 0),
        ]

    def hit(self, ball):
        """Indicate whether the *ball* hit the brick.

        Destroy the brick and modify the ball direction accordingly if
        necessary.

        :param ball: Instance of :class:`Ball`.

        :return: Boolean value.

        """
        impact_vector = Vector(0, 0)

        # Horizontal axis
        min_brick, max_brick = float("+inf"), float("-inf")
        min_ball = ball.position.x - ball.RADIUS
        max_ball = ball.position.x + ball.RADIUS

        for vertex in self.vertices():
            projection = vertex.dot(Vector(1, 0))
            min_brick = min(min_brick, projection)
            max_brick = max(max_brick, projection)

        if not (max_brick >= min_ball and max_ball >= min_brick):
            return False

        x = min(max_ball - min_brick, max_brick - min_ball)
        impact_vector += Vector(x, 0)

        # Vertical axis
        min_brick, max_brick = float("+inf"), float("-inf")
        min_ball = ball.position.y - ball.RADIUS
        max_ball = ball.position.y + ball.RADIUS

        for vertex in self.vertices():
            projection = vertex.dot(Vector(0, 1))
            min_brick = min(min_brick, projection)
            max_brick = max(max_brick, projection)

        if not (max_brick >= min_ball and max_ball >= min_brick):
            return False

        y = min(max_ball - min_brick, max_brick - min_ball)
        impact_vector += Vector(0, y)

        # If collision is confirmed, compute push vector.
        if impact_vector.x > impact_vector.y:
            ball.motion_vector *= Vector(1, -1)
        else:
            ball.motion_vector *= Vector(-1, 1)

        return True

    def compute_push_vector_horizontal(self, ball, axis):
        """Compute push vector if the ball collide with the brick on axis.

        :param ball: Instance of :class:`Ball`.

        :param axis: Instance of :class:`~arcade_nuke.utility.Vector`
            representing a unit vector of the horizontal or vertical axis.

        :return: Instance of :class:`~arcade_nuke.utility.Vector` or None.

        """

    def compute_push_vector_vertical(self, ball, axis):
        """Compute push vector if the ball collide with the brick on axis.

        :param ball: Instance of :class:`Ball`.

        :param axis: Instance of :class:`~arcade_nuke.utility.Vector`
            representing a unit vector of the horizontal or vertical axis.

        :return: Instance of :class:`~arcade_nuke.utility.Vector` or None.

        """

    def destroy(self):
        """Delete node."""
        node = self._get_node()
        nuke.delete(node)
        self._destroyed = True

    def _get_node(self):
        """Retrieve the the node representing the brick.

        Create the brick if necessary.

        """
        if self._destroyed:
            raise RuntimeError("Brick already destroyed...")

        node = nuke.toNode(self._name)

        if not node:
            node = getattr(nuke.nodes, self._node_class)(
                name=self._name,
                xpos=self._position.x,
                ypos=self._position.y,
                hide_input=True
            )
            node["autolabel"].setValue(self._label)

        return node
