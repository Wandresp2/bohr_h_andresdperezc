"""
streamlit_app.py — GUI web del modelo de Bohr.

Solo CONSUME la API pública de ``bohr_h_andresdperezc``. El paquete no
importa Streamlit: se puede reemplazar esta app por un notebook o un
script sin tocar core.py.

Preparación (una vez, desde la carpeta del proyecto)::

    python -m venv .venv
    .venv\\Scripts\\Activate.ps1
    python -m pip install -e ".[gui]"

Ejecutar::

    streamlit run streamlit_app.py
"""

from __future__ import annotations

import os

os.environ.setdefault("MPLBACKEND", "Agg")

import matplotlib.pyplot as plt
import streamlit as st

try:
    from bohr_h_andresdperezc import BohrAtom
except ImportError:
    raise SystemExit(
        "No se encontró la librería 'bohr_h_andresdperezc'.\n"
        "Desde la carpeta del proyecto, con el entorno virtual activo, ejecute:\n"
        '  python -m pip install -e ".[gui]"'
    ) from None

Z_MIN, Z_MAX = 1, 10
N_MIN, N_MAX = 1, 8


def _mostrar_figura(figura):
    st.pyplot(figura, clear_figure=True)
    plt.close(figura)


def main():
    st.set_page_config(
        page_title="Átomo de Bohr",
        page_icon="⚛",
        layout="wide",
    )

    st.title("Átomo de Bohr — hidrógeno e hidrogenoides")
    st.caption(
        "GUI de Streamlit sobre la librería `bohr-h-andresdperezc`. "
        "El paquete no depende de esta interfaz."
    )

    with st.sidebar:
        st.header("Parámetros")
        z = st.slider("Número atómico Z", min_value=Z_MIN, max_value=Z_MAX, value=1)
        n = st.slider("Nivel n", min_value=N_MIN, max_value=N_MAX, value=1)
        n_max_grafico = st.slider(
            "Niveles en los gráficos",
            min_value=N_MIN,
            max_value=N_MAX,
            value=5,
        )
        st.divider()
        st.markdown(
            """
**Modelo de Bohr** (un electrón).

- H: Z = 1
- He⁺: Z = 2
- Li²⁺: Z = 3

No describe bien átomos con varios electrones.
Unidades: eV, Å, nm, Hz.
Si el desarrollo se **expande**, hay que **validarlo** de nuevo.
            """
        )

    atomo = BohrAtom(Z=z)
    energia = atomo.energia(n)
    radio = atomo.radio(n)

    col_e, col_r, col_z = st.columns(3)
    col_e.metric(f"Energía E_{n}", f"{energia:.4f} eV")
    col_r.metric(f"Radio r_{n}", f"{radio:.4f} Å")
    col_z.metric("Átomo", f"Z = {z}")

    st.subheader("Transición electrónica")
    col_i, col_f = st.columns(2)
    n_inicial = col_i.number_input(
        "n inicial", min_value=N_MIN, max_value=N_MAX, value=3, step=1
    )
    n_final = col_f.number_input(
        "n final", min_value=N_MIN, max_value=N_MAX, value=2, step=1
    )

    if n_inicial == n_final:
        st.warning("Elija niveles distintos para calcular un fotón.")
        transicion = None
    else:
        transicion = atomo.transicion(int(n_inicial), int(n_final))
        tipo_legible = "emisión" if transicion.tipo == "emision" else "absorción"
        fila1 = st.columns(2)
        fila1[0].metric("Tipo", tipo_legible)
        fila1[1].metric("ΔE (eV)", f"{transicion.delta_e:.4f}")
        fila2 = st.columns(2)
        fila2[0].metric("Frecuencia (Hz)", f"{transicion.frecuencia:.3e}")
        fila2[1].metric("Longitud de onda (nm)", f"{transicion.longitud_onda:.1f}")
        st.caption(
            f"Energía del fotón = {transicion.energia_foton:.4f} eV. "
            "Si el electrón baja de nivel, el átomo emite; si sube, absorbe."
        )

    st.subheader("Gráficos")
    ver_niveles = st.checkbox("Niveles de energía y transiciones", value=True)
    ver_orbitas = st.checkbox("Órbitas electrónicas", value=True)

    col_g1, col_g2 = st.columns(2)
    if ver_niveles:
        with col_g1:
            n_graf = int(n_max_grafico)
            pares = None
            if transicion is not None:
                n_graf = max(n_graf, transicion.n_inicial, transicion.n_final)
                pares = [(transicion.n_inicial, transicion.n_final)]
            figura_niveles = atomo.graficar_niveles(n_graf, transiciones=pares)
            _mostrar_figura(figura_niveles)

    if ver_orbitas:
        with col_g2:
            figura_orbitas = atomo.graficar_orbitas(int(n_max_grafico))
            _mostrar_figura(figura_orbitas)


main()
