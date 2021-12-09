from unittest import TestCase
from models.safari import Safari
from models.animals import Lion, Zebra


class TestSafari(TestCase):
    def setUp(self):
        self.safari = Safari(2, 2)
        self.lion_male = Lion(self.safari, 'male')
        self.lion_female = Lion(self.safari, 'female')
        self.zebra = Zebra(self.safari, 'female')

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

    def test_count_species(self):
        self.assertEqual(self.safari.count_animals('lion'), 0)
        self.assertEqual(self.safari.count_animals('zebra'), 0)
        self.safari.insert(self.lion_male, (0, 0))
        self.assertEqual(self.safari.count_animals('lion'), 1)
        self.safari.insert(self.lion_female, (0, 1))
        self.safari.insert(self.zebra, (1, 1))
        self.assertEqual(self.safari.count_animals('lion'), 2)
        self.assertEqual(self.safari.count_animals('zebra'), 1)

    def test_get_species(self):
        self.assertFalse(self.safari.get_species())
        self.safari.insert(self.lion_male, (0, 0))
        self.assertEqual(self.safari.get_species(), {'lion'})
        self.safari.insert(self.zebra, (1, 1))
        self.assertEqual(self.safari.get_species(), {'zebra', 'lion'})

    def test_find_free_side_edge_slot(self):
        self.assertEqual(self.safari.find_free_side_edge_slot(), (0, 0))
        self.safari.insert(self.zebra, (0, 0))
        self.assertEqual(self.safari.find_free_side_edge_slot(), (0, 1))

    def test_find_free_side_edge_slot_and_insert_in_it(self):
        self.assertEqual(self.safari.find_free_side_edge_slot(), (0, 0))
        self.safari.insert(self.zebra, self.safari.find_free_side_edge_slot())
        self.assertEqual(self.safari.find_free_side_edge_slot(), (0, 1))
