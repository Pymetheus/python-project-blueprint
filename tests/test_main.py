import runpy
import sys


def test_main_runs_as_script(monkeypatch):
    """
    Ensure the module runs correctly when executed as __main__
    and cover the __main__ guard branch.
    Suppresses the runpy import warning by removing the module first.
    """

    # Patch setup_logging to avoid side effects
    monkeypatch.setattr("package_name.main.setup_logging", lambda *args, **kwargs: None)

    # Remove the already imported module to avoid warnings
    sys.modules.pop("package_name.main", None)

    # Execute as if run via `python -m package_name.main`
    runpy.run_module("package_name.main", run_name="__main__")
