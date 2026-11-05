Limitaciones y compatibilidad
=============================

Alcance físico
--------------

El modelo de Bohr describe un **átomo hidrogenoide**: núcleo de carga
:math:`Z` y **un solo electrón**.

Sí aplica
   H (:math:`Z=1`), He⁺ (:math:`Z=2`), Li²⁺ (:math:`Z=3`), …

No modela bien
   Átomos con varios electrones (He neutro, C, O, …).

Tampoco incluye relatividad, spin, estructura fina ni orbitales de la
mecánica cuántica moderna. Las órbitas son círculos en el plano, de
forma didáctica.

Si el desarrollo se **expande** (más unidades, más física, más
elementos), hay que **volver a validarlo**. Los tests actuales contrastan
valores de libro (:math:`E_1(\mathrm{H}) = -13.6\,\mathrm{eV}`,
:math:`r_1 = 0.529\,\text{Å}`, Balmer :math:`3\to 2` ≈ 656 nm).

Unidades por defecto
--------------------

================== ========
Magnitud           Unidad
================== ========
Energía            eV
Radio              Å
Longitud de onda   nm
Frecuencia         Hz
================== ========

Sistemas operativos
-------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Uso
     - Windows / Linux / macOS
   * - ``pip install``
     - Sí (Python ≥ 3.10)
   * - pytest, notebook, matplotlib
     - Sí
   * - Streamlit local
     - Sí (navegador)
   * - Docker + Streamlit
     - Sí (Docker Desktop o motor Docker)
   * - EC2 por IP pública
     - Sí (cualquier navegador)

Tkinter **no** es requisito. En Linux no hace falta ``python3-tk`` para
esta librería.
