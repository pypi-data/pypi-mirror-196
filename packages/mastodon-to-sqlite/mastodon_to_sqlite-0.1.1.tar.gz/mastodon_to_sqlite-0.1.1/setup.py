# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mastodon_to_sqlite']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'requests>=2.28.1,<3.0.0', 'sqlite-utils>=3.30,<4.0']

entry_points = \
{'console_scripts': ['mastodon-to-sqlite = mastodon_to_sqlite.cli:cli']}

setup_kwargs = {
    'name': 'mastodon-to-sqlite',
    'version': '0.1.1',
    'description': 'Save data from Mastodon to a SQLite database',
    'long_description': '# mastodon-to-sqlite\n\nSave data from Mastodon to a SQLite database.\n\n## Install\n\n```console\nfoo@bar:~$ pip install -e git+https://github.com/myles/mastodon-to-sqlite.git#egg=mastodon-to-sqlite\n```\n\n## Authentication\n\nFirst you will need to create an application on your Mastodon server. You\ncan find that on your Mastodon serer.\n\n```console\nfoo@bar:~$ mastodon-to-sqlite auth\nMastodon domain: xxx\n\nCreate a new application here: https://mastodon.social/settings/applications/new\nThen navigate to newly created application and paste in the following:\n\nYour access token: xxx\n```\n\nYou can verify that your authentication by running `mastodon-to-sqlite\nverify-auth`.\n\n## Retrieving Mastodon followers\n\nThe `followers` command will retrieve all the details about your Mastodon \nfollowers.\n\n```console\nfoo@bar:~$ mastodon-to-sqlite followers mastodon.db\n```\n\n## Retrieving Mastodon followings\n\nThe `followings` command will retrieve all the details about your Mastodon \nfollowings.\n\n```console\nfoo@bar:~$ mastodon-to-sqlite followings mastodon.db\n```\n\n## Retrieving Mastodon statuses\n\nThe `statuses` command will retrieve all the details about your Mastodon \nstatuses.\n\n```console\nfoo@bar:~$ mastodon-to-sqlite statuses mastodon.db\n```\n',
    'author': 'Myles Braithwaite',
    'author_email': 'me@mylesbraithwaite.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/myles/mastodon-to-sqlite',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
