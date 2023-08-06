# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zipminator']

package_data = \
{'': ['*']}

install_requires = \
['jupyter-sphinx>=0.4.0,<0.5.0',
 'numpy>=1.24.1,<2.0.0',
 'pandas>=1.5.2,<2.0.0',
 'pyzipper>=0.3.6,<0.4.0']

setup_kwargs = {
    'name': 'zipminator',
    'version': '0.3.0',
    'description': 'Zipminator is a lightweight Python package for compressing, encrypting, and deleting password-protected Pandas DataFrames.',
    'long_description': "# Zipminator\n\nZipminator is a lightweight python package with two main functionalities; Zipndel or Unzipndel, for zipping or unzipping a password-protected pandas DataFrame file, and then deleting the original file.\n\n\n# Example usage\n`pip  install zipminator`\n## zipit\n\n```python\nfrom zipminator.zipit import Zipndel\nimport pandas as pd\nimport getpass\nimport zipfile\nimport os\n```\n\n### create instance of Zipndel and call zipit method\n\n```python\nzipndel = Zipndel(file_name='df', file_format='csv')\ndf = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6], 'C': [7, 8, 9]})\nzipndel.zipit(df)\n```\n\n## unzipit\n\n```python\nfrom zipminator.unzipit import Unzipndel\n```\n\n### create instance of Unzipndel and call unzipit method\n\n```python\nunzipndel = Unzipndel(file_name='df', file_format='csv')\ndf = unzipndel.unzipit()\ndf\n```\n",
    'author': 'Daniel Mo Houshmand',
    'author_email': 'mo@qdaria.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://qdaria.github.io/zipminator/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
