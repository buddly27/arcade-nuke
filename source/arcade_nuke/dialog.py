# :coding: utf-8

from PySide2 import QtGui, QtWidgets, QtCore


class Player(QtWidgets.QDialog):

    def __init__(self, games, on_initiate, on_start, on_stop, parent=None):
        super(Player, self).__init__(parent)

        # Record callbacks.
        self._on_initiate = on_initiate
        self._on_start = on_start
        self._on_stop = on_stop

        # Initiate UI and timer.
        self._setup_ui()
        self._game_cbbox.addItems(games)
        self._initiate_btn.clicked.connect(self.initiate_game)
        self._play_btn.clicked.connect(self.start_playing)
        self._stop_btn.clicked.connect(self.stop_playing)

        # Move the window in the top left corner of the screen.
        self.move(0, 0)

        # Ensure that this dialog is always on top of all windows.
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)

        # Create timer and elapsed timer to display duration.
        self._duration_timer = QtCore.QTimer()
        self._duration_timer.setInterval(1000)
        self._duration_timer.timeout.connect(self._update_time)

        self._elapsed_timer = QtCore.QElapsedTimer()
        self._elapsed_timer.start()

        # Record state.
        self._running = False

        # Initiate state.
        self.reset()

    def reset(self):
        self._duration_timer.stop()
        self._duration_lbl.setText("{0:02}:{0:02}:{0:02}".format(0))
        self._message_lbl.setText("Press `A` to start and pause the game")

        self._initiate_btn.setEnabled(True)
        self._play_btn.setEnabled(True)
        self._stop_btn.setEnabled(False)
        self._game_cbbox.setEnabled(True)

        self._running = False

    def initiate_game(self):
        self._on_initiate(self._game_cbbox.currentText())

    def start_playing(self):
        self._duration_timer.start()
        self._elapsed_timer.restart()

        self._initiate_btn.setEnabled(False)
        self._play_btn.setEnabled(False)
        self._stop_btn.setEnabled(True)
        self._game_cbbox.setEnabled(False)

        self._on_start(self._game_cbbox.currentText())

        self._running = True

    def stop_playing(self):
        self.reset()

        self._on_stop(self._game_cbbox.currentText())

    def _update_time(self):
        seconds = self._elapsed_timer.elapsed() / 1000
        minutes = (seconds / 60) % 60
        hours = (seconds / 3600)

        self._duration_lbl.setText(
            "{:02}:{:02}:{:02}".format(hours, minutes, seconds)
        )

    def mouseMoveEvent(self, event):
        print(event)
        return super(Player, self).mouseMoveEvent(event)

    def event(self, event):
        if (
            isinstance(event, QtGui.QKeyEvent)
            and event.key() == QtCore.Qt.Key_Escape
        ):
            self.stop_playing()

            # Bi-pass QWidget logic to prevent window to close.
            return False

        elif (
            isinstance(event, QtGui.QKeyEvent)
            and event.key() == QtCore.Qt.Key_A
        ):
            if not self._running:
                self.start_playing()
            else:
                self.stop_playing()

        return super(Player, self).event(event)

    def _setup_ui(self):
        self.setWindowTitle("Arcade Games")

        layout = QtWidgets.QHBoxLayout(self)
        self._game_cbbox = QtWidgets.QComboBox(self)
        self._game_cbbox.setMinimumHeight(26)
        self._game_cbbox.setMinimumWidth(150)
        layout.addWidget(self._game_cbbox)

        self._initiate_btn = QtWidgets.QPushButton(self)
        self._initiate_btn.setStyleSheet("background-color: black")
        self._initiate_btn.setText("Initiate")
        layout.addWidget(self._initiate_btn)

        self._play_btn = QtWidgets.QPushButton(self)
        self._play_btn.setStyleSheet("background-color: grey")
        icon = self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay)
        self._play_btn.setIcon(icon)
        layout.addWidget(self._play_btn)

        self._stop_btn = QtWidgets.QPushButton(self)
        self._stop_btn.setStyleSheet("background-color: grey")
        icon = self.style().standardIcon(QtWidgets.QStyle.SP_MediaStop)
        self._stop_btn.setIcon(icon)
        layout.addWidget(self._stop_btn)

        self._message_lbl = QtWidgets.QLabel(self)
        self._message_lbl.setMinimumWidth(400)
        layout.addWidget(self._message_lbl)

        self._duration_lbl = QtWidgets.QLabel(self)
        self._duration_lbl.setMinimumWidth(60)
        layout.addWidget(self._duration_lbl)
