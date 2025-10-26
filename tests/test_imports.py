import importlib
import pytest


# Always-safe imports (fast, no heavy deps)
@pytest.mark.parametrize(
    "module",
    [
        "run_aura",
        "utils.config",
    ],
)
def test_imports_light(module):
    importlib.import_module(module)


# Optional: only run if streamlit & torch are installed in the environment
def test_import_streamlit_app_optionally():
    pytest.importorskip("streamlit")
    pytest.importorskip("torch")
    import importlib

    importlib.import_module("aura_streamlit_app")
