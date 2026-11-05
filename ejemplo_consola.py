"""Uso de la librería SIN interfaz gráfica: la lógica no depende de Streamlit.

Preparación (una vez, desde la carpeta del proyecto)::

    python -m venv .venv
    .venv\\Scripts\\Activate.ps1
    python -m pip install -e .

Ejecutar::

    python ejemplo_consola.py
"""

from pathlib import Path

try:
    from bohr_h_andresdperezc import BohrAtom
except ImportError:
    raise SystemExit(
        "No se encontró la librería 'bohr_h_andresdperezc'.\n"
        "Desde la carpeta del proyecto, con el entorno virtual activo, ejecute:\n"
        "  python -m pip install -e ."
    ) from None

import matplotlib

matplotlib.use("Agg")


def main():
    hidrogeno = BohrAtom(Z=1)
    helio = BohrAtom(Z=2)

    print("Hidrógeno (Z = 1)")
    print(f"  E_1 = {hidrogeno.energia(1):.2f} eV  (libro: -13.6 eV)")
    print(f"  r_1 = {hidrogeno.radio(1):.3f} Å  (libro: 0.529 Å)")
    print("  Niveles n = 1 … 4:")
    for n, energia, radio in zip(
        range(1, 5), hidrogeno.energias(4), hidrogeno.radios(4)
    ):
        print(f"    n = {n}:  E = {energia:8.3f} eV   r = {radio:7.3f} Å")

    print("\nHe⁺ (Z = 2): la energía escala con Z²")
    print(f"  E_1(He⁺) = {helio.energia(1):.2f} eV")
    print(f"  4 × E_1(H) = {4 * hidrogeno.energia(1):.2f} eV")

    balmer = hidrogeno.transicion(3, 2)
    print("\nTransición de Balmer 3 → 2 (emisión)")
    print(f"  tipo           = {balmer.tipo}")
    print(f"  ΔE             = {balmer.delta_e:.4f} eV")
    print(f"  energía fotón  = {balmer.energia_foton:.4f} eV")
    print(f"  frecuencia     = {balmer.frecuencia:.4e} Hz")
    print(f"  longitud onda  = {balmer.longitud_onda:.1f} nm  (libro: ≈ 656 nm)")

    absorcion = hidrogeno.transicion(2, 3)
    print("\nLa inversa 2 → 3 es absorción, con la misma λ")
    print(f"  tipo = {absorcion.tipo}   λ = {absorcion.longitud_onda:.1f} nm")

    carpeta = Path(__file__).resolve().parent / "examples"
    carpeta.mkdir(exist_ok=True)
    figura_niveles = hidrogeno.graficar_niveles(
        5, transiciones=[(3, 2), (4, 2), (2, 4)]
    )
    ruta_niveles = carpeta / "niveles_hidrogeno.png"
    figura_niveles.savefig(ruta_niveles, dpi=120)

    figura_orbitas = hidrogeno.graficar_orbitas(4)
    ruta_orbitas = carpeta / "orbitas_hidrogeno.png"
    figura_orbitas.savefig(ruta_orbitas, dpi=120)

    print("\nFiguras guardadas (backend Agg, sin ventana):")
    print(f"  {ruta_niveles}")
    print(f"  {ruta_orbitas}")
    print("\nEste script no usa Streamlit: el paquete funciona solo con pip.")


if __name__ == "__main__":
    main()
