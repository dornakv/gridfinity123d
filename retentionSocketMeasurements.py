class RetentionSocketMeasurements:
    def __init__(
        self,
        x_dim: float,
        y_dim: float,
        radius: float,
        top_chamfer_height: float,
        top_chamfer_width: float,
        middle_chamfer_height: float,
        middle_chamfer_width: float,
        bottom_chamfer_height: float,
        bottom_chamfer_width: float,
    ):
        self._x_dim = x_dim
        self._y_dim = y_dim
        self._radius = radius
        self._top_chamfer_height = top_chamfer_height
        self._top_chamfer_width = top_chamfer_width
        self._middle_chamfer_height = middle_chamfer_height
        self._middle_chamfer_width = middle_chamfer_width
        self._bottom_chamfer_height = bottom_chamfer_height
        self._bottom_chamfer_width = bottom_chamfer_width

    @property
    def x_dim(self):
        return self._x_dim

    @property
    def y_dim(self):
        return self._y_dim

    @property
    def radius(self):
        return self._radius

    @property
    def top_chamfer_height(self):
        return self._top_chamfer_height

    @property
    def top_chamfer_width(self):
        return self._top_chamfer_width

    @property
    def middle_chamfer_height(self):
        return self._middle_chamfer_height

    @property
    def middle_chamfer_width(self):
        return self._middle_chamfer_width

    @property
    def bottom_chamfer_height(self):
        return self._bottom_chamfer_height

    @property
    def bottom_chamfer_width(self):
        return self._bottom_chamfer_width

    @property
    def height(self):
        return (
            self._bottom_chamfer_height
            + self.middle_chamfer_height
            + self.top_chamfer_height
        )

    @property
    def floor_x_dim(self):
        return self.x_dim - 2 * (
            self.top_chamfer_width
            + self.middle_chamfer_width
            + self.bottom_chamfer_width
        )

    @property
    def floor_y_dim(self):
        return self.y_dim - 2 * (
            self.top_chamfer_width
            + self.middle_chamfer_width
            + self.bottom_chamfer_width
        )

    @property
    def floor_radius(self):
        return self.radius - (
            self.top_chamfer_width
            + self.middle_chamfer_width
            + self.bottom_chamfer_width
        )

    @property
    def middle_low_x_dim(self):
        return self.x_dim - 2 * (
            self.top_chamfer_width
            + self.middle_chamfer_width
        )

    @property
    def middle_low_y_dim(self):
        return self.y_dim - 2 * (
            self.top_chamfer_width
            + self.middle_chamfer_width
        )

    @property
    def middle_low_radius(self):
        return self.radius - (
            self.top_chamfer_width
            + self.middle_chamfer_width
        )

    @property
    def middle_high_x_dim(self):
        return self.x_dim - 2 * (self.top_chamfer_width)

    @property
    def middle_high_y_dim(self):
        return self.y_dim - 2 * (self.top_chamfer_width)

    @property
    def middle_high_radius(self):
        return self.radius - (self.top_chamfer_width)

    @property
    def top_x_dim(self):
        return self.x_dim

    @property
    def top_y_dim(self):
        return self.y_dim

    @property
    def top_radius(self):
        return self.radius
