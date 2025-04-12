import build123d as bd
from basePlateMeasurements import BasePlateMeasurements
from basePlateShim import BasePlateShim
import constants
import common

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
        self._measurements = measurements

        if x_units < 1: raise ValueError(f"{x_units=} must be at least 1")
        if y_units < 1: raise ValueError(f"{y_units=} must be at least 1")
        self._x_units = x_units
        self._y_units = y_units

        super().__init__(
            part=self._get_part(), rotation=rotation, align=bd.tuplify(align, 3), mode=mode
        )

    @classmethod
    def from_shim(
        cls,
        basePlateShim: BasePlateShim,
        measurements: BasePlateMeasurements = BasePlateMeasurements(),
        rotation: bd.RotationLike = (0, 0, 0),
        align: bd.Align | tuple[bd.Align, bd.Align, bd.Align] = (
            bd.Align.CENTER,
            bd.Align.CENTER,
            bd.Align.CENTER,
        ),
        mode: bd.Mode = bd.Mode.ADD
    ):
        if basePlateShim.x_unit_dim != measurements.x_unit_dim: raise ValueError(f"{basePlateShim.x_unit_dim=} != {measurements.x_unit_dim=}")
        if basePlateShim.y_unit_dim != measurements.y_unit_dim: raise ValueError(f"{basePlateShim.y_unit_dim=} != {measurements.y_unit_dim=}")
        if basePlateShim.radius != measurements.radius: raise ValueError(f"{basePlateShim.radius=} != {measurements.radius=}")

        return cls(
            basePlateShim.base_plate_x_units,
            basePlateShim.base_plate_y_units,
            measurements=measurements,
            rotation=rotation,
            align=align,
            mode=mode
        )
    
    @property
    def x_units(self): return self._x_units
    @property
    def y_units(self): return self._y_units
    @property
    def x_unit_dim(self): return self._measurements.x_unit_dim
    @property
    def y_unit_dim(self): return self._measurements.x_unit_dim
    @property
    def radius(self): return self._measurements.radius
    @property 
    def height(self): return self._measurements.height
    @property
    def top_chamfer_height(self): return self._measurements.top_chamfer_height
    @property
    def top_chamfer_width(self): return self._measurements.top_chamfer_width
    @property
    def bottom_chamfer_height(self): return self._measurements.bottom_chamfer_height
    @property
    def bottom_chamfer_width(self): return self._measurements.bottom_chamfer_width

    def _get_hole(self):
        if self.bottom_chamfer_height + self.top_chamfer_height > self.height:
            raise ValueError(f"{self.bottom_chamfer_height=} + {self.top_chamfer_height=} < {self.height=}")

        floor = common.GetRoundedRect(
            self.x_unit_dim - 2 * (self.top_chamfer_width + self.bottom_chamfer_width),
            self.y_unit_dim - 2 * (self.top_chamfer_width + self.bottom_chamfer_width),
            self.radius - self.top_chamfer_width - self.bottom_chamfer_width
        ) 

        middle = common.GetRoundedRect(
            self.x_unit_dim - 2 * (self.top_chamfer_width),
            self.y_unit_dim - 2 * (self.top_chamfer_width),
            self.radius - self.top_chamfer_width
        )

        top = common.GetRoundedRect(
            self.x_unit_dim,
            self.y_unit_dim,
            self.radius
        )

        # TODO: Rewrite layesrs array assembly cleaner
        layers = []
        layers.append(floor)
        layers.append(bd.Plane.XY.offset(self.bottom_chamfer_height) 
                      * middle)
        if self.height - self.top_chamfer_height - self.bottom_chamfer_height > constants.RESOLUTION:
            layers.append(bd.Plane.XY.offset(self.height - self.top_chamfer_height) 
                          * middle)
        layers.append(bd.Plane.XY.offset(self.height) 
                      * top)

        return bd.loft(
            layers,
            ruled=True
        )
    
    def get_outline_block(self, tolerance: float = 0):
        outline = common.GetRoundedRect(
            (self.x_units * self.x_unit_dim) + (2 * tolerance),
            (self.y_units * self.y_unit_dim) + (2 * tolerance),
            radius=self.radius
        )
        return bd.extrude(bd.make_face(outline), self.height)

    def _get_part(self):
        hole = self._get_hole()
        holes_grid = []
        for x in range(self.x_units):
            for y in range(self.y_units):
                # TODO: Rewrite cleaner 
                # moving because the outline is genrated centered in coords system
                x_center = x * self.x_unit_dim - ( (self.x_units - 1) * self.x_unit_dim / 2)
                y_center = y * self.y_unit_dim - ( (self.y_units - 1) * self.y_unit_dim / 2)

                holes_grid.append(bd.Pos(x_center, y_center) * hole)

        outline_block = self.get_outline_block()

        return outline_block - holes_grid
