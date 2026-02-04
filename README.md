<div align="center">

# Python Project Blueprint

[![Prek][prek-badge]](https://prek.j178.dev/)
[![Mypy][mypy-badge]](https://mypy-lang.org)
[![Ruff][ruff-badge]](https://github.com/astral-sh/ruff)
[![Pytest][pytest-badge]](https://docs.pytest.org/en/stable/)
[![Bandit][bandit-badge]](https://github.com/PyCQA/bandit)
[![Snyk][snyk-badge]](https://snyk.io)
[![Python Version][python-badge]](https://www.python.org/)
[![License][license-badge]](LICENSE.md)

[![PR Checks][pr-badge]](https://github.com/Pymetheus/python-project-blueprint/actions/workflows/pr-checks.yml)
[![Security][security-badge]](https://github.com/Pymetheus/python-project-blueprint/actions/workflows/security.yml)
[![CI][ci-badge]](https://github.com/Pymetheus/python-project-blueprint/actions/workflows/ci.yml)
[![CD][cd-badge]](https://github.com/Pymetheus/python-project-blueprint/actions/workflows/cd.yml)
[![CD][codecov-badge]](https://codecov.io/github/Pymetheus/python-project-blueprint)

[![Bootstrap][bootstrap-badge]](https://github.com/Pymetheus/python-project-blueprint/actions/workflows/bootstrap.yml)
[![Template][use-template-badge]](https://github.com/new?template_name=python-project-blueprint&template_owner=Pymetheus)

</div>

[prek-badge]: https://img.shields.io/badge/prek-enabled-4180b1
[mypy-badge]: https://img.shields.io/badge/mypy-checked-4180b1
[ruff-badge]: https://img.shields.io/badge/ruff-linted-4180b1
[pytest-badge]: https://img.shields.io/badge/pytest-tested-4180b1
[bandit-badge]: https://img.shields.io/badge/bandit-scanned-4180b1
[snyk-badge]: https://img.shields.io/badge/snyk-scanned-4180b1
[python-badge]: https://img.shields.io/badge/python-3.12%2B-blue?color=4180b1
[license-badge]: https://img.shields.io/github/license/Pymetheus/python-project-blueprint?color=4180b1
[pr-badge]: https://github.com/Pymetheus/python-project-blueprint/actions/workflows/pr-checks.yml/badge.svg
[security-badge]: https://github.com/Pymetheus/python-project-blueprint/actions/workflows/security.yml/badge.svg
[ci-badge]: https://github.com/Pymetheus/python-project-blueprint/actions/workflows/ci.yml/badge.svg
[cd-badge]: https://github.com/Pymetheus/python-project-blueprint/actions/workflows/cd.yml/badge.svg
[codecov-badge]: https://codecov.io/github/Pymetheus/python-project-blueprint/graph/badge.svg?token=Y4K5R5F457
[bootstrap-badge]: https://github.com/Pymetheus/python-project-blueprint/actions/workflows/bootstrap.yml/badge.svg
[use-template-badge]: https://img.shields.io/badge/Use%20this%20template-006222


A **production-ready Python project template** designed to remove setup friction and enforce best practices from the very first commit.

The **Python Project Blueprint** gives teams a clean, scalable foundation for Python applications and libraries,
with configuration management, structured logging, testing, security scanning, and CI/CD already integrated, so you can focus on building your product, not infrastructure.


> **Quick Start:** Follow the [Checklist](docs/CHECKLIST.md) to start your next Python project in seconds.

---

## Why This Template?

This blueprint provides a clear starting point that makes Python projects easier to maintain, review, and operate across environments and teams.
By establishing structure, tooling, and automation upfront, it reduces the need for later rewrites as projects grow in scope and complexity.


## Key Features

- **Modern Packaging**
  - `pyproject.toml` as the centralized configuration for packaging, tooling, and metadata
  - Strict `src/` layout to prevent import and packaging issues

- **Layered Configuration Management**
  - Type-safe settings using `pydantic-settings`
  - Environment-based configuration via `APP_ENV`
  - Clear separation of structure (`TOML`) and secrets (`.env`)

- **Production-Grade Logging**
  - Structured logging with `structlog`
  - Colorized developer output
  - JSON logs for production
  - Automatic masking of sensitive fields

- **Quality & Safety by Default**
  - Coverage enforcement with `pytest`
  - Cloud-based coverage reporting and visualization with `Codecov`
  - Minimum 80% coverage threshold
  - Fast linting and formatting via `ruff`
  - Strict static type checking with `mypy`

- **Security by Default**
  - Static analysis with `bandit`
  - Secret detection via `detect-secrets`
  - Dependency vulnerability scanning with `Snyk`

- **Automated CI/CD**
  - `prek` hooks for faster local enforcement
  - Workflows with fast dependency resolution using `uv`
  - Pull request gatekeeping workflows
  - CI verification and packaging
  - Automated CD and GitHub Releases
  - Dependabot for dependency updates

- **Governance at Scale**
  - Issue & PR templates
  - CODEOWNERS
  - Automated label synchronization


## Project Structure Overview
The blueprint enforces a clean, scalable project layout:

```bash
python-project-blueprint/
├── .config/             # Environment & structural configuration
├── .github/             # CI/CD, governance, automation
├── .log/                # Local artifacts (coverage, logs, caches)
├── docker/              # Containerization
├── docs/                # Project documentation
├── src/                 # Application / package source code
├── tests/               # Test suite (pytest)
└── pyproject.toml       # Centralized project configuration
```


## Getting Started

### 1. Create Your Repository
Click **“Use this template”** on GitHub to create a new repository.

### 2. Follow the Setup [Checklist](docs/CHECKLIST.md)
Work through the Checklist, which guides you step by step from:
- creating your repository
- configuring GitHub settings
- running the bootstrap workflow

This ensures a consistent, repeatable setup across teams and projects.

> **Note:** *Check out the [example project](https://github.com/Pymetheus/python-project-blueprint-example), to see how it looks like after the bootstrap workflow*

### 3. Install & Run

Install the project in editable mode with development dependencies:
```bash
# with pip
pip install -e ".[dev]"

# with uv
uv sync --extra dev

# with poetry
poetry install --extras dev
```

> **Note:** *You may use any package manager you prefer (pip, uv, poetry).*

Set up local git hooks for formatting, linting, and security checks:
```bash
prek install
```

> **Note:** *Git must be installed, and you must be inside the cloned Git repository.*

Run the application:
```bash
python -m <package_name>.main
```

At this point, the project is fully set up.
You can begin developing features and writing tests like any standard Python project.

> **Note:** *By default, the project runs in development mode (`APP_ENV=dev`).*


## Documentation

This repository includes detailed documentation to support both new users and advanced contributors:

### **[Checklist](docs/CHECKLIST.md)**
A hands-on execution guide that walks developers through the entire setup flow.
From clicking **[Use this template](https://github.com/new?template_name=python-project-blueprint&template_owner=Pymetheus)** to completing the bootstrap process and running the project locally.

This is the recommended starting point for new users.

### **[Instructions](docs/INSTRUCTIONS.md)**
The technical guide for the blueprint.

It explains:
- the architectural philosophy
- configuration and logging strategies
- CI/CD workflows
- governance and automation decisions

Use this when you want to understand *why* things are built the way they are.


## Who This Is For
The Python Project Blueprint is for developers and teams who want a reliable, production-ready starting point for Python projects, so they can focus on building features instead of setting up infrastructure.

Whether you’re starting a new project or establishing a shared standard, it provides a solid foundation that grows with your needs:
- from prototypes to production
- from individual contributors to teams
- from simple scripts to long-lived services


## Contributing
Your contributions are always welcome!
- For questions and general ideas, please use [GitHub Discussions](https://github.com/Pymetheus/python-project-blueprint/discussions)
- For bugs or concrete changes, please open an [Issue](https://github.com/Pymetheus/python-project-blueprint/issues) or [Pull Request](https://github.com/Pymetheus/python-project-blueprint/pulls) instead

## License
Licensed under the terms defined in [LICENSE.md](LICENSE.md).
