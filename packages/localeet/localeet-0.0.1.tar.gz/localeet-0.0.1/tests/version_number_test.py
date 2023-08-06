"""
Tests that version number has increased from PyPI-deployed version.
"""

import importlib
import sys
from pathlib import Path

import requests

import localeet


def test_version_has_been_updated() -> None:
    """Ensure latest version is greater than latest published version"""
    pypi_version = get_pypi_version()
    # add local repo to path to ensure we get local version
    project_dir = Path(__file__).resolve().parent
    sys.path.insert(0, str(project_dir))
    importlib.reload(localeet)
    assert localeet.__version__ > pypi_version


def get_pypi_version() -> str:
    """Return latest localeet version published to PyPI"""
    try:
        response = requests.get('https://pypi.org/pypi/localeet/json')
        response.raise_for_status()
        data = response.json()
        return data['info']['version']
    except requests.RequestException:
        raise
