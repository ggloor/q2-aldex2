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
        # effect plot
        plt.scatter(x="diff.win", y="diff.btw", data=table, color="grey", s = 10)

        # get maximum value of diff.btw to dynamically lengththen effect size line
        btw_max = table['diff.win'].max()

        # plot positive and negative effect size line
        plt.plot([0, btw_max], [0,btw_max], 'k--', [0,btw_max], [0,-btw_max], 'k--', linewidth=1)

        # change titles and labels
        plt.suptitle('Effect plot')
        plt.xlabel('Difference within')
        plt.ylabel('Difference between')

        img_fp = os.path.join(output_dir, "effect_plot.png")
        plt.savefig(img_fp)

        # get path of index file
        index = os.path.join(TEMPLATES, 'index.html')

        # plot_name displays whether effect or MA
        q2templates.render(index, output_dir, context={'plot_name': type})
