from unittest import TestCase
from models.safari import Safari
from models.animals import Lion, Zebra


class TestAnimals(TestCase):
    def setUp(self):
        self.safari = Safari(2, 2)
        self.lion_male = Lion(self.safari, 'male')
        self.lion_female = Lion(self.safari, 'female')
        self.zebra = Zebra(self.safari, 'female')
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

    def test_possible_directions(self):
        self.assertEqual(self.lion_male.possible_directions(), ['N', 'E', 'NE'])
        self.assertEqual(self.lion_female.possible_directions(), ['N', 'W', 'NW'])

    def test_move(self):
        self.assertEqual(self.lion_male.safari.field(0, 0), self.lion_male)
        self.assertNotEqual(self.lion_male.safari.field(0, 1), self.lion_male)
        self.lion_male.move('N', 1)
        self.assertEqual(self.lion_male.safari.field(0, 1), self.lion_male)
        self.assertNotEqual(self.lion_male.safari.field(0, 0), self.lion_male)

    def test_encounter_lion_eats_zebra(self):
        self.assertEqual(self.safari.find_object(self.lion_male), (0, 0))
        self.safari.insert(self.zebra, (0, 1))
        self.safari.encounter({}, self.zebra, self.lion_male)
        self.assertEqual(self.safari.find_object(self.lion_male), (0, 1))
        self.assertNotEqual(self.safari.find_object(self.lion_male), (0, 0))

    def test_lion_moves_and_eats_zebra(self):
        self.assertEqual(self.safari.find_object(self.lion_male), (0, 0))
        self.safari.insert(self.zebra, (0, 1))
        self.lion_male.move('N', 1)
        self.assertEqual(self.safari.find_object(self.lion_male), (0, 1))
        self.assertNotEqual(self.safari.find_object(self.lion_male), (0, 0))
        self.assertIn('eaten', self.safari.graveyard[self.zebra])

    def test_rest_in_peace(self):
        self.assertTrue(self.safari.find_object(self.lion_male))
        self.assertNotIn(self.lion_male, self.safari.graveyard)
        self.lion_male.rest_in_peace()
        self.assertFalse(self.safari.find_object(self.lion_male))
        self.assertIn(self.lion_male, self.safari.graveyard)
        self.assertEqual(self.safari.graveyard[self.lion_male], 'natural death')

    def test_birth_control(self):
        self.assertFalse('What about birth control, compadre?')
