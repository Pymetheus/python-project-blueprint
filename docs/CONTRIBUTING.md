## How to contribute to [[REPO_NAME]]

Contributions are welcome. Please use the repository's issue and pull-request process so changes can be discussed and reviewed.

#### **Did you find a bug?**

- Search [existing issues](https://github.com/[[USERNAME]]/[[REPO_NAME]]/issues) to see whether it has already been reported.
- If not, [open a new issue](https://github.com/[[USERNAME]]/[[REPO_NAME]]/issues/new) with a clear description and, where possible, steps to reproduce it.

#### **Did you write a patch that fixes a bug?**

- Fork the repository and create a branch for your change.
- Add or update tests that demonstrate the fix.
- Open a pull request with a title using the `fix:` prefix.

#### **Do you intend to add a new feature or change an existing one?**

- Open an issue first if the proposed change needs discussion.
- Create a branch, implement the change and add or update tests.
- Open a pull request using one of the accepted title prefixes.
- The PR workflow validates the title and applies a label based on its prefix.

| Title | Applied label | Description |
|:--|:--|:--|
| `feat:` | `feature` | Adds a new feature or capability |
| `fix:` | `bug` | Fixes a bug or incorrect behavior |
| `docs:` | `documentation` | Documentation-only changes |
| `style:` | `enhancement` | Code style changes without logic changes |
| `refactor:` | `refactor` | Restructures code without changing behavior |
| `perf:` | `enhancement` | Performance improvements |
| `test:` | `enhancement` | Adds or modifies tests |
| `build:` | `enhancement` | Build-system or dependency changes |
| `ci:` | `ci` | CI/CD configuration changes |
| `chore:` | `enhancement` | Maintenance tasks or housekeeping |

Before opening a pull request, run the relevant checks locally:

```bash
uv sync
uv run ruff check src/ tests/
uv run ruff format --check src/ tests/
uv run mypy src/
uv run pytest
```

You can install the configured local hooks with:

```bash
uv run prek install
```

#### **Do you have questions about the source code?**

Open a [GitHub Discussion](https://github.com/[[USERNAME]]/[[REPO_NAME]]/discussions) or contact the maintainers by [email](mailto:[[EMAIL]]).
