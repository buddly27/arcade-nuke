# :coding: utf-8

import nuke

import arcade_nuke

menu = nuke.menu("Nuke")
menu.addCommand("Arcade/Start Playing...", arcade_nuke.open_dialog)

