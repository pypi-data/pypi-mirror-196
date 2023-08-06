# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tabular_trees']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.0.0,<2.0.0', 'tqdm==4.46.1']

extras_require = \
{'lightgbm': ['lightgbm>=3.0.0,<4.0.0'],
 'sklearn': ['scikit-learn>=1.0.1,<2.0.0'],
 'xgboost': ['xgboost>=1.4.0,<2.0.0']}

setup_kwargs = {
    'name': 'tabular-trees',
    'version': '0.2.0',
    'description': 'Package for making analysis on tree-based models easier',
    'long_description': '# tabular-trees\n\n![PyPI](https://img.shields.io/pypi/v/tabular-trees?color=success&style=flat)\n![Read the Docs](https://img.shields.io/readthedocs/tabular-trees)\n![GitHub](https://img.shields.io/github/license/richardangell/tabular-trees)\n![GitHub last commit](https://img.shields.io/github/last-commit/richardangell/tabular-trees)\n![Build](https://github.com/richardangell/tabular-trees/actions/workflows/coverage.yml/badge.svg?branch=main)\n\n## Introduction\n\n`tabular-trees` is a package for making analysis on tree-based models easier. \n\nTree based models (specifically GBMs) from `xgboost`, `lightgbm` or `scikit-learn` can be exported to `TabularTrees` objects for further analysis.\n\nThe `explain` and `validate` modules contain functions that operate on `TabularTrees` objects.\n\nSee the [documentation](http://tabular-trees.readthedocs.io/) for more information.\n\n## Install\n\nThe easiest way to get `tabular-trees` is to install directly from [pypi](https://pypi.org/project/tabular-trees/):\n\n```\npip install tabular_trees\n```\n\n`tabular-trees` works with GBMs from `xgboost`, `lightgbm` or `scikit-learn`. These packages must be installed to use the relevant functionality from `tabular-trees`.\n\n`[lightgbm, sklearn, xgboost]` are optional depedencies that can be specified for `tabular-trees`. They can be installed along with `tabular-trees` as follows:\n\n```\npip install tabular_trees[lightgbm, sklearn]\n```\n\n## Build\n\n`tabular-trees` uses [poetry](https://python-poetry.org/) as the environment management and package build tool. Follow the instructions [here](https://python-poetry.org/docs/#installation) to install.\n\nOnce installed run \n\n```\npoetry install --with dev\n```\n\nto install the development dependencies. Other dependency groups are; `docs`, `lightgbm`, `sklearn` and `xgboost`.\n',
    'author': 'Richard Angell',
    'author_email': 'richardangell37@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/richardangell/tabular-trees',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
