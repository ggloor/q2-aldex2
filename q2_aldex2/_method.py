import os
import qiime2
import numpy as np
import pandas as pd
from biom import Table
import tempfile
import subprocess

import q2_aldex2
from q2_aldex2._visualizer import _effect_statistic_functions


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
        #differentials = summary[['effect']]
	# hack to fix column name for features because aldex removes
	#it in R because of row.names = 1

        summary.index.name = "featureid"
        return summary

def extract_differences(table: pd.DataFrame, sig_threshold: float = 0.1, effect_threshold: float = 1, difference_threshold: float = 1, test: str = 'welch') -> pd.DataFrame:

    # checks to make sure there is no error
    # ensure max or min, depending on case

    effect_statistic_function = _effect_statistic_functions[test]

    if sig_threshold < table[effect_statistic_function].min():
        raise ValueError("You have selected a significance threshold that is lower than minimum Q score (-p--sig-threshold). Select a higher threshold.")

    if effect_threshold > table['effect'].max():
        raise ValueError("You have selected an effect threshold that exceeds maximum effect size (-p--effect-threshold). Choose a lower threshold, or be aware that there there will be no features in the output.")

    if difference_threshold > table['diff.btw'].max():
        raise ValueError("You have selected a difference threshold that exceeds maximum difference (-p--difference-threshold). Choose a lower threshold, or be aware that there will be no features in the output.")

    # subset the table if it psases all the threshold
    differentials_sig = table[(table[effect_statistic_function] <= sig_threshold) & (table['effect'] > effect_threshold) & (table['diff.btw'] > difference_threshold)]

    return differentials_sig
