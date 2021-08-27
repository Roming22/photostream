# Template project for a Python package

- [How to use this project](#how-to-use-this-project)
  - [Prepare GitHub](#prepare-github)
  - [Create a new package from this template project](#create-a-new-package-from-this-template-project)
- [IDE](#ide)
- [Architecture](#architecture)
  - [File system organization](#file-system-organization)
  - [Quality Assurance](#quality-assurance)
    - [Formatting](#formatting)
    - [Linting](#linting)
    - [Testing](#testing)
    - [Type checking](#type-checking)
  - [CI/CD](#cicd)
  - [Versioning](#versioning)
  - [Makefile](#makefile)

## How to use this project

### Prepare GitHub

- Create a new project on [github.com](https://github.com/).
- Open the repository `Settings`.
- Click on `Secrets`.
- Click on `New repository secret`
- Use `Name`: `TEST_PYPI_API_TOKEN`
- Create the test secret:
  - Go to [test.pypi.org](https://test.pypi.org/)
  - Register an account and login
  - Go to `Account settings`
  - Scroll down to `API tokens` and click on `Add API token`
  - Use `Token name`: `github`, `Scope`: `Entire account (all projects)`
  - Click on `Add token`
  - Copy the token
- Copy the token into `Value`
- Click `Add secret`
- Create an account on [pypi.org](https://pypi.org/) (the name can be the same as for `test.pypi.org`) and create a new token.
- Create a new secret, using `Name`: `PYPI_API_TOKEN`, and cpoy the token into  `Value`.

### Create a new package from this template project

- Follow the instructions in `CONTRIBUTING.md` to setup the project.
- Run `tools/init.sh`.
- Open your project on Github.
- Click on `Actions`.
- Check that the CI/CD workflow completed successfully.
- Check that you can see your package in PyPi.

## IDE

`Visual Studio Code` is the recommended IDE for this project. It was chosen for the `Remote - Containers` extension that guarantees the same development environment for every developer. The project is configured so that everything works out of the box.

## Architecture

### File system organization

- `src`: the source code of the application, and nothing more.
- `tools`: anything else that's required to make the project work but is not a part of the application. This may include source code, shell scripts, configuration files, etc.
- `tools/tooling` is used to explicitely link the various configuration files to the software that requires it.
- `tests`: holds tests that can be run with `pytest`.

### Quality Assurance

#### Formatting

- python: [isort](https://github.com/PyCQA/isort) and [black](https://github.com/psf/black).

#### Linting

- python: [pylint](https://www.pylint.org/).
- shell scripts: [shellcheck](https://github.com/koalaman/shellcheck).

#### Testing

- python: [pytest](https://github.com/pytest-dev/pytest/), with [pytest-cov](https://github.com/pytest-dev/pytest-cov) to handle coverage and [pytest-xdist](https://github.com/ohmu/pytest-xdist) to handle parallelization.

#### Type checking

- python: [mypy](https://github.com/python/mypy)

### CI/CD

Whenever pull request is opened against the fork or a new changeset is pushed on the fork (including when a pull request is merged), the CI/CD will run. This is controlled by `.github/workflows/ci-cd.yml`. The content of the file is kept to a minimum, to keep it both readable and clean.

The CI/CD is split into two jobs. `CI` ensures that the tests pass with supported python versions, except the one used for releasing. `CI-CD` ensures that the tests pass with the version of python used for releasing, and uploads the corresponding package without any action from the user. This guarantees that all uploaded packages have been tested with the expected python version.

The version and the upload destination of the package depend on the action that triggered the CI/CD as well as the branch on which this action was triggered. All branches will upload to `test.pypi.org`, but `release/X.Y` branches will also upload to `pypi.org`.

### Versioning

Versioning for major and minor numbers is handled by creating `release/X.Y` branches. The patch number is automatically generated based on existing releases. See `tools/releasing/version.py` for more details.

### Makefile

The project uses a `Makefile` as a way to provide quick access to common commands. It should not be used to write complex scripts. It was chosen over `poetry` scripts because `make` is shorter to type than `poetry run`, despite the shortfall of `make` it is everywhere and many developers are used to `make target` commands, and finally the `Makefile` syntax should be awful enough that you would want to write a `shell` or `python` script if you wanted to do something complicated and call that from the `Makefile`.
