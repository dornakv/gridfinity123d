from ocp_vscode import show

from basePlate import BasePlate
from basePlateMeasurements import BasePlateMeasurements

import time

start = time.time()
measurements = BasePlateMeasurements()
# measurements.radius = 2.85
part = BasePlate(4, 5, measurements)
print(f"bp.get_part took {time.time() - start}s")

show(part)