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

## Autor

Andrés David Pérez Criollo — adperezc@udistrital.edu.co

Licencia MIT.
