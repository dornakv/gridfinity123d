import build123d as bd
from ocp_vscode import show

from grid import Grid
from basePlate import BasePlate

grid = Grid(5, 5)
bp = BasePlate(grid)
show(bp.get_part())