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
    """Test collision between several nodes."""
    import arcade_nuke.logic
    import arcade_nuke.node

    node1 = arcade_nuke.node.DotNode(0, 0)
    node2 = arcade_nuke.node.ViewerNode(12, 0)

    print(node1.middle_position)
    print(node2.middle_position)
    assert arcade_nuke.logic.collision(node1, node2) is None
