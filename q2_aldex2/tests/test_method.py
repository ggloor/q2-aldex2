import qiime2
import numpy as np
import pandas as pd
from sklearn.utils import check_random_state
from scipy.stats import pearsonr
import unittest
from q2_aldex2._method import aldex2


def random_block_table(reps, n_species,
                       species_mean=0,
                       species_var=1.,
                       effect_size=1,
                       library_size=10000,
                       microbe_total=100000, microbe_kappa=0.3,
                       microbe_tau=0.1, sigma=0.5, seed=None):
    """ Differential abundance analysis benchmarks.

    The simulation here consists of 3 parts

    Step 1: generate class probabilities using logistic distribution
    Step 2: generate coefficients from normal distributions
    Step 3: generate counts from species distributions

    Parameters
    ----------
    reps : int
        Number of replicate samples per test.
    n_species : int
        Number of species.
    species_loc : float
        Mean of the species prior.
    species_variance : float
        Variance of species log-fold differences
    effect_size : int
        The effect size difference between the feature abundances.
    n_contaminants : int
       Number of contaminant species.
    sigma: float
        Logistic error variance for class probabilities
    library_size : np.array
        A vector specifying the library sizes per sample.
    template : np.array
        A vector specifying feature abundances or relative proportions.

    Returns
    -------
    generator of
        pd.DataFrame
           Ground truth tables.
        pd.DataFrame
           Metadata group categories, n_diff and effect_size
        pd.Series
           Species actually differentially abundant.
    """
    state = check_random_state(seed)
    data = []

    n = reps * 2
    k = 2
    labels = np.array([-effect_size] * (n // 2) + [effect_size] * (n // 2))
    eps = np.random.logistic(loc=0, scale=sigma, size=n)
    class_probs = labels + eps

    X = np.hstack((np.ones((n, 1)), class_probs.reshape(-1, 1)))
    B = np.random.normal(loc=species_mean, scale=species_var, size=(k, n_species))

    ## Helper functions
    # Convert microbial abundances to counts
    def to_counts_f(x):
        n = state.lognormal(np.log(library_size), microbe_tau)
        p = x / x.sum()
        return state.poisson(state.lognormal(np.log(n*p), microbe_kappa))

    o_ids = ['F%d' % i for i in range(n_species)]
    s_ids = ['S%d' % i for i in range(n)]

    abs_table = pd.DataFrame(np.exp(X @ B) * microbe_total,
                             index=s_ids,
                             columns=o_ids)

    rel_data = np.vstack(abs_table.apply(to_counts_f, axis=1))

    rel_table = pd.DataFrame(rel_data,
                             index=s_ids,
                             columns=o_ids)

    metadata = pd.DataFrame({'labels': labels})
    metadata['effect_size'] = effect_size
    metadata['microbe_total'] = microbe_total
    metadata['class_logits'] = class_probs
    metadata['intercept'] = 1
    metadata.index = s_ids

    ground_truth = pd.DataFrame({
        'intercept': B[0, :],
        'categorical': B[1, :]
    }, index=o_ids)

    return abs_table, rel_table, metadata, ground_truth


class TestAldex2(unittest.TestCase):

    def setUp(self):

        np.random.seed(0)
        num_samples = 100
        reps = 50
        n_species = 200

        self.res = random_block_table(reps, n_species,
                                 species_mean=0,
                                 species_var=1,
                                 microbe_kappa=0.7,
                                 microbe_tau=0.7,
                                 library_size=10000,
                                 microbe_total=100000,
                                 effect_size=1)

    def test_aldex2(self):
        abs_table, rel_table, metadata, ground_truth = self.res

        rel_table.index.name = 'sampleid'
        metadata.index.name = 'sampleid'

        table = rel_table
        condition = 'labels'
        # Make sure that pandas treats the condition column as categorical, and
        # not numeric (since the "labels" are just ints, pandas infers this as
        # a numeric column) -- solution from
        # https://stackoverflow.com/a/22006514/10730311
        metadata[condition] = metadata[condition].astype(str)
        # metadata[condition] is just a pandas Series, which we can use to
        # create a qiime2.CategoricalMetadataColumn -- solution from
        # https://github.com/qiime2/q2-composition/blob/master/q2_composition/tests/test_ancom.py#L34
        metadata = qiime2.CategoricalMetadataColumn(metadata[condition])
        mc_samples = 128
        test = 't'
        denom = 'all'

        # TODO : allow for summary type
        diff = aldex2(table, metadata, mc_samples, test, denom)

        res = pearsonr(diff.values.ravel(),
                       ground_truth.categorical.values.ravel())

        # test to see if there is a tight correlation
        # which is not necessarily equal
        self.assertGreater(res[0], 0.9)
        self.assertLess(res[1], 1e-10)


if __name__ == "__main__":
    unittest.main()
