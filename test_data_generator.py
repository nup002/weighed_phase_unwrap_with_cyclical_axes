# -*- coding: utf-8 -*-
"""
@author: magne.lauritzen
"""

import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QLabel

DEFAULT_SHAPE = (256, 256)

class UnwrapComparator:
    def __init__(self, source_image, weights=None):
        self.weights = weights
        self.source_image = source_image
        self.wrapped_image = source_image % (2*np.pi)
        self.im_source = pg.ImageView()
        self.im_wrapped = pg.ImageView()
        self.im_weights = pg.ImageView()
        self.im_unwrapped = pg.ImageView()
        self.im_difference = pg.ImageView()
        self.win = QMainWindow()
        self.setup_plot_window()

    def setup_plot_window(self):
        # container widget with a layout to add QWidgets to
        cw = QWidget()
        self.win.setCentralWidget(cw)
        layout = QGridLayout()
        cw.setLayout(layout)
        layout.addWidget(QLabel("Original phase map"), 0, 0)
        layout.addWidget(QLabel("Wrapped phase map"), 2, 0)
        layout.addWidget(QLabel("Unwrapped phase map"), 4, 0)
        layout.addWidget(self.im_source, 1, 0)
        layout.addWidget(self.im_wrapped, 3, 0)
        layout.addWidget(self.im_unwrapped, 5, 0)
        layout.addWidget(QLabel("Weights map"), 0, 1)
        layout.addWidget(self.im_weights, 1, 1)
        layout.addWidget(QLabel("Difference map"), 4, 1)
        layout.addWidget(self.im_difference, 5, 1)

    def unwrap(self, callback):
        unwrapped = callback(self.wrapped_image, weight=self.weights)
        difference = self.source_image - unwrapped
        difference -= np.nanmean(difference)
        self.im_source.setImage(self.source_image)
        self.im_wrapped.setImage(self.wrapped_image)
        self.im_weights.setImage(self.weights)
        self.im_unwrapped.setImage(unwrapped)
        self.im_difference.setImage(difference)
        self.win.resize(1200, 1200)
        self.win.show()
        return self.win

def add_noise(img, sigma):
    gauss = np.random.normal(0, sigma, img.shape)
    return img + gauss

def linear_gradient(shape=DEFAULT_SHAPE, angle=0, phase_offset=0, scale=10, noise=0):
    """
    Generates a linear gradient.
    Args:
        shape: Image size in X,Y pixels
        angle: Direction of gradient in radians.
        phase_offset : Phase offset from 0 to 2pi
        scale: Amplitude of the gradient.
        noise: Gaussian noise level.
    Returns:

    """
    xy_grid = np.mgrid[0:2*np.pi:1j*shape[0], 0:2*np.pi:1j*shape[1]]
    direction_vector = np.array([np.cos(angle), np.sin(angle)])*scale
    vector_grid = xy_grid * direction_vector[:, None, None] + phase_offset
    return add_noise(np.sum(vector_grid, axis=0), noise)

def gaussian_gradient(shape=DEFAULT_SHAPE, angle=0, aspect_ratio = 1, sigma=0.5, scale=10, offset=(0, 0), noise=0):
    """
    Generates a 2D gaussian gradient.
    Args:
        shape: Image size in X,Y pixels
        angle: Direction of gradient in radians. Only applicable if aspect_ratio is not 1.
        aspect_ratio : Ovality. Defined as the ratio of sigma x / sigma y
        sigma: Standard deviation of gaussian gradient.
        scale: Amplitude of the gaussian.
        offset: Offset from the center. (-1, -1) places the center of the gaussian in the top left corner.
        noise: Gaussian noise level.
    Returns:

    """
    xy_grid = np.mgrid[-1:1:1j*shape[0], -1:1:1j*shape[1]] - np.array(list(offset))[:, None, None]
    direction_vector = np.array([np.cos(angle), np.sin(angle)])
    vector_grid = xy_grid * direction_vector[:, None, None]
    gaussian = scale*np.e**(-vector_grid[0]**2/(2*(sigma*aspect_ratio)**2))*np.e**(-vector_grid[1]**2/(2*(sigma**2)))
    return add_noise(gaussian, noise)
