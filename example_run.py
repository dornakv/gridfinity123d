from ocp_vscode import show

from basePlate import BasePlate
from basePlateShim import BasePlateShim

import build123d as bd

import time

start = time.time()
shim = BasePlateShim.offset_from_corner(300 * bd.MM, 230 * bd.MM, 0, 0)
part = BasePlate.from_shim(shim)
print(f"bp.get_part took {time.time() - start}s")

bd.export_step(shim + shim.offset * part, "res.step")
show(shim + shim.offset * part)