import numpy as np

# class QlModel based on  explanation of Dr. Soper
#
# (Foundations of Q-Learning) https://www.youtube.com/watch?v=__t2XRxXGxI
# Discusses the foundations of Q-learning,
# which is one of the major types of reinforcement learning within the broader realm of
# artificial intelligence and cognitive computing systems. Topics of discussion include
# what Q-learning is, characteristics of Q-learning models, what Q-values are, what
# temporal differences are, what the Bellman Equation is, and how the Q-learning process works.

# (A Profit-Maximizing Reinforcement Learning-Based AI System in Python): https://youtu.be/2Q9s2Rlzo0E
# Presents a complete walk-through (tutorial) of a Q-learning-based AI system written in Python.
# The video demonstrates how to define the environment's states, actions, and rewards, and how to train
# an AI agent to identify an optimal policy by using Q-learning. The business problem presented in the
# video is for an AI agent to learn to control warehouse robots such that a robot can take the shortest
# path between any point in the warehouse and the item packaging area, while simultaneously learning
# to avoid crashing into any shelves or other item storage locations.


class QlModel:
    def __init__(self, x, y, rewards):

        # Define initial position of AI agent
        self.x = x
        self.y = y

        # Read reward matrix from input
        self.rewards = rewards
        # Initialize q_values 3d matrix
        self.q_values = np.zeros((self.rewards.shape[0], self.rewards.shape[1], 4))

        # Numeric action code 0-up, 1-right, 2-down, 3-left
        self.actions = ['up', 'right', 'down', 'left']

        # Define training parameters
        self.epsilon = 0.9  # the percentage of time when we should take the best action (instead of a random action)
        self.discount_factor = 0.9  # discount factor for future rewards
        self.learning_rate = 0.9  # the rate at which the AI agent should learn
        self.epochs = 1000

        # Launch model training
        self.train()

        # Got the shortest path into attribute
        self.shortest_path = self.get_shortest_path(self.x, self.y)

    # define a function that determines if the specified location is a terminal state
    def is_terminal_state(self, current_row_index, current_column_index):
        # if the reward for this location is -1, then it is not a terminal state (i.e., it is a 'white square')
        if self.rewards[current_row_index, current_column_index] == -1.:
            return False
        else:
            return True

    # define a function that will choose a random, non-terminal starting location
    def set_starting_location(self):
        return self.x,  self.y

    # define an epsilon greedy algorithm that will choose which action to take next (i.e., where to move next)
    def get_next_action(self, current_row_index, current_column_index, epsilon):
        # if a randomly chosen value between 0 and 1 is less than epsilon,
        # then choose the most promising value from the Q-table for this state.
        if np.random.random() < epsilon:
            return np.argmax(self.q_values[current_row_index, current_column_index])
        else:  # choose a random action
            return np.random.randint(4)

    # define a function that will get the next location based on the chosen action
    def get_next_location(self, current_row_index, current_column_index, action_index):
        new_row_index = current_row_index
        new_column_index = current_column_index
        if self.actions[action_index] == 'up' and current_row_index > 0:
            new_row_index -= 1
        elif self.actions[action_index] == 'right' and current_column_index < self.rewards.shape[1] - 1:
            new_column_index += 1
        elif self.actions[action_index] == 'down' and current_row_index < self.rewards.shape[0] - 1:
            new_row_index += 1
        elif self.actions[action_index] == 'left' and current_column_index > 0:
            new_column_index -= 1
        return new_row_index, new_column_index

    # Define a function that will get the shortest path between any location within the warehouse that
    # the robot is allowed to travel and the item packaging location.
    def get_shortest_path(self, start_row_index, start_column_index):
        # return immediately if this is an invalid starting location
        if self.is_terminal_state(start_row_index, start_column_index):
            return []
        else:  # if this is a 'legal' starting location
            current_row_index, current_column_index = start_row_index, start_column_index
            shortest_path = list()
            shortest_path.append([current_row_index, current_column_index])
            # continue moving along the path until we reach the goal (i.e., the item packaging location)
            while not self.is_terminal_state(current_row_index, current_column_index):
                # get the best action to take
                action_index = self.get_next_action(current_row_index, current_column_index, 1.)
                # move to the next location on the path, and add the new location to the list
                current_row_index, current_column_index = self.get_next_location(current_row_index,
                                                                                 current_column_index,
                                                                                 action_index)
                shortest_path.append([current_row_index, current_column_index])
            return shortest_path

    def train(self):
        # run through 1000 training episodes
        for episode in range(self.epochs):
            # get the starting location for this episode
            row_index, column_index = self.set_starting_location()

            # continue taking actions (i.e., moving) until we reach a terminal state
            # (i.e., until we reach the item packaging area or crash into an item storage location)
            while not self.is_terminal_state(row_index, column_index):
                # choose which action to take (i.e., where to move next)
                action_index = self.get_next_action(row_index, column_index, self.epsilon)

                # perform the chosen action, and transition to the next state (i.e., move to the next location)
                old_row_index, old_column_index = row_index, column_index  # store the old row and column indexes
                row_index, column_index = self.get_next_location(row_index, column_index, action_index)

                # receive the reward for moving to the new state, and calculate the temporal difference
                reward = self.rewards[row_index, column_index]
                old_q_value = self.q_values[old_row_index, old_column_index, action_index]
                temporal_difference = reward + (
                            self.discount_factor * np.max(self.q_values[row_index, column_index])) - old_q_value

                # update the Q-value for the previous state and action pair
                new_q_value = old_q_value + (self.learning_rate * temporal_difference)
                self.q_values[old_row_index, old_column_index, action_index] = new_q_value


if __name__ == '__main__':
    pass
