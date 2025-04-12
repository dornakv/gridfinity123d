import build123d as bd
import constants
from basePlateMeasurements import BasePlateMeasurements

class BasePlateShimMeasurements():
    x_unit_dim: float = constants.X_UNIT_DIM
    y_unit_dim: float = constants.Y_UNIT_DIM
    radius: float = 4 * bd.MM  # for now, we support only same radius for the outside of shim as for the hole
    height: float= 4.65 * bd.MM

    tolerance: float = constants.TOLERANCE

    @classmethod
    def from_basePlateMeasurements(cls, basePlateMeasurements: BasePlateMeasurements):
        obj = cls()
        obj.x_unit_dim = basePlateMeasurements.x_unit_dim
        obj.y_unit_dim = basePlateMeasurements.y_unit_dim
        obj.radius = basePlateMeasurements.radius
        obj.height = basePlateMeasurements.height
        return obj