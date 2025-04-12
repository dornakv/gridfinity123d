from ocp_vscode import show

from basePlate import BasePlate
from basePlateMeasurements import BasePlateMeasurements
from basePlateShimMeasurements import BasePlateShimMeasurements
from basePlateShim import BasePlateShim

import build123d as bd

import time

start = time.time()
measurements = BasePlateMeasurements.with_top_ledge(0.4 * bd.MM)
shimMeasurements = BasePlateShimMeasurements.from_basePlateMeasurements(measurements)

shim = BasePlateShim.offset_from_corner(300 * bd.MM,
                                        230 * bd.MM,
                                        0,
                                        0,
                                        shimMeasurements)
part = BasePlate.from_shim(shim, measurements)
print(f"bp.get_part took {time.time() - start}s")

# bd.export_step(shim + shim.offset * part, "res.step")
show(shim + shim.offset * part)
