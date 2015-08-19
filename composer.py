#!/usr/bin/env python
import sys
import argparse
import numpy as np
from PIL import Image


def matrix3d(a1, b1, c1, d1, a2, b2, c2, d2, a3, b3, c3, d3, a4, b4, c4, d4):
    return np.matrix([
        [a1, a2, a3, a4],
        [b1, b2, b3, b4],
        [c1, c2, c3, c4],
        [d1, d2, d3, d4],
        #[a1, b1, c1, d1],
        #[a2, b2, c2, d2],
        #[a3, b3, c3, d3],
        #[a4, b4, c4, d4],
    ])


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('base', help='Base image (for the background)')
    parser.add_argument('image', help='Image to transform')
    parser.add_argument('-o', '--output', help='Output filename')
    args = parser.parse_args()

    base_im = Image.open(args.base)
    base_pix = base_im.load()

    im = Image.open(args.image)
    pix = im.load()
    m = matrix3d(0.311894, -0.0183492, 0, 0.000312516, 0.336065, 0.373659, 0, 0.0000710468, 0, 0, 1, 0, 138, 623, 0, 1)

    for i in range(im.width):
        for j in range(im.height):
            a = np.array([i, j, 1.0, 1.0])
            b = np.asarray(m.dot(a)).reshape(-1)
            x = int(b[0]/b[3])
            y = int(b[1]/b[3])
            if 0 <= x < base_im.width and 0 <= y < base_im.height:
                base_pix[x, y] = pix[i, j]

    base_im.save(args.output)


if __name__ == '__main__':
    main(sys.argv)
