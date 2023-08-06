# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['restore',
 'restore.management',
 'restore.management.commands',
 'restore.migrations']

package_data = \
{'': ['*']}

install_requires = \
['django>=4.1.7,<5.0.0', 'pyyaml==6.0']

setup_kwargs = {
    'name': 'django-restic-backup',
    'version': '0.3.0',
    'description': 'Restore files or/and database backup from an environment (backup server) with encrypted secret file after decrypting it (secret file is defined in settings.BACKUP_CONF_FILE',
    'long_description': 'None',
    'author': 'Dedomainia',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
