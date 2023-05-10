# -*- coding: utf-8 -*-
"""
@author: magne.lauritzen
"""
from test_data_generator import linear_gradient, gaussian_gradient, UnwrapComparator
from phase_unwrap import phase_unwrap, phase_unwrap_cyclical_axes
import pyqtgraph as pg
import numpy as np

ALGORITHM = phase_unwrap_cyclical_axes  # Pick from phase_unwrap or phase_unwrap_cyclical_axes

app = pg.mkQApp()

# Create phase map to unwrap
gaussian_map = gaussian_gradient(angle=np.pi/4, scale=20, sigma=0.5, aspect_ratio=1, noise=0.3)
final_map = gaussian_map# + linear_map

# Create circular area with weights=0
CIRCLE_RADIUS = 0.4
CIRCLE_OFFSET = [0.2, 0.2]  # Offset from image center
weights = np.ones_like(final_map)
image_grid = np.mgrid[-1:1:1j*final_map.shape[0], -1:1:1j*final_map.shape[1]]
image_grid -= np.array(CIRCLE_OFFSET)[:, None, None]
mask = np.sqrt(image_grid[0]**2 + image_grid[1]**2) < CIRCLE_RADIUS
weights[mask] = 0

# Perform unwrapping and display results
unwrap_test = UnwrapComparator(final_map, weights).unwrap(ALGORITHM)

app.exec()
