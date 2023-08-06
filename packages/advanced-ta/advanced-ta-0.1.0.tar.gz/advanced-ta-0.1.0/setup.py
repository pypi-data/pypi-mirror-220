# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['advanced_ta', 'advanced_ta.LorentzianClassification']

package_data = \
{'': ['*']}

install_requires = \
['TA-Lib>=0.4.27,<0.5.0',
 'mplfinance>=0.12.9-beta.7,<0.13.0',
 'numpy>=1.25.1,<2.0.0',
 'pandas>=2.0.3,<3.0.0',
 'python-dotenv>=1.0.0,<2.0.0',
 'scikit-learn>=1.3.0,<2.0.0']

setup_kwargs = {
    'name': 'advanced-ta',
    'version': '0.1.0',
    'description': 'Python implementation of Lorentzian Classification algorithm.',
    'long_description': 'This module is a python implementation of Lorentzian Classification algorithm developed by @jdehorty in pinescript. The original work can be found here - https://www.tradingview.com/script/WhBzgfDu-Machine-Learning-Lorentzian-Classification/\n\n## Prerequisites\n> Ensure that [TA-Lib](https://ta-lib.org/hdr_dw.html) is downloaded and built for your platform. Set `TA_INCLUDE_PATH` and `TA_LIBRARY_PATH` as mentioned in [ta-lib-python](https://github.com/TA-Lib/ta-lib-python#installation). TA-Lib package itself will be installed as a dependency of `advanced-ta`.',
    'author': 'Loki Arya',
    'author_email': 'loki.arya+osdev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
