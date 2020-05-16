# :coding: utf-8

import arcade_nuke.node


def draw_game_over(x, y):
    """Draw 'Game Over.' using dots.

    :param x: Position of the left corner of the pattern.

    :param y: Position of the top corner of the pattern.

    """
    words = [
        [
            [
                (1, 0), (2, 0), (3, 0), (4, 0), (0, 1), (0, 2), (3, 2), (4, 2),
                (0, 3), (4, 3), (1, 4), (2, 4), (3, 4), (4, 4)
            ],
            [
                (2, 0), (1, 1), (3, 1), (0, 2), (4, 2), (0, 3), (1, 3), (2, 3),
                (3, 3), (4, 3), (0, 4), (4, 4)
            ],
            [
                (0, 0), (4, 0), (0, 1), (1, 1), (3, 1), (4, 1), (0, 2), (2, 2),
                (4, 2), (0, 3), (4, 3), (0, 4), (4, 4)
            ],
            [
                (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (0, 1), (0, 2), (1, 2),
                (2, 2), (0, 3), (0, 4), (1, 4), (2, 4), (3, 4), (4, 4)
            ]
        ],
        [
            [
                (1, 0), (2, 0), (3, 0), (0, 1), (4, 1), (0, 2), (4, 2), (0, 3),
                (4, 3), (1, 4), (2, 4), (3, 4)
            ],
            [
                (0, 0), (4, 0), (0, 1), (4, 1), (0, 2), (4, 2), (1, 3), (3, 3),
                (2, 4)
            ],
            [
                (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (0, 1), (0, 2), (1, 2),
                (2, 2), (0, 3), (0, 4), (1, 4), (2, 4), (3, 4), (4, 4)
            ],
            [
                (0, 0), (1, 0), (2, 0), (3, 0), (0, 1), (4, 1), (0, 2), (1, 2),
                (2, 2), (3, 2), (0, 3), (4, 3), (0, 4), (4, 4)
            ]
        ],
        [
            [
                (0, 4)
            ]
        ]
    ]

    points = []

    _x = x
    for word in words:
        for letter in word:
            for index_x, index_y in letter:
                point = arcade_nuke.node.DotNode(
                    x=_x + arcade_nuke.node.DotNode.width() * index_x,
                    y=y + arcade_nuke.node.DotNode.height() * index_y,
                )
                point.create_node()
                points.append(point)
            _x += 11 * 6
        _x += 11 * 2

    return points


def draw_win(x, y):
    """Draw 'You win!' using dots.

    :param x: Position of the left corner of the pattern.

    :param y: Position of the top corner of the pattern.

    """
    words = [
        [
            [
                (0, 0), (4, 0), (1, 1), (3, 1), (2, 2), (2, 3), (2, 4)
            ],
            [
                (1, 0), (2, 0), (3, 0), (0, 1), (4, 1), (0, 2), (4, 2), (0, 3),
                (4, 3), (1, 4), (2, 4), (3, 4)
            ],
            [
                (0, 0), (4, 0), (0, 1), (4, 1), (0, 2), (4, 2), (0, 3), (4, 3),
                (1, 4), (2, 4), (3, 4)
            ]
        ],
        [
            [
                (0, 0), (4, 0), (0, 1), (4, 1), (0, 2), (2, 2), (4, 2), (0, 3),
                (1, 3), (3, 3), (4, 3), (0, 4), (4, 4)
            ],
            [
                (1, 0), (2, 0), (3, 0), (0, 1), (4, 1), (0, 2), (4, 2), (0, 3),
                (4, 3), (1, 4), (2, 4), (3, 4)
            ],
            [
                (0, 0), (4, 0), (0, 1), (1, 1), (4, 1), (0, 2), (2, 2), (4, 2),
                (0, 3), (3, 3), (4, 3), (0, 4), (4, 4)
            ]
        ],
        [
            [
                (0, 0), (0, 1), (0, 2), (0, 4)
            ]
        ]
    ]

    points = []

    _x = x
    for word in words:
        for letter in word:
            for index_x, index_y in letter:
                point = arcade_nuke.node.DotNode(
                    x=_x + arcade_nuke.node.DotNode.width() * index_x,
                    y=y + arcade_nuke.node.DotNode.height() * index_y,
                )
                point.create_node()
                points.append(point)
            _x += 11 * 6
        _x += 11 * 2

    return points
