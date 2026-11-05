"""Núcleo del modelo de Bohr para hidrógeno y átomos hidrogenoides.

Este módulo no depende de ninguna interfaz gráfica: solo usa NumPy.
Los gráficos matplotlib se agregan en una fase posterior.
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
    """Resultado de una transición electrónica n_inicial → n_final.

    Attributes
    ----------
    n_inicial, n_final : int
        Niveles de origen y destino.
    delta_e : float
        E(n_final) − E(n_inicial) en eV. Negativo en emisión.
    energia_foton : float
        |ΔE| en eV.
    frecuencia : float
        Frecuencia del fotón en Hz.
    longitud_onda : float
        Longitud de onda del fotón en nm.
    tipo : str
        ``"emision"`` si n_inicial > n_final; ``"absorcion"`` en caso contrario.
    """

    n_inicial: int
    n_final: int
    delta_e: float
    energia_foton: float
    frecuencia: float
    longitud_onda: float
    tipo: str


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
    RADIO_BOHR_A = 0.529
    PLANCK_J_S = 6.62607015e-34
    VELOCIDAD_LUZ_M_S = 299792458.0
    MASA_ELECTRON_KG = 9.1093837139e-31
    CARGA_ELEMENTAL_C = 1.602176634e-19

    def __init__(self, Z=1):
        self._z = _entero_positivo(Z, "Z")

    @property
    def Z(self):
        """Número atómico (carga nuclear efectiva)."""
        return self._z

    def energia(self, n):
        """Energía del nivel ``n`` en eV: E_n = −13.6 Z² / n²."""
        n = _entero_positivo(n, "n")
        return -self.ENERGIA_RYDBERG_EV * (self._z**2) / (n**2)

    def radio(self, n):
        """Radio de la órbita ``n`` en Å: r_n = n² a₀ / Z."""
        n = _entero_positivo(n, "n")
        return (n**2) * self.RADIO_BOHR_A / self._z

    def energias(self, n_max):
        """Energías de n = 1 … n_max en eV (arreglo de NumPy)."""
        n_max = _entero_positivo(n_max, "n_max")
        niveles = np.arange(1, n_max + 1)
        return -self.ENERGIA_RYDBERG_EV * (self._z**2) / (niveles**2)

    def radios(self, n_max):
        """Radios de n = 1 … n_max en Å (arreglo de NumPy)."""
        n_max = _entero_positivo(n_max, "n_max")
        niveles = np.arange(1, n_max + 1)
        return (niveles**2) * self.RADIO_BOHR_A / self._z

    def transicion(self, n_inicial, n_final):
        """Transición n_inicial → n_final: ΔE, frecuencia y longitud de onda.

        El fotón tiene energía |ΔE|. Si el electrón baja de nivel es emisión;
        si sube, absorción.
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

    def __repr__(self):
        return f"BohrAtom(Z={self._z})"
