from ocp_vscode import show

from basePlate import BasePlate
from basePlateMeasurements import BasePlateMeasurements
from basePlateShim import BasePlateShim

import build123d as bd

import time

start = time.time()
shim = BasePlateShim.offset_from_corner(300 * bd.MM, 230 * bd.MM, 0, 0)
base_plate_measurements = BasePlateMeasurements()
base_plate_measurements.top_ledge_width = 0.4 * bd.MM
base_plate_measurements.height -= base_plate_measurements.top_ledge_width
base_plate_measurements.top_chamfer_height -= base_plate_measurements.top_ledge_width
base_plate_measurements.top_chamfer_width -= base_plate_measurements.top_ledge_width
part = BasePlate.from_shim(shim, base_plate_measurements)
print(f"bp.get_part took {time.time() - start}s")

# bd.export_step(shim + shim.offset * part, "res.step")
show(shim + shim.offset * part)
