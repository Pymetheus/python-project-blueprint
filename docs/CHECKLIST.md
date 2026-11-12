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
- [ ] **USER:** Add `SNYK_TOKEN` as a **repository Actions secret** under **Settings** → **Secrets and variables** → **Actions** & **Dependabot**. (found under https://app.snyk.io/account → **Auth Token**)
- [ ] **USER:** Add `SNYK_ORG_ID` as a **repository Actions secret** under **Settings** → **Secrets and variables** → **Actions** & **Dependabot**. (found under https://app.snyk.io/org/ your-org /manage/settings → **Organization ID**)

> **Note:** *The security workflow runs Snyk Open Source and Snyk Code scans. Findings are reported as workflow annotations and SARIF artifacts; Snyk findings do not currently fail the workflow. If you do not want to use Snyk, remove or replace the `snyk-security-scan` job in `.github/workflows/security.yml`.*

### Codecov
- [ ] **USER:** Create a [Codecov account](https://app.codecov.io/login) if not already present.
- [ ] **USER:** Add `CODECOV_TOKEN` as a **repository Actions secret** under **Settings** → **Secrets and variables** → **Actions** & **Dependabot**. (found under https://app.codecov.io/gh/ your-org / your-repo /new → **Step 3: add token**)
- [ ] **USER:** Install the Codecov App on your GitHub organization and give repository access with `Only select repositories`.

> **Note:** *If you don't want to use Codecov for PR comments and testing visualization, delete the `codecov.yml` file and the `Upload coverage reports to Codecov` step in `.github/workflows/ci.yml` and `.github/workflows/pr-checks.yml`.*

### TestPyPI (Optional)
- [ ] **USER:** Create a [TestPyPI account](https://test.pypi.org/account/register/) if not already present.
- [ ] **USER:** Add a new project under [pending publisher](https://test.pypi.org/manage/account/publishing/)
- [ ] **USER:** Add `testpypi` as a **new environment** to the GitHub repository under **Settings** → **Environments**.
- [ ] **USER:** Update the TestPyPI environment URL at `.github/workflows/cd.yml` with your project URL.

> **Note:** *The CD workflow currently downloads and verifies the distribution artifact after a successful CI run. The publishing jobs, including `publish-test-pypi`, are commented out. Configure the TestPyPI trusted publisher and GitHub environment before enabling that job.*


## 3. Bootstrap your project
- [ ] **USER:** Open `.github/bootstrap-config.yml` and update details.
- [ ] **USER:** Commit directly to the `bootstrap` branch.
- [ ] **USER:** In the repository, go to **Actions** → **Bootstrap Template**, select **Run workflow**→ **Use workflow from branch** → choose `bootstrap` branch, and run the workflow.
- [ ] **USER:** Once the workflow has completed, open a pull request (base: `main` <- compare: `bootstrap`), prefix the title with `ci: bootstrap`, and create the pull request.
- [ ] **USER:** Once all checks have passed, merge the pull request and confirm the merge. You can now delete the `bootstrap` branch.
- [ ] **USER:** Verify that the CI workflow runs successfully on `main` after merging the PR.


## 4. Local Installation
After cloning the new repository to your local development machine and creating a virtual environment (using your preferred tool),
install your project and its development dependencies:

- [ ] **USER:** Install dependencies using **pip**, **uv**, or **poetry**:
  - `pip install -e . --group dev`.
  - `uv sync`.
  - `poetry install`.
- [ ] **USER:** Run `prek install`.
- [ ] **USER:** Run the application `python -m <package_name>.main`.

> **Note:** *Git must be installed, and you must be inside the cloned Git repository.*

The project is now fully initialized and ready for development.
You can start implementing features and adding tests.

> **Note:** *By default, the project runs in development mode (`APP_ENV=dev`).*

## 5. Recommended modifications after bootstrapping
### GitHub Repository Settings
Set branch protections with Repository Rules under **Settings** → **Rules**.
- [ ]  **USER:** Adjust `Bypass list`.
   - [ ]  **USER:** Add `Repository admin` to bypass list with `Exempt` allowance.
   - [ ]  **USER:** Add `Repository admin` to bypass list with `Dependabot` allowance.
- [ ]  **USER:** Tick `Restrict updates`.
- [ ]  **USER:** Tick `Restrict deletions`.
- [ ]  **USER:** Tick `Require a pull request before merging`.
   - [ ]  **USER:** Tick `Require review from Code Owners`.
   - [ ]  **USER:** Tick `Require approval of latest reviewable push`.
   - [ ]  **USER:** Tick `Require conversation resolution before merging`.
- [ ]  **USER:** Tick `Require status checks to pass`.
   - [ ]  **USER:** Tick `Require branches to be up to date before merging`.
- [ ]  **USER:** Tick `Block force pushes`.

Set Actions settings under **Settings** → **Actions** → **General**.
  - [ ]  **USER:** Tick `Allow USER actions and reusable workflows`.
  - [ ]  **USER:** Tick `Require approval for all external contributors`.
  - [ ]  **USER:** Tick Workflow permissions `Read repository contents and packages permissions`.

Set Advanced Security settings under **Settings** → **Advanced Security**.
  - [ ]  **USER:** Enable `Private vulnerability reporting`.
  - [ ]  **USER:** Enable `Dependency graph`.
  - [ ]  **USER:** Enable `Dependabot alerts`.
  - [ ]  **USER:** Enable `Dependabot malware alerts`.
  - [ ]  **USER:** Enable `Dependabot security updates`.
  - [ ]  **USER:** If you want CodeQL scanning, configure GitHub's default CodeQL setup or add a CodeQL workflow; this template does not currently include one.
  - [ ]  **USER:** Enable `Secret Protection`.
  - [ ]  **USER:** Enable `Push protection`.

### Git Flow branching strategy (Optional)
To switch the branching strategy, uncomment the relevant lines in:
- [ ] **USER:** `.github/workflows/pr-checks.yml`.
- [ ] **USER:** `.github/workflows/ci.yml`.
- [ ] **USER:** `.github/workflows/security.yml`.

Otherwise, delete the commented-out lines.

### Configuration Management
- [ ] **USER:** Rename `.config/.env.example` to `.config/.env.dev` and update required secrets.
- [ ] **USER:** Update required application settings in `.config/config.dev.toml`.
- [ ] **USER:** Update values to match your `.env.dev` and `.config/config.dev.toml` settings in `src/<your_package_name>/core/config.py`.

### Project Documents
- [ ] **USER:** Remove `.gitkeep` from `data/`, `notebooks/` or `res/` if you add real contents to those directories.
- [ ] **USER:** Review `docs/DOCUMENTATION.md` and update its links or project-specific documentation references.
- [ ] **USER:** Update License type if applicable.
- [ ] **USER:** Update dependencies & [dependency-groups] in `pyproject.toml` if applicable.
- [ ] **USER:** Update `docs/PROJECT_README.md` before bootstrapping. The bootstrap workflow replaces the template `README.md` with this file.


# Bootstrapping Workflow
The provided bootstrapping workflow (found in `.github/workflows/bootstrap.yml`) automatically configures, rebrands
and initializes your project based on the provided metadata and updated details in `.github/bootstrap-config.yml`.
Finally, the bootstrapping specific documents are deleted, leaving you with a clean repository.

The workflow uses the repository owner/name, repository description and email from `.github/bootstrap-config.yml` to personalize the project. It renames the Python package directory, updates matching placeholders, validates the generated package entry point, and then removes bootstrap-only files.

The workflow automatically updates the following sections:

### Setting up `.config/`
- [x] **BOOTSTRAP:** Update [[REPO_NAME]] in `.config/config.dev.toml`.

### Setting up `.github/`
- [x] **BOOTSTRAP:** Update [[USERNAME]] in `.github/CODEOWNERS` file to reflect ownership of repository creator.
- [x] **BOOTSTRAP:** Update [[USERNAME]] in `.github/dependabot.yml` to reflect reviewers & assignees.

> **Note:** *If ownership, reviewers or assignees are different to the repository creator, this needs to be manually updated.*

### Setting up `docker/`
- [x] **BOOTSTRAP:** Update [[PACKAGE_NAME]] in `docker/docker-compose.yml` & `docker/Dockerfile`.
- [x] **BOOTSTRAP:** Update `DISTRIBUTION-NAME` in `docker/Dockerfile` to reflect correct command.
- [x] **BOOTSTRAP:** Update `blueprint-docker` in `docker/docker-compose.yml` to reflect correct image & container_name.

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
- [x] **BOOTSTRAP:** Replace `README.md` with `docs/PROJECT_README.md` after applying placeholder replacements.

### Deleting bootstrapping specific documents
- [x] **BOOTSTRAP:** Delete `.github/workflows/bootstrap.yml`.
- [x] **BOOTSTRAP:** Delete `.github/bootstrap-config.yml`.
- [x] **BOOTSTRAP:** Delete `.github/scripts/bootstrap.py`.
- [x] **BOOTSTRAP:** Delete `docs/CHECKLIST.md`.
- [x] **BOOTSTRAP:** Delete `docs/INSTRUCTIONS.md`.
