from grid import Grid
import build123d as bd
import math
import numpy as np

class BasePlate:
    def __init__(self, grid: Grid):
        self._grid = grid

    algo = "profile_single"
    algo = "extrude"

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

    def _get_hole(self):
            inner_x_dim = self.x_dim - 2 * (self.top_chamfer_width + self.bottom_chamfer_width)
            inner_y_dim = self.y_dim - 2 * (self.top_chamfer_width + self.bottom_chamfer_width)

            floor = bd.make_face(bd.FilletPolyline(
                bd.Vector(0 - inner_x_dim / 2, 0 + inner_y_dim / 2),
                bd.Vector(0 - inner_x_dim / 2, 0 - inner_y_dim / 2),
                bd.Vector(0 + inner_x_dim / 2, 0 - inner_y_dim / 2),
                bd.Vector(0 + inner_x_dim / 2, 0 + inner_y_dim / 2),
                close=True,
                radius=self.radius
            ))

            inner_x_dim = self.x_dim - 2 * (self.top_chamfer_width)
            inner_y_dim = self.y_dim - 2 * (self.top_chamfer_width)

            middle = bd.make_face(bd.FilletPolyline(
                bd.Vector(0 - inner_x_dim / 2, 0 + inner_y_dim / 2),
                bd.Vector(0 - inner_x_dim / 2, 0 - inner_y_dim / 2),
                bd.Vector(0 + inner_x_dim / 2, 0 - inner_y_dim / 2),
                bd.Vector(0 + inner_x_dim / 2, 0 + inner_y_dim / 2),
                close=True,
                radius=self.radius
            ))

            inner_x_dim = self.x_dim
            inner_y_dim = self.y_dim

            top = bd.make_face(bd.FilletPolyline(
                bd.Vector(0 - inner_x_dim / 2, 0 + inner_y_dim / 2),
                bd.Vector(0 - inner_x_dim / 2, 0 - inner_y_dim / 2),
                bd.Vector(0 + inner_x_dim / 2, 0 - inner_y_dim / 2),
                bd.Vector(0 + inner_x_dim / 2, 0 + inner_y_dim / 2),
                close=True,
                radius=self.radius
            ))

            return  bd.loft((floor,
                                  bd.Plane.XY.offset(self.bottom_chamfer_height) * middle)) +\
                    bd.loft((bd.Plane.XY.offset(self.bottom_chamfer_height) * middle,
                                  bd.Plane.XY.offset(self.height-self.top_chamfer_height) * middle)) +\
                    bd.loft((bd.Plane.XY.offset(self.bottom_chamfer_height) * middle,
                                  bd.Plane.XY.offset(self.height-self.top_chamfer_height) * middle)) +\
                    bd.loft((bd.Plane.XY.offset(self.height-self.top_chamfer_height) * middle,
                                  bd.Plane.XY.offset(self.height) * top))
        
    def get_part(self):
        grid_size = [
            self._grid.bool_grid.shape[0] * self.x_dim,
            self._grid.bool_grid.shape[1] * self.y_dim
        ]
        outer_polyline = bd.FilletPolyline(
            bd.Vector(0 - self.x_dim / 2, grid_size[1] - self.y_dim / 2),
            bd.Vector(0 - self.x_dim / 2, 0 - self.y_dim / 2),
            bd.Vector(grid_size[0] - self.x_dim / 2, 0 - self.y_dim / 2),
            bd.Vector(grid_size[0] - self.x_dim / 2, grid_size[1] - self.y_dim / 2),
            close=True,
            radius=self.radius
        )

        hole = self._get_hole()

        holes = []
        for index, val in np.ndenumerate(self._grid.bool_grid):
            if not val:
                continue

            x_center = index[0] * self.x_dim
            y_center = index[1] * self.y_dim

            holes.append(bd.Pos(x_center, y_center) * hole)

        block = bd.extrude(bd.make_face(outer_polyline), self.height)

        return block - holes
