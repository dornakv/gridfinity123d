from ocp_vscode import show

from basePlate import BasePlate

import time

start = time.time()
part = BasePlate(5, 3)
print(f"bp.get_part took {time.time() - start}s")

show(part)