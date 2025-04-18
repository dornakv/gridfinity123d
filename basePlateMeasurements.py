import build123d as bd
import constants

class BasePlateMeasurements():
    x_unit_dim: float = constants.X_UNIT_DIM
    y_unit_dim: float = constants.Y_UNIT_DIM
    radius: float = 4 * bd.MM

    height: float= 4.65 * bd.MM
    top_chamfer_height: float = 2.15 * bd.MM
    top_chamfer_width: float = 2.15 * bd.MM
    middle_chamfer_height: float = 1.8 * bd.MM
    middle_chamfer_width: float = 0 * bd.MM
    bottom_chamfer_height: float = 0.7 * bd.MM
    bottom_chamfer_width: float = 0.7 * bd.MM
    top_ledge_width: float = 0 * bd.MM

    tolerance: float = constants.TOLERANCE

    @property
    def height(self): return self.bottom_chamfer_height + self.middle_chamfer_height + self.top_chamfer_height

    @classmethod
    def with_top_ledge(cls, top_ledge_width):
        obj = cls()
        if top_ledge_width <= 0: return obj

        obj.top_ledge_width = top_ledge_width
        obj.middle_chamfer_height -= top_ledge_width

        top_chamfer_ratio = obj.top_chamfer_width / obj.top_chamfer_height
        obj.top_chamfer_height -= top_ledge_width
        obj.top_chamfer_width = top_chamfer_ratio * obj.top_chamfer_height
        return obj