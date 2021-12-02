import os
import random
from time import sleep


all_possible_directions = ['N', 'S', 'E', 'W', 'NE', 'NW', 'SE', 'SW']


class Safari:
    def __init__(self, height, width):
        self.width = width
        self.height = height

        self.fields = {(x, y): [] for x in range(self.width) for y in range(self.height)}

    def insert(self, object_to_insert, slot):
        if self.fields[slot]:
            raise EnvironmentError(f'There is no space for {object_to_insert}.')
        elif self.find_object(object_to_insert):
            raise EnvironmentError(f'{object_to_insert} is already in that Safari.')

        self.fields[slot].append(object_to_insert)

    def field(self, x, y):
        return self.fields[(x, y)][0] if len(self.fields[(x, y)]) else self.fields[(x, y)]

    def find_object(self, object_to_find):
        for key, values in self.fields.items():
            if object_to_find in values:
                return key
        return False

    def get_animals(self):
        return [value[0] for field, value in self.fields.items() if value]

    def make_random_moves(self):
        for animal in self.get_animals():
            try:
                animal.move(random.choice(animal.possible_directions()), random.randint(0, 1))
            except KeyError:
                pass

    def visualise(self, println=False):
        print('\n' * 50) if println else None
        picture = ''
        picture += '-' * (self.width + 2) + '\n'
        for col in reversed(range(self.height)):
            picture += '|'
            side_comments = ''
            for row in range(self.width):
                if self.fields[row, col]:
                    picture += self.fields[row, col][0].symbol
                    side_comments += ', ' if side_comments else ''
                    side_comments += ' ' + self.fields[row, col][0].__str__()
                else:
                    picture += ' '
            picture += f'|{side_comments if side_comments else ""}\n'
        picture += '-' * (self.width + 2)
        if println:
            print(picture)
        return picture


class Animal:
    def __init__(self, safari, species, sex, symbol, name=None):
        if sex not in ['male', 'female']:
            raise ValueError

        self.safari = safari
        self.sex = sex
        self.species = species
        self.symbol = symbol
        self.name = name

        self.age = 0
        self.alive = True

    def move_on_field(self, new_field):
        old_field = self.safari.find_object(self)
        if not self.safari.fields[new_field]:
            self.safari.fields[old_field].remove(self)
            self.safari.fields[new_field].append(self)
            return True
        else:
            return False

    def possible_directions(self):
        return [direction for direction in all_possible_directions if self.field_to_move(direction, 1)]

    def field_to_move(self, direction, distance):
        old_field = self.safari.find_object(self)
        if direction not in all_possible_directions:
            raise ValueError('It is possible to move either: [N]orth, [S]outh, [E]ast, [W]est or combination S/N + E/W.')
        x, y = 0, 0
        if 'N' in direction:
            y = distance
        elif 'S' in direction:
            y = - distance
        if 'E' in direction:
            x = distance
        elif 'W' in direction:
            x = - distance
        new_field = old_field[0] + x, old_field[1] + y
        return new_field

    def move(self, direction, distance):
        self.move_on_field(self.field_to_move(direction, distance))

    def __str__(self):
        return f'{self.name if self.name else self.species} ({self.species})'


class Lion(Animal):
    def __init__(self, safari, sex, name=''):
        species = 'lion'
        symbol = 'L'
        super().__init__(safari, species, sex, symbol, name)


class Plant:
    def __init__(self, eatable=False, obstacle=False):
        self.eatable = eatable
        self.obstacle = obstacle
        self.symbol = 'T' if obstacle else '.'
