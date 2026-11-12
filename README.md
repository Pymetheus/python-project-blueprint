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
[![Codecov][codecov-badge]](https://codecov.io/github/Pymetheus/python-project-blueprint)

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


A **production-ready Python project template** designed to reduce repetitive setup tasks and establish good development practices from the very first commit.

The **Python Project Blueprint** provides a clean, scalable foundation for Python applications and libraries,
with configuration management, structured logging, testing, code quality tools, security scanning, containerization, and CI/CD already integrated,
so you can spend less time setting up projects and more time building your product.


> **Quick Start:** Follow the [Checklist](docs/CHECKLIST.md) to start your next Python project in seconds.

---

## Why This Template?

The Python Project Blueprint provides a clear starting point for Python applications and libraries, making projects easier to maintain, review, and operate across environments and teams.
By establishing structure, tooling, and automation upfront, it reduces repetitive setup work and helps avoid unnecessary rewrites as projects grow in scope and complexity.
The template provides the essential foundations while leaving application-specific architecture and infrastructure decisions to the project owner.
This gives developers the flexibility to shape their projects around their actual requirements without having to build the underlying development setup from scratch.


## Key Features

- **Modern Packaging**
  - `pyproject.toml` as the centralized configuration for packaging, tooling, and metadata
  - A `src/` layout separates the importable package from repository-level files
  - Setuptools builds wheel and source distributions

- **Layered Configuration Management**
  - `pydantic-settings` validates application settings
  - `APP_ENV` selects the environment-specific TOML and dotenv files.
  - Clear separation of structure (`TOML`) and secrets (`.env`)

- **Production-Grade Logging**
  - Structured logging with `structlog`
  - Colorized developer output
  - JSON logs for production
  - Automatic masking of sensitive top-level log fields based on predefined keywords

- **Testing & Code Quality**
  - Test execution with `pytest` and coverage measurement and enforcement with `pytest-cov`
  - Cloud-based coverage reporting and visualization with `Codecov`
  - Minimum 80% coverage threshold
  - Fast linting and formatting via `ruff`
  - Strict static type checking with `mypy`

- **Security by Default**
  - Local secret detection with `detect-secrets`
  - Repository secret scanning with `TruffleHog` in GitHub Actions
  - Dependency vulnerability scanning with `Snyk Open Source`
  - Static application security testing with `Snyk Code`
  - Static security analysis with `Bandit`

- **Containerization**
  - Multi-stage `Dockerfile` using `uv` for fast builds
  - `APP_ENV` configurable at build time and runtime
  - Minimal `docker-compose.yml` that can be extended with additional services
  - Optional multi-platform publishing to `GitHub Container Registry`

- **Automated CI/CD**
  - Local code quality and security checks with `prek`
  - Workflows with fast dependency resolution using `uv`
  - Automated pull request checks
  - CI verification, image building and packaging
  - Release workflow includes prepared publishing jobs for `TestPyPI`, `GHCR` and `GitHub Releases`
  - Dependency updates with `Dependabot`

- **Governance Management**
  - Issue & PR templates
  - CODEOWNERS
  - Automated label synchronization


## Project Structure Overview
The blueprint provides a clean, scalable starting layout:

```bash
python-project-blueprint/
├── .config/             # Environment-specific TOML and dotenv templates
├── .github/             # Workflows, issue templates, labels and repository automation
├── data/                # Local raw and processed data directories
├── docker/              # Dockerfile and Docker Compose configuration
├── docs/                # Setup, contribution, security and project documentation
├── notebooks/           # Exploratory notebooks
├── res/                 # Optional static resources
├── src/
│   └── package_name/    # Importable Python package
│       ├── core/        # Configuration and logging
│       ├── __init__.py
│       └── main.py
├── tests/               # Pytest suite
├── .dockerignore
├── .gitignore
├── .pre-commit-config.yaml
├── codecov.yml
├── LICENSE.md
└── pyproject.toml
```

The `.log/` directory is created locally when tools or the application write logs, coverage reports or caches. It is ignored by Git.

## Getting Started

### 1. Create Your Repository
Click **[Use this template](https://github.com/new?template_name=python-project-blueprint&template_owner=Pymetheus)** on GitHub and create a new repository.

### 2. Follow the Setup [Checklist](docs/CHECKLIST.md)

The checklist guides you through:
- creating the repository;
- configuring required GitHub secrets and optional publishing settings;
- running the bootstrap workflow;
- installing and running the generated project.

> **Note:** The [example project](https://github.com/Pymetheus/python-project-blueprint-example) shows a repository generated from this template.

### 3. Install & Run

Install the project and its development dependencies using your preferred supported package manager:
```bash
# with pip
pip install -e . --group dev

# with uv
uv sync

# with poetry
poetry install
```

> **Note:** *uv is the recommended package manager. Recent versions of pip and Poetry can also be used with the project's standard packaging metadata and dependency groups.*

Set up local git hooks for formatting, linting, and security checks:
```bash
prek install
```

> **Note:** *Git must be installed, and you must be inside the cloned Git repository.*

Run the application:
```bash
python -m package_name.main
```

At this point, your project is ready for development. You can start building features, adapting the configuration and writing tests.

> **Note:** *By default, the project runs in development mode (`APP_ENV=dev`).*


## Documentation

This repository includes detailed documentation to support both new users and advanced contributors:

### **[Checklist](docs/CHECKLIST.md)**

A step-by-step guide for creating a repository, configuring GitHub and running the bootstrap workflow. This is the recommended starting point.

### **[Instructions](docs/INSTRUCTIONS.md)**

A technical overview of the template's architecture, configuration, logging, tooling, automation and container setup.
Use this when you want to understand *why* things are built the way they are.


## Who This Is For
The blueprint is intended for developers who want a consistent Python project foundation without having to configure packaging, testing, quality tools and basic automation from scratch.

It is a starting point, not a prescribed application architecture. Add the modules, services, integrations and infrastructure that your project actually needs.


## Contributing
Contributions are welcome.

- For questions and general ideas, use [GitHub Discussions](https://github.com/Pymetheus/python-project-blueprint/discussions).
- For bugs or concrete changes, open an [Issue](https://github.com/Pymetheus/python-project-blueprint/issues) or [Pull Request](https://github.com/Pymetheus/python-project-blueprint/pulls).
- See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for contribution guidance.

## License
Licensed under the terms defined in [LICENSE.md](LICENSE.md).
