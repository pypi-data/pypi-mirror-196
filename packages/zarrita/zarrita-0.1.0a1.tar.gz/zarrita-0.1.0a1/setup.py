# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zarrita']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=22.2.0,<23.0.0',
 'cattrs>=22.2.0,<23.0.0',
 'fsspec>=2022.2.0,<2023.0.0',
 'numcodecs>=0.10.0,<0.11.0',
 'numpy>=1.24.2,<2.0.0']

setup_kwargs = {
    'name': 'zarrita',
    'version': '0.1.0a1',
    'description': '',
    'long_description': "# Zarrita\n\nZarrita is an experimental implementation of [Zarr v3](https://zarr-specs.readthedocs.io/en/latest/v3/core/v3.0.html) including [sharding](https://zarr.dev/zeps/draft/ZEP0002.html). This is only a technical proof of concept meant for generating sample datasets. Not recommended for production use.\n\n## Setup\n\n```python\nimport zarrita\nimport numpy as np\n\nstore = zarrita.FileSystemStore('file://./testdata')\n```\n\n## Create an array\n\n```python\na = zarrita.Array.create(\n    store,\n    'array',\n    shape=(6, 10),\n    dtype='int32',\n    chunk_shape=(2, 5),\n    codecs=[zarrita.codecs.gzip_codec(level=1)],\n    attributes={'question': 'life', 'answer': 42}\n)\na[:, :] = np.ones((6, 10), dtype='int32')\n```\n\n## Open an array\n\n```python\na = zarrita.Array.open(store, 'array')\nassert np.array_equal(a[:, :], np.ones((6, 10), dtype='int32'))\n```\n\n## Create an array with sharding\n\n```python\na = zarrita.Array.create(\n    store,\n    'sharding',\n    shape=(16, 16),\n    dtype='int32',\n    chunk_shape=(16, 16),\n    chunk_key_encoding=('v2', '.'),\n    codecs=[\n        zarrita.codecs.sharding_codec(\n            chunk_shape=(8, 8),\n            codecs=[zarrita.codecs.gzip_codec(level=1)]\n        ),\n    ],\n)\ndata = np.arange(0, 16 * 16, dtype='int32').reshape((16, 16))\na[:, :] = data\nassert np.array_equal(a[:, :], data)\n```\n\n## Create a group\n\n```python\ng = zarrita.Group.create(store, 'group')\ng2 = g.create_group('group2')\na = g2.create_array(\n    'array',\n    shape=(16, 16),\n    dtype='int32',\n    chunk_shape=(16, 16),\n)\na[:, :] = np.arange(0, 16 * 16, dtype='int32').reshape((16, 16))\n```\n\n## Open a group\n\n```python\ng = zarrita.Group.open(store, 'group')\ng2 = g['group2']\na = g['group2/array']\nassert np.array_equal(a[:, :], np.arange(0, 16 * 16, dtype='int32').reshape((16, 16)))\n```\n\n# Credits\n\nThis is a largely-rewritten fork of `zarrita` by [@alimanfoo](https://github.com/alimanfoo). It implements the Zarr v3 draft specification created by [@alimanfoo](https://github.com/alimanfoo), [@jstriebel](https://github.com/jstriebel), [@jbms](https://github.com/jbms) et al.\n\nLicensed under MIT\n",
    'author': 'Norman Rzepka',
    'author_email': 'code@normanrz.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
