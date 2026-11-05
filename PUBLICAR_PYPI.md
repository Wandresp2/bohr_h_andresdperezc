# Publicar la librería en PyPI — paso a paso

Solo se instala la **lógica** (`src/bohr_h_andresdperezc/`). El wheel no lleva `streamlit_app.py`, `ejemplo_consola.py`, `docs/`, `Dockerfile` ni el notebook: `pyproject.toml` busca paquetes únicamente dentro de `src/`. El sdist (`.tar.gz`) sí incluye `tests/` (habitual para que se puedan correr al bajar el fuente).

Las subidas (TestPyPI y PyPI) las hace el autor. Esta guía no pide tokens en el chat.

## 0. Estructura que debe tener el proyecto

```
entrega_libreria/
├── pyproject.toml
├── README.md
├── LICENSE
├── src/
│   └── bohr_h_andresdperezc/
│       ├── __init__.py     ← API pública y __version__
│       └── core.py
├── tests/test_core.py
├── streamlit_app.py        ← NO se publica
└── ejemplo_consola.py      ← NO se publica
```

Nombre PyPI (con guion) ≠ nombre de import (con guion bajo):

- se instala con `pip install bohr-h-andresdperezc`
- se importa con `from bohr_h_andresdperezc import BohrAtom`

La versión `0.1.0` debe coincidir en `pyproject.toml` y en `__init__.py`. **PyPI no permite subir dos veces la misma versión.**

Antes de publicar, busque el nombre en https://pypi.org/project/bohr-h-andresdperezc/ — si ya existe, cambie `name` en `pyproject.toml`.

## 1. Entorno virtual y herramientas

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Linux/macOS: `source .venv/bin/activate`.

Si PowerShell bloquea `Activate.ps1`: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` (una sola vez).

## 2. Verificar que todo funciona

```powershell
pytest -v
python ejemplo_consola.py
```

## 3. Construir los distribuibles

```powershell
Remove-Item -Recurse -Force dist -ErrorAction SilentlyContinue
python -m build
python -m twine check dist/*
```

Deben aparecer:

- `dist/bohr_h_andresdperezc-0.1.0.tar.gz`
- `dist/bohr_h_andresdperezc-0.1.0-py3-none-any.whl`

`twine check` debe decir **PASSED**.

## 4. Cuentas y tokens

1. TestPyPI (ensayo): https://test.pypi.org/account/register/
2. PyPI (oficial): https://pypi.org/account/register/

Son cuentas independientes. Ambas exigen 2FA.

En cada sitio: *Account settings → API tokens → Add API token*. El token empieza por `pypi-` y **solo se muestra una vez**.

Opcional: `C:\Users\SU_USUARIO\.pypirc` (nunca lo suba a GitHub):

```ini
[pypi]
  username = __token__
  password = pypi-...

[testpypi]
  username = __token__
  password = pypi-...
```

## 5. Ensayo en TestPyPI

```powershell
python -m twine upload --repository testpypi dist/*
```

Si no usó `.pypirc`, el usuario es literalmente `__token__` y la contraseña es el token.

Probar en un entorno **limpio** (numpy y matplotlib salen de PyPI real):

```powershell
python -m venv C:\temp\prueba-bohr
C:\temp\prueba-bohr\Scripts\Activate.ps1
python -m pip install `
    --index-url https://test.pypi.org/simple/ `
    --extra-index-url https://pypi.org/simple/ `
    bohr-h-andresdperezc
python -c "from bohr_h_andresdperezc import BohrAtom; print(BohrAtom(1).energia(1))"
```

Debe imprimir `-13.6`.

## 6. Publicación real en PyPI

Cuando TestPyPI funcione:

```powershell
python -m twine upload dist/*
```

Desde ese momento:

```bash
pip install bohr-h-andresdperezc
```

## 7. Publicar una versión nueva

1. Cambios + `pytest -v`.
2. Subir la versión en `pyproject.toml` y `__init__.py` (`0.1.0` → `0.1.1` o `0.2.0`).
3. Borrar `dist/`.
4. `python -m build` → `twine check dist/*` → `twine upload dist/*`.

## Errores frecuentes

| Mensaje | Causa | Solución |
|---|---|---|
| `403 Forbidden` / *not allowed to upload* | El nombre ya es de otra persona | Cambie `name` en `pyproject.toml` |
| `400 File already exists` | Esa versión ya se subió | Incremente la versión y reconstruya |
| `ModuleNotFoundError` tras instalar | Falta `__init__.py` o el paquete no está en `src/` | Revise la estructura |
| `InvalidDistribution` en `twine check` | README o metadatos mal formados | Corrija `pyproject.toml` / `README.md` |

## Resumen PowerShell (con `.pypirc` ya creado)

```powershell
cd "C:\Users\andre\OneDrive\Desktop\Universidad\Desarrollo de software\entrega_libreria"
.\.venv\Scripts\Activate.ps1
pytest -v
Remove-Item -Recurse -Force dist -ErrorAction SilentlyContinue
python -m build
python -m twine check dist/*
python -m twine upload --repository testpypi dist/*
# ...probar en un venv limpio...
python -m twine upload dist/*
```

Docker Hub, EC2 y GitHub Pages: ver `DESPLIEGUE.md`.
