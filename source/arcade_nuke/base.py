# :coding: utf-8

import abc

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
