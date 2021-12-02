from unittest import TestCase
from models import Safari, Lion


class TestAnimals(TestCase):
    def setUp(self) -> None:
        self.lion_male = Lion('male')
        self.lion_female = Lion('female')

    def test_creation(self):
        self.assertEqual(self.lion_male.species, 'lion')
        self.assertEqual(self.lion_female.species, 'lion')
        self.assertEqual(self.lion_male.sex, 'male')
        self.assertEqual(self.lion_female.sex, 'female')


class TestSafari(TestCase):
    def setUp(self):
        self.safari = Safari(2, 2)

    def test_creation(self):

        self.assertEqual(self.safari.fields, {(0, 0): None, (1, 0): None, (0, 1): None, (1, 1): None})
