from qiime2.plugin import (Str, Int, Choices, Citations,
                           MetadataColumn, Categorical, Plugin)
from q2_types.feature_table import FeatureTable, Frequency, Composition

import q2_aldex


plugin = Plugin(
    name='aldex2',
    version=q2_aldex2.__version__,
    website='https://github.com/mortonjt/q2-aldex2',
    package='q2_aldex2',
    description=('Analysis Of Differential Abundance Taking '
                 'Sample Variation Into Account'),
    short_description='Plugin for differential abundance analysis.',
    citations=Citations.load('citations.bib', package='q2_aldex2')
)

plugin.methods.register_function(
    function=q2_aldex2,
    inputs={'table': FeatureTable[Frequency]},
    parameters={'pseudocount': Int},
    outputs=[('composition_table', FeatureTable[Composition])],
    input_descriptions={
        'table': 'The feature table of abundances.',
        'metadata': 'The sample metadata.',
    },
    parameter_descriptions={
        'condition': 'The experimental condition of interest.',
        'mc_samples': 'The number of monte carlo samples',
        'test': 'The statistical test to run, options include `t`, or `glm`',
        'denom': 'The features used to decide a reference frame.'
    },
    output_descriptions={
        'differentials': 'The estimated per-feature differentials.',
        'summary': 'The per-feature summaries, including p-values.'
    }
)
