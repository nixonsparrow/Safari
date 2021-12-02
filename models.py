class Animal:
    def __init__(self, species, sex):
        if sex not in ['male', 'female']:
            raise ValueError
        self.sex = sex
        self.species = species

        self.age = 0


class Lion(Animal):
    def __init__(self, sex):
        species = 'lion'
        super().__init__(species, sex)


class Safari:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.fields = {(x, y): None for x in range(self.width) for y in range(self.height)}


if __name__ == '__main__':
    print(Safari(10, 5).fields)
