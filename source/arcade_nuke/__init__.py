# :coding: utf-8

from PySide2 import QtWidgets

import arcade_nuke.dialog
import arcade_nuke.breakout


def open_dialog():
    """Open dialog to start playing."""
    parent = QtWidgets.QApplication.activeWindow()

    controller = GameController()

    _dialog = arcade_nuke.dialog.Player(
        games=controller.games(),
        on_initiate=controller.initialize,
        on_start=controller.start,
        on_stop=controller.stop,
        parent=parent
    )
    _dialog.show()


class GameController(object):
    """Game Controller"""

    def __init__(self):
        """Initiate GameController."""
        self._mapping = {
            "Breakout 1": arcade_nuke.breakout.Game()
        }

    def games(self):
        """Return names of games."""
        return sorted(self._mapping.keys())

    def initialize(self, name):
        """Initiate a game."""
        self._mapping[name].initialize()

    def start(self, name):
        """Start a game."""
        self._mapping[name].start()

    def stop(self, name):
        """Stop a game."""
        self._mapping[name].stop()
