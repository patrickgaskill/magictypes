import unittest
import types
import magictypes


class CardTestCase(unittest.TestCase):
    def setUp(self):
        self.allprintings = magictypes.load_allprintings()
        self.cardtypes = magictypes.load_cardtypes()

    def find_card(self, set_code, card_name):
        card_model = next((c for c in self.allprintings[set_code]['cards']
                           if c['name'] == card_name), None)
        return types.SimpleNamespace(**card_model) if card_model else None

    def test_changelings(self):
        self.assertTrue(
            magictypes.has_every_creature_type(
                self.find_card('LGN', 'Mistform Ultimus')))

        self.assertFalse(
            magictypes.has_every_creature_type(
                self.find_card('MH1', 'Amorphous Axe')))

        self.assertFalse(
            magictypes.has_every_creature_type(
                self.find_card('LRW', 'Runed Stalactite')))

        self.assertTrue(
            magictypes.has_every_creature_type(
                self.find_card('LRW', 'Crib Swap')))

        self.assertTrue(
            magictypes.has_every_creature_type(
                self.find_card('LRW', 'Amoeboid Changeling')))


if __name__ == '__main__':
    unittest.main()