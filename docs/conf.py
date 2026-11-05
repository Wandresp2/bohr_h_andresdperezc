"""Configuración de Sphinx para bohr-h-andresdperezc."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

project = "bohr-h-andresdperezc"
author = "Andrés David Pérez Criollo"
copyright = "2026, Andrés David Pérez Criollo"
release = "0.1.0"
version = "0.1.0"
language = "es"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.mathjax",
    "myst_parser",
]

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

autodoc_member_order = "bysource"
autodoc_typehints = "description"
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True

html_theme = "furo"
html_title = "bohr-h-andresdperezc"
html_short_title = "Bohr"

myst_enable_extensions = ["dollarmath", "amsmath", "colon_fence"]

# PDF con rinohtype (no requiere LaTeX; útil en Windows).
rinoh_documents = [
    {
        "doc": "index",
        "target": "bohr-h-andresdperezc",
        "title": "bohr-h-andresdperezc — documentación",
        "author": "Andrés David Pérez Criollo",
        "toctree_only": False,
    }
]
