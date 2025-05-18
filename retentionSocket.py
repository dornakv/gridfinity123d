import build123d as bd
from retentionSocketMeasurements import RetentionSocketMeasurements
import common
import constants

class RetentionSocket(bd.BasePartObject):
    def __init__(
        self,
        measurements: RetentionSocketMeasurements,
        rotation: bd.RotationLike = (0, 0, 0),
        align: bd.Align | tuple[bd.Align, bd.Align, bd.Align] = (
            bd.Align.CENTER,
            bd.Align.CENTER,
            bd.Align.CENTER,
        ),
        mode: bd.Mode = bd.Mode.ADD
    ):
        self._measurements = measurements
        super().__init__(
            part=self._get_part(), rotation=rotation, align=bd.tuplify(align, 3), mode=mode
        )

    @property
    def floor_x_dim(self): return self._measurements.floor_x_dim
    @property
    def floor_y_dim(self): return self._measurements.floor_y_dim
    @property
    def floor_radius(self): return self._measurements.floor_radius
    @property
    def middle_low_x_dim(self): return self._measurements.middle_low_x_dim
    @property
    def middle_low_y_dim(self): return self._measurements.middle_low_y_dim
    @property
    def middle_low_radius(self): return self._measurements.middle_low_radius
    @property
    def middle_high_x_dim(self): return self._measurements.middle_high_x_dim
    @property
    def middle_high_y_dim(self): return self._measurements.middle_high_y_dim
    @property
    def middle_high_radius(self): return self._measurements.middle_high_radius
    @property
    def top_x_dim(self): return self._measurements.top_x_dim
    @property
    def top_y_dim(self): return self._measurements.top_y_dim
    @property
    def top_radius(self): return self._measurements.top_radius
    @property
    def bottom_chamfer_height(self): return self._measurements.bottom_chamfer_height
    @property
    def middle_chamfer_height(self): return self._measurements.middle_chamfer_height
    @property
    def top_chamfer_height(self): return self._measurements.top_chamfer_height

    def _get_part(self):
        floor = common.GetRoundedRect(
            self.floor_x_dim,
            self.floor_y_dim,
            self.floor_radius
        )

        middle_low = common.GetRoundedRect(
            self.middle_low_x_dim,
            self.middle_low_y_dim,
            self.middle_low_radius
        )

        middle_high = common.GetRoundedRect(
            self.middle_high_x_dim,
            self.middle_high_y_dim,
            self.middle_high_radius
        )

        top = common.GetRoundedRect(
            self.top_x_dim,
            self.top_y_dim,
            self.top_radius
        )

        plane: bd.Plane = bd.Plane.XY
        layers = [plane * floor]
        if self.bottom_chamfer_height > constants.RESOLUTION:
            plane = plane.offset(self.bottom_chamfer_height)
            layers.append(plane * middle_low)
        if self.middle_chamfer_height > constants.RESOLUTION:
            plane = plane.offset(self.middle_chamfer_height)
            layers.append(plane * middle_high)
        if self.top_chamfer_height > constants.RESOLUTION:
            plane = plane.offset(self.top_chamfer_height)
            layers.append(plane * top)
        
        if len(layers) <= 1:
            raise ValueError(f"None of the layers high enough ({constants.RESOLUTION=}): {self.bottom_chamfer_height=}, {self.middle_chamfer_height=}, {self.top_chamfer_height=}")
        
        return bd.loft(
            layers,
            ruled=True
        )