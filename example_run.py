import build123d as bd
from ocp_vscode import show

from basePlate import BasePlate

import time

bp = BasePlate(5,3)

start = time.time()
part = bp.get_part()
print(f"bp.get_part took {time.time() - start}s")

show(part)