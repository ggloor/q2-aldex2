# ----------------------------------------------------------------------------
# Copyright (c) 2017-2019, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
from setuptools import setup, find_packages

import versioneer

setup(
    name="q2-aldex2",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(),
    author="Greg Gloor",
    author_email="ggloor@uwo.ca",
    description="Analysis Of Differential Abundance Taking Sample Variation Into Account",
    license='GPLv3',
    url="https://www.bioconductor.org/packages/devel/bioc/html/ALDEx2.html",
    entry_points={
        'qiime2.plugins': ['q2-gneiss=q2_gneiss.plugin_setup:plugin']
    },
    package_data={
        "q2_aldex2": ['citations.bib'],
    },
    zip_safe=False,
)
