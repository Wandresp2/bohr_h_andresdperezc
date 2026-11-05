"""Pruebas de la física de Bohr. Ejecutar con: pytest -v"""

import numpy as np
import pytest

from bohr_h_andresdperezc import BohrAtom, Transicion


def test_energia_fundamental_hidrogeno():
    assert BohrAtom(1).energia(1) == pytest.approx(-13.6)


def test_radio_bohr_hidrogeno():
    assert BohrAtom(1).radio(1) == pytest.approx(0.529)


def test_energia_proporcional_a_uno_sobre_n_cuadrado():
    h = BohrAtom(1)
    assert h.energia(2) == pytest.approx(h.energia(1) / 4)
    assert h.energia(3) == pytest.approx(h.energia(1) / 9)


def test_energia_proporcional_a_z_cuadrado():
    h = BohrAtom(1)
    he = BohrAtom(2)
    assert he.energia(1) == pytest.approx(4 * h.energia(1))


def test_radio_crece_con_n_cuadrado_y_cae_con_z():
    h = BohrAtom(1)
    assert h.radio(2) == pytest.approx(4 * h.radio(1))
    assert BohrAtom(2).radio(1) == pytest.approx(h.radio(1) / 2)


def test_balmer_hidrogeno_3_a_2_es_emision_656_nm():
    transicion = BohrAtom(1).transicion(3, 2)
    assert isinstance(transicion, Transicion)
    assert transicion.tipo == "emision"
    assert transicion.delta_e < 0
    assert transicion.energia_foton == pytest.approx(abs(transicion.delta_e))
    assert transicion.longitud_onda == pytest.approx(656, abs=2)


def test_subir_de_nivel_es_absorcion():
    transicion = BohrAtom(1).transicion(2, 3)
    assert transicion.tipo == "absorcion"
    assert transicion.delta_e > 0
    assert transicion.longitud_onda == pytest.approx(
        BohrAtom(1).transicion(3, 2).longitud_onda
    )


def test_energias_y_radios_hasta_n_max():
    h = BohrAtom(1)
    energias = h.energias(3)
    radios = h.radios(3)
    assert energias.shape == (3,)
    assert radios.shape == (3,)
    assert np.allclose(energias, [h.energia(n) for n in (1, 2, 3)])
    assert np.allclose(radios, [h.radio(n) for n in (1, 2, 3)])


@pytest.mark.parametrize("z", [0, -1, 1.5, True, "1", 1.0])
def test_z_invalido(z):
    with pytest.raises(ValueError):
        BohrAtom(z)


@pytest.mark.parametrize("n", [0, -2, 2.5, False, 1.0])
def test_n_invalido(n):
    h = BohrAtom(1)
    with pytest.raises(ValueError):
        h.energia(n)
    with pytest.raises(ValueError):
        h.radio(n)


def test_transicion_al_mismo_nivel():
    with pytest.raises(ValueError):
        BohrAtom(1).transicion(2, 2)
