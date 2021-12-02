from unittest import TestCase
from models import Safari, Lion, Plant


class TestAnimals(TestCase):
    def setUp(self):
        self.safari = Safari(2, 2)
        self.lion_male = Lion(self.safari, 'male')
        self.lion_female = Lion(self.safari, 'female')
        self.safari.insert(self.lion_male, (0, 0))
        self.safari.insert(self.lion_female, (1, 0))

    def test_creation(self):
        self.assertEqual(self.lion_male.species, 'lion')
        self.assertEqual(self.lion_female.species, 'lion')
        self.assertEqual(self.lion_male.sex, 'male')
        self.assertEqual(self.lion_female.sex, 'female')

    def test_movement(self):
        self.assertEqual(self.safari.find_object(self.lion_male), (0, 0))
        self.lion_male.move_on_field((0, 1))
        self.assertIsNot(self.lion_male, self.safari.field(0, 0))
        self.assertIs(self.lion_male, self.safari.field(0, 1))

        self.lion_male.move('E', 1)
        self.assertIsNot(self.lion_male, self.safari.field(0, 1))
        self.assertIs(self.lion_male, self.safari.field(1, 1))
        self.lion_male.move('SW', 1)
        self.assertIs(self.lion_male, self.safari.field(0, 0))

        self.assertRaises(ValueError, self.lion_male.move, 'SD', 1)
        self.assertRaises(KeyError, self.lion_male.move, 'S', 1)


class TestPlants(TestCase):
    def setUp(self):
        self.plant = Plant()

    def test_creation(self):
        self.assertFalse(self.plant.eatable)
        self.assertFalse(self.plant.obstacle)
        self.assertEqual(self.plant.symbol, '.')


class TestSafari(TestCase):
    def setUp(self):
        self.safari = Safari(2, 2)
        self.lion_male = Lion(self.safari, 'male')
        self.lion_female = Lion(self.safari, 'female')

    def test_creation(self):
        self.assertEqual(self.safari.fields, {(0, 0): [], (1, 0): [], (0, 1): [], (1, 1): []})

    def test_insertion(self):
        self.assertIsNot(self.lion_male, self.safari.field(0, 0))
        self.safari.insert(self.lion_male, (0, 0))
        self.assertIs(self.lion_male, self.safari.field(0, 0))

        self.assertRaises(EnvironmentError, self.safari.insert, self.lion_female, (0, 0))
        self.safari.insert(self.lion_female, (0, 1))
        self.assertRaises(EnvironmentError, self.safari.insert, self.lion_female, (1, 0))

    def test_visualisation(self):
        self.safari.insert(self.lion_male, (0, 0))
        self.assertEqual(self.safari.visualise(), '----\n|  |\n|L | lion (lion)\n----')
        self.lion_male.move_on_field((1, 0))
        self.assertEqual(self.safari.visualise(), '----\n|  |\n| L| lion (lion)\n----')


class TestRandomMovements(TestCase):
    def setUp(self):
        self.safari = Safari(20, 20)
        self.lion_male = Lion(self.safari, 'male')
        self.lion_female = Lion(self.safari, 'female')
        self.safari.insert(self.lion_male, (19, 19))
        self.safari.insert(self.lion_female, (0, 0))

    def test_random_movements(self):
        self.assertEqual(self.safari.find_object(self.lion_male), (19, 19))
        self.assertEqual(self.safari.find_object(self.lion_female), (0, 0))
        while self.safari.find_object(self.lion_male) == (19, 19) or self.safari.find_object(self.lion_female) == (0, 0):
            self.safari.make_random_moves()

        self.assertNotEqual(self.safari.find_object(self.lion_male), (19, 19))
        self.assertNotEqual(self.safari.find_object(self.lion_female), (0, 0))

