# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pydantic_ome_ngff', 'pydantic_ome_ngff.latest', 'pydantic_ome_ngff.v04']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.4,<2.0.0']

setup_kwargs = {
    'name': 'pydantic-ome-ngff',
    'version': '0.2.0',
    'description': 'Pydantic models for the OME-NGFF',
    'long_description': '# pydantic-ome-ngff\n## about\nPydantic models for OME-NGFF metadata. Versions 0.4 and the latest (v0.5-dev) are currently supported. \n\nsupported metadata models: \n\n- [`multiscales`](https://github.com/JaneliaSciComp/pydantic-ome-ngff/blob/main/src/pydantic_ome_ngff/latest/multiscales.py) ([spec](https://ngff.openmicroscopy.org/latest/#multiscale-md))\n- [`axes`](https://github.com/JaneliaSciComp/pydantic-ome-ngff/blob/main/src/pydantic_ome_ngff/latest/axes.py) ([spec](https://ngff.openmicroscopy.org/latest/#axes-md))\n- [`coordinateTransformations`](https://github.com/JaneliaSciComp/pydantic-ome-ngff/blob/main/src/pydantic_ome_ngff/latest/coordinateTransformations.py) ([spec](https://ngff.openmicroscopy.org/latest/#trafo-md))\n- [`plate`](https://github.com/JaneliaSciComp/pydantic-ome-ngff/blob/main/src/pydantic_ome_ngff/latest/plate.py) ([spec](https://ngff.openmicroscopy.org/latest/#plate-md))\n- [`well`](https://github.com/JaneliaSciComp/pydantic-ome-ngff/blob/main/src/pydantic_ome_ngff/latest/well.py) ([spec](https://ngff.openmicroscopy.org/latest/#well-md))\n- [`imageLabel`](https://github.com/JaneliaSciComp/pydantic-ome-ngff/blob/main/src/pydantic_ome_ngff/latest/imageLabel.py) ([spec](https://ngff.openmicroscopy.org/latest/#label-md))\n\n`omero` and `bioformats2raw` are not currently supported, but contributions adding\nsupport for those models would be welcome.\n\nSupport for container-level validation (i.e., checking that multiscale or coordinate \ntransformation metadata is compatible with a hierarchical array / group layout) is being added incrementally. \n\n## installation\n\n```bash\npip install pydantic-ome-ngff\n```\n\n## development\n\n1. clone this repo\n2. install [poetry](https://python-poetry.org/)\n3. run `poetry install --with dev` to get dev dependencies\n4. run `pre-commit install` to install [pre-commit hooks](https://github.com/JaneliaSciComp/pydantic-ome-ngff/blob/main/.pre-commit-config.yaml)',
    'author': 'Davis Vann Bennett',
    'author_email': 'davis.v.bennett@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
