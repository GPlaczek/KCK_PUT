#!/usr/bin/env python3

from matplotlib import pyplot as plt
import numpy as np
import pandas as ps


def avg(d):
    return sum(d) / len(d)


fig, (ax0, ax1) = plt.subplots(nrows=1, ncols=2)
ax2 = ax0.twiny()
box = {}

# Input files are expected to be in resources/ directory
for (file_name, marker_style, label) in zip(
    ["1c.csv", "1crs.csv", "1ers.csv", "2c.csv", "2crs.csv"],
    ["o", "v", "D", "s", "d"],
    ["1-Coev", "1-Coev-RS", "1-Evol-RS", "2-Coev", "2-Coev-RS"]):
    data = ps.read_csv("resources/{}".format(file_name))
    efforts = data["effort"].values
    times = [
        avg([100 * i for i in data.iloc[d, 2:]])
        for d in data["generation"].values
    ]
    ax0.plot(list(map(lambda x: x / 1000, efforts)),
             times,
             markevery=25,
             marker=marker_style,
             markeredgewidth=0.5,
             markeredgecolor=[0, 0, 0],
             label=label)
    box[label] = [100 * i for i in data.iloc[-1].values[2:]]
    ax0.axes.set_xlim([0, 500])
    # ax2.plot(markers, 'o', marker=".", linestyle="none")
ax2.set_xticks(range(0, 201, 40))
ax2.set_xlim([0, 200])

ax0.set_xlabel(r"Rozegranych gier $[\times1000]$")
ax0.set_ylabel(r"Odsetek wygranych gier $[\%]$")
ax2.set_xlabel("Pokolenie")
ax0.set_ylim([60, 100])

boxes = {
    k: v
    for k, v in sorted(box.items(), key=lambda x: avg(x[1]), reverse=True)
}
ax1.boxplot(boxes.values(),
            notch=True,
            showmeans=True,
            showfliers=True,
            meanprops={
                'marker': 'o',
                'markeredgecolor': 'black',
                'markerfacecolor': 'blue'
            },
            boxprops={
                'color': 'blue',
                'linewidth': 1.5
            },
            flierprops={
                'marker': '+',
                'markeredgecolor': 'blue'
            },
            medianprops={
                'color': 'red',
                'linewidth': 1.5
            },
            whiskerprops={
                'color': 'blue',
                'linestyle': '--',
                'linewidth': 1.5,
                'dashes': (6, 6)
            })

ax1.set_ylim([60, 100])
ax1.set_xticklabels(boxes.keys())
ax1.yaxis.tick_right()
ax1.xaxis.set_tick_params(rotation=30)

ax0.legend(numpoints=2, loc="lower right")
ax0.grid(True, axis="both", linestyle='--', linewidth=1)
ax1.grid(True, axis="both", linestyle='--', linewidth=1)
plt.show()
