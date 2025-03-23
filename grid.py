import numpy as np

class Grid:
    def __init__(self, x_units: int, y_units: int):
        self._x_units = x_units
        self._y_units = y_units
        self._bool_grid = np.full((self.x_units, self.y_units), True)

    def _get_x_units(self):
        return self._x_units
    
    def _set_x_units(self, x_units: int):
        self._x_units = x_units

    x_units = property(_get_x_units, _set_x_units)

    def _get_y_units(self):
        return self._y_units
    
    def _set_y_units(self, y_units: int):
        self._y_units = y_units

    y_units = property(_get_y_units, _set_y_units)

    def _get_bool_grid(self):
        return self._bool_grid

    bool_grid = property(_get_bool_grid)

    #todo subtract and add grids together to create different shapes        
