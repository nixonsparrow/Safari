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


class TestRandomMovements(TestCase):
    def setUp(self):
        self.safari = Safari(20, 20)
        self.lion_male = Lion(self.safari, 'male')
        self.lion_female = Lion(self.safari, 'female')
        self.zebra = Zebra(self.safari, 'female')
        self.safari.insert(self.lion_male, (19, 19))
        self.safari.insert(self.lion_female, (0, 0))

    def test_random_movements(self):
        self.assertEqual(self.safari.find_object(self.lion_male), (19, 19))
        self.assertEqual(self.safari.find_object(self.lion_female), (0, 0))
        while self.safari.find_object(self.lion_male) == (19, 19) or self.safari.find_object(self.lion_female) == (0, 0):
            self.safari.make_random_moves()

        self.assertNotEqual(self.safari.find_object(self.lion_male), (19, 19))
        self.assertNotEqual(self.safari.find_object(self.lion_female), (0, 0))

    def test_eat_on_random_movements(self):
        self.safari_small = Safari(3, 3)
        zebra = Zebra(self.safari_small, 'female')
        lion = Lion(self.safari_small, 'female')
        self.safari_small.insert(zebra, (0, 0))
        self.safari_small.insert(lion, (2, 2))
        while self.safari_small.find_object(zebra):
            self.safari_small.make_random_moves()
        self.assertIn(zebra, self.safari_small.graveyard)
        self.assertFalse(self.safari_small.find_object(zebra))
        self.assertTrue(self.safari_small.find_object(lion))

    def test_random_movements_epic_style(self):
        i = 0
        [self.safari.insert(Zebra(self.safari, 'female'), (x, 18)) for x in range(20)]
        while i < 1000:
            self.safari.make_random_moves()
            i += 1

        # for field in self.safari.fields.values():
        #     if field:
        #         for obj in field:
        #             print(obj, obj.age)
        # print(self.safari.graveyard, len(self.safari.graveyard))
