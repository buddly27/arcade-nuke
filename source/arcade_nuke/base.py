# :coding: utf-8

import abc

import nuke
from PySide2 import QtCore


class GameOver(Exception):
    """Exception to raise when the game is over."""

    def __init__(self, success=False):
        """Initialize Exception."""
        self.success = success


class GameSignal(QtCore.QObject):
    """Collection of signals emitted by the game."""

    stopped = QtCore.Signal()


class BaseGame(object):
    """Base class for all games.
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        """Initialize the game."""
        self._timer = QtCore.QTimer()
        self._timer.setInterval(0)
        self._timer.timeout.connect(self._process)

        # Collection of signals.
        self._signal = GameSignal()

        # Record states.
        self._initialized = False
        self._running = False

    @property
    def signal(self):
        """Return Collection of signals emitted by the game"""
        return self._signal

    def initialized(self):
        """Indicate whether the game is initialized."""
        return self._initialized

    def running(self):
        """Indicate whether the game is running."""
        return self._running

    def start(self):
        """Start the game."""
        if not self._initialized:
            return

        self._timer.start()
        self._running = True

    def stop(self):
        """Stop the game."""
        if not self._initialized:
            return

        self._timer.stop()
        self._running = False

    @abc.abstractmethod
    def initialize(self):
        """Initialize the game."""
        self._initialized = True

    @abc.abstractmethod
    def _process(self):
        """Method called for each move of the game."""


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

    _x = x
    for word in words:
        for letter in word:
            for index_x, index_y in letter:
                nuke.nodes.Dot(
                    xpos=_x + 11 * index_x,
                    ypos=y + 11 * index_y,
                    hide_input=True
                )
            _x += 11 * 6
        _x += 11 * 2


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

    _x = x
    for word in words:
        for letter in word:
            for index_x, index_y in letter:
                nuke.nodes.Dot(
                    xpos=_x + 11 * index_x,
                    ypos=y + 11 * index_y,
                    hide_input=True
                )
            _x += 11 * 6
        _x += 11 * 2
