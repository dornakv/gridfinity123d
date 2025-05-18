import build123d as bd

# Values here shouldn't need changing, only when you REALLY know
# what you are doing
# most values can be changed in the respective Measurement classes

# For checking whether some parts would be too small to generate,
# often due to floating point errors
RESOLUTION = 0.001 * bd.MM
# BasePlate tolerance has on each side outside, shim has on each side inside
TOLERANCE = 0.10 * bd.MM
X_UNIT_DIM: float = 42 * bd.MM
Y_UNIT_DIM: float = 42 * bd.MM
HEIGHT_UNIT_DIM: float = 7 * bd.MM
