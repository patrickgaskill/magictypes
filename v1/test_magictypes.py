import unittest
import types
import magictypes

allprintings = magictypes.load_allprintings()
cardtypes = magictypes.load_cardtypes()


class CardTestCase(unittest.TestCase):
    def setUp(self):
        self.allprintings = allprintings
        self.cardtypes = cardtypes

    def find_card(self, set_code, card_name):
        card_model = next((c for c in self.allprintings[set_code]['cards']
                           if c['name'] == card_name), None)
        return types.SimpleNamespace(**card_model) if card_model else None


class ChangelingsTestCase(CardTestCase):
    def test_mistform_ultimus(self):
        self.assertTrue(
            magictypes.has_every_creature_type(
                self.find_card('LGN', 'Mistform Ultimus')))

    def test_amorphous_axe(self):
        self.assertFalse(
            magictypes.has_every_creature_type(
                self.find_card('MH1', 'Amorphous Axe')))

    def test_runed_stalactite(self):
        self.assertFalse(
            magictypes.has_every_creature_type(
                self.find_card('LRW', 'Runed Stalactite')))

    def test_crib_swap(self):
        self.assertTrue(
            magictypes.has_every_creature_type(
                self.find_card('LRW', 'Crib Swap')))

    def test_amoeboid_changeling(self):
        self.assertTrue(
            magictypes.has_every_creature_type(
                self.find_card('LRW', 'Amoeboid Changeling')))


class TokensTestCase(CardTestCase):
    pass


if __name__ == '__main__':
    unittest.main()