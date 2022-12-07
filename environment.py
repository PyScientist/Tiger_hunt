from animals import Tiger, Rabbit, Squirrel
import numpy as np
from ql_model import QlModel
import msvcrt
import random


def wait_for_next_step():
    print("\nPress Any key, to continue....")
    msvcrt.getch()


class Environment:
    def __init__(self, cols, rows):
        # cols = x coordinate, rows = y coordinate
        self.start_point = (0, 0)
        self.cols = cols
        self.rows = rows
        # Initialization of main field
        self.field = np.zeros((self.cols, self.rows), int)
        # Initialization of rewards array where tiger can go anywhere
        self.rewards = np.full((self.cols, self.rows), -1)
        self.animals = {}
        self.ql_model = None
        self.num_of_steps = 0

    def start(self):
        # Initialize animals
        self.animals['Tiger'] = Tiger(self.start_point[0], self.start_point[1])
        self.animals['Squirrel #1'] = Squirrel(3, 5)
        self.animals['Squirrel #2'] = Squirrel(4, 5)
        self.animals['Squirrel #3'] = Squirrel(5, 5)
        self.animals['Squirrel #4'] = Squirrel(6, 5)
        self.animals['Rabbit #1'] = Rabbit(7, 8, 'Rabbit #1')
        self.animals['Rabbit #2'] = Rabbit(8, 8, 'Rabbit #2')
        self.animals['Rabbit #3'] = Rabbit(9, 8, 'Rabbit #3')
        self.reward_update()

        while True:
            # Check is tiger at lair otr not
            self.check_tiger_is_home()
            # Check do we already catch the rabbit or not
            self.check_rabit_catch_or_not()
            self.check_is_the_tiger_near_rabbit()
            self.reward_update()
            self.show()
            if self.animals['Tiger'].at_lair and (self.animals['Tiger'].is_hungry is False):
                break
            self.step()
            # wait_for_next_step()

        print(self.num_of_steps)

    def reward_update(self):
        if self.animals['Tiger'].is_hungry:
            for animal in self.animals:
                if self.animals[animal].type == 3:  # for Squirrels
                    self.rewards[self.animals[animal].x, self.animals[animal].y] = -100
                if self.animals[animal].type == 2:
                    self.rewards[self.animals[animal].x, self.animals[animal].y] = 100
                if self.animals[animal].type == 1:
                    self.rewards[self.animals[animal].x, self.animals[animal].y] = -1
        else:
            for animal in self.animals:
                if self.animals[animal].type == 3:  # for Squirrels
                    self.rewards[self.animals[animal].x, self.animals[animal].y] = -100
                if self.animals[animal].type == 2:
                    self.rewards[self.animals[animal].x, self.animals[animal].y] = -10
                if self.animals[animal].type == 1:
                    self.rewards[self.animals[animal].x, self.animals[animal].y] = -1
            self.rewards[self.start_point[0], self.start_point[1]] = 100

    def step(self):
        self.num_of_steps += 1
        # Initialize the initial location of rewards corresponding to animals position
        # build ql_model for initial state
        self.ql_model = QlModel(self.animals['Tiger'].x, self.animals['Tiger'].y, self.rewards)
        # get next step cell from the shortest path
        self.animals['Tiger'].move(self.ql_model.shortest_path[1])

    def show(self):
        self.field = np.zeros((self.cols, self.rows), int)
        for animal in self.animals:
            self.field[self.animals[animal].x, self.animals[animal].y] = self.animals[animal].type
        print(self.field, '\n')

    def check_is_the_tiger_near_rabbit(self):

        def jump_aside(rabbit):

            directions = ['up', 'right', 'down', 'left']
            direction = directions[random.randint(0, 3)]
            cell_to_jump_is_not_available = False

            if direction == 'up':
                coords = (rabbit.x+1, rabbit.y)
            elif direction == 'down':
                coords = (rabbit.x-1, rabbit.y)
            elif direction == 'right':
                coords = (rabbit.x, rabbit.y+1)
            elif direction == 'left':
                coords = (rabbit.x, rabbit.y-1)
            else:
                coords = (rabbit.x, rabbit.y - 1)

            for key in self.animals:
                x = self.animals[key].x
                y = self.animals[key].y
                if (coords[0] == x) and (coords[1] == y) or (x >= self.rows) or (y >= self.cols):
                    cell_to_jump_is_not_available = True
                else:
                    pass

            if (rabbit.is_tired is False) and (cell_to_jump_is_not_available is False):
                rabbit.jump(coords)
                rabbit.is_tired = True
            else:
                print(f'{rabbit.name} try to escape but cell was absent or lies outside the visibility field')

        def escape(rabbit):
            rabbit_to_escape = rabbit.name
            print(rabbit_to_escape)
            jump_aside(rabbit)

        for animal in self.animals:
            if 'Rabbit' in animal:
                t_x = self.animals['Tiger'].x
                t_y = self.animals['Tiger'].y
                r_x = self.animals[animal].x
                r_y = self.animals[animal].y

                if (r_x == t_x+1) and (r_y == t_y):
                    escape(self.animals[animal])
                elif (r_x == t_x-1) and (r_y == t_y):
                    escape(self.animals[animal])
                elif (r_x == t_x) and (r_y == t_y+1):
                    escape(self.animals[animal])
                elif (r_x == t_x) and (r_y == t_y-1):
                    escape(self.animals[animal])
                else:
                    pass

    def check_rabit_catch_or_not(self):
        rabit_to_eat = None
        for animal in self.animals:
            if 'Rabbit' in animal:
                if (self.animals[animal].x == self.animals['Tiger'].x)\
                        and (self.animals[animal].y == self.animals['Tiger'].y):
                    self.animals['Tiger'].is_hungry = False
                    rabit_to_eat = self.animals[animal].name
        if rabit_to_eat is not None:
            self.animals.pop(rabit_to_eat)

    def check_tiger_is_home(self):
        if (self.animals['Tiger'].x == self.start_point[0]) and (self.animals['Tiger'].y == self.start_point[1]):
            self.animals['Tiger'].at_lair = True
        else:
            self.animals['Tiger'].at_lair = False

    def __show_reword(self):
        for row in self.rewards:
            print(row)


if __name__ == '__main__':
    pass
