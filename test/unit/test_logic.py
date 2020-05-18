# :coding: utf-8


def test_collision_threshold(mocker):
    """Nodes do not collide if distance between them is superior to threshold.
    """
    import arcade_nuke.logic
    from arcade_nuke.logic import Vector

    node1 = mocker.Mock(
        middle_position=Vector(0, 0),
        normals=[Vector(1, 0)],
        projection=lambda _: (-50, 50)
    )
    node2 = mocker.Mock(
        middle_position=Vector(51, 0),
        normals=[Vector(1, 0)],
        projection=lambda _: (0, 80)
    )

    node1.middle_position = Vector(0, 0)
    node2.middle_position = Vector(51, 0)
    assert arcade_nuke.logic.collision(node1, node2) is None

    node1.middle_position = Vector(0, 0)
    node2.middle_position = Vector(50, 0)
    assert arcade_nuke.logic.collision(node1, node2) is not None

    node1.middle_position = Vector(0, 0)
    node2.middle_position = Vector(5, 0)
    assert arcade_nuke.logic.collision(node1, node2, threshold=4) is None
