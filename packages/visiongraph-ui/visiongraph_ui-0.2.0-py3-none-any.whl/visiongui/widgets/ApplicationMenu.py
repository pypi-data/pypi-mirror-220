from pathlib import Path
from typing import Optional, Any

from duit.event.Event import Event
from open3d.visualization import gui
from visiongraph.util import OSUtils


class ApplicationMenu:
    MENU_OPEN = 1
    MENU_SAVE = 2
    MENU_SAVE_AS = 3
    MENU_QUIT = 4
    MENU_ABOUT = 5

    def __init__(self, title: str):
        self.title = title
        self.settings_file: Optional[Path] = None

        self.menu: Optional[gui.Menu] = None
        self.window: Optional[gui.Window] = None

        self.on_open_settings: Event[Path] = Event()
        self.on_save_settings: Event[Path] = Event()
        self.on_about: Event[ApplicationMenu] = Event()

    def __enter__(self):
        # on windows & linux attach before ui creation
        if not OSUtils.isMacOSX():
            gui.Application.instance.menubar = self.create_menu_bar()

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any):
        # on macOS attach after ui creation
        if OSUtils.isMacOSX():
            gui.Application.instance.menubar = self.create_menu_bar()

    def create_menu_bar(self) -> Optional[gui.Menu]:
        if gui.Application.instance.menubar is not None:
            return None

        app_menu = gui.Menu()
        app_menu.add_item("About", self.MENU_ABOUT)
        app_menu.add_separator()
        app_menu.add_item("Quit", self.MENU_QUIT)

        settings_menu = gui.Menu()
        settings_menu.add_item("Open", self.MENU_OPEN)
        settings_menu.add_separator()
        settings_menu.add_item("Save", self.MENU_SAVE)
        settings_menu.add_item("Save As...", self.MENU_SAVE_AS)

        menu = gui.Menu()
        menu.add_menu(self.title, app_menu)
        menu.add_menu("Settings", settings_menu)

        self.menu = menu
        return menu

    def attach_menu_handlers(self, window: gui.Window):
        self.window = window

        window.set_on_menu_item_activated(self.MENU_QUIT, window.close)
        window.set_on_menu_item_activated(self.MENU_ABOUT, self._on_menu_about)

        window.set_on_menu_item_activated(self.MENU_OPEN, self._on_menu_open)
        window.set_on_menu_item_activated(self.MENU_SAVE, self._on_menu_save)
        window.set_on_menu_item_activated(self.MENU_SAVE_AS, self._on_menu_save_as)

    def _on_menu_open(self):
        dialog = gui.FileDialog(gui.FileDialog.OPEN, "Open Settings", self.window.theme)
        dialog.add_filter(".json", "JSON")

        def on_cancel():
            self.window.close_dialog()

        def on_done(path: str):
            self.window.close_dialog()
            self.settings_file = Path(path)
            self.on_open_settings(self.settings_file)

        dialog.set_on_done(on_done)
        dialog.set_on_cancel(on_cancel)
        self.window.show_dialog(dialog)

    def _on_menu_save(self):
        if self.settings_file is None:
            self._on_menu_save_as()
            return

        self.on_save_settings(self.settings_file)

    def _on_menu_save_as(self):
        dialog = gui.FileDialog(gui.FileDialog.SAVE, "Save Settings", self.window.theme)
        dialog.add_filter(".json", "JSON")

        def on_cancel():
            self.window.close_dialog()

        def on_done(path: str):
            self.window.close_dialog()
            self.settings_file = Path(path)
            self.on_save_settings(self.settings_file)

        dialog.set_on_done(on_done)
        dialog.set_on_cancel(on_cancel)
        self.window.show_dialog(dialog)

    def _on_menu_about(self):
        self.on_about(self)
