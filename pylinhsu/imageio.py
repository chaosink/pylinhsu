import numpy as np
from imageio import *

# EXR_DEFAULT = 0  # save data as half with piz-based wavelet compression
# EXR_FLOAT = 0x0001  # save data as float instead of half (not recommended)
# EXR_NONE = 0x0002  # save with no compression
# EXR_ZIP = 0x0004  # save with zlib compression, in blocks of 16 scan lines
# EXR_PIZ = 0x0008  # save with piz-based wavelet compression
# EXR_PXR24 = 0x0010  # save with lossy 24-bit float compression
# EXR_B44 = 0x0020  # save with lossy 44% float compression
#                   # - goes to 22% when combined with EXR_LC
# EXR_LC = 0x0040  # save images with one luminance and two chroma channels,
#                  # rather than as RGB (lossy compression)

def imwrite_float(file_path, img):
    imwrite(file_path, img.astype(np.float32), flags=plugins._freeimage.IO_FLAGS.EXR_FLOAT)

def imwrite_half(file_path, img):
    imwrite(file_path, img.astype(np.float32))

imread = v2.imread
