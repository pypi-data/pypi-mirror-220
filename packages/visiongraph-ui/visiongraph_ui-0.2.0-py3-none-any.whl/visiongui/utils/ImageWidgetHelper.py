import vector
import visiongraph as vg
from open3d.visualization import gui


def transform_to_image_coordinates(image_widget: gui.ImageWidget,
                                   image_size: vg.Size2D, position: vector.Vector2D) -> vector.Vector2D:
    frame: gui.Rect = image_widget.frame

    # does only work if UIImage is set to ASPECT
    # https://github.com/isl-org/Open3D/blob/master/cpp/open3d/visualization/gui/UIImage.cpp#L255-L270
    aspect = image_size.width / image_size.height
    w_at_height = float(frame.height) * aspect
    h_at_width = float(frame.width) / aspect
    if w_at_height <= frame.width:
        params_width = w_at_height
        params_height = float(frame.height)
    else:
        params_width = float(frame.width)
        params_height = h_at_width

    ix = max(0.0, (float(frame.width) - params_width) / 2.0)
    iy = max(0.0, (float(frame.height) - params_height) / 2.0)

    px = vg.map_value(position.x, ix, ix + params_width, 0, image_size.width)
    py = vg.map_value(position.y, iy, iy + params_height, 0, image_size.height)

    return vector.obj(x=px, y=py)
