import build123d as bd
import constants
from retentionSocketMeasurements import RetentionSocketMeasurements

class BinMeasurements():
    x_unit_dim: float = constants.X_UNIT_DIM
    y_unit_dim: float = constants.Y_UNIT_DIM
    height_unit_dim: float = constants.HEIGHT_UNIT_DIM
    radius: float = 4 * bd.MM
    floor_fillet_radius: float = 2 * bd.MM

    floor_thickness: float = 2.25 * bd.MM
    wall_thickness: float = 1.2 * bd.MM

    bin_gap: float = 0.5 * bd.MM

    retention_socket_top_chamfer_height: float = 2.15 * bd.MM
    retention_socket_top_chamfer_width: float = 2.15 * bd.MM
    retention_socket_middle_chamfer_height: float = 1.8 * bd.MM
    retention_socket_middle_chamfer_width: float = 0 * bd.MM
    retention_socket_bottom_chamfer_height: float = 0.8 * bd.MM
    retention_socket_bottom_chamfer_width: float = 0.8 * bd.MM

    @property
    def retention_socket_measurements(self):
        return RetentionSocketMeasurements(
            x_dim = self.x_unit_dim - self.bin_gap,
            y_dim = self.y_unit_dim - self.bin_gap,
            radius = self.radius - (self.bin_gap / 2),
            top_chamfer_height = self.retention_socket_top_chamfer_height,
            top_chamfer_width = self.retention_socket_top_chamfer_width,
            middle_chamfer_height = self.retention_socket_middle_chamfer_height,
            middle_chamfer_width = self.retention_socket_middle_chamfer_width,
            bottom_chamfer_height = self.retention_socket_bottom_chamfer_height,
            bottom_chamfer_width = self.retention_socket_bottom_chamfer_width,
        )