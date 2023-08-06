from duit.ui.open3d.Open3dPropertyRegistry import init_open3d_registry
from open3d.visualization import gui


class UIContext:
    def __init__(self):
        self.open3d_app: gui.Application = gui.Application.instance

    def __enter__(self):
        self.init()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.run()

    def init(self):
        init_open3d_registry()
        self.open3d_app.initialize()

    def run(self):
        self.open3d_app.run()
