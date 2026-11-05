"""Núcleo del modelo de Bohr.

En esta fase el paquete solo expone la clase ``BohrAtom`` con las constantes
físicas encapsuladas. Los cálculos, validaciones y gráficos se agregan en
fases posteriores.
"""


class BohrAtom:
    """Átomo hidrogenoide según el modelo de Bohr.

    Parameters
    ----------
    Z : int, optional
        Número atómico (carga nuclear). El hidrógeno es ``Z=1``.
        El valor no se valida todavía; eso corresponde a la fase 2.
    """

    # Valores de libro (didácticos). Hay que validar el desarrollo si se expande.
    ENERGIA_RYDBERG_EV = 13.6
    RADIO_BOHR_A = 0.529
    PLANCK_J_S = 6.62607015e-34
    VELOCIDAD_LUZ_M_S = 299792458.0
    MASA_ELECTRON_KG = 9.1093837139e-31
    CARGA_ELEMENTAL_C = 1.602176634e-19

    def __init__(self, Z=1):
        self._z = Z

    @property
    def Z(self):
        """Número atómico (carga nuclear efectiva)."""
        return self._z

    def __repr__(self):
        return f"BohrAtom(Z={self._z})"
