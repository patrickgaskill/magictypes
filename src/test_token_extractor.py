def test_decree_of_justice(get_card, extractor):
    card = get_card("Decree of Justice")
    tokens = extractor.extract(card)
    assert len(tokens) == 2
    angel, soldier = tokens
    assert angel.supertypes == []
    assert angel.types == ["Creature"]
    assert angel.subtypes == ["Angel"]
    assert soldier.supertypes == []
    assert soldier.types == ["Creature"]
    assert soldier.subtypes == ["Soldier"]
