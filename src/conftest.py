import pytest
import magictypes
from token_extractor import TokenExtractor


@pytest.fixture(scope="session")
def cards():
    return magictypes.load_cards()


@pytest.fixture(scope="session")
def get_card(cards):
    def _get_card(name):
        return next(
            (c for c in cards if c.name == name),
            None,
        )

    return _get_card


@pytest.fixture(scope="session")
def extractor():
    return TokenExtractor()