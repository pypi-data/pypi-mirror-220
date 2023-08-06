from dataclasses import dataclass
from typing import Set, Callable, List, Union

from open3d.cpu.pybind.visualization import gui
from visiongraph.util import OSUtils


@dataclass
class KeyHandler:
    keys: Set[int]
    callback: Callable[[], None]


class KeyStrokeDetector:

    def __init__(self):
        self._pressed_keys: Set[int] = set()

        self.key_handlers: List[KeyHandler] = []

    def register(self, callback: Callable[[], None], *keys: Union[int, gui.KeyName]):
        int_keys = [int(k) for k in keys]
        self.key_handlers.append(KeyHandler(set(int_keys), callback))

    def on_key_pressed(self, event: gui.KeyEvent) -> bool:
        key_handled = False

        if event.type == gui.KeyEvent.DOWN:
            self._pressed_keys.add(event.key)

            for handler in self.key_handlers:
                if handler.keys.issubset(self._pressed_keys):
                    key_handled = True
                    handler.callback()

        elif event.type == gui.KeyEvent.UP:
            if event.key in self._pressed_keys:
                self._pressed_keys.remove(event.key)

        return key_handled

    @property
    def meta_key(self) -> gui.KeyName:
        meta_key = gui.KeyName.LEFT_CONTROL
        if OSUtils.isMacOSX():
            meta_key = gui.KeyName.META

        return meta_key
