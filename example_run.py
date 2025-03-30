from ocp_vscode import show

from basePlate import BasePlate
from basePlateMeasurements import BasePlateMeasurements

import time

start = time.time()
measurements = BasePlateMeasurements()
measurements.x_dim = 21
part = BasePlate(5, 3, measurements)
print(f"bp.get_part took {time.time() - start}s")

show(part)