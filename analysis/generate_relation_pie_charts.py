import os
import pandas as pd
import networkx as nx
import networkx.algorithms.community as nx_com
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from collections import Counter
import numpy as np
import seaborn as sns 

def autopct_generator(limit):
    def inner_autopct(pct):
        return ('%1.1f%%' % pct) if pct > limit else ''
    return inner_autopct

print("Generating pie charts for relations...")
data_dir = os.getcwd() + "/analysis/data/relation_distribution"
graphics_output_dir = os.getcwd() + "/analysis/output/relation_distribution/"
# Get a list of all files in data directory
data_files = [f for f in os.listdir(data_dir) if f.endswith(".csv")]
for file in data_files:
    df = pd.read_csv(data_dir + "/{}".format(file))
    labels = []
    for i, relation in enumerate(df["p"]):
        if df["percentage"][i] > 0.05:
            relation = relation.split("/")[-1]
            labels.append(relation.replace("http://bias.org/vocab/", ""))
        else:
            labels.append("")
    
    sizes= df["percentage"]
    fig, ax = plt.subplots()
    
    plt.pie(sizes,labels=labels, startangle=90, autopct=autopct_generator(5), textprops={'fontsize': 10}, colors=sns.color_palette('Set2'))
    fig.savefig(graphics_output_dir + '/{}.png'.format(file.replace(".csv", "")), dpi=300, bbox_inches="tight")


    
   
   




