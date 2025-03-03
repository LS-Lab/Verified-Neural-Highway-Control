import onnx
import onnxruntime as ort

import sys

import numpy as np

from highway_env.vehicle.kinematics import Vehicle
Vehicle.MIN_SPEED = 0.0

from highway_reproduction import *
from custom_highway import *

# Acceleration control bug: Must be >0 to avoid car accidentally going backwards...
BrakingVehicle.MIN_SPEED = 1.0

# CONFIG:
# Worst-case braking value
Bmin=5.0 #3.0
Bmax=5.0
Amax=5.0
T=1.0
L=5.0
V=40.5
REPORT_FAILED_INV = False

envs = reproduce_crash_get_envs(None,worst_case_braking=-Bmin)

NUM_EVAL_STEPS = 1_000 #20_000

# CONFIG:
# Choose NN to use for simulation:
# ort_sess = ort.InferenceSession('../nets/highspeed-rew-1-adjusted.onnx')
ort_sess = ort.InferenceSession('../nets/nn_small_improved-ld-adjusted.onnx')


def invariant(xf, vf, xl, vl):
    res= vl >= -0.5 and vf >= -0.5 and vl <= V and vf <= V and xf + L <= xl and xf + vf**2/(2*Bmin) + L < xl + vl**2/(2*Bmax)
    if not res and REPORT_FAILED_INV:
        print("-- Invariant failed --")
        print(-vl-0.1)
        print(-vf-0.1)
        print(vl-V)
        print(vf-V)
        print(xf + L-xl)
        print(xf + vf**2/(2*Bmin) + L - xl - vl**2/(2*Bmax))
    return res

def modelplex(xf, vf, xl, vl, x1post, x2post, x3post):
    return (
        x1post >= x2post and x1post >= x3post or (
        x2post > x1post and x2post >= x3post and (
            -Bmin <= 0 and 0 <= Amax and vf >= 0 and
            xf + vf**2/(2*Bmin) + (0/Bmin + 1)*(T*vf) + L  <  xl + vl**2/(2*Bmax)
        )) or (
        x3post > x1post and x3post > x2post and ((-Bmin <= Amax and vf + Amax*T  <  0 and
         xf + vf**2/(2*(-Amax)) + L  <  xl + vl**2/(2*Bmax) ) or (
        -Bmin <= Amax and vf + Amax*T >= 0 and
        xf + vf**2/(2*Bmin) + (Amax/Bmin + 1)*(Amax/2*T**2 + T*vf) + L  <  xl + vl**2/(2*Bmax))
        ))
    )

def jsc_options(xf, vf, xl, vl):
    options = np.array([-np.inf, -np.inf, -np.inf])
    options[0]=1.0
    assert modelplex(xf, vf, xl, vl,1.0,0.0,0.0)
    if (
        -Bmin <= 0 and 0 <= Amax and vf >= 0 and
        xf + vf**2/(2*Bmin) + (0/Bmin + 1)*(T*vf) + L  <  xl + vl**2/(2*Bmax)
        ):
        assert modelplex(xf, vf, xl, vl,0.0,1.0,0.0)
        options[1]=1.0
    if ((-Bmin <= Amax and vf + Amax*T  <  0 and
         xf + vf**2/(2*(-Amax)) + L  <  xl + vl**2/(2*Bmax) ) or (
        -Bmin <= Amax and vf + Amax*T >= 0 and
        xf + vf**2/(2*Bmin) + (Amax/Bmin + 1)*(Amax/2*T**2 + T*vf) + L  <  xl + vl**2/(2*Bmax))
        ):
        assert modelplex(xf, vf, xl, vl,0.0,0.0,1.0)
        options[2]=1.0
    return options

# Example for different behaviour between the three:
# [[1.0,0.0,0.0,0.05,0.0,1.0,5.25,0.0,0.1,0.0]+[0.0]*15]
def classic_action(obs):
    outputs = ort_sess.run(None, {'input': obs})
    return np.argmax(outputs[0])

def veriphy_action(obs):
    outputs = ort_sess.run(None, {'input': obs})
    if modelplex(5*40*obs[0][1], 2*40*obs[0][3], 5*40*(obs[0][1]+obs[0][6]), 2*40*(obs[0][3]+obs[0][8]), outputs[0][0][0], outputs[0][0][1], outputs[0][0][2]):
        return np.argmax(outputs[0])
    else:
        return 0


def jsc_action(obs):
    outputs = ort_sess.run(None, {'input': obs})
    if not invariant(5*40*obs[0][1], 2*40*obs[0][3], 5*40*(obs[0][1]+obs[0][6]), 2*40*(obs[0][3]+obs[0][8])):
        return np.argmax(outputs[0])
    else:
        allowed_options = jsc_options(5*40*obs[0][1], 2*40*obs[0][3], 5*40*(obs[0][1]+obs[0][6]), 2*40*(obs[0][3]+obs[0][8]))
        if len(allowed_options) == 0:
            return 0
        else:
            res = np.argmax(outputs[0][0] * allowed_options)
            return res

all_results = []

for _, env in envs:
    env.configure({
        "vehicles_density": 0.5,
        #"simulation_frequency": 100
    })

# Evaluate all on the same set of initial observations

# CONFIG:
# First line: Run for worst-case envirionment
# Second line: Run for all environments
for (env_idx,(b_val,env)) in enumerate([envs[-1]]):
# for (env_idx,(b_val,env)) in enumerate(envs):
    Bmin = b_val
    init_observations = []
    REPORT_FAILED_INV = False
    print("Generating datapoints...")
    while len(init_observations) < NUM_EVAL_STEPS:
        obs = [envs[-1][1].reset()[0].reshape(25)]
        if invariant(5*40*obs[0][1], 2*40*obs[0][3], 5*40*(obs[0][1]+obs[0][6]), 2*40*(obs[0][3]+obs[0][8])) and obs[0][8] < obs[0][13] and obs[0][13] < obs[0][18] and obs[0][18] < obs[0][23]:
            init_observations.append(obs[0])
            #print(obs[0][[1,3,6,8,13,18]])
    print("Running simulation...")
    REPORT_FAILED_INV = True
    for (policy_idx,policy) in enumerate([classic_action, veriphy_action, jsc_action]):
    #for (policy_idx,policy) in enumerate([jsc_action]):
        resolutions = [15, 100] if policy_idx == 2 else [15]
        for resolution in resolutions:
            env.configure({
                "simulation_frequency": resolution
            })
            all_results.append([])
            for obs_idx in range(NUM_EVAL_STEPS):
                action_counter = [0]*3
                init_in_inv = False
                #while not init_in_inv:
                env.unwrapped.set_observation_seed(init_observations[obs_idx])
                state = env.reset()[0]
                init_state = state
                #print(5*40*state[0][1], 2*40*state[0][3], 5*40*(state[0][1]+state[1][1]), 2*40*(state[0][3]+state[1][3]), end="; ")
                init_in_inv = invariant(5*40*state[0][1], 2*40*state[0][3], 5*40*(state[0][1]+state[1][1]), 2*40*(state[0][3]+state[1][3]))
                #print("DONE")
                done = False
                truncated = False
                crashed = False
                reward_sum = 0.0
                while not done and not truncated:
                    action = policy([state.reshape(25)])
                    next_state, reward, done, truncated, info = env.step(action)
                    state = next_state
                    reward_sum += reward

                    action_counter[action] += 1

                    if info and info['crashed']:
                        #print("crash")
                        crashed = True
                        # if init_in_inv and policy_idx != 0:
                        #     print("Found crash from inside invariant")
                        #     print("State: ", init_state)
                        #     print("Actions: ", action_counter)
                        break
                all_results[-1].append((init_in_inv, crashed, action_counter, reward_sum))
            # Summarize results
            print("------------------------------")
            print("Environment: ", env_idx)
            print("Policy: ", policy.__name__)
            print("Resolution: ", resolution)
            print("Results: ")
            inside_inv_count = sum([1 for (init_in_inv,_,_,_) in all_results[-1] if init_in_inv])
            print("Start inside invariant: ", inside_inv_count, "/", NUM_EVAL_STEPS)
            print("Crashes: ", sum([1 for (_,crashed,_,_) in all_results[-1] if crashed]), "/", NUM_EVAL_STEPS)
            print("Crashes inside invariant: ", sum([1 for (init_in_inv,crashed,_,_) in all_results[-1] if init_in_inv and crashed]), "/", NUM_EVAL_STEPS)
            print("Average reward): ", sum([reward for (_,_,_,reward) in all_results[-1]])/NUM_EVAL_STEPS, "+-", np.std([reward for (_,_,_,reward) in all_results[-1]]))
            print("Action distribution: ", [sum([action_counter[action_idx] for (_,_,action_counter,_) in all_results[-1]]) for action_idx in range(3)])
            sys.stderr.flush()
            sys.stdout.flush()
    