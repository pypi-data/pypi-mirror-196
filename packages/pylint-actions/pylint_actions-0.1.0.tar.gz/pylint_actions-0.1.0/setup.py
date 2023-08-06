# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pylint_actions']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pylint-actions',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Pylint plugin for GitHub Actions annotations\nThis is a plugin for [Pylint](https://www.pylint.org/) that allows it to output annotations \nin the format that GitHub Actions understands. \nSee annotations from [examples](https://github.com/skhomuti/pylint-actions/actions/workflows/example.yml) workflows.\nAlso these annotations will be displayed in your pull requests changes\n\n# Installation\nSo simple:\n```bash\npip install pylint-actions\n```\n\n# Usage\nAdd the following to your `pyproject.toml` file:\n```toml\n[tool.pylint.main]\nload-plugins = "pylint_actions"\n```\nOr load the plugin with any available pylint configuration variants except command line arguments.\n\nNext, run pylint with the `--output-format=actions` option, or shorted `-f actions`.\n\nIn your GitHub Actions workflow, use it like this:\n```yaml\n- name: Run pylint\n  run: poetry run pylint -f actions src\n```',
    'author': 'skhomuti',
    'author_email': 'skhomuti@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
