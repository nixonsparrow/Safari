from unittest import TestCase
from models.environment import Plant


class TestPlants(TestCase):
    def setUp(self):
        self.plant = Plant()

    def test_creation(self):
        self.assertFalse(self.plant.eatable)
        self.assertFalse(self.plant.obstacle)
        self.assertEqual(self.plant.symbol, '.')
