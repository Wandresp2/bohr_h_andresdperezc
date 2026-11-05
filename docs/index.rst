bohr-h-andresdperezc
====================

Librería didáctica en Python del **modelo de Bohr** para el hidrógeno y
átomos hidrogenoides (un electrón, número atómico :math:`Z`).

Instalación::

   pip install bohr-h-andresdperezc

Uso mínimo::

   from bohr_h_andresdperezc import BohrAtom

   h = BohrAtom(Z=1)
   print(h.energia(1))       # -13.6 eV
   print(h.radio(1))         # 0.529 Å
   print(h.transicion(3, 2)) # emisión, λ ≈ 656 nm

La clase :class:`~bohr_h_andresdperezc.BohrAtom` encapsula las constantes
físicas y expone cálculos y gráficos. La GUI de Streamlit **no** forma
parte del paquete: vive en ``streamlit_app.py`` y solo llama a esta API.

.. toctree::
   :maxdepth: 2
   :caption: Contenido

   instalacion
   uso
   api
   gui
   limitaciones
   publicar

Autor
-----

Andrés David Pérez Criollo — adperezc@udistrital.edu.co

Licencia MIT. Versión |release|.
