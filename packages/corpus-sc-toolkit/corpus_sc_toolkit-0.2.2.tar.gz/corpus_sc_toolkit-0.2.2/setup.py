# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['corpus_sc_toolkit',
 'corpus_sc_toolkit.decisions',
 'corpus_sc_toolkit.decisions.fields',
 'corpus_sc_toolkit.decisions.justice',
 'corpus_sc_toolkit.statutes']

package_data = \
{'': ['*'],
 'corpus_sc_toolkit': ['_sql/analysis/*',
                       '_sql/base/*',
                       '_sql/codes/*',
                       '_sql/codes/events/*',
                       '_sql/decisions/*',
                       '_sql/decisions/inclusions/*',
                       '_sql/statutes/*',
                       '_sql/statutes/references/*'],
 'corpus_sc_toolkit.statutes': ['_tmp/*']}

install_requires = \
['citation-utils>=0.2.8,<0.3.0',
 'corpus-pax>=0.1.24,<0.2.0',
 'markdownify>=0.11.6,<0.12.0',
 'pylts>=0.0.8,<0.0.9',
 'statute-trees>=0.1.4,<0.2.0',
 'unidecode>=1.3.6,<2.0.0']

setup_kwargs = {
    'name': 'corpus-sc-toolkit',
    'version': '0.2.2',
    'description': 'Toolkit to process component elements of a Philippine Supreme Court decision.',
    'long_description': '# corpus-sc-toolkit\n\n![Github CI](https://github.com/justmars/corpus-sc-toolkit/actions/workflows/main.yml/badge.svg)\n\nToolkit to process component elements of a Philippine Supreme Court decision.\n\n## Development\n\nSee [documentation](https://justmars.github.io/corpus-sc-toolkit).\n\n1. Run `poetry shell`\n2. Run `poetry update`\n3. Run `pytest`\n',
    'author': 'Marcelino G. Veloso III',
    'author_email': 'mars@veloso.one',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://mv3.dev',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
