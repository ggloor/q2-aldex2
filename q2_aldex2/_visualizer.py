import os
import qiime2
import numpy as np
import pandas as pd
import q2templates
import pkg_resources
import matplotlib.pyplot as plt
from biom import Table
import tempfile
import subprocess


TEMPLATES = pkg_resources.resource_filename('q2_aldex2', 'assets')

def effect_plot(output_dir: str, table: pd.DataFrame, type: str) -> None:

    #fun
        # base effect plot to build on
        plt.scatter(x="diff.win", y="diff.btw", data=table, color="grey", s = 6)

        # get maximum value of diff.btw to dynamically lengththen effect size line
        btw_max = table['diff.win'].max()

        # get points that pass rare threshold
        # change rare to parameter eventually
        rare = 0
        rare_points = table["rab.all"] < rare

        # sig cutoff for expected benjamini hochberg correct p value of welchs t test
        # change cutoff to parameter eventually
        cutoff = 0.1
        called = table["we.eBH"] <= cutoff

        # plot positive and negative effect size line
        plt.plot([0, btw_max], [0,btw_max], color = "grey", linestyle='dashed', linewidth=1)
        plt.plot([0,btw_max], [0,-btw_max], color = "grey", linestyle='dashed', linewidth=1)

        # colour for rare points
        plt.scatter(x="diff.win", y="diff.btw", data=table[rare_points], color="black", s = 6)

        # colour for significant points
        plt.scatter(x="diff.win", y="diff.btw", data=table[called], color="red", s = 6)

        # change titles and labels
        plt.suptitle('Effect plot')
        plt.xlabel('Median Log2 difference within groups')
        plt.ylabel('Median Log2 difference between groups')

        img_fp = os.path.join(output_dir, "effect_plot.png")
        plt.savefig(img_fp)

        # get path of index file
        index = os.path.join(TEMPLATES, 'index.html')

        # plot_name displays whether effect or MA
        q2templates.render(index, output_dir, context={'plot_name': type})
