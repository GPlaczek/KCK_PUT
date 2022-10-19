#!/usr/bin/env python

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

def hsv2rgb(h, s, v):
    i = int(h * 6)
    f = h * 6 - i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    x = i % 6
    if s == 0: return (v, v, v)
    if x == 0: return (v, t, p)
    if x == 1: return (q, v, p)
    if x == 2: return (p, v, t)
    if x == 3: return (p, q, v)
    if x == 4: return (t, p, v)
    if x == 5: return (v, p, q)

def gradient(v, b):
    return hsv2rgb(3/8-3/8*v, 1-b**3, 0.5+0.5*b)

def normalize(v, max, min):
    return (v - min) / (max - min)

def angle(v1, v2):
     v1_u = v1 / np.linalg.norm(v1)
     v2_u = v2 / np.linalg.norm(v2)
     return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

with open('resources/big.dem') as f:
    width, height, dist = [int(i) for i in f.readline().split()]
    map = np.array([[float(x) for x in i.split()] for i in f.readlines()])
    max = np.amax(map)
    min = np.amin(map)
    # gradient = np.array([[gradient(normalize(v, max, min)) for v in i] for i in map])
    light = np.empty((500, 500, 3))
    sun = np.array((1000, 500, 300))
    for i in range(len(map) - 1):
        for j in range(len(map[i]) - 1):
            d = np.array((i+1, j, map[i+1][j]))
            r = np.array((i, j+1, map[i][j+1]))
            rd = np.array((i+1, j+1, map[i+1][j+1]))
            v = np.cross(d-r, r-rd)
            ang = angle(sun, v)
            light[i][j] = gradient(normalize(map[i][j], max, min), ang/3.14)

    imgplot = plt.imshow(light)
    plt.savefig('mapa_cienie.pdf')
