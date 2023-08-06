# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['newrelic_sb_sdk',
 'newrelic_sb_sdk.alerts',
 'newrelic_sb_sdk.client',
 'newrelic_sb_sdk.core',
 'newrelic_sb_sdk.dashboards',
 'newrelic_sb_sdk.graphql',
 'newrelic_sb_sdk.utils']

package_data = \
{'': ['*']}

install_requires = \
['enforce-typing>=1.0.0.post1,<2.0.0',
 'python-dotenv>=1.0.0,<2.0.0',
 'requests>=2.28.2,<3.0.0',
 'semver>=2.13.0,<3.0.0',
 'sgqlc>=16.1,<17.0']

setup_kwargs = {
    'name': 'newrelic-sb-sdk',
    'version': '0.2.0',
    'description': 'New Relic SDK to interact with API for data retrieving',
    'long_description': '![Community-Project](https://gitlab.com/softbutterfly/open-source/open-source-office/-/raw/master/banners/softbutterfly-open-source--banner--community-project.png)\n\n![PyPI - Supported versions](https://img.shields.io/pypi/pyversions/wagtail-sb-admin-interface)\n![PyPI - Package version](https://img.shields.io/pypi/v/wagtail-sb-admin-interface)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/wagtail-sb-admin-interface)\n![PyPI - MIT License](https://img.shields.io/pypi/l/wagtail-sb-admin-interface)\n\n[![Build Status](https://www.travis-ci.org/softbutterfly/wagtail-sb-admin-interface.svg?branch=develop)](https://www.travis-ci.org/softbutterfly/wagtail-sb-admin-interface)\n[![Codacy Badge](https://app.codacy.com/project/badge/Grade/e35e7095857b416696eb58a4ed5d9a15)](https://www.codacy.com/gh/softbutterfly/wagtail-sb-admin-interface/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=softbutterfly/wagtail-sb-admin-interface&amp;utm_campaign=Badge_Grade)\n[![Codacy Badge Coverage](https://app.codacy.com/project/badge/Coverage/e35e7095857b416696eb58a4ed5d9a15)](https://www.codacy.com/gh/softbutterfly/wagtail-sb-admin-interface/dashboard?utm_source=github.com&utm_medium=referral&utm_content=softbutterfly/wagtail-sb-admin-interface&utm_campaign=Badge_Coverage)\n[![codecov](https://codecov.io/gh/softbutterfly/wagtail-sb-admin-interface/branch/master/graph/badge.svg?token=pbqXUUOu1F)](https://codecov.io/gh/softbutterfly/wagtail-sb-admin-interface)\n\n# New Relic SB SDK\n\nNew Relic SDK built by SoftButterfly to automate common New Relic One observability platform tasks\n\n## Requirements\n\n- Python 3.8.1 or higher\n- `enforce-typing`\n- `python-dotenv`\n- `requests`\n- `semver`\n- `sgqlc`\n\n## Install\n\nInstall from PyPI\n\n```bash\npip install newrelic-sb-sdk\n```\n\n## Docs\n\n- [Ejemplos](https://gitlab.com/softbutterfly/open-source/newrelic-sb-sdk/wiki)\n- [Wiki](https://gitlab.com/softbutterfly/open-source/newrelic-sb-sdk/wiki)\n\n## Changelog\n\nAll changes to versions of this library are listed in the [change history](./CHANGELOG.md).\n\n## Development\n\nCheck out our [contribution guide](./CONTRIBUTING.md).\n\n## Contributors\n\nSee the list of contributors [here](https://gitlab.com/softbutterfly/open-source/wagtail-sb-admin-interface/-/graphs/master).\n\n## License\n\nThis project is licensed under the terms of the MIT license. See the <a href="./LICENSE.txt" download>LICENSE</a> file.\n',
    'author': 'SoftButterfly Development Team',
    'author_email': 'dev@softbutterfly.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/softbutterfly/open-source/wagtail-sb-admin-interface',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
