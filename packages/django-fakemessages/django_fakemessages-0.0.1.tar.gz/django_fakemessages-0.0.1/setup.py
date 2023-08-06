# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fakemessages', 'fakemessages.management', 'fakemessages.management.commands']

package_data = \
{'': ['*']}

install_requires = \
['django>=3.2,<5.0', 'translate-toolkit>=3.8.5,<4.0.0']

setup_kwargs = {
    'name': 'django-fakemessages',
    'version': '0.0.1',
    'description': 'Generate fake language files',
    'long_description': '# django-fakemessages - Generate fake language files for your [Django Project](https://djangoproject.com/)\n\n[![CI tests](https://github.com/pfouque/django-fakemessages/actions/workflows/test.yml/badge.svg)](https://github.com/pfouque/django-fakemessages/actions/workflows/test.yml)\n[![codecov](https://codecov.io/github/pfouque/django-fakemessages/branch/master/graph/badge.svg?token=GWGDR6AR6D)](https://codecov.io/github/pfouque/django-fakemessages)\n[![Documentation](https://img.shields.io/static/v1?label=Docs&message=READ&color=informational&style=plastic)](https://github.com/pfouque/django-fakemessages#settings)\n[![MIT License](https://img.shields.io/static/v1?label=License&message=MIT&color=informational&style=plastic)](https://github.com/pfouque/django-fakemessages/LICENSE)\n\n\n## Introduction\n\nLooking for missing translations in your Django project? Let\'s censor what is done and see what remains!\n\n## Resources\n\n-   Package on PyPI: [https://pypi.org/project/django-fakemessages/](https://pypi.org/project/django-fakemessages/)\n-   Project on Github: [https://github.com/pfouque/django-fakemessages](https://github.com/pfouque/django-fakemessages)\n\n## Requirements\n\n-   Django >=3.2\n-   Python >=3.8\n-   Translate-toolkit >=3.8.5\n\n## How to\n\n1. Install\n    ```\n    $ pip install "django-fakemessages"\n    ```\n\n2. Register fakemessage in your list of Django applications:\n    ```\n    INSTALLED_APPS = [\n        # ...\n        "fakemessages",\n        # ...\n    ]\n    ```\n\n3. Update your settings:\n    ```\n    if DEBUG:\n        """Add our fake language to Django"""\n        from django.conf.locale import LANG_INFO\n\n        FAKE_LANGUAGE_CODE = "kl"\n\n        LANG_INFO[FAKE_LANGUAGE_CODE] = {\n            "bidi": False,\n            "code": FAKE_LANGUAGE_CODE,\n            "name": "▮▮▮▮▮▮▮▮",\n            "name_local": "🖖 ▮▮▮▮▮▮▮",\n        }\n        LANGUAGES.append((FAKE_LANGUAGE_CODE, "🖖 ▮▮▮▮▮▮▮"))\n    ```\n\n4. 🎉 Voila!\n\n\n## Contribute\n\n### Principles\n\n-   Simple for developers to get up-and-running\n-   Consistent style (`black`, `ruff`)\n-   Future-proof (`pyupgrade`)\n-   Full type hinting (`mypy`)\n\n### Coding style\n\nWe use [pre-commit](https://pre-commit.com/) to run code quality tools.\n[Install pre-commit](https://pre-commit.com/#install) however you like (e.g.\n`pip install pre-commit` with your system python) then set up pre-commit to run every time you\ncommit with:\n\n```bash\n> pre-commit install\n```\n\nYou can then run all tools:\n\n```bash\n> pre-commit run --all-files\n```\n\nIt includes the following:\n\n-   `poetry` for dependency management\n-   `Ruff`, `black` and `pyupgrade` linting\n-   `mypy` for type checking\n-   `Github Actions` for builds and CI\n\nThere are default config files for the linting and mypy.\n\n### Tests\n\n#### Tests package\n\nThe package tests themselves are _outside_ of the main library code, in a package that is itself a\nDjango app (it contains `models`, `settings`, and any other artifacts required to run the tests\n(e.g. `urls`).) Where appropriate, this test app may be runnable as a Django project - so that\ndevelopers can spin up the test app and see what admin screens look like, test migrations, etc.\n\n#### Running tests\n\nThe tests themselves use `pytest` as the test runner. If you have installed the `poetry` evironment,\nyou can run them thus:\n\n```\n$ poetry run pytest\n```\n\nor\n\n```\n$ poetry shell\n(django-fakemessages-py3.10) $ pytest\n```\n\n#### CI\n\n- `.github/workflows/lint.yml`: Defines and ensure coding rules on Github.\n\n- `.github/workflows/test.yml`: Runs tests on all compatible combinations of Django (3.2+) & Python (3.8+) in a Github matrix.\n\n- `.github/workflows/coverage.yml`: Calculates the coverage on an up to date version.\n',
    'author': 'Pascal Fouque',
    'author_email': 'fouquepascal@gmail.com',
    'maintainer': 'Pascal Fouque',
    'maintainer_email': 'fouquepascal@gmail.com',
    'url': 'https://github.com/pfouque/django-fakemessages',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
