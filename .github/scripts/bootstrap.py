"""Bootstrap the Python Project Blueprint into a standalone project."""

import argparse
import ast
import json
import keyword
import os
import re
import sys
import tomllib
from datetime import UTC, datetime
from pathlib import Path

BOOTSTRAP_WORKFLOW = Path(".github/workflows/bootstrap.yml")
BOOTSTRAP_CONFIG = Path(".github/bootstrap-config.yml")
BOOTSTRAP_SCRIPT = Path(".github/scripts/bootstrap.py")
BOOTSTRAP_ONLY_PATHS = (
    BOOTSTRAP_WORKFLOW,
    BOOTSTRAP_CONFIG,
    BOOTSTRAP_SCRIPT,
    Path("docs/CHECKLIST.md"),
    Path("docs/INSTRUCTIONS.md"),
)

IGNORED_DIRECTORIES = (".git",)

PLACEHOLDER = re.compile(r"\[\[[A-Z_]+]]|DISTRIBUTION-NAME|package_name|blueprint-docker|AUTHOR@EXAMPLE\.COM")


class BootstrapError(Exception):
    """Raised when the template cannot be transformed safely."""


def log(message):
    print(f"[bootstrap] {message}", flush=True)


def repository_root(explicit_root=None):
    if explicit_root:
        root = Path(explicit_root).expanduser().resolve()
    elif Path(__file__).resolve().parent.name == "scripts":
        root = Path(__file__).resolve().parents[2]
    else:
        root = Path.cwd().resolve()

    if not (root / "pyproject.toml").is_file():
        raise BootstrapError(f"Repository root does not contain pyproject.toml: {root}")
    return root


def get_env(variable):
    value = os.environ.get(variable, "").strip()
    if not value:
        raise BootstrapError(f"{variable} is required.")
    return value


def load_metadata():
    slug = get_env("GITHUB_REPOSITORY")
    if slug.count("/") != 1:
        raise BootstrapError("GITHUB_REPOSITORY must use the form 'owner/repository'.")

    owner, repository = slug.split("/", 1)
    if not owner or not repository:
        raise BootstrapError("GITHUB_REPOSITORY must use the form 'owner/repository'.")

    description = get_env("BOOTSTRAP_DESCRIPTION")

    email = get_env("BOOTSTRAP_EMAIL")
    if not re.fullmatch(r"[^@\s<>]+@[^@\s<>]+\.[^@\s<>]+", email):
        raise BootstrapError(f"Invalid author email address: {email!r}.")

    year = str(datetime.now(UTC).year)

    package = re.sub(r"[^A-Za-z0-9]+", "_", repository).strip("_").lower()

    if not package.isidentifier() or keyword.iskeyword(package):
        raise BootstrapError(f"Repository name {repository!r} produces an invalid Python package name {package!r}.")

    distribution = re.sub(r"[^A-Za-z0-9]+", "-", repository).strip("-").lower()

    return {
        "owner": owner,
        "repository": repository,
        "description": description,
        "email": email,
        "year": year,
        "package": package,
        "distribution": distribution,
    }


def iter_text_files(root):
    for path in root.rglob("*"):
        relative = path.relative_to(root)

        if not path.is_file() or path.is_symlink():
            continue
        if relative in BOOTSTRAP_ONLY_PATHS:
            continue
        if any(part in IGNORED_DIRECTORIES for part in relative.parts):
            continue

        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        except OSError as exc:
            raise BootstrapError(f"Could not read {relative}: {exc}") from exc

        if "\0" not in content:
            yield path


def replace_text(path, metadata):
    original = path.read_text(encoding="utf-8")

    replacements = {
        "[[REPO_NAME]]": metadata["repository"],
        "[[DESCRIPTION]]": json.dumps(metadata["description"], ensure_ascii=False)[1:-1],
        "[[PACKAGE_NAME]]": metadata["package"],
        "[[USERNAME]]": metadata["owner"],
        "[[EMAIL]]": metadata["email"],
        "[[YEAR]]": metadata["year"],
        "DISTRIBUTION-NAME": metadata["distribution"],
        "AUTHOR@EXAMPLE.COM": metadata["email"],
        "package_name": metadata["package"],
        "blueprint-docker": metadata["distribution"],
    }

    updated = PLACEHOLDER.sub(lambda match: replacements.get(match.group(), match.group()), original)

    if updated != original:
        path.write_text(updated, encoding="utf-8", newline="")
        return True

    return False


def validate_project(root, final=False):
    try:
        with (root / "pyproject.toml").open("rb") as file:
            config = tomllib.load(file)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise BootstrapError(f"Invalid pyproject.toml: {exc}") from exc

    project = config.get("project", {})
    if not isinstance(project, dict):
        raise BootstrapError("pyproject.toml must contain a valid [project] table.")

    scripts = project.get("scripts", {})
    project_name = project.get("name")
    if not isinstance(scripts, dict) or not isinstance(project_name, str):
        raise BootstrapError("pyproject.toml must define project.name and project.scripts.")

    project_script = scripts.get(project_name)
    if not isinstance(project_script, str) or ":" not in project_script:
        raise BootstrapError(f"Missing console script for {project_name!r}.")

    module, function = project_script.split(":", 1)
    package_name = module.split(".", 1)[0]
    main_file = root / "src" / package_name / "main.py"

    if module != f"{package_name}.main" or not function:
        raise BootstrapError(f"Invalid console script target: {project_script!r}.")

    if not main_file.is_file() or not (root / "tests").is_dir() or not (root / "README.md").is_file():
        raise BootstrapError("Generated project is missing main.py, tests/, or README.md.")

    try:
        tree = ast.parse(main_file.read_text(encoding="utf-8"), filename=str(main_file))
    except (OSError, SyntaxError, UnicodeDecodeError) as exc:
        raise BootstrapError(f"Invalid entry-point file {main_file}: {exc}") from exc

    if not any(
        isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == function for node in tree.body
    ):
        raise BootstrapError(f"Console script function {project_script!r} does not exist.")

    for path in iter_text_files(root):
        relative = path.relative_to(root)

        if path.suffix == ".py" and path != main_file:
            try:
                ast.parse(path.read_text(encoding="utf-8"), filename=str(relative))
            except (OSError, SyntaxError, UnicodeDecodeError) as exc:
                raise BootstrapError(f"Invalid Python file {relative}: {exc}") from exc

        content = path.read_text(encoding="utf-8")
        if PLACEHOLDER.search(content):
            raise BootstrapError(f"Unresolved template placeholder in {relative}.")

    if final:
        remaining = [str(path) for path in BOOTSTRAP_ONLY_PATHS if (root / path).exists()]
        if remaining:
            raise BootstrapError(f"Bootstrap-only files remain: {', '.join(remaining)}.")


def prepare(root):
    required_files = (
        Path("pyproject.toml"),
        Path("docs/PROJECT_README.md"),
        BOOTSTRAP_SCRIPT,
        BOOTSTRAP_WORKFLOW,
        BOOTSTRAP_CONFIG,
    )

    missing = [str(path) for path in required_files if not (root / path).is_file()]

    if not (root / "src/package_name").is_dir():
        missing.append("src/package_name")

    if missing:
        raise BootstrapError("Not an unbootstrapped blueprint; missing or invalid: " + ", ".join(missing))

    metadata = load_metadata()
    source = root / "src/package_name"
    target = root / "src" / metadata["package"]
    readme_template = root / "docs/PROJECT_README.md"
    readme = root / "README.md"

    if target != source and target.exists():
        raise BootstrapError(f"Target package directory already exists: {target.relative_to(root)}.")

    log(f"Preparing {metadata['owner']}/{metadata['repository']}.")

    changed = sum(replace_text(path, metadata) for path in iter_text_files(root))

    if target != source:
        source.rename(target)

    readme.unlink(missing_ok=True)
    readme_template.rename(readme)

    validate_project(root)

    log(f"Prepared project successfully; updated {changed} text files.")
    log("Run finalize to remove bootstrap-only files.")


def finalize(root):
    validate_project(root)
    if not (root / BOOTSTRAP_WORKFLOW).is_file() or not (root / BOOTSTRAP_SCRIPT).is_file():
        raise BootstrapError("Expected bootstrap workflow and script before cleanup.")

    log("Removing bootstrap-only files.")
    for relative in BOOTSTRAP_ONLY_PATHS:
        (root / relative).unlink(missing_ok=True)

    scripts = root / ".github/scripts"
    if scripts.is_dir() and not any(scripts.iterdir()):
        scripts.rmdir()
    validate_project(root, final=True)
    log("Final repository passed structural validation.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "finalize"))
    parser.add_argument("--root", help="Repository root; defaults to the root containing this script.")
    args = parser.parse_args()
    try:
        root = repository_root(args.root)
        (prepare if args.command == "prepare" else finalize)(root)
    except (BootstrapError, OSError) as exc:
        print(f"::error::{exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
