import build123d as bd
from ocp_vscode import show

from grid import Grid
from basePlate import BasePlate

import time

grid = Grid(5,5)
bp = BasePlate(grid)

start = time.time()
part = bp.get_part()
print(f"bp.get_part took {time.time() - start}s")

show(part)