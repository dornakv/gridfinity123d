import build123d as bd
import constants
from retentionSocketMeasurements import RetentionSocketMeasurements


class BasePlateMeasurements:
    x_unit_dim: float = constants.X_UNIT_DIM
    y_unit_dim: float = constants.Y_UNIT_DIM
    radius: float = 4 * bd.MM

    max_height: float = 4.65 * bd.MM
    top_chamfer_height: float = 2.15 * bd.MM
    top_chamfer_width: float = 2.15 * bd.MM
    middle_chamfer_height: float = 1.8 * bd.MM
    middle_chamfer_width: float = 0 * bd.MM
    bottom_chamfer_height: float = 0.7 * bd.MM
    bottom_chamfer_width: float = 0.7 * bd.MM
    top_ledge_width: float = 0 * bd.MM

    tolerance: float = constants.TOLERANCE

    @property  # smaller than retention_scoket leads to a ledge
    def height(self):
        return min(self.retention_socket_measurements.height, self.max_height)

    @property
    def retention_socket_measurements(self):
        return RetentionSocketMeasurements(
            x_dim=self.x_unit_dim,
            y_dim=self.y_unit_dim,
            radius=self.radius,
            top_chamfer_height=self.top_chamfer_height,
            top_chamfer_width=self.top_chamfer_width,
            middle_chamfer_height=self.middle_chamfer_height,
            middle_chamfer_width=self.middle_chamfer_width,
            bottom_chamfer_height=self.bottom_chamfer_height,
            bottom_chamfer_width=self.bottom_chamfer_width,
        )
