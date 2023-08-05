# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydantic_numpy']

package_data = \
{'': ['*']}

install_requires = \
['compress-pickle[lz4]', 'numpy', 'pydantic', 'ruamel-yaml>=0.17.21,<0.18.0']

setup_kwargs = {
    'name': 'pydantic-numpy',
    'version': '2.0.0',
    'description': 'Seamlessly integrate numpy arrays into pydantic models',
    'long_description': '# pydantic-numpy\n\nIntegrate NumPy into Pydantic, and provide tooling! `NumpyModel` make it possible to dump and load `np.ndarray` within model fields!\n\n### Install\n```shell\npip install pydantic-numpy\n```\n\n## Usage\n\nFor more examples see [test_ndarray.py](./tests/test_ndarray.py)\n\n```python\nimport pydantic_numpy.dtype as pnd\nfrom pydantic_numpy import NDArray, NDArrayFp32, NumpyModel\n\n\nclass MyPydanticNumpyModel(NumpyModel):\n    K: NDArray[float, pnd.float32]\n    C: NDArrayFp32  # <- Shorthand for same type as K\n\n\n# Instantiate from array\ncfg = MyPydanticNumpyModel(K=[1, 2])\n# Instantiate from numpy file\ncfg = MyPydanticNumpyModel(K={"path": "path_to/array.npy"})\n# Instantiate from npz file with key\ncfg = MyPydanticNumpyModel(K={"path": "path_to/array.npz", "key": "K"})\n\ncfg.K\n# np.ndarray[np.float32]\n\ncfg.dump("path_to_dump")\ncfg.load("path_to_dump")\n```\n\n### Data type (dtype) support!\n\nThis package also comes with `pydantic_numpy.dtype`, which adds subtyping support such as `NDArray[float, pnd.float32]`. All subfields must be from this package as numpy dtypes have no Pydantic support, which is implemented in this package through the [generic class workflow](https://pydantic-docs.helpmanual.io/usage/types/#generic-classes-as-types).\n\n## Considerations\n\nThe `NDArray` class from `pydantic-numpy` is daughter of `np.ndarray`. IDEs and linters might complain that you are passing an incorrect `type` to a model. The only solution is to merge these change into `numpy`.\n\nYou can also use the `typings` in `pydantic.validate_arguments`.\n\nYou can install from [cheind\'s](https://github.com/cheind/pydantic-numpy) repository if you want Python `3.8` support.\n\n## History\n\nThe original idea originates from [this discussion](https://gist.github.com/danielhfrank/00e6b8556eed73fb4053450e602d2434), and forked from [cheind\'s](https://github.com/cheind/pydantic-numpy) repository.\n',
    'author': 'Can H. Tartanoglu',
    'author_email': 'canhtart@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/caniko/pydantic-numpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
