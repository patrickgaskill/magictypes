import pytest

from mtgjsondata import MtgjsonData
from tokenextractor import TokenExtractor


@pytest.fixture(scope="session")
def mtgjsondata():
    return MtgjsonData()


@pytest.fixture(scope="session")
def extractor():
    return TokenExtractor()
