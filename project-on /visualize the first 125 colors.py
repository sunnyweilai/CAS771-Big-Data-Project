# --------------------------visualize the first 125 colors

import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt
import matplotlib.patches as patches
sample_n = 250
colors = pd.read_csv('lego_database/colors.csv')

print(colors.head(sample_n))
print(len(colors['rgb'].unique()))

fig1 = plt.figure()
sq = 0.2
width = 5 + sq * len(colors['rgb'])

fig1, axarr = plt.subplots(3, sharex=True)
axarr[0].set_xlim((0, 11))
axarr[0].set_ylim((0, 0.2))
axarr[0].axis('off')
fig1.set_figheight(15)
fig1.set_figwidth(30)
for k in range(1, 50):
    axarr[0].add_patch(
        patches.Rectangle(
            (0.1 + k * 0.2, 0.1),  # (x,y)
            0.2,  # width
            0.2,  # height
            facecolor="#" + colors['rgb'][k],
        )
    )

axarr[1].set_xlim((0, 11))
axarr[1].set_ylim((0, 0.2))
axarr[1].axis('off')
for k in range(50, 100):
    axarr[1].add_patch(
        patches.Rectangle(
            (0.1 + (k - 50) * 0.2, 0.1),  # (x,y)
            0.2,  # width
            0.2,  # height
            facecolor="#" + colors['rgb'][k],
        )
    )

axarr[2].set_xlim((0, 11))
axarr[2].set_ylim((0, 0.2))
axarr[2].axis('off')
for k in range(100, 124):
    axarr[2].add_patch(
        patches.Rectangle(
            (0.1 + (k - 100) * 0.2, 0.1),  # (x,y)
            0.2,  # width
            0.2,  # height
            facecolor="#" + colors['rgb'][k],
        )
    )

# fig1.savefig('rect1.png', dpi=90, bbox_inches='tight')