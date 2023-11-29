from pylinhsu import image_processing as ip
from pylinhsu import imageio as iio

import numpy as np


def test_alpha_gradient():
    img = ip.alpha_gradient_hdr(101)
    iio.imwrite_float("test/alpha_gradient.101.exr", img)
    img = ip.alpha_gradient_srgb_ldr(101)
    iio.imwrite("test/alpha_gradient.101.png", img)


def test_get_circle_mask_sampled():
    img = np.zeros([10, 21, 3])
    iio.imwrite_float("test/get_circle_mask_alpha.input.exr", img)
    mask = ip.get_circle_mask_alpha(img)
    iio.imwrite_float("test/get_circle_mask_alpha.exr", mask)
    mask = ip.get_circle_mask_alpha(img.astype(np.uint8))
    iio.imwrite("test/get_circle_mask_alpha.png", mask)
