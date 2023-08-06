# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openeo_pg_parser_networkx']

package_data = \
{'': ['*']}

install_requires = \
['geojson-pydantic>=0.5.0,<0.6.0',
 'networkx>=2.8.6,<3.0.0',
 'numpy>=1.24.1,<2.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'pydantic>=1.9.1,<2.0.0',
 'pyproj>=3.4.0,<4.0.0',
 'shapely>=1.8']

extras_require = \
{'plot': ['matplotlib>=3.7.1,<4.0.0']}

setup_kwargs = {
    'name': 'openeo-pg-parser-networkx',
    'version': '2023.3.0',
    'description': 'Parse OpenEO process graphs from JSON to traversible Python objects.',
    'long_description': '# OpenEO Process Graph Parser (Python & networkx)\n![PyPI - Status](https://img.shields.io/pypi/status/openeo-pg-parser-networkx)\n![PyPI](https://img.shields.io/pypi/v/openeo-pg-parser-networkx)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/openeo-pg-parser-networkx)\n[![codecov](https://codecov.io/github/Open-EO/openeo-pg-parser-networkx/branch/main/graph/badge.svg?token=KEAKFB8AFX)](https://codecov.io/github/Open-EO/openeo-pg-parser-networkx)\n\nPython package to parse OpenEO process graphs from raw JSON into fully traversible [`networkx`](https://github.com/networkx/networkx) graph objects.\nThis package is an evolution of the [openeo-pg-parser-python](https://github.com/Open-EO/openeo-pg-parser-python) package.\n\n## Installation\nThis package can be installed with pip:\n\n```\npip install openeo-pg-parser-networkx\n```\n\nTo enable plotting also install the `plot` extra:\n```\npip install openeo-pg-parser-networkx[plot]\n```\n\nCurrently Python versions 3.9 and 3.10 are supported.\n\n## Basic usage\n(An example notebook of using `openeo-pg-parser-networkx` together with a process implementation source like [`openeo-processes-dask`](https://github.com/Open-EO/openeo-processes-dask) can be found in `openeo-pg-parser-networkx/examples/01_minibackend_demo.ipynb`.)\n\n**Parse a JSON OpenEO process graph:**\n\n```\nfrom openeo_pg_parser_networkx import OpenEOProcessGraph\n\nEVI_GRAPH_PATH = "../tests/data/graphs/pg-evi-example.json"\n\nparsed_graph = OpenEOProcessGraph.from_file(EVI_GRAPH_PATH)\n```\n\n```\n> Deserialised process graph into nested structure\n> Walking node root-7ecd43ed-b694-4a18-8805-eb366d277c8e\n> Walking node mintime-7ecd43ed-b694-4a18-8805-eb366d277c8e\n> Walking node min-80d5faba-c298-4d2f-82f5-be06ee417565\n> Walking node evi-7ecd43ed-b694-4a18-8805-eb366d277c8e\n> Walking node m3-657ee106-6571-4509-a1cf-59f212286011\n> Walking node div-657ee106-6571-4509-a1cf-59f212286011\n> Walking node sub-657ee106-6571-4509-a1cf-59f212286011\n> Walking node nir-657ee106-6571-4509-a1cf-59f212286011\n> Walking node red-657ee106-6571-4509-a1cf-59f212286011\n> Walking node sum-657ee106-6571-4509-a1cf-59f212286011\n> Walking node nir-657ee106-6571-4509-a1cf-59f212286011\n> Walking node m1-657ee106-6571-4509-a1cf-59f212286011\n> Walking node red-657ee106-6571-4509-a1cf-59f212286011\n> Walking node m2-657ee106-6571-4509-a1cf-59f212286011\n> Walking node blue-657ee106-6571-4509-a1cf-59f212286011\n> Walking node load_collection-7ecd43ed-b694-4a18-8805-eb366d277c8e\n```\n\n**Plot it:**\n\n```\nparsed_graph.plot()\n```\n\n![example process graph](./examples/images/reduce_evi.png)\n\nTo execute a process graph, `OpenEOProcessGraph` needs to know which Python code to call for each of the nodes in the graph. This information is provided by a "process registry", which is basically a dictionary that maps each `process_id` to its actual Python implementation as a `Callable`.\n\n**Register process implementations to a "process registry":**\n\nThe `ProcessRegistry` object also allows registering wrapper functions that will be wrapped around each registered process implementation.\nSee [openeo-processes-dask](https://github.com/Open-EO/openeo-processes-dask/blob/main/openeo_processes_dask/core.py) for an example of a wrapper function that resolves incoming parameters.\n\n```\nfrom openeo_pg_parser_networkx import ProcessRegistry\n\nfrom openeo_processes_dask.process_implementations import apply, ndvi, multiply, load_collection, save_result\nfrom openeo_processes_dask.core import process\n\n# `process` is wrapped around each registered implementation\nprocess_registry = ProcessRegistry(wrap_funcs=[process])\n\nprocess_registry["apply"] =  apply\nprocess_registry["ndvi"] =  ndvi\nprocess_registry["multiply"] =  multiply\nprocess_registry["load_collection"] =  load_collection\nprocess_registry["save_result"] =  save_result\n```\n\n**Build an executable callable from the process graph:**\n\n```\npg_callable = parsed_graph.to_callable(process_registry=process_registry)\n```\n\n**Execute that callable like a normal Python function:**\n\n```\npg_callable\n```\n\n```\n> Running process load_collection\n> Running process apply\n> ...\n```\n\n## Development environment\n`openeo-pg-parser-networkx` requires poetry `>1.2`, see their [docs](https://python-poetry.org/docs/#installation) for installation instructions.\n\nTo setup the python venv and install this project into it run:\n```\npoetry install\n```\n\nTo add a new core dependency run:\n```\npoetry add some_new_dependency\n```\n\nTo add a new development dependency run:\n```\npoetry add some_new_dependency --group dev\n```\n\nTo run the test suite run:\n```\npoetry run python -m pytest\n```\n\nNote that you can also use the virtual environment that\'s generated by poetry as the kernel for the ipynb notebooks.\n\n### Pre-commit hooks\nThis repo makes use of [pre-commit](https://pre-commit.com/) hooks to enforce linting & a few sanity checks.\nIn a fresh development setup, install the hooks using `poetry run pre-commit install`.\nThese will then automatically be checked against your changes before making the commit.\n',
    'author': 'Lukas Weidenholzer',
    'author_email': 'lukas.weidenholzer@eodc.eu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Open-EO/openeo-pg-parser-networkx',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
