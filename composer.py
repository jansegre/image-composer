#!/usr/bin/env python
import sys
import argparse
import numpy as np
from PIL import Image


class Camera(object):

    def __init__(self, c, t, e):
        self.c = np.array(c)
        self.e = np.array(e)
        m1 = np.matrix([
            [            1,              0,              0],
            [            0,  np.cos(-t[0]), -np.sin(-t[0])],
            [            0,  np.sin(-t[0]),  np.cos(-t[0])],
        ])
        m2 = np.matrix([
            [ np.cos(-t[1]),             0,  np.sin(-t[1])],
            [             0,             1,              0],
            [-np.sin(-t[1]),             0,  np.cos(-t[1])],
        ])
        m3 = np.matrix([
            [ np.cos(-t[1]), -np.sin(-t[1]),             0],
            [ np.sin(-t[1]),  np.cos(-t[1]),             0],
            [             0,              0,             1],
        ])
        self.m = m1 * m2 * m3

    def project(self, a):
        a = np.array(a)
        d = self.m.dot(a - self.c)
        d = np.asarray(d).reshape(-1)
        e = self.e
        ed = e[2] / d[2]
        bx = ed * d[0] - e[0]
        by = ed * d[1] - e[1]
        return np.array([bx, by])


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

    cam = Camera([4000, 1000, 5000], [0.3, 0, 0], [5000, 1000, 6000])

    f = 2.0
    m = np.matrix([
        [1, 0, 0,   0],
        [0, 1, 0,   0],
        [0, 0, 1/f, 0],
    ])

    for i in range(im.width):
        for j in range(im.height):
            a = np.array([i, j, 0.])
            b = cam.project(a)
            x = int(b[0])
            y = int(b[1])
            if 0 <= x < base_im.width and 0 <= y < base_im.height:
                base_pix[x, y] = pix[i, j]

    base_im.save(args.output)


if __name__ == '__main__':
    main(sys.argv)
