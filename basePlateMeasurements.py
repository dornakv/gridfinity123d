import build123d as bd

class BasePlateMeasurements():
    x_dim: float = 42 * bd.MM
    y_dim: float = 42 * bd.MM
    radius: float = 4 * bd.MM

    height: float= 4.65 * bd.MM
    top_chamfer_height: float = 2.15 * bd.MM
    top_chamfer_width: float = 2.15 * bd.MM
    bottom_chamfer_height: float = 0.7 * bd.MM
    bottom_chamfer_width: float = 0.7 * bd.MM