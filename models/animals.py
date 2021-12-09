import random


all_possible_directions = ['N', 'S', 'E', 'W', 'NE', 'NW', 'SE', 'SW']


class Animal:
    def __init__(self, safari, species, predator, sex, symbol, name=None):
        if sex not in ['male', 'female']:
            raise ValueError

        self.safari = safari
        self.sex = sex
        self.species = species
        self.symbol = symbol
        self.predator = predator
        self.name = name

        self.kingdom = 'animal'
        self.age = 0
        self.alive = True

    def move_on_field(self, new_field):
        old_field = self.safari.find_object(self)
        if not self.safari.fields[new_field]:
            self.safari.fields[old_field].remove(self)
            self.safari.fields[new_field].append(self)
            return True
        else:
            self.safari.encounter({}, self.safari.field(new_field[0], new_field[1]), self)
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
        try:
            new_field = old_field[0] + x, old_field[1] + y
            if new_field in self.safari.fields:
                return new_field
        except TypeError:
            pass
        return False

    def move(self, direction, distance):
        self.move_on_field(self.field_to_move(direction, distance))

    def eat(self, target, fields_engaged=None):
        field = self.safari.find_object(target)

        if fields_engaged:
            for k, v in fields_engaged:
                if v == target:
                    del fields_engaged[k]

        self.safari.put_in_graveyard(target, 'eaten')
        self.move_on_field(field)

        return fields_engaged

    def procreate(self, target):
        female = [animal for animal in [self, target] if animal.sex == 'female'][0]
        female_x, female_y = self.safari.find_object(female)
        new_born = type(target)(self.safari, random.choice(['female', 'male']))
        for x, y in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            try:
                self.safari.insert(new_born, (female_x + x, female_y + y))
            except EnvironmentError:
                pass

    def __str__(self):
        return f'{self.name if self.name else self.species} ({self.species})'


class Lion(Animal):
    def __init__(self, safari, sex, name=''):
        species = 'lion'
        symbol = 'L'
        predator = True
        super().__init__(safari=safari, species=species, predator=predator, sex=sex,
                         symbol=symbol, name=name)


class Zebra(Animal):
    def __init__(self, safari, sex, name=''):
        species = 'zebra'
        symbol = 'Z'
        predator = False
        super().__init__(safari=safari, species=species, predator=predator, sex=sex,
                         symbol=symbol, name=name)
