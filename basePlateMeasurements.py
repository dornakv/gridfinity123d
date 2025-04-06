import build123d as bd
import constants

class BasePlateMeasurements():
    x_unit_dim: float = constants.X_UNIT_DIM
    y_unit_dim: float = constants.Y_UNIT_DIM
    radius: float = 4 * bd.MM

    height: float= 4.65 * bd.MM
    top_chamfer_height: float = 2.15 * bd.MM
    top_chamfer_width: float = 2.15 * bd.MM
    bottom_chamfer_height: float = 0.7 * bd.MM
    bottom_chamfer_width: float = 0.7 * bd.MM
