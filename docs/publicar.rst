Construir HTML, PDF y GitHub Pages
==================================

Los comandos de **PyPI, Docker Hub y EC2** están en la raíz del
repositorio (no se copian aquí para no duplicar versiones):

* ``PUBLICAR_PYPI.md`` — ensayo en TestPyPI y luego PyPI. Solo se
  publica ``src/bohr_h_andresdperezc/``.
* ``DESPLIEGUE.md`` — ``docker push``, EC2 (puerto 8501, sin
  contraseña) y GitHub Pages.

Instale las herramientas de documentación una vez::

   python -m pip install -e ".[docs]"

HTML (Sphinx + Furo)
--------------------

Desde la **raíz del proyecto**, en Windows, Linux o macOS::

   sphinx-build -b html docs docs/_build/html

Abra ``docs/_build/html/index.html`` en el navegador.

Con Make (si tiene ``make``)::

   cd docs
   make html

En Windows sin Make use ``docs\make.bat html``.

PDF
---

**Opción A — rinohtype (recomendada en Windows).** No instala LaTeX::

   sphinx-build -b rinoh docs docs/_build/rinoh

El archivo queda en ``docs/_build/rinoh/bohr-h-andresdperezc.pdf``.
Equivale a ``make pdf`` o ``docs\make.bat pdf``.

**Opción B — LaTeX** (MiKTeX o TeX Live)::

   sphinx-build -M latexpdf docs docs/_build

Equivale a ``make latexpdf`` dentro de ``docs/``.

GitHub Pages
------------

La publicación la hace el autor del repositorio. Dos caminos:

1. **GitHub Actions** (incluido ``.github/workflows/pages.yml``):

   - En el repo: *Settings → Pages → Source: GitHub Actions*.
   - Cada push a ``main`` construye Sphinx y publica el HTML.

2. **Carpeta / rama a mano:** suba el contenido de
   ``docs/_build/html`` a la rama ``gh-pages``. Incluya un archivo
   vacío ``.nojekyll`` en la raíz de esa rama para que GitHub no
   ignore ``_static``.

La URL típica será
``https://<usuario>.github.io/<repositorio>/``.
