Uso
===

Cálculos
--------

::

   from bohr_h_andresdperezc import BohrAtom

   hidrogeno = BohrAtom(Z=1)
   helio = BohrAtom(Z=2)

   hidrogeno.energia(1)   # -13.6 eV
   hidrogeno.radio(1)     # 0.529 Å
   hidrogeno.energias(4)  # E_1 … E_4
   hidrogeno.radios(4)

   t = hidrogeno.transicion(3, 2)
   t.tipo            # "emision"
   t.longitud_onda   # ≈ 656 nm
   t.frecuencia      # Hz
   t.delta_e         # eV (negativo en emisión)

He⁺ (:math:`Z = 2`) tiene la misma forma; las energías escalan con
:math:`Z^2`.

Fórmulas (valores de libro)
---------------------------

.. math::

   E_n = -13.6\,\mathrm{eV}\cdot\frac{Z^2}{n^2},
   \qquad
   r_n = n^2\cdot\frac{a_0}{Z},
   \qquad
   a_0 \approx 0.529\,\text{Å}

El fotón de una transición lleva :math:`|\Delta E|`. Unidades por
defecto: **eV**, **Å**, **nm**, **Hz**.

Gráficos
--------

Los métodos devuelven una figura de matplotlib (no abren una ventana de
Tkinter). En un script puede guardar el archivo; en un notebook se
muestra sola::

   fig = hidrogeno.graficar_niveles(5, transiciones=[(3, 2), (4, 2)])
   fig.savefig("niveles.png")

   fig2 = hidrogeno.graficar_orbitas(4)
   fig2.savefig("orbitas.png")

``transiciones`` acepta un par ``(n_inicial, n_final)``, una lista de
pares o un objeto :class:`~bohr_h_andresdperezc.Transicion`.

Ejemplos del repositorio
------------------------

- ``python ejemplo_consola.py`` — imprime resultados y guarda PNG en
  ``examples/``.
- ``examples/notebook_didactico.ipynb`` — teoría breve y llamadas a la
  API.

Ninguno de los dos usa Streamlit: demuestran que el paquete es
independiente de la GUI.
