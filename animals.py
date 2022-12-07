class Animal:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, coord):
        self.x = coord[0]
        self.y = coord[1]


class Rabbit(Animal):
    def __init__(self, x, y, name):
        super().__init__(x, y)
        self.name = name
        self.type = 2
        self.min_escape_ver = 0.6
        self.is_tired = False

    def jump(self, coord):
        self.x = coord[0]
        self.y = coord[1]


class Squirrel(Animal):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = 3


class Tiger(Animal):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = 1
        self.is_hungry = True
        self.at_lair = True


if __name__ == '__main__':
    pass
