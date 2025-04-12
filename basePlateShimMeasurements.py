import build123d as bd
import constants

class BasePlateShimMeasurements():
    x_unit_dim: float = constants.X_UNIT_DIM
    y_unit_dim: float = constants.Y_UNIT_DIM
    radius: float = 4 * bd.MM  # for now, we support only same radius for the outside of shim as for the hole
    height: float= 4.65 * bd.MM

    tolerance: float = constants.TOLERANCE