import pytest


def test_dungeon_release_date(mtgjsondata):
    card = mtgjsondata.get_card_by_name("Dungeon of the Mad Mage")
    assert card.set_code == "TAFR"
    assert card.release_date == "2021-07-23"
