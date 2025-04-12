import build123d as bd
import math
from basePlateShimMeasurements import BasePlateShimMeasurements
import common
from typing import Union

class BasePlateShim(bd.BasePartObject):
    def __init__(
        self,
        x_dim: float,
        y_dim: float,
        x_offset: float = 0 * bd.MM,
        y_offset: float = 0 * bd.MM,
        measurements: BasePlateShimMeasurements = BasePlateShimMeasurements(),
        rotation: bd.RotationLike = (0, 0, 0),
        align: bd.Align | tuple[bd.Align, bd.Align, bd.Align] = (
            bd.Align.CENTER,
            bd.Align.CENTER,
            bd.Align.CENTER,
        ),
        mode: bd.Mode = bd.Mode.ADD
    ):
        self._measurements = measurements

        if x_dim <= 0: raise ValueError(f"{x_dim=} must be more than 0")
        if y_dim <= 0 : raise ValueError(f"{y_dim=} must be more than 0")
        self._x_dim = x_dim
        self._y_dim = y_dim
        self._offset = bd.Pos(x_offset, y_offset, 0)

        part = self._get_part()
        if align is not None:
            align = bd.tuplify(align, 3)
            bbox = part.bounding_box()
            offset = bbox.to_align_offset(align)
        
        super().__init__(
            part=part,
            rotation=rotation,
            align=bd.tuplify(align, 3),
            mode=mode
        )

        if offset is not None:
            self._offset.position += offset
    
    @classmethod
    def offset_from_corner(
        cls,
        x_dim: float,
        y_dim: float,
        x_offset: float = 0 * bd.MM,
        y_offset: float = 0 * bd.MM,
        measurements: BasePlateShimMeasurements = BasePlateShimMeasurements(),
        rotation: bd.RotationLike = (0, 0, 0),
        align: bd.Align | tuple[bd.Align, bd.Align, bd.Align] = (
            bd.Align.CENTER,
            bd.Align.CENTER,
            bd.Align.CENTER,
        ),
        mode: bd.Mode = bd.Mode.ADD
    ):
        inner_x_dim = (math.floor(x_dim / measurements.x_unit_dim) * measurements.x_unit_dim) + (2 * measurements.tolerance)
        inner_y_dim = (math.floor(y_dim / measurements.y_unit_dim) * measurements.y_unit_dim) + (2 * measurements.tolerance)

        x_offset -= ((x_dim - inner_x_dim) / 2)
        y_offset -= ((y_dim - inner_y_dim) / 2)

        # We are cutting out base plate + 2x tolerance, in order 
        # for the actual base plate to start at left bottom corner,
        # we need to move by one tolerance
        x_offset -= measurements.tolerance
        y_offset -= measurements.tolerance

        return cls(
            x_dim,
            y_dim,
            x_offset=x_offset,
            y_offset=y_offset,
            measurements=measurements,
            rotation=rotation,
            align=align,
            mode=mode
        )

    @property
    def x_dim(self): return self._x_dim
    @property
    def y_dim(self): return self._y_dim
    @property
    def offset(self): return self._offset
    @property
    def x_unit_dim(self): return self._measurements.x_unit_dim
    @property
    def y_unit_dim(self): return self._measurements.x_unit_dim
    @property
    def radius(self): return self._measurements.radius
    @property 
    def height(self): return self._measurements.height
    @property
    def tolerance(self): return self._measurements.tolerance

    @property
    def base_plate_x_units(self): return math.floor(self._x_dim / self.x_unit_dim)
    @property
    def base_plate_y_units(self): return math.floor(self._y_dim / self.y_unit_dim)        

    def _get_part(self):
        outer = bd.extrude(
            common.GetRoundedRect(
                self.x_dim,
                self.y_dim,
                0
            ),
            self.height / 2,
            both=True
        )
        
        if self.base_plate_x_units == 0 or self.base_plate_y_units == 0:
            return outer

        # base plate with tolerance
        inner = self.offset * bd.extrude(
            common.GetRoundedRect(
                (self.base_plate_x_units * self.x_unit_dim) + (2 * self.tolerance),
                (self.base_plate_y_units * self.y_unit_dim) + (2 * self.tolerance),
                0
            ),
            self.height / 2,
            both=True
        )

        shim = outer - inner
        outer = None
        inner = None
        max_filelt = self.radius + self.tolerance

        edges_to_fillet = dict()
        for face in shim.faces().filter_by(bd.Axis.Z, reverse=True):
            face_vert_edges = face.edges().filter_by(bd.Axis.Z)
            if len(face_vert_edges) != 2: continue
            face_width = face_vert_edges[0].distance_to(face_vert_edges[1])
            allowed_fillet = face_width / 2 - self.tolerance
            for edge in face_vert_edges:
                if edge in edges_to_fillet:
                    curr_edge_fillet = edges_to_fillet[edge]
                    edges_to_fillet[edge] = min(curr_edge_fillet, allowed_fillet)
                else:
                    edges_to_fillet[edge] = min(allowed_fillet, max_filelt)

        for edge in edges_to_fillet:
            edge.topo_parent = shim
            shim = bd.fillet([edge], edges_to_fillet[edge])

        return shim