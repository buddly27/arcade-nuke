# :coding: utf-8

import pytest


@pytest.fixture(autouse=True)
def setup(mocker):
    """Mock BaseNode module to only use initial position."""
    import arcade_nuke.node

    mocker.patch.object(
        arcade_nuke.node.BaseNode, "node",
        lambda self: mocker.Mock(
            xpos=lambda: self._position.x,
            ypos=lambda: self._position.y,
        )
    )


def test_collision():
    """Test collision between a Dot and a Viewer nodes at various positions.
    """
    import arcade_nuke.logic
    import arcade_nuke.node

    # Dot node on the left of the Viewer node evolving on the Y axis.
    node1 = arcade_nuke.node.DotNode(0, -1)
    node2 = arcade_nuke.node.ViewerNode(14, 0)
    assert arcade_nuke.logic.collision(node1, node2) is None

    node1 = arcade_nuke.node.DotNode(0, 0)
    node2 = arcade_nuke.node.ViewerNode(14, 0)
    assert arcade_nuke.logic.collision(node1, node2) == node2.normals[1] * -1

    node1 = arcade_nuke.node.DotNode(0, 1)
    node2 = arcade_nuke.node.ViewerNode(14, 0)
    assert arcade_nuke.logic.collision(node1, node2) == node2.normals[1] * -1

    node1 = arcade_nuke.node.DotNode(0, 2)
    node2 = arcade_nuke.node.ViewerNode(14, 0)
    assert arcade_nuke.logic.collision(node1, node2) == node2.normals[1] * -1

    node1 = arcade_nuke.node.DotNode(0, 3)
    node2 = arcade_nuke.node.ViewerNode(14, 0)
    assert arcade_nuke.logic.collision(node1, node2) == node2.normals[2]

    node1 = arcade_nuke.node.DotNode(0, 4)
    node2 = arcade_nuke.node.ViewerNode(14, 0)
    assert arcade_nuke.logic.collision(node1, node2) == node2.normals[2]

    node1 = arcade_nuke.node.DotNode(0, 5)
    node2 = arcade_nuke.node.ViewerNode(14, 0)
    assert arcade_nuke.logic.collision(node1, node2) == node2.normals[2]

    node1 = arcade_nuke.node.DotNode(0, 6)
    node2 = arcade_nuke.node.ViewerNode(14, 0)
    assert arcade_nuke.logic.collision(node1, node2) is None

    # Dot node on the right of the Viewer node evolving on the Y axis.
    node1 = arcade_nuke.node.DotNode(110, -1)
    node2 = arcade_nuke.node.ViewerNode(14, 0)
    assert arcade_nuke.logic.collision(node1, node2) is None

    node1 = arcade_nuke.node.DotNode(110, 0)
    node2 = arcade_nuke.node.ViewerNode(14, 0)
    assert arcade_nuke.logic.collision(node1, node2) == node2.normals[2] * -1

    node1 = arcade_nuke.node.DotNode(110, 1)
    node2 = arcade_nuke.node.ViewerNode(14, 0)
    assert arcade_nuke.logic.collision(node1, node2) == node2.normals[2] * -1

    node1 = arcade_nuke.node.DotNode(110, 2)
    node2 = arcade_nuke.node.ViewerNode(14, 0)
    assert arcade_nuke.logic.collision(node1, node2) == node2.normals[2] * -1

    node1 = arcade_nuke.node.DotNode(110, 3)
    node2 = arcade_nuke.node.ViewerNode(14, 0)
    assert arcade_nuke.logic.collision(node1, node2) == node2.normals[1]

    node1 = arcade_nuke.node.DotNode(110, 4)
    node2 = arcade_nuke.node.ViewerNode(14, 0)
    assert arcade_nuke.logic.collision(node1, node2) == node2.normals[1]

    node1 = arcade_nuke.node.DotNode(110, 5)
    node2 = arcade_nuke.node.ViewerNode(14, 0)
    assert arcade_nuke.logic.collision(node1, node2) == node2.normals[1]

    node1 = arcade_nuke.node.DotNode(110, 6)
    node2 = arcade_nuke.node.ViewerNode(14, 0)
    assert arcade_nuke.logic.collision(node1, node2) is None
