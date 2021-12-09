import random
import sys


all_possible_directions = ['N', 'S', 'E', 'W', 'NE', 'NW', 'SE', 'SW']


class Safari:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.graveyard = {}

        self.fields = {(x, y): [] for x in range(self.width) for y in range(self.height)}

    def find_free_side_edge_slot(self):
        for x in range(self.height):
            for y in [0, self.width - 1]:
                if not self.field(x, y):
                    return x, y

    def insert(self, object_to_insert, slot=None):
        if not slot:
            self.find_free_side_edge_slot()
        if self.fields[slot]:
            raise EnvironmentError(f'There is no space for {object_to_insert}.')
        elif self.find_object(object_to_insert):
            raise EnvironmentError(f'{object_to_insert} is already in that Safari.')

        self.fields[slot].append(object_to_insert)

    def remove(self, object_to_remove):
        self.fields[self.find_object(object_to_remove)].remove(object_to_remove)

    def put_in_graveyard(self, target, cause):
        self.remove(target)
        self.graveyard[target] = cause

    def field(self, x, y):
        return self.fields[(x, y)][0] if len(self.fields[(x, y)]) else self.fields[(x, y)]

    def find_object(self, object_to_find):
        for key, values in self.fields.items():
            if object_to_find in values:
                return key
        return False

    def get_species(self):
        return set([animal.species for animal in self.get_animals()])

    def get_animals(self, species=None):
        all_animals = [value[0] for field, value in self.fields.items() if value]
        if species:
            return [animal for animal in all_animals if animal.species == species]
        return all_animals

    def count_animals(self, species=None):
        return len(self.get_animals(species=species))

    def encounter(self, fields_engaged, the_object, another_object):

        if the_object.kingdom == 'animal' and another_object.kingdom == 'animal':
            if the_object.predator and not another_object.predator:
                the_object.eat(another_object)
            elif not the_object.predator and another_object.predator:
                another_object.eat(the_object)
            else:
                pass

        return fields_engaged

    def make_random_moves(self):
        fields_engaged = {}
        for animal in self.get_animals():
            try:            # ADD CURRENT FIELD
                fields_engaged[self.find_object(animal)] = animal
                            # PREDICT MOVE
                try:
                    direction, distance = random.choice(animal.possible_directions()), random.randint(0, 1)
                    field_to_move = animal.field_to_move(direction, distance)
                            # CHECK FIELD FROM MOVEMENT PREDICTION
                    if self.field(field_to_move[0], field_to_move[1]):
                        for an_object in self.fields[(field_to_move[0], field_to_move[1])]:
                            fields_engaged = self.encounter(fields_engaged, animal, an_object)
                    else:   # IF NO ENCOUNTER - MOVE
                        animal.move(random.choice(animal.possible_directions()), random.randint(0, 1))

                        fields_engaged[self.find_object(animal)] = animal
                except IndexError:
                    pass
            except KeyError:
                pass

    def visualise(self, println=False, count_species=False):
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
        if count_species:
            counted_species = [f' {species}: {self.count_animals(species)}' for species in self.get_species()]
            for c_species in counted_species:
                picture += c_species
        if println:
            sys.stdout.write(picture + '\n')
        return picture


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


class Plant:
    def __init__(self, eatable=False, obstacle=False):
        self.eatable = eatable
        self.obstacle = obstacle
        self.symbol = 'T' if obstacle else '.'
        self.kingdom = 'plant'
