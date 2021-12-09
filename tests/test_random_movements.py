from unittest import TestCase
from models.safari import Safari
from models.animals import Lion, Zebra


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
