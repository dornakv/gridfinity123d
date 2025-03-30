import build123d as bd
import math
import numpy as np

class BasePlate:
    def __init__(self, x_units: int, y_units: int):
        self.x_units: int = x_units
        self.y_units: int = y_units

    x_dim: float = 42 * bd.MM
    y_dim: float = 42 * bd.MM
    radius: float = 4 * bd.MM

    height: float= 4.65 * bd.MM
    top_chamfer_height: float = 2.15 * bd.MM
    top_chamfer_angle: float = math.pi / 2  # from horizontal
    bottom_chamfer_height: float = 0.7 * bd.MM
    bottom_chamfer_angle: float = math.pi / 2  # from horizontal

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

    def _get_outline(self):
        grid_size = [
            self.x_units * self.x_dim,
            self.y_units * self.y_dim
        ]

        return bd.FilletPolyline(
            bd.Vector(0 - self.x_dim / 2, grid_size[1] - self.y_dim / 2),
            bd.Vector(0 - self.x_dim / 2, 0 - self.y_dim / 2),
            bd.Vector(grid_size[0] - self.x_dim / 2, 0 - self.y_dim / 2),
            bd.Vector(grid_size[0] - self.x_dim / 2, grid_size[1] - self.y_dim / 2),
            close=True,
            radius=self.radius
        )
    
    def _get_outline_block(self):
        outline = self._get_outline()
        return bd.extrude(bd.make_face(outline), self.height)

    def get_part(self):
        hole = self._get_hole()
        outline = self._get_outline()

        holes_grid = []
        for x in range(self.x_units):
            for y in range(self.y_units):
                x_center = x * self.x_dim
                y_center = y * self.y_dim

                holes_grid.append(bd.Pos(x_center, y_center) * hole)

        outline_block = self._get_outline_block()

        return outline_block - holes_grid
