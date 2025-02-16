from collections import namedtuple
import numpy as np
import torch

Transition = namedtuple('Transition', ('state', 'action', 'next_state', 'reward', 'terminal'))


class ReplayMemory:
    """ Memory of an Deep Q-Network agent

    Parameters
    -----------
    input_shape: array-like or tuple
        size of the input to the network
    max_capacity: int
        maximum number of stored memories

    Attributes
    -----------
    counter: int
        how many times we pushed new observations
    states: nd-array
        nd-array containing all states in memory
    actions: array-like
        array with all actions that were taken
    next_states: nd-array
        nd-array with new state s' after action a
    rewards: array-like
        array of rewards for taking action a in state s
    terminals: array-like
        array of elements signaling whether the episode has terminated
    """

    def __init__(self, input_shape, max_capacity=int(1e6)):
        self.max_capacity = max_capacity
        self.counter = 0

        self.states = [np.zeros((4, 84, 84), dtype=np.uint8)] * self.max_capacity
        self.actions = np.zeros(self.max_capacity, dtype=np.int8)
        self.next_states = [np.zeros((4, 84, 84), dtype=np.uint8)] * self.max_capacity
        self.rewards = np.zeros(self.max_capacity, dtype=np.int8)
        self.terminals = np.zeros(self.max_capacity, dtype=np.bool)

    def push(self, *args):
        """ Adds a new transition to memory
        Parameters
        -----------
        args : tuple
            transition tuple (state, action, next_state, reward, terminal)
        """
        # Unpack the transition tuple
        self.assign(Transition(*args))
        # Update current index
        self.counter += 1

    def sample(self, n_transitions):
        """ Samples a number of random transitions from memory
        Parameters
        -----------
        n_transitions: int
            number of samples to return

        Returns
        -----------
        transitions: tuple of array-like objects
            tuples (state, action, next_state, reward, terminal)
            each tuple element of n_transitions length
        """
        # memory might not be full, so don't sample over all elements
        max_idx = min(self.counter, self.max_capacity)
        indices = np.random.choice(max_idx, n_transitions, replace=False)
        states = np.stack([self.states[i] for i in indices], axis=0)
        next_states = np.stack([self.next_states[i] for i in indices], axis=0)
        return states, self.actions[indices], next_states, self.rewards[indices], self.terminals[indices]

    def assign(self, transition):
        """ Unpacks the transition to memory """
        # if memory full start overwriting oldest elements
        next_available = self.counter if self.counter < self.max_capacity else self.counter % self.max_capacity

        self.states[next_available] = transition.state
        self.next_states[next_available] = transition.next_state
        self.rewards[next_available] = transition.reward
        self.actions[next_available] = transition.action
        self.terminals[next_available] = transition.terminal
