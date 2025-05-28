import gym
from stable_baselines3 import PPO
from stable_baselines3.common.envs import DummyVecEnv

class SimpleTherapyEnv(gym.Env):
    def __init__(self):
        super(SimpleTherapyEnv, self).__init__()
        self.observation_space = gym.spaces.Discrete(5)
        self.action_space = gym.spaces.Discrete(3)
        self.state = 0

    def reset(self):
        self.state = 0
        return self.state

    def step(self, action):
        reward = 1 if action == (self.state % 3) else 0
        self.state = (self.state + 1) % 5
        done = False
        return self.state, reward, done, {}

if __name__ == "__main__":
    env = DummyVecEnv([lambda: SimpleTherapyEnv()])
    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=1000)
    print("Trained PPO model for adaptive therapy.")