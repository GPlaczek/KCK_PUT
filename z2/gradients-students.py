#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division             # Division in Python 2.7
import matplotlib
matplotlib.use('Agg')                       # So that we can render files without GUI
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np

from matplotlib import colors

def plot_color_gradients(gradients, names):
    # For pretty latex fonts (commented out, because it does not work on some machines)
    #rc('text', usetex=True) 
    #rc('font', family='serif', serif=['Times'], size=10)
    rc('legend', fontsize=10)

    column_width_pt = 400         # Show in latex using \the\linewidth
    pt_per_inch = 72
    size = column_width_pt / pt_per_inch

    fig, axes = plt.subplots(nrows=len(gradients), sharex=True, figsize=(size, 0.75 * size))
    fig.subplots_adjust(top=1.00, bottom=0.05, left=0.25, right=0.95)


    for ax, gradient, name in zip(axes, gradients, names):
        # Create image with two lines and draw gradient on it
        img = np.zeros((2, 1024, 3))
        for i, v in enumerate(np.linspace(0, 1, 1024)):
            img[:, i] = gradient(v)

        im = ax.imshow(img, aspect='auto')
        im.set_extent([0, 1, 0, 1])
        ax.yaxis.set_visible(False)

        pos = list(ax.get_position().bounds)
        x_text = pos[0] - 0.25
        y_text = pos[1] + pos[3]/2.
        fig.text(x_text, y_text, name, va='center', ha='left', fontsize=10)

    fig.savefig('my-gradients.pdf')

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

def gradient_rgb_bw(v):
    return (v, v, v)


def gradient_rgb_gbr(v):
    return (
        0 if v < 0.5 else 2*v-1,
        1-2*v if v < 0.5 else 0,
        2*v if v < 0.5 else 2-2*v)


def gradient_rgb_gbr_full(v):
    g = 0
    if v < 0.25: g = 1
    elif v < 0.5: g = 1 - 4 * (v - 0.25)
    else: g = 0
    b = 0
    if v < 0.25: b = 4 * v
    elif v < 0.75: b = 1
    else: b = 1 - 4 * (v - 0.75)
    r = 0
    if v < 0.5: r = 0
    elif v < 0.75: r = 4 * (v - 0.5)
    else: r = 1
    return(r, g, b)

    return (0, 0, 0)


def gradient_rgb_wb_custom(v):
    b = 0
    if v < 1/7: b = 1
    elif v < 2/7: b = 1
    elif v < 3/7: b = 1
    elif v < 4/7: b = 1 - 7 * (v - 3/7)
    else: b = 0
    g = 0
    if v < 1/7: g = 1 - 7 * v
    elif v < 2/7: g = 0
    elif v < 3/7: g = 7 * (v - 2/7)
    elif v < 4/7: g = 1
    elif v < 5/7: g = 1
    elif v < 6/7: g = 1 - 7 * (v - 5/7)
    else: g = 0
    r = 0
    if v < 1/7: r = 1
    elif v < 2/7: r = 1 - 7 * (v - 1/7)
    elif v < 3/7: r = 0
    elif v < 4/7: r = 0
    elif v < 5/7: r = 7 * (v - 4/7)
    elif v < 6/7: r = 1
    else: r = 1 - 7 * (v - 6/7)
    # numerical error
    if r < 0: r = 0

    return (r, g, b)


def gradient_hsv_bw(v):
    return hsv2rgb(0, 0, v)


def gradient_hsv_gbr(v):
    return hsv2rgb(3/8+5/8*v, 1, 1)

def gradient_hsv_unknown(v):
    return hsv2rgb(3/8 - 1/2*v, 0.33, 1)


def gradient_hsv_custom(v):
    return hsv2rgb(2*v, 1 - v , 1 - 0.1 * v)


if __name__ == '__main__':
    def toname(g):
        return g.__name__.replace('gradient_', '').replace('_', '-').upper()

    gradients = (gradient_rgb_bw, gradient_rgb_gbr, gradient_rgb_gbr_full, gradient_rgb_wb_custom,
                 gradient_hsv_bw, gradient_hsv_gbr, gradient_hsv_unknown, gradient_hsv_custom)

    plot_color_gradients(gradients, [toname(g) for g in gradients])
