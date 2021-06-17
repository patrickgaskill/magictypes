import pytest

from mtgjsondata import MtgjsonData


@pytest.fixture(scope="session")
def mtgjsondata():
    return MtgjsonData()
