import qiime2
from qiime2.plugin import (Str, Int, Choices, Citations,
                           Metadata, Categorical, Plugin)
from q2_types.feature_table import FeatureTable, Frequency, Composition
from q2_types.feature_data import FeatureData, Differential

import q2_aldex2
from q2_aldex2._method import aldex2


# TODO: will need to fix the version number
__version__ = '1.14.1'

plugin = Plugin(
    name='aldex2',
    version=__version__,
    website='https://github.com/mortonjt/q2-aldex2',
    package='q2_aldex2',
    description=('Analysis Of Differential Abundance Taking '
                 'Sample Variation Into Account'),
    short_description='Plugin for differential abundance analysis.',
    citations=Citations.load('citations.bib', package='q2_aldex2')
)

plugin.methods.register_function(
    function=aldex2,
    name=('Analysis Of Differential Abundance'),
    description=('Performs log-ratio transformation and statistical testing'),
    inputs={'table': FeatureTable[Frequency]},
    # TODO: will need to provide restrictions on input parameters.
    # see q2-composition for examples on how to do this
    # https://github.com/qiime2/q2-composition/blob/master/q2_composition/plugin_setup.py#L48
    parameters={'metadata': Metadata,
                'condition': Str,
                'mc_samples': Int,
                'test': Str,
                'denom': Str},
    outputs=[('differentials', FeatureData[Differential])],
    input_descriptions={
        'table': 'The feature table of abundances.'
    },
    parameter_descriptions={
        'metadata': 'Sample metadata',
        'condition': 'The experimental condition of interest.',
        'mc_samples': 'The number of monte carlo samples',
        'test': 'The statistical test to run, options include `t`, or `glm`',
        'denom': 'The features used to decide a reference frame.'
    },
    output_descriptions={
        'differentials': 'The estimated per-feature differentials.'
    }
)

# TODO: Need to add a visualizer to summarize the aldex2 results
