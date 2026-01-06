# Developer Guide & Architecture
This document explains the architectural decisions, automation, and conventions built into the Python Project Blueprint.
For setup steps, follow the [Checklist](CHECKLIST.md).


This template provides a production-ready foundation for Python libraries, internal services, APIs, data pipelines, and small-to-medium backend applications.
It reduces setup and automation overhead, allowing teams to focus on application logic while enforcing industry best practices from the first commit.


The **Python Project Blueprint** comes with built-in:

| Feature                      | Description                                                                                                                                                    |
|:-----------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Project Management**       | `pyproject.toml` as the centralized configuration for packaging, tooling, metadata and dependency management.                                                  |
| **Config Management**        | `pydantic-settings` for type-safe environment variable loading and validation.                                                                                 |
| **Structured Logging**       | `structlog` integration for JSON streams (production) and colored console output (development).                                                                |
| **Professional Layout**      | `src/` directory structure to ensure package integrity and prevent local import conflicts.                                                                     |
| **Comprehensive Testing**    | `pytest` paired with coverage reporting and enforced minimum thresholds for deep visibility into code health.                                                  |
| **Static Analysis**          | `ruff` for linting/formatting and `mypy` for strict static type checking.                                                                                      |
| **Automated Security**       | `Snyk` (OSS) and `bandit` (SAST) integrated to scan for vulnerabilities and leaked secrets.                                                                    |
| **Standardized Governance**  | Automated label synchronization, Issue templates, and Pull Request templates.                                                                                  |
| **Local Automation**         | `.pre-commit-config.yaml` for linting, formatting, and security checks.                                                                                        |
| **CI/CD Pipeline**           | `pr-checks`, `ci`, `cd`, and `security` GitHub Actions workflows.                                                                                              |
| **Instant Bootstrapping**    | A `bootstrap.yml` GitHub Action to rebrand and initialize the repository in seconds.                                                                           |

> **Note on Bootstrapping Process:**
>
> *Some files and workflows (e.g. `bootstrap.yml`, `CHECKLIST.md`, `INSTRUCTIONS.md`) exist only to initialize the repository and are automatically removed after the bootstrap process completes.*
>
> *See the [Checklist](/docs/CHECKLIST.md) for more details*

## Table of Contents
- [Template Architecture Overview](#template-architecture-overview)
- [Configuration Management](#configuration-management)
- [Logging Management](#logging-management--artifacts)
- [Automation & GitHub](#github-actions--automation)
- [Data & Environment Management](#data--environment-management)
- [Source Code](#source-code-management)
- [Testing Management](#testing-management)
- [Project Management with pyproject.toml](#project-management-with-pyprojecttoml)

---

## Template Architecture Overview

The blueprint adopts a **Modular Layered Architecture** designed to scale from a simple script to a complex enterprise application.
By strictly separating source code from environment concerns (configuration, data, logs),
the project ensures that components can be swapped, updated, or scaled independently without side effects.

This structure is optimized for dual-use development:
* **As a Package:** The `src/` layout and `pyproject.toml` ensure your code is ready for distribution on PyPI or internal registries.
* **As an Application:** The type-safe configuration and structured logging provide the robust infrastructure required for stable production deployments and cloud-native environments.

```bash
python-project-blueprint/
├── .config/
│   ├── .env.example                # Template for environment variables
│   └── config.dev.toml             # Development-specific configuration
├── .github/
│   ├── ISSUE_TEMPLATE/             # Standardized bug & feature tracking
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   ├── workflows/                  # Automation (CI/CD, Security, Bootstrap)
│   │   ├── bootstrap.yml           # Deleted after bootstrap process
│   │   ├── cd.yml
│   │   ├── ci.yml
│   │   ├── label-sync.yml
│   │   ├── pr-checks.yml
│   │   └── security.yml
│   ├── bootstrap-config.yml        # Deleted after bootstrap process
│   ├── CODEOWNERS                  # Access control and review authority
│   ├── dependabot.yml              # Automated dependency updates
│   ├── labels.yml                  # Standardized issue/PR labeling
│   └── PULL_REQUEST_TEMPLATE.md    # PR quality checklist
├── .log/                           # Local artifacts (Logs, Coverage, Cache)
│   ├── coverage/
│   │   ├── htmlcov/
│   │   ├── .coverage
│   │   └── coverage.xml
│   ├── mypy_cache/
│   └── logs.json
├── data/                           # Local data storage (Raw/Processed)
│   ├── processed/
│   └── raw/
├── docker/                         # Containerization logic
│   ├── Dockerfile
│   └── docker-compose.yml
├── docs/                           # Project & Governance documentation
│   ├── CHECKLIST.md                # Deleted after bootstrap process
│   ├── CODE_OF_CONDUCT.md
│   ├── CONTRIBUTING.md
│   ├── DOCUMENTATION.md
│   ├── INSTRUCTIONS.md             # Deleted after bootstrap process
│   └── SECURITY.md
├── notebooks/                      # Exploratory research & prototyping
├── res/                            # Static resources (images, etc.)
├── src/
│   └── package_name                # Core logic
│       ├── utils/                  # Shared utilities
│       │   ├── __init__.py
│       │   ├── config.py
│       │   └── logger.py
│       ├── __init__.py
│       └── main.py
├── tests/                          # Test suite (Pytest)
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_config.py
│   ├── test_logger.py
│   └── test_main.py
├── .dockerignore                   # Docker build exclusions
├── .gitignore                      # Git exclusions
├── .pre-commit-config.yaml         # Local linting/security gates
├── LICENSE.md                      # Usage permissions
├── pyproject.toml                  # Central configuration hub (Dependencies & Tools)
└── README.md                       # Project landing page
```

### Naming convention
To ensure consistency across the stack and avoid import conflicts between local folders and installed packages,
strict naming conventions are enforced.

| Used for                            | Style      | Example                            |
|-------------------------------------|------------|------------------------------------|
| GitHub repo, PyPI name, CLI command | kebab-case | `python-project-blueprint`         |
| Python package, Python files        | snake_case | `package_name`, `template_code.py` |
| Docker image                        | kebab-case | `template-app:latest`              |

---

## Configuration Management
This directory orchestrates the application's configuration using a **Layered Configuration Strategy**.
This ensures a clean separation between structural application settings (TOML) and sensitive credentials (.env).

The configuration loading logic (found in `src/package_name/utils/config.py`) follows this hierarchy, where lower layers override upper ones:

1.  **Pydantic Defaults:** Defined in the code (failsafe values).
2.  **`config.{APP_ENV}.toml`:** Structural configuration (ports, hosts, feature flags). **Committed to Git.**
3.  **`.env.{APP_ENV}`:** Secrets and credentials (API Keys, DB Passwords). **Ignored by Git.**
4.  **System Environment Variables:** OS-level overrides (highest priority, ideal for Docker/Kubernetes).

### Included Files
- **`config.dev.toml`**: The default configuration for local development.
- **`.env.example`**: A template listing placeholder secrets.

> **Note:** *Copy `.env.example` to create your local `.env.dev` (or `.env.{APP_ENV}` for other environments).*

### Switching Environments
The application defaults to `dev` mode.
To run in `prod` mode, you simply set the `APP_ENV` environment variable.
The system will then automatically look for `config.prod.toml` and `.env.prod`.

**Example: Running in Production Mode**
```bash
# Linux / macOS
APP_ENV=prod
pip install -e .
python -m package_name.main

# Windows (PowerShell)
$env:APP_ENV = "prod"
pip install -e .
python -m package_name.main
```

---

## Logging Management & Artifacts
A dedicated workspace for local artifacts and build metadata.
This directory is strictly ignored by Git to prevent accidental leakage of logs, local paths, or coverage reports.

- **`logs.json`**: When `write_to_disk=True` is enabled in your configuration, `structlog` streams machine-readable JSON logs here.
- **`coverage/`**: Contains HTML and XML reports generated by `pytest-cov`, allowing you to visualize untested code paths in your browser.
- **`mypy_cache/`**: Stores incremental type-checking data to significantly speed up subsequent `mypy` runs by only analyzing changed files.

### Advanced Logging Features
The logger (configured in `src/package_name/utils/logger.py`) includes several production-grade processors:

* **Security Masking:** An automated `mask_sensitive_data` processor scans log events for keys like `password` and replaces them with `********` to prevent credential leakage.
* **Environment Context:** Every log entry is automatically tagged with the current `APP_ENV` via a dedicated processor, making it easy to filter logs.
* **Dual Rendering:**
    * **Development:** Uses `ConsoleRenderer` for colorized, human-readable output.
    * **Production:** Uses `JSONRenderer` for machine-readable logs, structured for easy parsing by log aggregators.

---

## GitHub Actions & Automation
This project leverages GitHub Actions and pre-commit hooks to automate the entire development lifecycle, ensuring that high standards are maintained by default.
It houses the governance documents (templates) and the CI/CD pipelines (workflows) that enforce code quality, security, and release standards automatically.
By using these tools, the project ensures that every contribution is vetted before it touches the `main` branch.

### Project Governance Automation
To scale collaboration and maintain a clean repository, the following tools are integrated:

* **Standardized Entry Points:** `ISSUE_TEMPLATE/` and `PULL_REQUEST_TEMPLATE.md` ensure that every **bug report** or **feature request** contains the necessary technical context (logs, environment info, reproduction steps).
* **Automated Labeling (`label-sync.yml`):** Automatically synchronizes repository labels based on a central `labels.yml` file, keeping the project organized and searchable.
* **Access Control (`CODEOWNERS`):** Defines which team members are responsible for specific parts of the codebase, automatically assigning them as reviewers for relevant Pull Requests.

---

### CI/CD Workflow Automation
The repository includes a suite of production-grade automation workflows and services.
These are optimized for **GitHub Flow** (feature branches merging into `main`), ensuring a fast and stable release cycle.
Where applicable, CI/CD workflows use `uv` for dependency installation and resolution to significantly reduce runtime and GitHub Actions minutes.


> **Note on Branching Strategy:**
>
> *While optimized for GitHub Flow, the workflows are flexible.*
>
> *To enable a **Git Flow** strategy (using `develop` and `release` branches), refer to the specific uncommenting instructions in the `docs/CHECKLIST.md`.*

#### Automation Overview
| Workflow                     | Trigger                        | Purpose                                                         |
|------------------------------|--------------------------------|-----------------------------------------------------------------|
| 1) `.pre-commit-config.yaml` | On every commit                | **Local Guard.** First line of defense.                         |
| 2) `pr-checks.yml`           | Pull Requests to main          | **Gatekeeping.** Blocks broken or messy code from being merged. |
| 3) `ci.yml`                  | Push to main & manual          | **Verification.** Proves the package is ready for distribution. |
| 4) `cd.yml`                  | On completed `CI` workflow run | **Automation.** Handles the releasing (TestPyPI/Releases).      |
| 5) `security.yml`            | Pull Requests to main & manual | **Protection.** Scans for vulnerabilities and leaked secrets.   |
| 6) Dependabot                | Scheduled                      | **Maintenance.** Automated dependency updates.                  |

---

#### Pre-commit Workflow
The first line of defense for code quality.
By running checks locally before every commit, we eliminate "fix style" commits and ensure a clean history.

> **Purpose:** First line of defense.
>
> **When:** On every commit.
>
> **Focus:** Catch formatting, linting and security issues before any commit.

**Integrated Hooks:**
- **`pre-commit-hooks`**: General workspace hygiene (removes trailing whitespace, fixes end-of-file, checks YAML/TOML syntax).
- **`ruff`**: An extremely fast Python linter and formatter.
- **`bandit`**: Scans for common security issues in Python code.
- **`detect-secrets`**: Prevents accidental commits of API keys or passwords.

---

#### Pull Request Checks Workflow
The automated gatekeeper for the `main` branch.
This workflow ensures that every contribution meets the project's quality, stability, and documentation standards before it is merged.

> **Purpose:** Fast feedback, standardized history, and automated categorization.
>
> **When:** On Pull Requests to `main` branch.
>
> **Focus:** Static analysis (linting/types), unit testing, and metadata validation.

````yaml
name: PR Checks

on:
  pull_request:
    branches:
      - main
    types:
      - opened
      - synchronize
      - reopened
      - edited
      - ready_for_review

jobs:
  pr-title-check:       # Ensures history is semantic and searchable.
  pr-description-check: # Guarantees context for every code change.
  lint:                 # Enforces style via Ruff
  mypy:                 # Verifies type safety
  test:                 # Executes unit tests and generates coverage artifacts.
  conflict-check:       # Detects merge conflicts early.
  size-check:           # Warns if large files are being detected.
  pr-checks-summary:    # Provides a summary of the previous jobs.
  pr-labeler:           # Automates project board organization.
````

> **Note:** *Detailed test coverage artifacts are available under the Actions > Artifacts tab for every successful run.*


**PR Guidelines:** This project uses [Conventional Commits](https://www.conventionalcommits.org/) for PR titles.

**PR Title Format:** `<type>: <description>`

**PR Title Types:** Standardized titles are enforced for searchability and labeling.

**PR Title Examples:**
- ✅ `feat: add user login`
- ❌ `Updated code` (missing type)

**PR Types & Labeling:**

The repository automatically assigns labels to pull requests based on their title.
The Labeler runs after `pr-checks-summary` and errors in `pr-labeler` will not fail the `pr-checks` workflow.

| Title       | Applied Label   | Description                                  |
|-------------| --------------- | -------------------------------------------- |
| `feat:`     | `feature`       | Adds a new feature or capability             |
| `fix:`      | `bug`           | Fixes a bug or incorrect behavior            |
| `docs:`     | `documentation` | Documentation-only changes                   |
| `style:`    | `enhancement`   | Code style changes (no logic changes)        |
| `refactor:` | `refactor`      | Code restructuring without functional change |
| `perf:`     | `enhancement`   | Performance improvements                     |
| `test:`     | `enhancement`   | Adding or modifying tests                    |
| `build:`    | `enhancement`   | Build system or dependency changes           |
| `ci:`       | `ci`            | CI/CD configuration changes                  |
| `chore:`    | `chore`         | Maintenance tasks or housekeeping            |

---

#### CI Workflow
This workflow serves as the final verification engine for the codebase.
The CI process performs a deep validation to ensure that the integrated code is correctly versioned, stable, and ready for distribution.

> **Purpose:** Final verification and build preparation.
>
> **When:** Pushes to main
>
> **Focus:** Extensive testing, distribution builds, and smoke testing

````yaml
name: CI

on:
  push:
    branches:
      - main
  workflow_dispatch: {}

jobs:
  verify-version:      # Preventing deployment collisions.
  test:                # Executes the complete test suite with coverage.
  build-distribution:  # Packages the code into a distributable format.
  smoke-test:          # Proves the package is installable and functional.
````

> **Note:** *Detailed test coverage artifacts are available under the Actions > Artifacts tab for every successful run.*

---

#### CD Workflow
This workflow automates the final stage of the software lifecycle: **Delivery**.
By triggering only after a completed CI run, it ensures that only fully vetted and smoke-tested code is ever published to the ecosystem.

> **Purpose:** Production deployments
>
> **When:** On completed `CI` workflow run
>
> **Focus:** Publish package and create release

````yaml
name: CD

on:
  workflow_run:
    workflows: [ "CI" ]
    types:
    - completed
  workflow_dispatch: {}

jobs:
  download-distribution:  # Retrieves the verified artifacts from the CI pipeline.
  publish-test-pypi:      # Distributes the package to a test registry for validation.
  github-release:         # Formalizes the version with a GitHub Release and changelog.
````
> **Note:** *Deployments in `cd.yml` are commented out. Uncomment them once you are ready to deploy.*

---

#### Security Workflow
This workflow acts as an automated security audit, scanning your codebase and dependencies for vulnerabilities before any code is merged.
It ensures the project remains compliant with basic security standards.

> **Purpose:** Security audits & vulnerability scanning
>
> **When:** On PRs
>
> **Focus:** Dependencies, code security, SAST

````yaml
name: Security Scan

on:
  pull_request:
    branches:
      - main
  workflow_dispatch: {}

jobs:
  snyk-security-scan:     # Evaluates third-party library code security
  bandit-sast:            # Deep-scans internal code for security flaws.
  secrets-scan:           # Ensures no credentials or keys are leaked.
````
> **Note:** *Requires `SNYK_TOKEN` to be set in GitHub Actions Secrets.*

> **Note:** *Detailed security audit reports from Snyk and Bandit are preserved as HTML artifacts in the Actions > Artifacts tab.*

---

#### Dependabot Workflow
This configuration automates dependency management by proactively checking for updates and security patches across your entire stack.
When a new version is released, Dependabot opens a Pull Request to keep the project current and secure.

> **Purpose:** Keep the project current and secure
>
> **When:** Scheduled
>
> **Focus:** Dependency management

**Supports:**
- **pip** (Python)
- **github-actions**
- **docker**

---

## Data & Environment Management

This layer handles the physical assets, environment virtualization, and project documentation that support the core source code.
By isolating these from the `src/` directory, the project remains clean, portable, and secure.

### Storage & Resources
* **`data/`**: Structured into `raw/` and `processed/`. This directory is for local data persistence. It is strictly ignored by Git to ensure that large datasets or sensitive user information are never committed to version control.
* **`notebooks/`**: A dedicated space for exploratory data analysis (EDA), prototyping, and research. Keeping these separate from the source code ensures that "scratchpad" code and heavy output cells do not clutter production logic.
* **`res/`**: Short for "Resources." This folder houses static assets required by the repository, for example images.

### Containerization & Environment
* **`docker/`**: Contains the `Dockerfile` and `docker-compose.yml`. Storing these in a dedicated subdirectory rather than the root keeps the workspace organized and allows for multiple environment configurations (e.g., development vs. production) to coexist easily.
* **`.dockerignore` & `.gitignore`**: These files are precision-tuned to ensure only essential source files enter the build context or the repository. They explicitly exclude local artifacts like `.log/`, `data/`, and `__pycache__`.

### Documentation & Governance
* **`docs/`**: The central hub for project knowledge. While the `README.md` serves as the landing page, `docs/` houses deep-dives like `CONTRIBUTING.md`, `SECURITY.md`, and technical specifications.
* **`LICENSE.md`**: Defines the legal framework and usage permissions for the code.
* **`README.md`**: The "Front Desk" of the project—focused on high-level overviews, quick-start instructions, and architectural summaries.

---

## Source Code Management

The `src/` directory houses the actual source code of the project.
By using the **src-layout**, we ensure that the code is only importable when properly installed, preventing common packaging bugs and ensuring a clean separation between the project root and the application logic.

### Internal Structure: `src/package_name/`
The internal structure follows a modular design to keep the source code of your application organized:

* **`main.py`**: The central entry point for the application. It orchestrates the startup, including configuration loading and logger initialization.
* **`utils/`**: A dedicated subdirectory for utilities:
    * **`config.py`**: Contains the Pydantic-based configuration logic that implements the layered loading strategy.
    * **`logger.py`**: Defines the `structlog` integrated with the standard `logging` module, including security masking.

### Scalability Strategy
As the project grows from a simple script to an enterprise-grade application, you can expand this directory by adding:
- **`api/`**: For FastAPI/Flask routes and schemas.
- **`services/`**: For business logic and external integrations.
- **`models/`**: For database entities and data structures.

---

## Testing Management

The `tests/` directory is structured to provide high coverage with minimal friction, utilizing `pytest` as the primary engine for both unit and integration testing.

### Test Suite Structure
* **`conftest.py`**: The central hub for shared `pytest` fixtures. This allows you to define reusable components that are automatically available to all test files.
* **`test_main.py`**, **`test_config.py` & `test_logger.py`**: Baseline tests that ensure the source code is functioning correctly.

### Quality Metrics & Artifacts
The testing workflow is integrated with the `.log/` directory to provide deep insights into code health:

* **Automated Coverage**: Every test run generates a `.coverage` report, allowing you to see exactly which lines of code are untested.
* **Coverage Threshold**: The project enforces a **minimum coverage of 80%**. If code coverage falls below this mark, the `pr-checks` workflow will fail, preventing merges that reduce test quality.

### Running Tests
Pytest is configured via `pyproject.toml` to include coverage reporting and verbose output by default.


Just run:
```bash
pytest
```

---

## Project Management with pyproject.toml

The `pyproject.toml` file is the central coordination point of the blueprint. It centralizes all configuration into a single, standardized location.

### Core Components

* **Metadata & Distribution:** Defines the package name, versioning, and authors. It explicitly maps the CLI command to the `main()` function in your source code, enabling instant installation.
* **Dependency Management:**
  * **Production:** Strictly minimal, focusing on robust core libraries like `pydantic-settings` and `structlog`.
  * **Development (`dev`):** Includes a complete suite for testing (`pytest`), formatting (`ruff`), type-checking (`mypy`), and security auditing (`bandit`).
* **Source Layout:** Uses `tool.setuptools.packages.find` to explicitly point to the `src/` directory, enforcing the clean package structure discussed in the Architecture section.

### Tool Orchestration

The blueprint configures each tool to respect the project's layered architecture:

| Tool         | Focus            | Key Configuration                                                                          |
|:-------------|:-----------------|:-------------------------------------------------------------------------------------------|
| **Ruff**     | Speed & Linting  | Configured with a 120-character line length and auto-fix capabilities.                     |
| **Pytest**   | Verification     | Integrated with `coverage` to enforce a minimum **80% coverage threshold**.                |
| **Mypy**     | Type Safety      | Configured for `strict = true` with cached data redirected to `.log/mypy_cache`.           |
| **Bandit**   | Security         | Scans source code for vulnerabilities while ignoring test files to reduce false positives. |
| **Coverage** | Quality Metrics  | Redirects all output artifacts (HTML, XML, .coverage) to the `.log/` directory.            |

### Semantic Versioning & Release
The `version` field in this file is the authoritative reference.
The **CI Workflow** uses this to verify that versions are bumped before a release, ensuring that the distribution published to PyPI or GitHub is always unique and traceable.
