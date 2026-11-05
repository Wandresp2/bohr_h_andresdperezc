"""Núcleo del modelo de Bohr para hidrógeno y átomos hidrogenoides.

Este módulo no depende de Streamlit ni de Tkinter. Los gráficos se generan
con matplotlib y se devuelven como figuras para script, notebook o GUI.
"""

from dataclasses import dataclass

import numpy as np

__all__ = ["BohrAtom", "Transicion"]


def _entero_positivo(valor, nombre):
    """Exige un entero ≥ 1. Rechaza bool, flotantes y cero o negativos."""
    if isinstance(valor, bool) or not isinstance(valor, (int, np.integer)):
        raise ValueError(
            f"{nombre} debe ser un entero ≥ 1; se recibió {valor!r}."
        )
    valor = int(valor)
    if valor < 1:
        raise ValueError(
            f"{nombre} debe ser un entero ≥ 1; se recibió {valor}."
        )
    return valor


@dataclass(frozen=True)
class Transicion:
    """Resultado de una transición electrónica n_inicial → n_final."""

    n_inicial: int
    """Nivel de origen."""

    n_final: int
    """Nivel de destino."""

    delta_e: float
    """E(n_final) − E(n_inicial) en eV. Negativo en emisión."""

    energia_foton: float
    """Energía del fotón (valor absoluto de delta_e) en eV."""

    frecuencia: float
    """Frecuencia del fotón en Hz."""

    longitud_onda: float
    """Longitud de onda del fotón en nm."""

    tipo: str
    """``emision`` si n_inicial > n_final; ``absorcion`` en caso contrario."""


class BohrAtom:
    """Átomo hidrogenoide según el modelo de Bohr (un electrón, carga nuclear Z).

    Unidades por defecto (didácticas): energía en eV, radio en Å, longitud de
    onda en nm, frecuencia en Hz. Si el modelo se expande, hay que validarlo.

    Parameters
    ----------
    Z : int, optional
        Número atómico. El hidrógeno es ``Z=1``, He⁺ es ``Z=2``, etc.
    """

    # Valores de libro (didácticos). Hay que validar el desarrollo si se expande.
    ENERGIA_RYDBERG_EV = 13.6
    """Energía de Rydberg didáctica en eV."""

    RADIO_BOHR_A = 0.529
    """Radio de Bohr :math:`a_0` en Å."""

    PLANCK_J_S = 6.62607015e-34
    """Constante de Planck en J·s."""

    VELOCIDAD_LUZ_M_S = 299792458.0
    """Velocidad de la luz en m/s."""

    MASA_ELECTRON_KG = 9.1093837139e-31
    """Masa del electrón en kg."""

    CARGA_ELEMENTAL_C = 1.602176634e-19
    """Carga elemental en C (también convierte eV a J)."""

    def __init__(self, Z=1):
        """Crea un átomo hidrogenoide de número atómico ``Z``.

        Raises
        ------
        ValueError
            Si ``Z`` no es un entero ≥ 1.
        """
        self._z = _entero_positivo(Z, "Z")

    @property
    def Z(self):
        """Número atómico (carga nuclear efectiva)."""
        return self._z

    def energia(self, n):
        """Energía del nivel ``n`` en eV: :math:`E_n = -13.6 Z^2 / n^2`.

        Returns
        -------
        float

        Raises
        ------
        ValueError
            Si ``n`` no es un entero ≥ 1.
        """
        n = _entero_positivo(n, "n")
        return -self.ENERGIA_RYDBERG_EV * (self._z**2) / (n**2)

    def radio(self, n):
        """Radio de la órbita ``n`` en Å: :math:`r_n = n^2 a_0 / Z`.

        Returns
        -------
        float

        Raises
        ------
        ValueError
            Si ``n`` no es un entero ≥ 1.
        """
        n = _entero_positivo(n, "n")
        return (n**2) * self.RADIO_BOHR_A / self._z

    def energias(self, n_max):
        """Energías de n = 1 … n_max en eV (arreglo de NumPy).

        Returns
        -------
        numpy.ndarray
        """
        n_max = _entero_positivo(n_max, "n_max")
        niveles = np.arange(1, n_max + 1)
        return -self.ENERGIA_RYDBERG_EV * (self._z**2) / (niveles**2)

    def radios(self, n_max):
        """Radios de n = 1 … n_max en Å (arreglo de NumPy).

        Returns
        -------
        numpy.ndarray
        """
        n_max = _entero_positivo(n_max, "n_max")
        niveles = np.arange(1, n_max + 1)
        return (niveles**2) * self.RADIO_BOHR_A / self._z

    def transicion(self, n_inicial, n_final):
        """Transición n_inicial → n_final: ΔE, frecuencia y longitud de onda.

        El fotón tiene energía :math:`|\\Delta E|`. Si el electrón baja de
        nivel es emisión; si sube, absorción.

        Returns
        -------
        Transicion

        Raises
        ------
        ValueError
            Si los niveles no son enteros ≥ 1 o si son iguales.
        """
        n_inicial = _entero_positivo(n_inicial, "n_inicial")
        n_final = _entero_positivo(n_final, "n_final")
        if n_inicial == n_final:
            raise ValueError(
                "n_inicial y n_final deben ser distintos para una transición."
            )

        delta_e = self.energia(n_final) - self.energia(n_inicial)
        energia_foton = abs(delta_e)
        frecuencia, longitud_onda = self._foton_desde_energia_ev(energia_foton)
        tipo = "emision" if n_inicial > n_final else "absorcion"
        return Transicion(
            n_inicial=n_inicial,
            n_final=n_final,
            delta_e=delta_e,
            energia_foton=energia_foton,
            frecuencia=frecuencia,
            longitud_onda=longitud_onda,
            tipo=tipo,
        )

    def _foton_desde_energia_ev(self, energia_ev):
        """Convierte |ΔE| en eV a frecuencia (Hz) y longitud de onda (nm)."""
        energia_j = energia_ev * self.CARGA_ELEMENTAL_C
        frecuencia = energia_j / self.PLANCK_J_S
        longitud_onda_nm = (self.VELOCIDAD_LUZ_M_S / frecuencia) * 1e9
        return frecuencia, longitud_onda_nm

    def graficar_niveles(self, n_max, transiciones=None):
        """Diagrama de niveles de energía E_n (eV) y, si se piden, transiciones.

        Parameters
        ----------
        n_max : int
            Último nivel dibujado (n = 1 … n_max).
        transiciones : secuencia opcional
            Pares ``(n_inicial, n_final)``, objetos ``Transicion``, o uno solo
            de esos elementos. Las flechas bajan en emisión y suben en absorción.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt

        n_max = _entero_positivo(n_max, "n_max")
        pares = self._pares_transicion(transiciones, n_max)

        fig, ax = plt.subplots(figsize=(7.5, 5.5), layout="constrained")
        x0, x1 = 0.12, 0.78
        for n in range(1, n_max + 1):
            energia = self.energia(n)
            ax.hlines(energia, x0, x1, colors="#2c3e50", linewidth=1.6)
            ax.text(
                x1 + 0.03,
                energia,
                f"n = {n}   {energia:.2f} eV",
                va="center",
                fontsize=9,
            )

        ax.axhline(0.0, color="#7f8c8d", linestyle="--", linewidth=1, label="ionización (E = 0)")

        hubo_emision = False
        hubo_absorcion = False
        for i, (n_inicial, n_final) in enumerate(pares):
            x = 0.22 + 0.5 * (i + 1) / (len(pares) + 1)
            emision = n_inicial > n_final
            color = "#d35400" if emision else "#2980b9"
            etiqueta = None
            if emision and not hubo_emision:
                etiqueta = "emisión"
                hubo_emision = True
            elif not emision and not hubo_absorcion:
                etiqueta = "absorción"
                hubo_absorcion = True
            ax.annotate(
                "",
                xy=(x, self.energia(n_final)),
                xytext=(x, self.energia(n_inicial)),
                arrowprops=dict(arrowstyle="->", color=color, lw=1.7),
            )
            if etiqueta:
                ax.plot([], [], color=color, lw=1.7, label=etiqueta)

        ax.set_xlim(0.0, 1.35)
        ax.set_xticks([])
        ax.set_ylabel("Energía (eV)")
        ax.set_title(f"Niveles de energía — BohrAtom(Z={self._z})")
        ax.grid(axis="y", alpha=0.3)
        if hubo_emision or hubo_absorcion:
            ax.legend(loc="lower right")
        return fig

    def graficar_orbitas(self, n_max):
        """Órbitas circulares de radio r_n en el plano (Å), con el núcleo en el origen.

        Returns
        -------
        matplotlib.figure.Figure
        """
        import matplotlib.pyplot as plt
        from matplotlib.patches import Circle

        n_max = _entero_positivo(n_max, "n_max")
        radios = self.radios(n_max)
        fig, ax = plt.subplots(figsize=(6.5, 6.5), layout="constrained")
        colores = plt.cm.tab10.colors

        for indice, radio in enumerate(radios, start=1):
            anillo = Circle(
                (0.0, 0.0),
                radio,
                fill=False,
                linewidth=1.5,
                edgecolor=colores[(indice - 1) % 10],
                label=f"n = {indice}  ({radio:.3f} Å)",
            )
            ax.add_patch(anillo)

        radio_nucleo = 0.08 * float(radios[0])
        ax.add_patch(Circle((0.0, 0.0), radio_nucleo, color="#c0392b", zorder=5, label="núcleo"))

        margen = 1.15 * float(radios[-1])
        ax.set_xlim(-margen, margen)
        ax.set_ylim(-margen, margen)
        ax.set_aspect("equal")
        ax.set_xlabel("x (Å)")
        ax.set_ylabel("y (Å)")
        ax.set_title(f"Órbitas electrónicas — BohrAtom(Z={self._z})")
        ax.legend(loc="upper right", fontsize=8)
        ax.grid(alpha=0.25)
        return fig

    def _pares_transicion(self, transiciones, n_max):
        """Normaliza transiciones a una lista de pares (n_inicial, n_final)."""
        if transiciones is None:
            return []
        if isinstance(transiciones, Transicion) or _es_par_niveles(transiciones):
            items = [transiciones]
        else:
            try:
                items = list(transiciones)
            except TypeError as error:
                raise ValueError(
                    "transiciones debe ser un par (n_inicial, n_final), "
                    "un Transicion o una secuencia de ellos."
                ) from error

        pares = []
        for item in items:
            if isinstance(item, Transicion):
                n_inicial, n_final = item.n_inicial, item.n_final
            elif _es_par_niveles(item):
                n_inicial, n_final = item
            else:
                raise ValueError(
                    "Cada transición debe ser un par (n_inicial, n_final) "
                    "o un objeto Transicion."
                )
            n_inicial = _entero_positivo(n_inicial, "n_inicial")
            n_final = _entero_positivo(n_final, "n_final")
            if n_inicial == n_final:
                raise ValueError(
                    "n_inicial y n_final deben ser distintos para una transición."
                )
            if n_inicial > n_max or n_final > n_max:
                raise ValueError(
                    f"La transición {n_inicial}→{n_final} exige n_max ≥ {max(n_inicial, n_final)}."
                )
            pares.append((n_inicial, n_final))
        return pares

    def __repr__(self):
        return f"BohrAtom(Z={self._z})"


def _es_par_niveles(item):
    """True si item es un par de números (n_inicial, n_final), no una lista de pares."""
    if isinstance(item, Transicion):
        return True
    if not isinstance(item, (tuple, list)) or len(item) != 2:
        return False
    return not isinstance(item[0], (tuple, list, Transicion))
