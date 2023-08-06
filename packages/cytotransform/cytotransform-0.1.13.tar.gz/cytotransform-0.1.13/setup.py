# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cytotransform']

package_data = \
{'': ['*'], 'cytotransform': ['logicle_ext/*']}

install_requires = \
['joblib>=1.2.0,<2.0.0',
 'matplotlib>=3.7.1,<4.0.0',
 'numpy>=1.24.2,<2.0.0',
 'pybind11>=2.10.4,<3.0.0',
 'scipy>=1.10.1,<2.0.0',
 'setuptools>=67.7.1,<68.0.0']

setup_kwargs = {
    'name': 'cytotransform',
    'version': '0.1.13',
    'description': 'Rapid transformations for cytometry data',
    'long_description': '# Cytotransfrom\n\n![PyPI](https://img.shields.io/pypi/v/cytotransform)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cytotransform)\n![PyPI - Wheel](https://img.shields.io/pypi/wheel/cytotransform)\n![PyPI - License](https://img.shields.io/pypi/l/cytotransform)\n![Codecov](https://img.shields.io/codecov/c/github/burtonrj/cytotransform)\n![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/burtonrj/cytotransform/build.yaml)\n\n## Description\n\nCytotransform is a python package for transforming flow cytometry data. It implements the following transformations\naccording to the GatingML 2.0 definitions (https://flowcyt.sourceforge.net/gating/latest.pdf):\n\n- Parametrized logarithmic transformation\n- Parametrized inverse hyperbolic sine transformation (asinh)\n- Logicle transformation\n- Hyperlog transformation\n\nEach transformation is implemented as a `Transform` class with a `transform` method that takes a numpy array as input\nand returns the transformed array. The `Transform` class also has a `transform_inverse` method that takes a numpy array\nas input and returns the inverse transformed array. Each implementation includes validation of the input parameters. The\ntransform classes support multiprocessing out of the box and if `n_jobs` is set to more than 0, then the input data will\nbe split into `n` batches depending on the number of cores available and each batch will be transformed in parallel.\nIf `n_jobs` is set to -1, then all available cores will be used. If `n_jobs` is set to 0, then no multiprocessing will\nbe used.\n\nCytotransform is thanks to the fantastic community of scientists and developers in the single cell and flow\ncytometry data analysis ecosystem. It implements the FastLogicle C++ library for logicle transformations\noriginally implemented by Wayne A Moore and David R Parks (see https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4761345/).\nCode was inspired by the great work by Scott White (https://github.com/whitews/FlowKit) and Brian Teague\n(https://github.com/cytoflow).\n\n## Installation\n\nCytotransform can be installed from PyPi using pip:\n\n```bash\npip install cytotransform\n```\n\n## Usage\n\n### Parametrized logarithmic transformation\n\n```python\nfrom cytotransform import ParametrizedLogTransform\ntransformer = ParametrizedLogTransform(m=4.5, t=262144, n_jobs=-1)\ntransformed_data = transformer.transform(data)\ndata = transformer.inverse_transform(transformed_data)\n```\n\n### Parametrized inverse hyperbolic sine transformation (asinh)\n\n```python\nfrom cytotransform import AsinhTransform\ntransformer = AsinhTransform(m=4.5, t=262144, a=0.0, n_jobs=-1)\ntransformed_data = transformer.transform(data)\ndata = transformer.inverse_transform(transformed_data)\n```\n\n### Logicle transformation\n\n```python\nfrom cytotransform import LogicleTransform\ntransformer = LogicleTransform(t=262144, w=0.5, m=4.5, a=0.0, n_jobs=-1)\ntransformed_data = transformer.transform(data)\ndata = transformer.inverse_transform(transformed_data)\n```\n\n### Hyperlog transformation\n\n```python\nfrom cytotransform import HyperlogTransform\ntransformer = HyperlogTransform(t=262144, w=0.5, m=4.5, a=0.0, n_jobs=-1)\ntransformed_data = transformer.transform(data)\ndata = transformer.inverse_transform(transformed_data)\n```\n\n## License\n\nCytotransform is licensed under the MIT license, is free to use, and comes with no warranty whatsoever.\n',
    'author': 'Ross Burton',
    'author_email': 'burtonrossj@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
