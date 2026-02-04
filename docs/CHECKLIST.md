# Checklist for using the Python Project Blueprint
Follow this checklist to set up your own Python project with the Python Project Blueprint.

**Legend**
- **USER:** Manual action performed by the developer.
- **BOOTSTRAP:** Automatically handled by the bootstrap workflow.


## 1. [Use this template](https://github.com/new?template_name=python-project-blueprint&template_owner=Pymetheus)
- [ ] **USER:** Click `Use this template` and `Create a new repository`.
- [ ] **USER:** Update `Repository name`, `Description`, and choose visibility.
- [ ] **USER:** From `main`, create a new branch named `bootstrap` for one-time initialization.

> **Note:** *The bootstrapping process uses the repository metadata, such as GitHub username, repository name,
> and description, to configure and rebrand your project.
> The `bootstrap` branch is used only for initializing and configuring the project, it will be deleted after bootstrapping.
> See [Bootstrapping Workflow](#bootstrapping-workflow) for details.*


## 2. GitHub Repository Secrets & Environments
### Snyk Account
- [ ] **USER:** Create a [Snyk account](https://app.snyk.io/login) if not already present.
- [ ] **USER:** Add `SNYK_TOKEN` as a **new repository secret** under **Settings** → **Secrets and variables** → **Actions** & **Dependabot**. (found under https://app.snyk.io/account → **Auth Token**)
- [ ] **USER:** Add `SNYK_ORG_ID` as a **new repository secret** under **Settings** → **Secrets and variables** → **Actions** & **Dependabot**. (found under https://app.snyk.io/org/ your-org /manage/settings → **Organization ID**)

> **Note:** *If you don't want to use Snyk for security scanning, delete or replace the `snyk-security-scan` job in `.github/workflows/security.yml`.*

### Codecov
- [ ] **USER:** Create a [Codecov account](https://app.codecov.io/login) if not already present.
- [ ] **USER:** Add `CODECOV_TOKEN` as a **new repository secret** under **Settings** → **Secrets and variables** → **Actions** & **Dependabot**. (found under https://app.codecov.io/gh/ your-org / your-repo /new → **Step 3: add token**)
- [ ] **USER:** Install the Codecov App on your GitHub organization and give repository access with `Only select repositories`.

> **Note:** *If you don't want to use Codecov for PR comments and testing visualization, delete the `codecov.yml` file and the `Upload coverage reports to Codecov` step in `.github/workflows/ci.yml` and `.github/workflows/pr-checks.yml`.*

### TestPyPI (Optional)
- [ ] **USER:** Create a [TestPyPI account](https://test.pypi.org/account/register/) if not already present.
- [ ] **USER:** Add a new project under [pending publisher](https://test.pypi.org/manage/account/publishing/)
- [ ] **USER:** Add `testpypi` as a **new environment** to the GitHub repository under **Settings** → **Environments**.
- [ ] **USER:** Update the TestPyPI environment URL at `.github/workflows/cd.yml` with your project URL.

> **Note:** *Deployments in `cd.yml` are commented out by default. Uncomment them once you are ready to deploy.*
> *As a result, **TestPyPI** setup can also be completed later. Delete or replace the `publish_test_pypi` job if not needed.*


## 3. Bootstrap your project
- [ ] **USER:** Open `.github/bootstrap-config.yml` and update details.
- [ ] **USER:** Commit directly to the `bootstrap` branch.
- [ ] **USER:** In the repository, go to **Actions** → **Bootstrap Template**, select **Run workflow**→ **Use workflow from branch** → choose `bootstrap` branch, and run the workflow.
- [ ] **USER:** Once the workflow has completed, open a pull request (base: `main` <- compare: `bootstrap`), prefix the title with `ci: bootstrap`, and create the pull request.
- [ ] **USER:** Once all checks have passed, merge the pull request and confirm the merge. You can now delete the `bootstrap` branch.
- [ ] **USER:** Verify that the CI workflow runs successfully on `main` after merging the PR.


## 4. Local Installation
After cloning the new repository to your local development machine and creating a virtual environment (using your preferred tool),
install your project using the package manager of your choice:

- [ ] **USER:** Install dependencies using **pip**, **uv**, or **poetry**:
  - `pip install -e ".[dev]"`.
  - `uv sync --extra dev`.
  - `poetry install --extras dev`.
- [ ] **USER:** Run `prek install`.
- [ ] **USER:** Run the application `python -m <package_name>.main`.

> **Note:** *Git must be installed, and you must be inside the cloned Git repository.*

The project is now fully initialized and ready for development.
You can start implementing features and adding tests.

> **Note:** *By default, the project runs in development mode (`APP_ENV=dev`).*

## 5. Recommended modifications after bootstrapping
### Git Flow branching strategy (Optional)
To switch the branching strategy, uncomment the relevant lines in:
- [ ] **USER:** `.github/workflows/pr-checks.yml`.
- [ ] **USER:** `.github/workflows/ci.yml`.
- [ ] **USER:** `.github/workflows/security.yml`.

Otherwise, delete the commented-out lines.

### Configuration Management
- [ ] **USER:** Rename `.config/.env.example` to `.config/.env.dev` and update required secrets.
- [ ] **USER:** Update required application settings in `.config/config.dev.toml`.
- [ ] **USER:** Update values to match your `.env.dev` and `.config/config.dev.toml` settings in `src/<your_package_name>/utils/config.py`.

### Project Documents
- [ ] **USER:** Delete `.gitkeep` in `data/`, `notebooks/` and `res/` if applicable, empty directories will disappear from GitHub.
- [ ] **USER:** Update text in `docs/DOCUMENTATION.md` if applicable.
- [ ] **USER:** Update License type if applicable.
- [ ] **USER:** Update dependencies & [project.optional-dependencies] in `pyproject.toml` if applicable.
- [ ] **USER:** Update text in `README.md`.


# Bootstrapping Workflow
The provided bootstrapping workflow (found in `.github/workflows/bootstrap.yml`) automatically configures, rebrands
and initializes your project based on the provided metadata and updated details in `.github/bootstrap-config.yml`.
Finally, the bootstrapping specific documents are deleted, leaving you with a clean repository.

The workflow automatically updates the following sections:

### Setting up `.config/`
- [x] **BOOTSTRAP:** Update [[REPO_NAME]] in `.config/config.dev.toml`.

### Setting up `.github/`
- [x] **BOOTSTRAP:** Update [[USERNAME]] in `.github/CODEOWNERS` file to reflect ownership of repository creator.
- [x] **BOOTSTRAP:** Update [[USERNAME]] in `.github/dependabot.yml` to reflect reviewers & assignees.

> **Note:** *If ownership, reviewers or assignees are different to the repository creator, this needs to be manually updated.*

### Setting up `docker/`
- [x] **BOOTSTRAP:** Update [[PACKAGE_NAME]] in `docker/docker-compose.yml` & `docker/Dockerfile`.

### Setting up `docs/`
- [x] **BOOTSTRAP:** Update [[EMAIL]] in `docs/CODE_OF_CONDUCT.md` to reflect correct contact.
- [x] **BOOTSTRAP:** Update [[REPO_NAME]] in `docs/CONTRIBUTING.md` to reflect correct repository name.
- [x] **BOOTSTRAP:** Update [[USERNAME]] in `docs/CONTRIBUTING.md` to reflect correct username.
- [x] **BOOTSTRAP:** Update [[EMAIL]] in `docs/CONTRIBUTING.md` to reflect correct contact.
- [x] **BOOTSTRAP:** Update [[REPO_NAME]] in `docs/SECURITY.md` to reflect correct repository name.
- [x] **BOOTSTRAP:** Update [[EMAIL]] in `docs/SECURITY.md` to reflect correct contact.

### Setting up `src/`
- [x] **BOOTSTRAP:** Update `src/package_name` directory.
- [x] **BOOTSTRAP:** Update `package_name` in `src/package_name/__init__.py`.
- [x] **BOOTSTRAP:** Update `package_name` imports in `src/package_name/main.py`.

### Setting up `tests/`
- [x] **BOOTSTRAP:** Update `package_name` in `tests/test_config.py`.
- [x] **BOOTSTRAP:** Update `package_name` in `tests/test_logger.py`.
- [x] **BOOTSTRAP:** Update `package_name` in `tests/test_main.py`.

### Setting up `LICENSE.md`
- [x] **BOOTSTRAP:** Update [[YEAR]] in `LICENSE.md`.
- [x] **BOOTSTRAP:** Update [[USERNAME]] in `LICENSE.md`.

### Setting up `pyproject.toml`
- [x] **BOOTSTRAP:** Update [project] metadata.
- [x] **BOOTSTRAP:** Update [project.urls].
- [x] **BOOTSTRAP:** Update [project.scripts].
- [x] **BOOTSTRAP:** Update known-first-party in [tool.ruff.lint.isort] for import sorting.
- [x] **BOOTSTRAP:** Update files in [tool.mypy].

### Setting up `README.md`
- [x] **BOOTSTRAP:** Update [[REPO_NAME]] in `README.md`.

### Deleting bootstrapping specific documents
- [x] **BOOTSTRAP:** Delete `.github/workflows/bootstrap.yml`.
- [x] **BOOTSTRAP:** Delete `.github/bootstrap-config.yml`.
- [x] **BOOTSTRAP:** Delete `docs/CHECKLIST.md`.
- [x] **BOOTSTRAP:** Delete `docs/INSTRUCTIONS.md`.
- [x] **BOOTSTRAP:** Replace `README.md` with `docs/PROJECT_README.md`.
