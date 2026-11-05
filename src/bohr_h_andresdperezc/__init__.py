"""Modelo de Bohr para hidrógeno y átomos hidrogenoides.

Uso rápido::

    from bohr_h_andresdperezc import BohrAtom

    h = BohrAtom(Z=1)
    print(h.energia(1), h.radio(1))
    print(h.transicion(3, 2))
    h.graficar_niveles(5, transiciones=[(3, 2)])
    h.graficar_orbitas(4)
"""

from .core import BohrAtom, Transicion

__version__ = "0.1.0"

__all__ = [
    "BohrAtom",
    "Transicion",
    "__version__",
]
