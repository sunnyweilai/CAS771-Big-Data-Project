import numpy as np
import pandas as pd
from plotnine import *


import matplotlib.pyplot as plt
import seaborn as sns
import csv
import matplotlib.pyplot as plt
import matplotlib.patches as patches


# from subprocess import check_output
# print(check_output(["ls", "lego_database"]).decode("utf8"))

colors = pd.read_csv("lego_database/colors.csv")
inventories = pd.read_csv("lego_database/inventories.csv")
inventory_parts = pd.read_csv("lego_database/inventory_parts.csv")
inventory_sets = pd.read_csv("lego_database/inventory_sets.csv")
part_categories = pd.read_csv("lego_database/part_categories.csv")
parts = pd.read_csv("lego_database/parts.csv")
sets = pd.read_csv("lego_database/sets.csv")
themes = pd.read_csv("lego_database/themes.csv")

# ------------------munge and create new table
color_sets = themes
color_sets['root_id'] = np.where(color_sets['parent_id'].isnull(), color_sets['id'], color_sets['parent_id'])
# print(color_sets['root_id'])

color_sets['theme'] = color_sets['name']
color_sets['theme_id'] = color_sets['id']
color_sets = pd.DataFrame.filter(color_sets, items=['root_id', 'theme', 'theme_id'])
color_sets = pd.merge(color_sets, sets, on='theme_id', how='inner')
color_sets['set_name'] = color_sets['name']
color_sets = pd.DataFrame.filter(color_sets, items=['set_num', 'set_name', 'year', 'root_id', 'theme', 'theme_id'])
# print(color_sets)
color_sets = pd.merge(color_sets, inventories, on='set_num', how='inner')
inventory_parts['id'] = inventory_parts['inventory_id']
color_sets = pd.merge(color_sets, inventory_parts, on='id', how='inner')
colors['color_id'] = colors['id']
color_sets = pd.merge(color_sets, colors, on='color_id', how='inner')
color_sets['rgba'] = np.where(color_sets['is_trans'] == 't', '#' + color_sets['rgb'].astype(str) + str(80), '#' + color_sets['rgb'].astype(str) + 'FF' )
color_sets = pd.DataFrame.filter(color_sets, items = ['set_num', 'set_name', 'theme_id', 'theme', 'root_id', 'rgba', 'year', 'quantity'])


# expand the rows based on the value of the 'quantity' column
color_sets = np.repeat(color_sets.values, color_sets['quantity'].values, axis=0)
color_sets = pd.DataFrame(color_sets, columns=['set_num', 'set_name', 'theme_id', 'theme', 'root_id', 'rgba', 'year', 'quantity'])
color_sets = color_sets.drop('quantity', axis=1)

# print(color_sets)

# ------------------------------color frequency analysis
freq_tbl = pd.DataFrame.filter(color_sets, items = ['year', 'rgba'])
# print(freq_tbl)

# define a function to add a new column -- 'n' to fre_tbl
# def add_n(freq_tbl):
#     freq_tbl['n'] = freq_tbl['rgba'].count()
#     return freq_tbl
#
# freq_tbl = freq_tbl.groupby(['year', 'rgba'])
# freq_tbl = freq_tbl.apply(add_n)
# print(freq_tbl)


# create new table to calculate the frequency of each color in every year
freq_tbl = freq_tbl.sort_values(by = ['year','rgba'], ascending = True)
freq_tbl['n'] = freq_tbl.groupby(['year', 'rgba'])['rgba'].transform('count')
freq_tbl['percent'] = freq_tbl['n'].divide(freq_tbl.groupby(['year'])['n'].transform('count'))
# print(freq_tbl)

# ----------------try to use plotnine to make a plot
pal = (color_sets['rgba']).unique()
pal = np.unique(pal)
# # print(pal)
#
breaks = np.arange(1950,2018,10)
# print(breaks)
uni_color_graph = (ggplot(freq_tbl,aes(x='year', y='percent', fill = 'rgba')) + geom_col(width = 1) +
scale_fill_manual(values = pal) +
scale_x_discrete(limits = breaks) )
# theme(panel_background = element_rect(fill = "#f0f0f0"),
# plot_background = element_rect(fill = "#f8f8f8"),
# text = element_text(size  = 13),
# axis_title = element_text(size = 9, color = "gray15"),
# legend_position = "none",
# axis_text_y = element_blank(),
# axis_ticks = element_blank(),
# panel_grid = element_blank()))

uni_color_graph.save(filename="myPlot3.png", width= 6, height= 4)




# -------------------try sns to make a plot
# pal = (color_sets['rgba']).unique()
# pal = np.unique(pal)
# # print(pal)

# uni_col_graph = sns.barplot(x='year', y= 'rgba', palette=pal, data=freq_tbl)
# uni_col_graph = sns.barplot(x='year', y= 'rgba', hue=pal,data=freq_tbl)
# uni_col_graph.savefig("figure-2.png")






