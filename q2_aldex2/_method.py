import os
import qiime2
import numpy as np
import pandas as pd
from biom import Table
import tempfile
import subprocess


def run_commands(cmds, verbose=True):
    if verbose:
        print("Running external command line application(s). This may print "
              "messages to stdout and/or stderr.")
        print("The command(s) being run are below. These commands cannot "
              "be manually re-run as they will depend on temporary files that "
              "no longer exist.")
    for cmd in cmds:
        if verbose:
            print("\nCommand:", end=' ')
            print(" ".join(cmd), end='\n\n')
        subprocess.run(cmd, check=True)


def aldex2(table: pd.DataFrame,
           metadata: qiime2.Metadata,
           condition: str,
           mc_samples: int = 128,
           test: str = 't',
           denom: str = 'all') -> pd.DataFrame:

    with tempfile.TemporaryDirectory() as temp_dir_name:
        biom_fp = os.path.join(temp_dir_name, 'input.tsv.biom')
        map_fp = os.path.join(temp_dir_name, 'input.map.txt')
        summary_fp = os.path.join(temp_dir_name, 'output.summary.txt')

        table.to_csv(biom_fp, sep='\t')
        metadata.to_dataframe().to_csv(map_fp, sep='\t')

        cmd = ['run_aldex2.R', biom_fp, map_fp, condition, mc_samples,
               test, denom, summary_fp]
        cmd = list(map(str, cmd))

        try:
            run_commands([cmd])
        except subprocess.CalledProcessError as e:
            raise Exception("An error was encountered while running ALDEx2"
                            " in R (return code %d), please inspect stdout"
                            " and stderr to learn more." % e.returncode)

        summary = pd.read_csv(summary_fp, index_col=0)
        differentials = summary[['effect']]
        # don't return summary for now (TODO!)
        return differentials
