#!/usr/bin/env python3

import locale
import gettext
from pathlib import Path

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from controller import Controller
from model import Model
from view import view

if __name__ == '__main__':
    # usamos el default locale en el resto de la ejecución
    # el default locale es el que tenga configurado la usuaria
    #locale.setlocale(locale.LC_ALL, '')

    # Establecemos la BBDD de traducciones
    LOCALE_DIR = Path(__file__).parent / "locale"
    locale.bindtextdomain('Covid', LOCALE_DIR)
    gettext.bindtextdomain('Covid', LOCALE_DIR)
    gettext.textdomain('Covid')

    controller = Controller()
    controller.set_model(Model())
    controller.set_view(view())
    controller.main()