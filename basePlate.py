import build123d as bd
from basePlateMeasurements import BasePlateMeasurements

class BasePlate(bd.BasePartObject):
    def __init__(
        self,
        x_units: int,
        y_units: int,
        measurements: BasePlateMeasurements = BasePlateMeasurements(),
        rotation: bd.RotationLike = (0, 0, 0),
        align: bd.Align | tuple[bd.Align, bd.Align, bd.Align] = (
            bd.Align.CENTER,
            bd.Align.CENTER,
            bd.Align.CENTER,
        ),
        mode: bd.Mode = bd.Mode.ADD
    ):
        super().__init__(
            part=self._get_part(x_units, y_units, measurements), rotation=rotation, align=bd.tuplify(align, 3), mode=mode
        )

    def _get_hole(self, measurements: BasePlateMeasurements):
            inner_x_dim = measurements.x_dim - 2 * (measurements.top_chamfer_width + measurements.bottom_chamfer_width)
            inner_y_dim = measurements.y_dim - 2 * (measurements.top_chamfer_width + measurements.bottom_chamfer_width)

            top_chamfer_lower_radius = measurements.radius - measurements.top_chamfer_width
            bottom_chamfer_lower_radius = measurements.radius - measurements.top_chamfer_width - measurements.bottom_chamfer_width

            floor = bd.make_face(bd.FilletPolyline(
                bd.Vector(0 - inner_x_dim / 2, 0 + inner_y_dim / 2),
                bd.Vector(0 - inner_x_dim / 2, 0 - inner_y_dim / 2),
                bd.Vector(0 + inner_x_dim / 2, 0 - inner_y_dim / 2),
                bd.Vector(0 + inner_x_dim / 2, 0 + inner_y_dim / 2),
                close=True,
                radius=bottom_chamfer_lower_radius
            ))

            inner_x_dim = measurements.x_dim - 2 * (measurements.top_chamfer_width)
            inner_y_dim = measurements.y_dim - 2 * (measurements.top_chamfer_width)

            middle = bd.make_face(bd.FilletPolyline(
                bd.Vector(0 - inner_x_dim / 2, 0 + inner_y_dim / 2),
                bd.Vector(0 - inner_x_dim / 2, 0 - inner_y_dim / 2),
                bd.Vector(0 + inner_x_dim / 2, 0 - inner_y_dim / 2),
                bd.Vector(0 + inner_x_dim / 2, 0 + inner_y_dim / 2),
                close=True,
                radius=top_chamfer_lower_radius
            ))

            inner_x_dim = measurements.x_dim
            inner_y_dim = measurements.y_dim

            top = bd.make_face(bd.FilletPolyline(
                bd.Vector(0 - inner_x_dim / 2, 0 + inner_y_dim / 2),
                bd.Vector(0 - inner_x_dim / 2, 0 - inner_y_dim / 2),
                bd.Vector(0 + inner_x_dim / 2, 0 - inner_y_dim / 2),
                bd.Vector(0 + inner_x_dim / 2, 0 + inner_y_dim / 2),
                close=True,
                radius=measurements.radius
            ))

            return  bd.loft((floor,
                                  bd.Plane.XY.offset(measurements.bottom_chamfer_height) * middle)) +\
                    bd.loft((bd.Plane.XY.offset(measurements.bottom_chamfer_height) * middle,
                                  bd.Plane.XY.offset(measurements.height-measurements.top_chamfer_height) * middle)) +\
                    bd.loft((bd.Plane.XY.offset(measurements.bottom_chamfer_height) * middle,
                                  bd.Plane.XY.offset(measurements.height-measurements.top_chamfer_height) * middle)) +\
                    bd.loft((bd.Plane.XY.offset(measurements.height-measurements.top_chamfer_height) * middle,
                                  bd.Plane.XY.offset(measurements.height) * top))

    def _get_outline(self, x_units: int, y_units: int, measurements: BasePlateMeasurements):
        grid_size = [
            x_units * measurements.x_dim,
            y_units * measurements.y_dim
        ]

        return bd.FilletPolyline(
            bd.Vector(0 - measurements.x_dim / 2, grid_size[1] - measurements.y_dim / 2),
            bd.Vector(0 - measurements.x_dim / 2, 0 - measurements.y_dim / 2),
            bd.Vector(grid_size[0] - measurements.x_dim / 2, 0 - measurements.y_dim / 2),
            bd.Vector(grid_size[0] - measurements.x_dim / 2, grid_size[1] - measurements.y_dim / 2),
            close=True,
            radius=measurements.radius
        )
    
    def _get_outline_block(self, x_units: int, y_units: int, measurements: BasePlateMeasurements):
        outline = self._get_outline(x_units, y_units, measurements)
        return bd.extrude(bd.make_face(outline), measurements.height)

    def _get_part(self, x_units: int, y_units: int, measurements: BasePlateMeasurements):
        hole = self._get_hole(measurements)
        holes_grid = []
        for x in range(x_units):
            for y in range(y_units):
                x_center = x * measurements.x_dim
                y_center = y * measurements.y_dim

                holes_grid.append(bd.Pos(x_center, y_center) * hole)

        outline_block = self._get_outline_block(x_units, y_units, measurements)

        return outline_block - holes_grid
