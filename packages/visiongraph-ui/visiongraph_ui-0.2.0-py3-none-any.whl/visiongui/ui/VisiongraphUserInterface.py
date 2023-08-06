import logging
import traceback
from pathlib import Path
from typing import Generic, TypeVar

from open3d.visualization import gui

from visiongui.app.VisiongraphApp import VisiongraphApp
from visiongui.ui.BaseUserInterface import T, BaseUserInterface

TA = TypeVar("TA", bound=VisiongraphApp)


class VisiongraphUserInterface(Generic[TA, T], BaseUserInterface[T]):
    def __init__(self, app: TA, width: int = 800, height: int = 600,
                 attach_interrupt_handler: bool = False, handle_graph_state: bool = True):
        super().__init__(app.config, app.graph.name, width, height, attach_interrupt_handler)

        self.app = app
        self.graph = app.graph
        self.graph.on_exception = self._on_graph_exception

        self.handle_graph_state = handle_graph_state
        if self.handle_graph_state:
            self.graph.open()

        self.menu.on_open_settings += self._on_open_settings
        self.menu.on_save_settings += self._on_save_settings

    def _on_graph_exception(self, pipeline, ex):
        # display error message in console
        logging.warning("".join(traceback.TracebackException.from_exception(ex).format()))

        # close application on graph exception
        gui.Application.instance.post_to_main_thread(self.window, gui.Application.instance.quit)

    def _on_close(self):
        if self.handle_graph_state:
            self.graph.close()
        gui.Application.instance.quit()

    def _on_open_settings(self, path: Path):
        self.app.load_config(path)

    def _on_save_settings(self, path: Path):
        self.app.save_config(path)
