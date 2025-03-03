import warnings
import os
import sys

import gymnasium as gym
import highway_env
from highway_env.envs.highway_env import HighwayEnv
from highway_env.vehicle.kinematics import Vehicle
from highway_env.vehicle.behavior import IDMVehicle
from highway_env import utils
from highway_env.utils import near_split
import numpy as np
from stable_baselines3 import DQN
from stable_baselines3.common.callbacks import CheckpointCallback
from gymnasium.envs.registration import register
import torch
import time

register(
    id='highway-env-fast-seedable-v0',
    entry_point='custom_highway:HighwayEnvSeedable'
)

def reproduce_crash_get_envs(observation, worst_case_braking=-3.0, weak_brake=True):
    all_envs = []
    env_default = gym.make("highway-env-fast-seedable-v0", render_mode=None)
    env_default.configure({
        "observation_seed": observation
    })
    all_envs.append((5.0,env_default))

    if weak_brake:
        env_min_braking = gym.make("highway-env-fast-seedable-v0", render_mode=None)
        env_min_braking.configure({
            "observation_seed": observation,
            "action": {
                "type": "custom_highway.AsymmetricDiscreteAction",
                "acceleration_range": [-3.0, 5.0],
                "longitudinal": True,
                "lateral": False,
                "speed_range": [0, 40],
                "dynamical": False,
                "clip": True}
        })
        all_envs.append((3.0,env_min_braking))

    env_front_brakes = gym.make("highway-env-fast-seedable-v0", render_mode=None)
    env_front_brakes.configure({
        "observation_seed": observation,
        "action": {
            "type": "custom_highway.AsymmetricDiscreteAction",
            "acceleration_range": [worst_case_braking, 5.0],
            "longitudinal": True,
            "lateral": False,
            "speed_range": [0, 40],
            "dynamical": False,
            "clip": True},
        "other_vehicles_type": "custom_highway.BrakingVehicle"
    })
    all_envs.append((-worst_case_braking,env_front_brakes))
    return all_envs

def set_observation_seed(envs, observation_seed):
    for env in envs:
        env.unwrapped.set_observation_seed(observation_seed)

def load_model(model_path):
    return DQN.load(model_path)

def reproduce_crash_evaluate(all_envs, model, test_runs = 100, default_action = 0,render=False,seed=None):
    #model = DQN.load(model_path)
    #print("hi",file=sys.stderr)
    crashes = []
    rewards = []
    default_crashes = []
    default_rewards = []
    for env in all_envs:
        for ask_model in [True, False]:
            # if ask_model:
            #     print("Testing model")
            # else:
            #     print("Testing default action")
            total_reward = 0
            crash_counter = 0
            for _ in range(test_runs):
                obs = env.reset(seed=seed)[0]
                #print("Initial Observation: ", obs, file=sys.stderr)
                done = False
                truncated = False
                while not done and not truncated:
                    if ask_model:
                        action, _states = model.predict(obs, deterministic=True)
                    else:
                        action = default_action
                    next_state, reward, done, truncated, info = env.step(action)
                    if render:
                        env.render()
                        time.sleep(1.0)
                    total_reward += reward
                    obs = next_state
                    if info and info["crashed"]:
                        crash_counter += 1
            if ask_model:
                rewards.append(total_reward)
                crashes.append(crash_counter)
            else:
                default_rewards.append(total_reward)
                default_crashes.append(crash_counter)
    return (crashes, rewards), (default_crashes, default_rewards)

def reproduce_crash_evaluate_with_trajectory(all_envs, model_path, test_runs = 100, default_action = 0,render=False,seed=None):
    get_trajectories = True
    model = DQN.load(model_path)
    crashes = []
    rewards = []
    default_crashes = []
    default_rewards = []
    all_states = []
    default_all_states = []
    for env in all_envs:
        for ask_model in [True, False]:
            if ask_model:
                print("Testing model")
            else:
                print("Testing default action")
            total_reward = 0
            crash_counter = 0
            obs = env.reset(seed=seed)[0]
            if ask_model:
                all_states.append(obs)
            else:
                default_all_states.append(obs)
            for _ in range(test_runs):
                obs = env.reset(seed=seed)[0]
                done = False
                truncated = False
                while not done and not truncated:
                    if ask_model:
                        action, _states = model.predict(obs, deterministic=True)
                    else:
                        action = default_action
                    next_state, reward, done, truncated, info = env.step(action)
                    if render:
                        env.render()
                        time.sleep(1.0)
                    total_reward += reward
                    obs = next_state
                    if ask_model:
                        all_states.append(obs)
                    else:                    
                        default_all_states.append(obs)
                    if info and info["crashed"]:
                        crash_counter += 1
            if ask_model:
                rewards.append(total_reward)
                crashes.append(crash_counter)
            else:
                default_rewards.append(total_reward)
                default_crashes.append(crash_counter)
    if get_trajectories:
        return (crashes, rewards), (default_crashes, default_rewards), all_states, default_all_states
    else:
        return (crashes, rewards), (default_crashes, default_rewards)