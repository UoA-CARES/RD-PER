import torch
import numpy as np

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

class ReplayBuffer(object):
    def __init__(self, state_dim, action_dim, max_capacity=int(1e6)):
        self.max_size = max_capacity
        self.ptr = 0
        self.size = 0

        self.state = np.zeros((max_capacity, state_dim))
        self.action = np.zeros((max_capacity, action_dim))
        self.next_state = np.zeros((max_capacity, state_dim))
        self.reward = np.zeros((max_capacity, 1))
        self.done = np.zeros((max_capacity, 1))

        self.device = DEVICE

    def add(self, state, action, reward, next_state, done):
        self.state[self.ptr] = state
        self.action[self.ptr] = action
        self.next_state[self.ptr] = next_state
        self.reward[self.ptr] = reward
        # self.not_done[self.ptr] = 1. - done
        self.done[self.ptr] = done

        self.ptr = (self.ptr + 1) % self.max_size
        self.size = min(self.size + 1, self.max_size)

    def sample(self, batch_size):
        ind = np.random.randint(self.size, size=batch_size)

        # return self.state[ind], self.action[ind], self.reward[ind], self.next_state[ind], self.done[ind]

        return (
            torch.FloatTensor(self.state[ind]).to(self.device),
            torch.FloatTensor(self.action[ind]).to(self.device),
            torch.FloatTensor(self.reward[ind]).to(self.device),
            torch.FloatTensor(self.next_state[ind]).to(self.device),
            torch.FloatTensor(self.done[ind]).to(self.device)
        )