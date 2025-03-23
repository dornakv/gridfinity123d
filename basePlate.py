from grid import Grid
import build123d as bd
import math
import numpy as np

class BasePlate:
    def __init__(self, grid: Grid):
        self._grid = grid

    x_dim = 42 * bd.MM
    y_dim = 42 * bd.MM
    radius = 4 * bd.MM

    height = 4.65 * bd.MM
    top_chamfer_height = 2.15 * bd.MM
    top_chamfer_angle = math.pi / 2  # from horizontal
    bottom_chamfer_height = 0.7 * bd.MM
    bottom_chamfer_angle = math.pi / 2  # from horizontal

    top_chamfer_width = top_chamfer_height * math.atan(top_chamfer_angle)
    bottom_chamfer_width = bottom_chamfer_height * math.atan(bottom_chamfer_angle)

    def get_single(self, x_center: float, y_center: float):
        if self.radius <= (self.top_chamfer_width + self.bottom_chamfer_width):
            raise Exception(f"radius {self.radius} too small, it needs to be larger than {self.top_chamfer_width + self.bottom_chamfer_width}")

        path = bd.FilletPolyline(
            bd.Vector(x_center - self.x_dim / 2, y_center + self.y_dim / 2),
            bd.Vector(x_center - self.x_dim / 2, y_center - self.y_dim / 2),
            bd.Vector(x_center + self.x_dim / 2, y_center - self.y_dim / 2),
            bd.Vector(x_center + self.x_dim / 2, y_center + self.y_dim / 2),
            close=True,
            radius=self.radius
        )

        profile = bd.Polyline(
            bd.Vector(0, 0),
            bd.Vector(self.top_chamfer_width + self.bottom_chamfer_width,0),
            bd.Vector(self.top_chamfer_width, self.bottom_chamfer_height),
            bd.Vector(self.top_chamfer_width, self.height - self.top_chamfer_height),
            bd.Vector(0, self.height),
            close=True
        )

        profile = bd.Plane.XZ * profile
        profile = bd.Pos(x_center - self.x_dim / 2, y_center, 0) * profile

        return bd.sweep(profile, path)

    def get_part(self):
        res = bd.Sketch()
        for index, val in np.ndenumerate(self._grid.bool_grid):
            if val:
                res += self.get_single(index[0] * self.x_dim, index[1] * self.y_dim)
        return res