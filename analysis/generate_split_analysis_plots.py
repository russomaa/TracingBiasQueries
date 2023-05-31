import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# Create pie charts for split distribution
target_dir = os.getcwd() + "/analysis/data/split_statistics/"
data_files = [f for f in os.listdir(target_dir) if os.path.isfile(target_dir + f)]
for file in data_files:
    df = pd.read_csv(target_dir + file)
    for index, row in df.iterrows():
        labels = ['Training', 'Validation', 'Test']
        data = [row[2]/row[1]*100, row[3]/row[1]*100, row[4]/row[1]*100]
        fig, ax = plt.subplots()
        ax.bar(labels, data)
        title = row[0] + " - " + file.split(".")[0]
        ax.set_title(title)
        fig.savefig(os.getcwd() + '/analysis/output/split_analysis/{}.png'.format(title), dpi=fig.dpi)

