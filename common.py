import build123d as bd
import constants
from retentionSocketMeasurements import RetentionSocketMeasurements

def GetRoundedRect(x_dim: float, y_dim: float, radius: float) -> bd.BaseSketchObject:
    if x_dim <= constants.RESOLUTION: raise ValueError(x_dim)
    if y_dim <= constants.RESOLUTION: raise ValueError(y_dim)
    if radius < 0: raise ValueError(radius)

    if radius > constants.RESOLUTION:
        return bd.RectangleRounded(x_dim, y_dim, radius)
    return bd.Rectangle(x_dim, y_dim)

# TODO create separate class as bd.BasePartObject
def GetRetentionSocket(retention_socket_measurements: RetentionSocketMeasurements):
    floor = GetRoundedRect(
        retention_socket_measurements.floor_x_dim,
        retention_socket_measurements.floor_y_dim,
        retention_socket_measurements.floor_radius
    )

    middle_low = GetRoundedRect(
        retention_socket_measurements.middle_low_x_dim,
        retention_socket_measurements.middle_low_y_dim,
        retention_socket_measurements.middle_low_radius
    )

    middle_high = GetRoundedRect(
        retention_socket_measurements.middle_high_x_dim,
        retention_socket_measurements.middle_high_y_dim,
        retention_socket_measurements.middle_high_radius
    )

    top = GetRoundedRect(
        retention_socket_measurements.top_x_dim,
        retention_socket_measurements.top_y_dim,
        retention_socket_measurements.top_radius
    )

    plane: bd.Plane = bd.Plane.XY
    layers = [plane * floor]
    if retention_socket_measurements.bottom_chamfer_height > constants.RESOLUTION:
        plane = plane.offset(retention_socket_measurements.bottom_chamfer_height)
        layers.append(plane * middle_low)
    if retention_socket_measurements.middle_chamfer_height > constants.RESOLUTION:
        plane = plane.offset(retention_socket_measurements.middle_chamfer_height)
        layers.append(plane * middle_high)
    if retention_socket_measurements.top_chamfer_height > constants.RESOLUTION:
        plane = plane.offset(retention_socket_measurements.top_chamfer_height)
        layers.append(plane * top)
    
    if len(layers) <= 1:
        raise ValueError(f"None of the layers high enough ({constants.RESOLUTION=}): {retention_socket_measurements.bottom_chamfer_height=}, {retention_socket_measurements.middle_chamfer_height=}, {retention_socket_measurements.top_chamfer_height=}")
    
    return bd.loft(
        layers,
        ruled=True
    )