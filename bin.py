import build123d as bd
from binMeasurements import BinMeasurements
from retentionSocket import RetentionSocket
import constants
import common


class Bin(bd.BasePartObject):
    def __init__(
        self,
        x_units: int,
        y_units: int,
        height_units: int,
        measurements: BinMeasurements = BinMeasurements(),
        rotation: bd.RotationLike = (0, 0, 0),
        align: bd.Align | tuple[bd.Align, bd.Align, bd.Align] = (
            bd.Align.CENTER,
            bd.Align.CENTER,
            bd.Align.CENTER,
        ),
        mode: bd.Mode = bd.Mode.ADD,
    ):
        self._measurements = measurements

        if x_units < 1:
            raise ValueError(f"{x_units=} must be at least 1")
        if y_units < 1:
            raise ValueError(f"{y_units=} must be at least 1")
        if height_units < 1:
            raise ValueError(f"{height_units=} must be at least 1")
        self._x_units = x_units
        self._y_units = y_units
        self._height_units = height_units

        super().__init__(
            part=self._get_part(),
            rotation=rotation,
            align=bd.tuplify(align, 3),
            mode=mode,
        )

    @property
    def x_units(self):
        return self._x_units

    @property
    def y_units(self):
        return self._y_units

    @property
    def height_units(self):
        return self._height_units

    @property
    def x_unit_dim(self):
        return self._measurements.x_unit_dim

    @property
    def y_unit_dim(self):
        return self._measurements.y_unit_dim

    @property
    def radius(self):
        return self._measurements.radius

    @property
    def floor_fillet_radius(self):
        return self._measurements.floor_fillet_radius

    @property
    def height_unit_dim(self):
        return self._measurements.height_unit_dim

    @property
    def retention_socket_measurements(self):
        return self._measurements.retention_socket_measurements

    @property
    def bin_gap(self):
        return self._measurements.bin_gap

    @property
    def floor_thickness(self):
        return self._measurements.floor_thickness

    @property
    def wall_thickness(self):
        return self._measurements.wall_thickness

    def _get_part(self):
        retention_socket = RetentionSocket(self.retention_socket_measurements)
        sockets_grid = []
        for x in range(self.x_units):
            for y in range(self.y_units):
                # TODO: Rewrite cleaner
                x_center = x * self.x_unit_dim - (
                    (self.x_units - 1) * self.x_unit_dim / 2
                )
                y_center = y * self.y_unit_dim - (
                    (self.y_units - 1) * self.y_unit_dim / 2
                )

                sockets_grid.append(
                    bd.Pos(x_center, y_center) * retention_socket
                )

        outer_floor_outline = common.GetRoundedRect(
            (self.x_units * self.x_unit_dim) - (2 * self.bin_gap),
            (self.y_units * self.y_unit_dim) - (2 * self.bin_gap),
            radius=self.radius,
        )
        inner_floor_outline = common.GetRoundedRect(
            (self.x_units * self.x_unit_dim)
            - (2 * self.bin_gap)
            - (2 * self.wall_thickness),
            (self.y_units * self.y_unit_dim)
            - (2 * self.bin_gap)
            - (2 * self.wall_thickness),
            radius=self.radius,
        )

        floor_plane = bd.Plane.XY.offset(
            self.retention_socket_measurements.height + self.floor_thickness
        )
        wall = None
        if (
            self.height_units * self.height_unit_dim
            - self.retention_socket_measurements.height
            > constants.RESOLUTION
        ):
            wall_face = bd.make_face(outer_floor_outline) - bd.make_face(
                inner_floor_outline
            )
            wall_face = floor_plane * wall_face
            wall = bd.extrude(
                wall_face,
                self.height_units * self.height_unit_dim
                - self.retention_socket_measurements.height,
            )

        floor_face = bd.make_face(floor_plane * outer_floor_outline)
        floor = bd.extrude(floor_face, -self.floor_thickness)

        bin = bd.Part(wall + floor + sockets_grid)

        # Fillet inner edges at floor
        # TODO: first filter horizontal faces,
        # make method to check if face is on plane,
        # then get edges of plane.. should be faster.
        # Also do this before merging sockets_gird with the rest,
        # so we do not need to check features on sockets..
        edges = bin.edges().filter_by(
            lambda edge: common.IsEdgeOnPlane(edge, floor_plane)
        )
        bin = bin.fillet(self.floor_fillet_radius, edges)

        return bin
