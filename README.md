# bohr-h-andresdperezc

Librería didáctica en Python del **modelo de Bohr** para el hidrógeno y átomos hidrogenoides (núcleo de carga `Z` y **un solo electrón**). Calcula energías, radios de órbita y transiciones (ΔE, frecuencia y longitud de onda del fotón) y genera gráficos de niveles y de órbitas.

Se instala con **guion** y se importa con **guion bajo**:

```text
pip install bohr-h-andresdperezc
from bohr_h_andresdperezc import BohrAtom
```

La GUI de Streamlit **no** forma parte del paquete: vive en este repositorio (`streamlit_app.py`) y en la imagen Docker. El paquete no depende de Streamlit ni de Tkinter.

Versión **0.1.0**. Python **≥ 3.10**. Licencia **MIT**.

## Requisitos y sistemas

Corre en **Windows, Linux y macOS** (Python 3.10 o superior).

| Uso | Windows | Linux | macOS |
|---|---|---|---|
| `pip install` + cálculos + matplotlib | Sí | Sí | Sí |
| pytest y notebook | Sí | Sí | Sí |
| Streamlit en el navegador | Sí | Sí | Sí |
| Docker + Streamlit | Sí (Docker Desktop) | Sí | Sí |
| EC2 por IP pública | Sí (cualquier navegador) | igual | igual |

Tkinter **no** es requisito. En Linux no hace falta `python3-tk`.

## Instalación

Cuando el paquete esté en [PyPI](https://pypi.org/project/bohr-h-andresdperezc/):

```bash
pip install bohr-h-andresdperezc
```

Eso instala la **lógica y los gráficos matplotlib**. No instala Streamlit ni copia `streamlit_app.py`.

### Desarrollo (modo editable)

Desde la carpeta del proyecto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev,docs]"
```

En Linux o macOS: `source .venv/bin/activate` y el mismo `pip install`.

Extras opcionales:

| Extra | Qué añade |
|---|---|
| `[gui]` | Streamlit, para `streamlit run streamlit_app.py` (hace falta el archivo del repo) |
| `[dev]` | pytest, build, twine |
| `[docs]` | Sphinx, Furo, rinohtype |

Todo junto: `python -m pip install -e ".[gui,dev,docs]"`.

Si PowerShell bloquea `Activate.ps1`: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` (una sola vez).

## Uso básico

```python
from bohr_h_andresdperezc import BohrAtom

hidrogeno = BohrAtom(Z=1)
helio = BohrAtom(Z=2)          # He⁺

print(hidrogeno.energia(1))    # -13.6 eV
print(hidrogeno.radio(1))      # 0.529 Å

balmer = hidrogeno.transicion(3, 2)
print(balmer.tipo)             # emision
print(balmer.longitud_onda)    # ≈ 656 nm
print(balmer.frecuencia)       # Hz
print(balmer.delta_e)          # eV (negativo en emisión)

fig = hidrogeno.graficar_niveles(5, transiciones=[(3, 2), (4, 2)])
fig.savefig("niveles.png")

fig2 = hidrogeno.graficar_orbitas(4)
fig2.savefig("orbitas.png")
```

`Z` y `n` deben ser enteros ≥ 1. Si no, se lanza `ValueError` con un mensaje en español.

### Métodos de `BohrAtom`

| Método | Resultado |
|---|---|
| `energia(n)` | `E_n` en eV |
| `radio(n)` | `r_n` en Å |
| `energias(n_max)` / `radios(n_max)` | arreglo NumPy, `n = 1 … n_max` |
| `transicion(n_inicial, n_final)` | objeto `Transicion` |
| `graficar_niveles(n_max, transiciones=None)` | figura matplotlib |
| `graficar_orbitas(n_max)` | figura matplotlib (círculos en el plano) |

Los gráficos **devuelven** la figura; no abren una ventana de Tkinter. En un script se guarda el PNG; en un notebook se muestra sola.

`transicion` rellena `n_inicial`, `n_final`, `delta_e`, `energia_foton`, `frecuencia`, `longitud_onda` y `tipo` (`emision` o `absorcion`).

### Fórmulas (valores de libro)

```text
E_n = -13.6 eV · Z² / n²
r_n = n² · a₀ / Z          a₀ ≈ 0.529 Å
ΔE  = E(n_final) − E(n_inicial)
```

El fotón lleva `|ΔE|`. Hidrógeno `3 → 2` (Balmer, H-alpha): λ ≈ 656 nm.

### Unidades por defecto

| Magnitud | Unidad |
|---|---|
| Energía | eV |
| Radio | Å |
| Longitud de onda | nm |
| Frecuencia | Hz |

## Ejemplos (sin Streamlit)

Demuestran que el paquete funciona **solo con pip**:

- `python ejemplo_consola.py` — cálculos en terminal y PNG en `examples/`.
- `examples/notebook_didactico.ipynb` — teoría breve y llamadas a la librería (Jupyter).

## Pruebas

```powershell
python -m pip install -e ".[dev]"
pytest -v
```

Los tests contrastan valores de libro (`E_1(H) = -13.6 eV`, `r_1 = 0.529 Å`, Balmer ≈ 656 nm) y comprueban que `graficar_*` devuelve una `Figure`.

## GUI (Streamlit, opcional)

La interfaz **no se publica en PyPI**. Hay que clonar este repositorio:

```powershell
python -m pip install -e ".[gui]"
streamlit run streamlit_app.py
```

Abra http://localhost:8501. Sliders: `Z` de 1 a 10, `n` de 1 a 8; transiciones y gráficos.

## Docker

Cualquier sistema con Docker abre la misma GUI en el navegador (no usa Tkinter). Streamlit escucha en `0.0.0.0:8501`.

```bash
docker build -t andresperez3/bohr-h-andresdperezc:0.1.0 .
docker run --rm -p 8501:8501 andresperez3/bohr-h-andresdperezc:0.1.0
```

http://localhost:8501

El `docker push` a Docker Hub (usuario `andresperez3`) lo hace el autor. Detalle de Hub, **EC2** (puerto 8501 abierto, **sin contraseña**, no dejarla 24/7) y GitHub Pages: [`DESPLIEGUE.md`](DESPLIEGUE.md).

## Documentación (Sphinx)

```powershell
python -m pip install -e ".[docs]"
sphinx-build -b html docs docs/_build/html
sphinx-build -b rinoh docs docs/_build/rinoh
```

HTML: `docs/_build/html/index.html`. PDF: `docs/_build/rinoh/bohr-h-andresdperezc.pdf`.

GitHub Pages: *Settings → Pages → GitHub Actions* (flujo en `.github/workflows/pages.yml`). La URL del repositorio se añadirá cuando exista.

## Publicar en PyPI (lo hace el autor)

Paso a paso, primero TestPyPI y luego PyPI: [`PUBLICAR_PYPI.md`](PUBLICAR_PYPI.md).

Solo se instala `src/bohr_h_andresdperezc/`. `streamlit_app.py`, tests, docs, Docker y el notebook quedan fuera del wheel.

## Limitaciones

- Es el **modelo de Bohr**, no mecánica cuántica moderna: no hay orbitales, spin, estructura fina ni relatividad. Las órbitas son círculos en el plano, de forma didáctica.
- Solo un electrón. Sí: H (`Z=1`), He⁺ (`Z=2`), Li²⁺ (`Z=3`). No modela bien He neutro, C, O, etc.
- Unidades fijas (eV, Å, nm, Hz).
- Si el desarrollo se **expande** (más unidades, más física, más elementos), hay que **volver a validarlo**. Los tests actuales cubren los valores de libro citados arriba.

## Autor

Andrés David Pérez Criollo — adperezc@udistrital.edu.co

Universidad Distrital Francisco José de Caldas.

Licencia MIT. Ver [`LICENSE`](LICENSE).
