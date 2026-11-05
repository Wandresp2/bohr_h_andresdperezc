# bohr-h-andresdperezc

Librería didáctica en Python del **modelo de Bohr** para el hidrógeno y átomos hidrogenoides (un electrón, número atómico \(Z\)).

Esta es la estructura instalable del paquete (fase 1). Los cálculos, gráficos, tests y la GUI se completan en fases siguientes.

## Instalación (desarrollo)

Desde la carpeta del proyecto, con Python 3.10 o superior:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
```

En Linux o macOS: `source .venv/bin/activate`.

Instalación publicada (cuando el paquete esté en PyPI):

```bash
pip install bohr-h-andresdperezc
```

## Uso básico

```python
from bohr_h_andresdperezc import BohrAtom

hidrogeno = BohrAtom(Z=1)
print(hidrogeno.energia(1), hidrogeno.radio(1))
print(hidrogeno.transicion(3, 2))
```

## Ejemplos (sin Streamlit)

- `python ejemplo_consola.py` — cálculos en terminal y figuras PNG en `examples/`.
- `examples/notebook_didactico.ipynb` — teoría breve y llamadas a la librería.

## GUI (Streamlit, opcional)

La interfaz **no forma parte del paquete**. Instálela solo si quiere jugar en el navegador:

```powershell
python -m pip install -e ".[gui]"
streamlit run streamlit_app.py
```

Abra http://localhost:8501. Sliders: \(Z\) de 1 a 10, \(n\) de 1 a 8.

## Docker

Cualquier sistema operativo con Docker abre la misma GUI en el navegador (no usa Tkinter).

```bash
docker build -t andresperez3/bohr-h-andresdperezc:0.1.0 .
docker run --rm -p 8501:8501 andresperez3/bohr-h-andresdperezc:0.1.0
```

Abra http://localhost:8501.

El `docker push` a Docker Hub (usuario `andresperez3`) lo hace el autor:

```bash
docker push andresperez3/bohr-h-andresdperezc:0.1.0
```

Después, en otra máquina:

```bash
docker pull andresperez3/bohr-h-andresdperezc:0.1.0
docker run --rm -p 8501:8501 andresperez3/bohr-h-andresdperezc:0.1.0
```

## Documentación (Sphinx)

```powershell
python -m pip install -e ".[docs]"
sphinx-build -b html docs docs/_build/html
sphinx-build -b rinoh docs docs/_build/rinoh
```

HTML: `docs/_build/html/index.html`. PDF: `docs/_build/rinoh/bohr-h-andresdperezc.pdf`.
GitHub Pages: ver `docs/publicar.rst` (el autor publica el sitio).

## Publicar (lo hace el autor)

- PyPI: [`PUBLICAR_PYPI.md`](PUBLICAR_PYPI.md) (primero TestPyPI).
- Docker Hub, EC2 (puerto 8501, sin contraseña) y GitHub Pages: [`DESPLIEGUE.md`](DESPLIEGUE.md).

## Autor

Andrés David Pérez Criollo — adperezc@udistrital.edu.co

Licencia MIT.
