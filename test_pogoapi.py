# test pogoapi.py


import pogoapi
import pytest


def test_number_of_types():
    assert len(pogoapi.type_effectiveness.keys()) == 18


@pytest.fixture
def fighting():
    return pogoapi.type_effectiveness['Fighting']


def test_fighting_is_super_effective_against_normal(fighting):
    assert fighting['Normal'] == pogoapi.SUPER_EFFECTIVE


def test_fighting_is_normal_against_dragon(fighting):
    assert fighting['Dragon'] == pogoapi.NORMAL


def test_fighting_is_not_very_effective_against_bug(fighting):
    assert fighting['Bug'] == pogoapi.NOT_VERY_EFFECTIVE


def test_fighting_is_ineffective_against_ghost(fighting):
    assert fighting['Ghost'] == pogoapi.INEFFECTIVE
