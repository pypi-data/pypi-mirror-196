# Contributing to cincodex

Contributions are welcome! Feel free to open an issue that describes a bug you're encountering or if you have ideas for new features.

Cincodex uses [poetry](https://python-poetry.org/) for dependency management. To setup a local development environment:

1. Install Python 3.10 or newer.
2. [Install poetry](https://python-poetry.org/docs/#installation).
3. Install development dependencies:
   ```bash
   poetry install --with dev
   ```

Once setup, there are multiple [poe](https://github.com/nat-n/poethepoet) commands to format source code and run checks:

```bash
# format all source code
poetry run poe format

# run source code checks (linting, formatting, type checking, etc.)
poetry run poe checks

# run spell checking (required nodejs and the cspell package)
# you most likely don't need to run this locally since CI runs this for you
poetry run poe check-spelling

# run unit tests
poetry run poe tests

# build the sphinx HTML docs
poetry run poe build-docs

# run the entire CI pipeline locally
poetry run poe ci
```

Cincodex uses the following tools for CI:

- **Formatting**
  - [blue](https://blue.readthedocs.io/en/latest/) - code formatting
  - [isort](https://pycqa.github.io/isort/) - import sorting
- **Linting**
  - [flake8](https://flake8.pycqa.org/en/latest/) - code linting
  - [mypy](https://www.mypy-lang.org/) - static type checking
  - [bandit](https://bandit.readthedocs.io/en/latest/) - secure code checking
  - [cspell](https://cspell.org/) - source code spell checking. *Note:* spell checking is not run as part of `poetry run poe checks` since it depends on Nodejs and the cspell package being installed. cspell runs as part of GitLab CI.
- **Testing**
  - [pytest](https://pytest.org/) - unit test framework
  - [coverage](https://coverage.readthedocs.io/) - code coverage
- **Documentation**
  - [Sphinx](https://www.sphinx-doc.org/) - API documentation generation
