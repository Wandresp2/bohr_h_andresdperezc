Instalación
===========

Requisito: **Python 3.10 o superior**, en Windows, Linux o macOS.

Desde PyPI
----------

Cuando el paquete esté publicado::

   pip install bohr-h-andresdperezc

Eso instala la **lógica y los gráficos matplotlib**. No instala Streamlit.

Desarrollo (modo editable)
--------------------------

Desde la carpeta del proyecto::

   python -m venv .venv

En Windows (PowerShell)::

   .\.venv\Scripts\Activate.ps1
   python -m pip install -e ".[dev,docs]"

En Linux o macOS::

   source .venv/bin/activate
   python -m pip install -e ".[dev,docs]"

Extras opcionales:

- ``[gui]`` — Streamlit, para ``streamlit run streamlit_app.py``
- ``[dev]`` — pytest, build, twine
- ``[docs]`` — Sphinx, Furo, rst2pdf

Nombre PyPI vs import
---------------------

Se instala con guion y se importa con guion bajo::

   pip install bohr-h-andresdperezc
   from bohr_h_andresdperezc import BohrAtom
