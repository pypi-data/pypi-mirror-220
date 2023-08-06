import signal
from abc import ABC
from functools import partial
from typing import TypeVar, Any, Generic, Callable, Optional

import cv2
import numpy as np
from duit.ui.open3d.Open3dPropertyPanel import Open3dPropertyPanel
from open3d import geometry
from open3d.visualization import gui

from visiongui.utils.KeyStrokeDetector import KeyStrokeDetector
from visiongui.widgets.ApplicationMenu import ApplicationMenu

T = TypeVar("T", bound=Any)


class BaseUserInterface(Generic[T], ABC):

    def __init__(self, config: T, title: str, width: int = 800, height: int = 600,
                 attach_interrupt_handler: bool = False):
        self.config = config
        self.title = title

        # setup ui and menu
        self.menu = ApplicationMenu(title)
        with self.menu:
            self.window: gui.Window = gui.Application.instance.create_window(title, width, height)
        self.menu.attach_menu_handlers(self.window)
        self.menu.on_about = self._on_menu_about

        self.em = self.window.theme.font_size

        # setup ui hooks
        self.window.set_on_layout(self._on_layout)
        self.window.set_on_close(self._on_close)

        # setup hot keys
        self.key_detector = KeyStrokeDetector()
        self._setup_hotkeys(self.key_detector)

        # setup base widgets
        self.image_view = gui.ImageWidget(geometry.Image(self.placeholder_image))
        self.image_view.set_on_mouse(self._on_image_view_mouse_event)
        self.window.add_child(self.image_view)

        self.settings_panel = Open3dPropertyPanel(self.window)
        self.settings_panel.data_context = self.config
        self.settings_panel_width = 25 * self.em
        self.window.add_child(self.settings_panel)

        # attach signal handler
        if attach_interrupt_handler:
            signal.signal(signal.SIGINT, self._signal_handler)

    def _on_layout(self, layout_context: gui.LayoutContext):
        content_rect = self.window.content_rect

        self.image_view.frame = gui.Rect(content_rect.x, content_rect.y,
                                         content_rect.width - self.settings_panel_width,
                                         content_rect.height)

        self.settings_panel.frame = gui.Rect(self.image_view.frame.get_right(),
                                             content_rect.y, self.settings_panel_width,
                                             content_rect.height)

    def _on_close(self):
        gui.Application.instance.quit()

    def _signal_handler(self, signal_type: signal, frame: Any):
        self.window.close()

    def _setup_hotkeys(self, key_detector: KeyStrokeDetector):
        self.window.set_on_key(key_detector.on_key_pressed)

        meta_key = key_detector.meta_key
        key_detector.register(partial(self.invoke_on_gui, self.menu._on_menu_open), meta_key, gui.KeyName.O)
        key_detector.register(partial(self.invoke_on_gui, self.menu._on_menu_save), meta_key, gui.KeyName.S)
        key_detector.register(partial(self.invoke_on_gui, self.window.close), meta_key, gui.KeyName.Q)

    def _on_image_view_mouse_event(self, event: gui.MouseEvent) -> int:
        return 0

    def update_image_view(self, image: np.ndarray, image_widget: Optional[gui.ImageWidget] = None):
        view = image_widget if image_widget is not None else self.image_view
        o3d_image = geometry.Image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        def update():
            view.update_image(o3d_image)

        self.invoke_on_gui(update)

    @property
    def placeholder_image(self) -> np.ndarray:
        return np.zeros(shape=(1, 1, 3), dtype="uint8")

    def invoke_on_gui(self, callback: Callable[[], None]):
        gui.Application.instance.post_to_main_thread(self.window, callback)

    def _on_menu_about(self, sender: Any):
        self.window.show_message_box("About", self.about_text)

    @property
    def about_text(self):
        return f"Hello from {self.title}"
