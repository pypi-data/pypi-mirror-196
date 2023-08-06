# sync-version
[![pytest](https://github.com/ffreemt/sync-version/actions/workflows/routine-tests.yml/badge.svg)](https://github.com/ffreemt/sync-version/actions)[![python](https://img.shields.io/static/v1?label=python+&message=3.8%2B&color=blue)](https://www.python.org/downloads/)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/sync_version.svg)](https://badge.fury.io/py/sync_version)

sync version in pyproject.toml (if pyproject.toml does not have version info, then version in package.json) with __version__ in __init__.py

## Install it

```shell
pip install sync-version

# or pip install git+https://github.com/ffreemt/sync-version
# poetry add git+https://github.com/ffreemt/sync-version
# git clone https://github.com/ffreemt/sync-version && cd sync-version
```

## Use it
```python

poetry version prerelease
sync-version  # or python -m sync_version

poetry version patch
sync-version  # or python -m sync_version

# dry-run
sync-version --dry-run

# debug and dry-run
sync-version --debug --dry-run

```

## Typical workflow
```
poetry version prerelease
# yarn version --new-version 0.1.5ax, for example, if necessary

sync-version  # update __version__ in module_name/__init__.py

git add . && git commit -m "Update ..."
git push

poetry build  # or pdm build
poetry publish  # or pdm publish --no-build or twine upload --skip=existing dist\*