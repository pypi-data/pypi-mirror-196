# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fluidsimfoam',
 'fluidsimfoam.output',
 'fluidsimfoam.resources',
 'fluidsimfoam.solvers',
 'fluidsimfoam.util']

package_data = \
{'': ['*']}

install_requires = \
['fluiddyn>=0.5.2,<0.6.0',
 'fluidsim-core>=0.7.2,<0.8.0',
 'inflection>=0.5.1,<0.6.0',
 'ipython>=8.11.0,<9.0.0',
 'jinja2>=3.1.2,<4.0.0',
 'pandas>=1.5.3,<2.0.0']

entry_points = \
{'console_scripts': ['fluidsimfoam-info = '
                     'fluidsimfoam.util.console:print_versions',
                     'fluidsimfoam-ipy-load = '
                     'fluidsimfoam.util.console:start_ipython_load_sim']}

setup_kwargs = {
    'name': 'fluidsimfoam',
    'version': '0.0.1',
    'description': 'Python framework for OpenFOAM',
    'long_description': '# Fluidsimfoam\n\n<!-- badges -->\n\nPython framework for [OpenFOAM]\n\nFluidsimfoam is a Python package which **will** allow one to write [Fluidsim]\nsolvers based for the simulations on the C++ CFD code [OpenFOAM]. There\n**will** be open-source solvers (in particular fluidsimfoam-phill and\nfluidsimfoam-tgv) and it **will** not be difficult to write your own solver\nbased on your [OpenFOAM] cases.\n\nWith a Fluidsimfoam solver, it **will** becomes very easy to\n\n- launch/restart simulations with Python scripts and terminal commands,\n- load simulations, read the associated parameters/data and produce nice figures/movies.\n\nFluidsimfoam can be seen as a workflow manager for [OpenFOAM] or a Python\nwrapper around [OpenFOAM]. It uses [OpenFOAM] on the background and is thus NOT\na rewrite of [OpenFOAM]!\n\nFluidsimfoam is now in very early development. The goal is to get the\nequivalent of [Snek5000], our Fluidsim framework for [Nek5000].\n\n## Related projects\n\n- [PyFoam] ([PyPI package](https://pypi.org/project/PyFoam/),\n  [hg repo](http://hg.code.sf.net/p/openfoam-extend/PyFoam)) Python utilities for\n  OpenFOAM. GNU GPL. Still maintained. Should be used by Fluidsimfoam.\n\n- [Fluidfoam] Another Fluiddyn package (like Fluidsimfoam) to use/plot OpenFOAM\n  data. Will be used by Fluidsimfoam.\n\n- [PythonFlu] ([wiki](https://openfoamwiki.net/index.php/Contrib_pythonFlu))\n\n- [Swak4Foam]\n\n[PyFoam]: https://openfoamwiki.net/index.php/Contrib/PyFoam\n[fluidsim]: https://fluidsim.readthedocs.io\n[fluidfoam]: https://fluidfoam.readthedocs.io\n[openfoam]: https://openfoam.org/\n[nek5000]: https://nek5000.mcs.anl.gov/\n[snek5000]: https://snek5000.readthedocs.io\n[PythonFlu]: http://pythonflu.wikidot.com/\n[Swak4Foam]: https://openfoamwiki.net/index.php/Contrib/swak4Foam\n',
    'author': 'pierre.augier',
    'author_email': 'pierre.augier@univ-grenoble-alpes.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
