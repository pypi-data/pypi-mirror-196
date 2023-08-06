# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['peepomap']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.0,<4.0.0', 'numpy>=1.21.4,<2.0.0']

setup_kwargs = {
    'name': 'peepomap',
    'version': '0.1.2',
    'description': 'Just some extra Peepo-Powered Matplotlib colormaps.',
    'long_description': '# ![PeepoPing_48x48](https://user-images.githubusercontent.com/12076399/201158312-96136d13-5a86-4aba-8a16-7cfc978b16dc.png) Peepomap\n\nJust some extra Peepo-Powered Matplotlib colormaps.\n\n## 📦 Installation\n\n```bash\npip install peepomap\n```\n\n## 🎨 Colormaps\n\n```python\nimport peepomap\n\npeepomap.tools.display_colormaps(pepomap.cmaps)\n```\n\n![pepomap_colormaps_darkbg](samples/pepomap_colormaps_darkbg.png#gh-dark-mode-only)\n\n![pepomap_colormaps_lightbg](samples/pepomap_colormaps_lightbg.png#gh-light-mode-only)\n\n## 💻 How to use\n\nSimple import and choose a colormap from the above list by it`s name.\n\n```python\nimport peepomap\n\ncmap = peepomap.cmaps["storm"]\n```\n\n## 🏗️ Development\n\nCreate the virtual env using [Poetry](https://github.com/python-poetry/poetry):\n\n```bash\npoetry install\n```\n',
    'author': 'ericmiguel',
    'author_email': 'ericmiguel@id.uff.br',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ericmiguel/peepomap',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<3.11',
}


setup(**setup_kwargs)
