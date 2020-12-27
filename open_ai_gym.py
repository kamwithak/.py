"""

An online implementation of Open AI's Gym can be found in this GitHub repo:
- https://gist.github.com/HenryJia/23db12d61546054aa43f8dc587d9dc2c

Target State: [0, 0, 0, np.pi]

"""

import numpy as np
import gym

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))

env = gym.make('CartPole-v0')
desired_mask = np.array([0, 0, 1, 0])
desired_target = np.array([0, 0, 0, np.pi])

P, I, D = 0.1, 0.01, 0.5

for i_episode in range(20):
    state = env.reset()
    integral = 0
    derivative = 0
    prev_error = 0
    for t in range(500):
        env.render()
        error = state-desired_target

        integral += error
        derivative = error-prev_error
        prev_error = error

        pid = np.dot(P*error + I*integral + D*derivative, desired_mask)
        action = sigmoid(pid)
        action = np.round(action).astype(np.int32)

        state, reward, done, info = env.step(action)
        if done:
            print("Episode finished after {} timesteps".format(t+1))
            break
env.close()
