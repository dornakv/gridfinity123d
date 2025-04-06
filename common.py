import build123d as bd
import constants

def GetRoundedRect(x_dim: float, y_dim: float, radius: float) -> bd.BaseSketchObject:
    if x_dim <= constants.RESOLUTION: raise ValueError(x_dim)
    if y_dim <= constants.RESOLUTION: raise ValueError(y_dim)
    if radius < 0: raise ValueError(radius)

    if radius > constants.RESOLUTION:
        return bd.RectangleRounded(x_dim, y_dim, radius)
    return bd.Rectangle(x_dim, y_dim)