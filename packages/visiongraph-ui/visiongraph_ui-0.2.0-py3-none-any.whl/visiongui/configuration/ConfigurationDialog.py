from typing import Any, Optional

from duit.event.Event import Event
from duit.ui.open3d.Open3dPropertyPanel import Open3dPropertyPanel
from open3d.visualization import gui


class ConfigurationDialog(gui.Dialog):
    def __init__(self, config: Any, window: gui.Window, title: str = "VisionGraph Configuration"):
        super().__init__(title)

        self.window = window

        self.title = title
        self.config = config

        self._create_ui()

    def _create_ui(self):
        window_rect: gui.Rect = self.window.content_rect

        self.frame = gui.Rect(0, 0, window_rect.width * 0.8, window_rect.height * 0.8)

        self.container = gui.Vert(4, gui.Margins(10, 10, 10, 10))

        title_label = gui.Label(self.title)
        self.container.add_child(title_label)

        self.panel = Open3dPropertyPanel(self.window)
        self.container.add_child(self.panel)
        self.panel.data_context = self.config

        self.add_child(self.container)

        self.submit_button = gui.Button("Submit")
        self.submit_button.set_on_clicked(self._on_submit_button_clicked)
        self.container.add_stretch()
        self.container.add_child(self.submit_button)

        self.on_submit = Event()

    def _on_submit_button_clicked(self):
        self.window.close_dialog()
        self.on_submit.invoke(self.config)
