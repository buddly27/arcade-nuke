# :coding: utf-8

from PySide2 import QtWidgets, QtCore

import arcade_nuke.dialog
import arcade_nuke.breakout


def open_dialog():
    """Open dialog to start playing."""
    parent = QtWidgets.QApplication.activeWindow()

    mapping = {
        "Breakout 1": arcade_nuke.breakout.BreakoutGame(
            generator=arcade_nuke.breakout.brick_generator1
        ),
        "Breakout 2": arcade_nuke.breakout.BreakoutGame(
            generator=arcade_nuke.breakout.brick_generator2
        )
    }

    _dialog = arcade_nuke.dialog.Player(games=mapping, parent=parent)
    _dialog.show()
