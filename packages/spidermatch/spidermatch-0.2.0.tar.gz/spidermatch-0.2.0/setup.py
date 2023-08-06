# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spidermatch', 'spidermatch.lib', 'tests']

package_data = \
{'': ['*'],
 'spidermatch': ['assets/icon_teal.png',
                 'assets/icon_teal.png',
                 'assets/icon_teal.png',
                 'assets/icon_teal.png',
                 'assets/icon_teal.png',
                 'assets/icon_teal.png',
                 'assets/icon_transparent.png',
                 'assets/icon_transparent.png',
                 'assets/icon_transparent.png',
                 'assets/icon_transparent.png',
                 'assets/icon_transparent.png',
                 'assets/icon_transparent.png',
                 'assets/logo.png',
                 'assets/logo.png',
                 'assets/logo.png',
                 'assets/logo.png',
                 'assets/logo.png',
                 'assets/logo.png',
                 'assets/logo_dark.png',
                 'assets/logo_dark.png',
                 'assets/logo_dark.png',
                 'assets/logo_dark.png',
                 'assets/logo_dark.png',
                 'assets/logo_dark.png',
                 'assets/logo_light.png',
                 'assets/logo_light.png',
                 'assets/logo_light.png',
                 'assets/logo_light.png',
                 'assets/logo_light.png',
                 'assets/logo_light.png',
                 'assets/spidermatch.icns',
                 'assets/spidermatch.icns',
                 'assets/spidermatch.icns',
                 'assets/spidermatch.icns',
                 'assets/spidermatch.icns',
                 'assets/spidermatch.icns',
                 'windows/*']}

install_requires = \
['PyQt6>=6.2.3,<7.0.0',
 'beartype>=0.10.4,<0.11.0',
 'luqum>=0.11.0,<0.12.0',
 'qt-material>=2.10,<3.0',
 'rich>=12.2.0,<13.0.0',
 'zenserp>=0.2,<0.3']

entry_points = \
{'console_scripts': ['spidermatch = spidermatch.main:run']}

setup_kwargs = {
    'name': 'spidermatch',
    'version': '0.2.0',
    'description': 'App for setting up automated spiders for incidents covered by local news in a certain country.',
    'long_description': '# SpiderMatch\n\n[![image](https://img.shields.io/pypi/v/spidermatch.svg)](https://pypi.python.org/pypi/spidermatch) [![Bundle App](https://github.com/agucova/spidermatch/actions/workflows/main.yml/badge.svg)](https://github.com/agucova/spidermatch/actions/workflows/main.yml)\n\n![](spidermatch/assets/logo_dark.png#gh-dark-mode-only)\n![](spidermatch/assets/logo_light.png#gh-light-mode-only)\n\n\n> **Note**\n> This app is currently available in Spanish only. An Eglish version is coming soon.\n\nAn open-source app for setting up search engine lookups for incidents covered by local news in a certain country. This app is used for criminology research in policing.\n\n## Installation\nThe app is available on PyPI, so you can install it with pip:\n\n```bash\npip install spidermatch\n```\n\nBundled version of the apps are also available for Windows, Linux and macOS (unsigned).\nYou can find them in the [releases](https://github.com/agucova/spidermatch/releases) section.\n\n## Usage\n\nThis app integrates with ZenSerp, a search engine API. You will need to create an account and get an API key. You can do so [here](https://zenserp.com/).\n\n## Contributing\nSee [CONTRIBUTING.md](CONTRIBUTING.md).\n\n## License\nThis project is licensed under the terms of the [GPLv3](https://www.gnu.org/licenses/gpl-3.0.html) license. See [LICENSE](LICENSE) for more information.\n',
    'author': 'Agustín Covarrubias',
    'author_email': 'agucova@uc.cl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/agucova/spidermatch',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
