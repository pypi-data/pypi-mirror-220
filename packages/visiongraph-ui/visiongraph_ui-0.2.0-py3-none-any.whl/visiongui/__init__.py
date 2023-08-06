from duit.ui.open3d.Open3dPropertyRegistry import init_open3d_registry
from open3d.visualization import gui


def init_app_context():
    init_open3d_registry()

    app = gui.Application.instance
    app.initialize()
