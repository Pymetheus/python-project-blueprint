# Developer Guide & Architecture

This document explains the architecture, configuration, tooling and automation included in the Python Project Blueprint. For the setup sequence, follow the [Checklist](CHECKLIST.md).

The blueprint provides a reusable starting point for Python packages and applications. It includes packaging, settings management, logging, tests, quality tools, security checks, container configuration and GitHub automation. Application-specific architecture and infrastructure are intentionally left to the project owner.

The **Python Project Blueprint** includes:

| Feature | Description                                                                                                                                                             |
|:--|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Project Management** | `pyproject.toml` centralizes package metadata, dependency groups and tool configuration.                                                                                |
| **Configuration** | `pydantic-settings` loads and validates values from environment variables, dotenv and TOML files.                                                                       |
| **Structured Logging** | `structlog` integrates with standard logging and supports human-readable console output, JSON output and optional rotating file logs.                                   |
| **Package Layout** | A `src/` layout separates the importable package from repository-level files.                                                                                           |
| **Testing** | `pytest` and `pytest-cov` run tests and enforce a minimum coverage threshold.                                                                                           |
| **Static Analysis** | `Ruff` provides linting and formatting; `Mypy` performs static type checking.                                                                                           |
| **Security** | `Snyk`, `Bandit` and `TruffleHog` are used in the security workflow; `detect-secrets` is included as a local hook.                                                      |
| **Containerization** | A multi-stage `Docker` build installs runtime dependencies with `uv` and runs the application as a non-root user.                                                       |
| **Governance** | Issue and pull-request templates, CODEOWNERS and label synchronization support repository maintenance.                                                                  |
| **Local Hooks** | `.pre-commit-config.yaml` defines hooks for linting, formatting, and security checks using `prek`.                                                                      |
| **CI/CD** | GitHub Actions validate pull requests, test the project, build distributions and smoke-test the Docker image. Publishing jobs in CD are provided as commented examples. |
| **Bootstrapping** | A one-time GitHub Actions workflow personalizes the template and removes bootstrap-only files.                                                                          |

> **Bootstrapping note:** `bootstrap.yml`, `bootstrap-config.yml`, `bootstrap.py`, `CHECKLIST.md` and this `INSTRUCTIONS.md` file are used to initialize a repository. The bootstrap workflow removes them after initialization. See the [Checklist](CHECKLIST.md) before running the workflow.

## Table of Contents

- [Template Architecture Overview](#template-architecture-overview)
- [Configuration Management](#configuration-management)
- [Logging Management & Artifacts](#logging-management--artifacts)
- [GitHub Actions & Automation](#github-actions--automation)
- [Data & Environment Management](#data--environment-management)
- [Containerization](#containerization)
- [Source Code Management](#source-code-management)
- [Testing Management](#testing-management)
- [Project Management with pyproject.toml](#project-management-with-pyprojecttoml)

---

## Template Architecture Overview

The blueprint separates importable source code from repository-level configuration, data, logs and automation. This keeps the package focused while giving developers clear locations for project assets and tooling.

It can be used as the starting point for either:
- **A package:** the `src/` layout and build configuration support wheel and source-distribution builds.
- **An application:** the settings and logging modules provide reusable startup infrastructure.

```text
python-project-blueprint/
├── .config/
│   ├── .env.example
│   └── config.dev.toml
├── .github/
│   ├── ISSUE_TEMPLATE/
│   ├── scripts/
│   │   └── bootstrap.py
│   ├── workflows/
│   │   ├── bootstrap.yml
│   │   ├── cd.yml
│   │   ├── ci.yml
│   │   ├── label-sync.yml
│   │   ├── pr-checks.yml
│   │   └── security.yml
│   ├── bootstrap-config.yml
│   ├── CODEOWNERS
│   ├── dependabot.yml
│   ├── labels.yml
│   └── PULL_REQUEST_TEMPLATE.md
├── data/
│   ├── processed/
│   └── raw/
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── docs/
│   ├── CHECKLIST.md
│   ├── CODE_OF_CONDUCT.md
│   ├── CONTRIBUTING.md
│   ├── DOCUMENTATION.md
│   ├── INSTRUCTIONS.md
│   ├── PROJECT_README.md
│   └── SECURITY.md
├── notebooks/
├── res/
├── src/
│   └── package_name/
│       ├── core/
│       │   ├── __init__.py
│       │   ├── config.py
│       │   └── logger.py
│       ├── __init__.py
│       └── main.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_config.py
│   ├── test_logger.py
│   └── test_main.py
├── .dockerignore
├── .gitignore
├── .pre-commit-config.yaml
├── codecov.yml
├── LICENSE.md
├── README.md
└── pyproject.toml
```

The `.log/` directory is generated locally by tests, tools or the application. It is ignored by Git and is not a tracked source directory.

### Naming convention

The bootstrap workflow derives the distribution name and Python package name from the new repository name. A lowercase, hyphen-separated repository name is recommended for readability; the workflow normalizes the derived distribution and package names.

| Used for | Style | Example |
|:--|:--|:--|
| Repository name (recommended) | lowercase, hyphen-separated | `my-python-project` |
| Distribution name and console command | lowercase, hyphen-separated | `my-python-project` |
| Python package and Python modules | lowercase snake_case | `my_python_project`, `main.py` |
| Docker image and container names | lowercase, hyphen-separated | `my-python-project:latest` |

The distribution name and import package name are separate concepts. A distribution may use hyphens while its import package uses underscores.

---

## Configuration Management

Configuration is implemented in `src/package_name/core/config.py` using `pydantic-settings`. TOML files hold non-secret application settings, while dotenv files can hold local development secrets.

### Configuration sources and precedence

The configuration loading logic follows this hierarchy, from highest to lowest priority:

1. **Process environment variables** – Variables provided by the operating system, shell, Docker or deployment environment.
2. **The environment-specific dotenv file** – Variables loaded from the corresponding .env file, when available.
3. **The environment-specific TOML file** – Settings loaded from the corresponding TOML configuration file.
4. **Pydantic model defaults** – Default values defined in the settings models.

For example, `DATABASE__HOST` overrides `database.host` from the TOML file. The nested environment variable delimiter is `__`.

### Included files

- **`.config/config.dev.toml`** contains the development defaults for `app_name`, database connection settings and API base URL.
- **`.config/.env.example`** provides example environment variables. It is not loaded automatically; copy it to `.config/.env.dev` for local development.

The dotenv file is ignored by Git. Do not commit real credentials.

### Selecting an environment

`APP_ENV` selects the files to load. It defaults to `dev` and is normalized to lowercase. For example, `APP_ENV=prod` selects:

- `.config/config.prod.toml`
- `.config/.env.prod`

Set `APP_ENV` before the application imports `package_name.core.config`, because the selected environment and configuration paths are determined when that module is imported.

`APP_CONFIG_DIR` overrides the default `.config` directory. Relative paths are resolved from the process's current working directory.

**Linux / macOS:**

```bash
APP_ENV=prod python -m package_name.main
```

**Windows PowerShell:**

```powershell
$env:APP_ENV = "prod"
python -m package_name.main
```

The example project defaults to development settings. Production deployments should normally provide configuration through process environment variables rather than relying on a local dotenv file.

---

## Logging Management & Artifacts

Logging is configured in `src/package_name/core/logger.py` using `structlog` integrated with Python's standard `logging` module.

### Console and file output

`setup_logging()` selects the console renderer through its `pretty_print` argument:

- `pretty_print=True` uses `structlog.dev.ConsoleRenderer` for human-readable console output.
- `pretty_print=False` uses `structlog.processors.JSONRenderer` for JSON output. This is the function's default.

File logging is disabled by default. Set `write_to_disk=True` to create `.log/logs.json`. The file handler rotates at 10 MB and retains three backup files. The console handler remains enabled.

### Logging processors

The configured processor chain includes:

- **Environment context:** adds `_env` using the normalized `APP_ENV` value.
- **Sensitive-field masking:** masks top-level event fields when their key contains one of the configured case-insensitive keywords: `password`, `token`, `secret`, `key` or `auth`.
- **Standard metadata:** adds logger name, log level and an ISO-formatted timestamp, and formats exception information.

Masking is based on event-field names. It is not a general-purpose recursive secret scanner; avoid logging credentials or sensitive payloads in the first place.

### Local artifacts

The `.log/` directory is ignored by Git. Depending on which tools are run and how logging is configured, it can contain:
- `logs.json` and rotated log files;
- `.log/coverage/` with coverage data and HTML/XML reports;
- `.log/mypy_cache/` with Mypy incremental cache data.

---

## GitHub Actions & Automation

The repository uses GitHub Actions for pull-request checks, CI, security scanning, label synchronization and the optional release pipeline. The default branch strategy is GitHub Flow, with `main` as the target branch. Some workflows contain commented branch filters that can be enabled if the project adopts additional branches.

### Project Governance Automation

- **Issue templates:** `.github/ISSUE_TEMPLATE/` provides bug-report and feature-request templates.
- **Pull-request template:** `.github/PULL_REQUEST_TEMPLATE.md` prompts contributors to describe changes and testing.
- **CODEOWNERS:** `.github/CODEOWNERS` assigns repository ownership and review responsibility.
- **Label synchronization:** `label-sync.yml` synchronizes repository labels from `.github/labels.yml` when that file changes on `main`, or when manually dispatched.
- **Dependabot:** `.github/dependabot.yml` checks Python dependencies, GitHub Actions and Docker dependencies weekly.

### CI/CD Workflow Automation

The workflows use `uv` for dependency resolution and installation where configured.

#### Automation Overview

| Workflow or tool | Trigger | Purpose |
|:--|:--|:--|
| `.pre-commit-config.yaml` | Local Git hooks after `prek install` | Runs selected hygiene, linting and security hooks on commits. |
| `pr-checks.yml` | Pull requests targeting `main` | Validates PR metadata, lint, types, tests, coverage and repository hygiene. |
| `ci.yml` | Pushes to `main` and manual dispatch | Runs the full platform/Python test matrix, builds distributions and smoke-tests the package and Docker image. |
| `cd.yml` | Successful completion of CI on `main` | Downloads and verifies the CI distribution artifact. Publishing jobs are currently commented out. |
| `security.yml` | Pull requests to `main`, weekly schedule and manual dispatch | Runs dependency, source-code and secret scans. |
| Dependabot | Weekly schedule | Opens dependency update pull requests. |
| `label-sync.yml` | Changes to `.github/labels.yml` on `main`, or manual dispatch | Synchronizes repository labels. |

#### Prek Workflow

The `.pre-commit-config.yaml` file defines local hooks. Install them from the repository root after installing the development dependencies:

```bash
prek install
```

The configured hooks include:
- **pre-commit-hooks:** trailing whitespace, end-of-file, YAML and TOML checks, large-file checks and executable shebang checks;
- **Ruff:** linting with `--fix` and formatting;
- **detect-secrets:** scans files for potential secrets;
- **Bandit:** checks Python code for common security issues.

These hooks run locally when the installed Git hook is triggered. They do not run automatically until `prek install` has been executed. Mypy and pytest are run by GitHub workflows rather than configured as local hooks.

#### Pull Request Checks Workflow

`pr-checks.yml` targets pull requests to `main`. It uses Python 3.12 and runs the following jobs:

- **PR title validation:** checks titles against the configured Conventional Commit types (`feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`).
- **PR description validation:** requires a description of at least 50 characters.
- **Lint and format:** runs `ruff check` and `ruff format --check` against `src/` and `tests/`.
- **Type checking:** runs Mypy against `src/`.
- **Tests:** runs pytest with coverage and uploads coverage artifacts and a Codecov report.
- **Conflict check:** searches tracked files outside `.github/` for merge-conflict markers.
- **File-size check:** fails if files larger than 10 MB are found.
- **Summary:** fails if a required check failed or was cancelled.
- **PR labeler:** applies a label based on the title prefix. It runs after the summary and is configured not to fail the workflow if labeling itself fails.

The PR title label mapping is:

| Title prefix | Applied label |
|:--|:--|
| `feat:` | `feature` |
| `fix:` | `bug` |
| `docs:` | `documentation` |
| `style:`, `perf:`, `test:`, `build:`, `chore:` | `enhancement` |
| `refactor:` | `refactor` |
| `ci:` | `ci` |

A title may also use a scope, for example `feat(api): add endpoint`.

Coverage reports are uploaded as workflow artifacts and sent to Codecov. Codecov's project target is 80%; patch coverage is informational in `codecov.yml`.

#### CI Workflow

`ci.yml` runs on pushes to `main` and can also be started manually. It:

1. Checks that the version in `pyproject.toml` does not already have a corresponding `v<version>` Git tag.
2. Runs the full test suite on Ubuntu, Windows and macOS with Python 3.12, 3.13 and 3.14.
3. Builds the source distribution and wheel after the test matrix succeeds.
4. Builds the Docker image and runs its default command as a container smoke test.
5. Installs the built wheel in a clean job, verifies that the package can be imported and runs its console-script entry point when one is present.

Coverage artifacts are uploaded from the Ubuntu/Python 3.12 matrix run and that run also uploads coverage to Codecov.

#### CD Workflow

`cd.yml` is triggered by a completed CI workflow run on `main`. The active `download-distribution` job runs only when the triggering CI run succeeded and downloads the distribution artifact produced by that run.

The Docker publishing, TestPyPI publishing and GitHub Release jobs are present as commented-out examples. They do not run in the current configuration. Before enabling them, configure the relevant registry permissions, TestPyPI trusted publisher and GitHub environment, and verify the package/repository-specific values.

#### Security Workflow

`security.yml` runs on:
- pull requests targeting `main`;
- a weekly schedule at 00:00 UTC every Monday;
- manual workflow dispatch.

It contains three scans:

- **Snyk:** runs Snyk Open Source against that dependency set, and runs Snyk Code against the source. SARIF reports are uploaded as workflow artifacts. Findings are surfaced as workflow annotations; the current shell handling does not fail the job for Snyk findings or scanner errors.
- **Bandit:** scans `src/` using the configuration in `pyproject.toml` and uploads a JSON report. Bandit's command exit status is not suppressed, so findings can fail this job.
- **TruffleHog:** scans the pull-request changes for PR events and scans repository history for scheduled or manually dispatched runs.

The workflow requires `SNYK_TOKEN` and `SNYK_ORG_ID` repository Actions secrets for Snyk. Uploading SARIF to GitHub's Security dashboard is commented out and is not currently enabled.

#### Dependabot Workflow

Dependabot is configured to check the following ecosystems weekly:
- **pip:** Python project dependencies in the repository root;
- **github-actions:** GitHub Actions references;
- **docker:** the Dockerfile in `/docker`.

It opens pull requests with configured labels and commit-message prefixes. The Python dependency updates are assigned to the configured repository owner after bootstrap.

---

## Data & Environment Management

This section describes the repository-level directories that support development. Their contents are not automatically part of the installed Python package.

### Storage & Resources

- **`data/`:** contains `raw/` and `processed/` directories. `.gitignore` keeps data files out of version control while retaining the empty directory structure with `.gitkeep` files. `.dockerignore` excludes the directory from Docker build context.
- **`notebooks/`:** a location for exploratory analysis, prototyping and research. It is excluded from Docker build context.
- **`res/`:** an optional location for static repository resources. It is excluded from Docker build context; move or package any runtime assets that the application needs before relying on them in a container.

### Documentation & Governance

- **`docs/`:** contains setup instructions, contribution guidance, security policy, code of conduct and the generated-project README template.
- **`LICENSE.md`:** contains the project's license.
- **`README.md`:** the repository landing page. During bootstrap, it is replaced by `docs/PROJECT_README.md`.
- **`.dockerignore` and `.gitignore`:** exclude local environments, caches, generated artifacts and other files from the Docker build context and Git repository, respectively.

---

## Containerization

The `docker/` directory contains the Dockerfile and a minimal Docker Compose configuration.

### Multi-Stage Docker Build

The Dockerfile has two stages:

- **Builder:** uses the Astral `uv` image to resolve and install the project and its runtime dependencies. Development dependencies are excluded.
- **Runtime:** uses a slim Python image, copies the virtual environment from the builder and runs the configured console command as a non-root user.

### Environment Configuration

The Dockerfile declares:

```dockerfile
ARG APP_ENV=DEV
ENV APP_ENV=$APP_ENV
```

The build argument sets the image's default environment. A container runtime can override `APP_ENV` when starting the container. The application normalizes the value to lowercase when selecting configuration files.

The image sets the virtual environment on `PATH`, enables unbuffered Python output, disables bytecode writes and runs as the `nonroot` user (UID/GID 999). Development dependencies, including `python-dotenv`, are excluded. The `.dockerignore` also excludes dotenv files, so configure containers through runtime environment variables. If you deliberately mount a dotenv file into a container, add `python-dotenv` to the runtime dependencies.

### Docker Compose

`docker/docker-compose.yml` defines a single application service and builds from the repository root using `docker/Dockerfile`. It sets `APP_ENV=DEV`. It is a minimal starting point; it does not provision a database or other supporting services.

### Multi-Architecture Support

The commented-out Docker publishing job in `cd.yml` contains a Buildx configuration for `linux/amd64` and `linux/arm64`. Multi-platform publishing is not active until that job is enabled and configured.

---

## Source Code Management

The `src/` directory contains the importable Python package. The `src/` layout helps ensure tests and tools exercise the installed package rather than accidentally importing a same-named package from the repository root.

### Internal Structure: `src/package_name/`

- **`main.py`:** example application entry point. It configures logging, loads settings and emits startup messages. Replace or extend it with application-specific behavior.
- **`core/config.py`:** defines the Pydantic settings models and environment/TOML loading.
- **`core/logger.py`:** configures `structlog` and standard logging, including environment context and sensitive-field masking.
- **`__init__.py`:** exposes the installed distribution version as `__version__`, falling back to `"unknown"` if package metadata is unavailable.

### Scalability Strategy

The template intentionally starts with a small package. Add modules when the application needs them.

---

## Testing Management

The `tests/` directory contains baseline tests for configuration, logging and the example entry point. The tests are intended to be extended or replaced as application behavior grows.

### Test Suite Structure

- **`conftest.py`:** sets `APP_ENV=dev` for the test process.
- **`test_config.py`:** checks loading the development configuration, environment-variable overrides and validation errors.
- **`test_logger.py`:** checks environment context, sensitive-field masking, console handlers and rotating file logging.
- **`test_main.py`:** checks the module's `__main__` execution path.

### Quality Metrics & Artifacts

Pytest is configured in `pyproject.toml` with `pytest-cov`. Running the test suite generates:
- terminal coverage output;
- an HTML report in `.log/coverage/htmlcov/`;
- an XML report at `.log/coverage/coverage.xml`;
- coverage data in `.log/coverage/.coverage`.

The configured minimum total coverage is **80%**. A test run fails if the threshold is not met. The PR workflow also uploads coverage artifacts and sends the report to Codecov.

### Running Tests Locally

Install the development dependency group, then run:

```bash
uv sync
uv run pytest
```

Alternatively, with a recent pip version that supports dependency groups:

```bash
python -m pip install -e . --group dev
pytest
```

### Coverage Reporting with Codecov

`codecov.yml` configures Codecov's pull-request comment layout and coverage status targets:
- the project coverage target is 80%;
- patch coverage is informational;
- the PR comment displays the diff, flags and files sections.

The PR checks workflow uploads coverage on pull requests. The CI workflow uploads coverage from the Ubuntu/Python 3.12 matrix run. Codecov reporting requires the repository's Codecov integration and `CODECOV_TOKEN` secret.

---

## Project Management with pyproject.toml

`pyproject.toml` is the central configuration file for package metadata, dependencies, build settings and developer tools.

### Core Components

- **Metadata & Distribution:** `[project]` defines the distribution name, version, description, Python requirement, license, authors, dependencies and project URLs.
- **Console command:** `[project.scripts]` maps the distribution command to `package_name.main:main`.
- **Dependencies:** the runtime dependencies are `pydantic`, `pydantic-settings` and `structlog`.
- **Dependency groups:**
  - `test` contains `pytest` and `pytest-cov`;
  - `quality` contains `prek`, Bandit, Ruff and Mypy;
  - `dev` includes the `test` and `quality` groups plus `python-dotenv`.
- **Build backend:** Setuptools discovers packages under `src/` and has namespace-package discovery disabled.

The project requires Python **3.12 or newer**. The CI matrix currently tests Python 3.12, 3.13 and 3.14.

### Tool Orchestration

| Tool | Purpose | Key configuration |
|:--|:--|:--|
| **Ruff** | Linting and formatting | 120-character line length, Python 3.12 target. |
| **Pytest** | Test execution | Discovers tests under `tests/`, adds coverage reporting and verbose output. |
| **Coverage** | Coverage measurement | Branch coverage enabled; minimum total coverage 80%; reports written under `.log/coverage/`. |
| **Mypy** | Static type checking | Strict mode enabled with selected definition/decorator checks relaxed; cache stored in `.log/mypy_cache/`. |
| **Bandit** | Python security analysis | Scans source code; excludes tests and virtual environments and skips B101. |
| **Prek** | Local hooks | Runs file hygiene, Ruff, detect-secrets and Bandit hooks defined in `.pre-commit-config.yaml`. |

### Semantic Versioning & Release

The CI workflow checks whether the version defined in pyproject.toml already exists as a Git tag (v<version>).
If the tag exists, the workflow fails and requires the project version to be changed before proceeding. This helps prevent reusing an existing release version.
The version follows the project's chosen versioning convention. Actual publishing and release creation depend on the corresponding CD jobs being enabled and configured.
