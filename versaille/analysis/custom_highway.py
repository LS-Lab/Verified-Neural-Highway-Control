import highway_env
from highway_env.envs.highway_env import HighwayEnvFast
from highway_env.vehicle.kinematics import Vehicle
from highway_env import utils
from highway_env.utils import near_split
from highway_env.envs.common.action import ContinuousAction
from gymnasium import spaces

import numpy as np

class BrakingVehicle(Vehicle):

    MIN_SPEED=0.0

    def act(self, action=None) -> None:
        super().act({
            "steering": 0.0,
            "acceleration": -5.0
        })
    
    def randomize_behavior(self) -> None:
        pass

    @classmethod
    def create_random(cls, road, speed=None, lane_from=None, lane_to=None, lane_id=None, spacing=1.0):
        #print("Spacing: ", spacing)
        res = super().create_random(road, speed, lane_from, lane_to, lane_id, spacing)
        #print(res)
        return res

class AsymmetricDiscreteAction(ContinuousAction):
    def __init__(
        self,
        env,
        acceleration_range: tuple[float, float] | None = None,
        steering_range: tuple[float, float] | None = None,
        longitudinal: bool = True,
        lateral: bool = True,
        dynamical: bool = False,
        clip: bool = True,
        actions_per_axis: int = 3,
        **kwargs,
    ) -> None:
        super().__init__(
            env,
            acceleration_range=acceleration_range,
            steering_range=steering_range,
            longitudinal=longitudinal,
            lateral=lateral,
            dynamical=dynamical,
            clip=clip,
        )
        self.actions_per_axis = actions_per_axis

    def space(self):
        return spaces.Discrete(3)


    def act(self, action):
        if self.speed_range:
            self.controlled_vehicle.MIN_SPEED, self.controlled_vehicle.MAX_SPEED = self.speed_range
        if action == 0:
            self.controlled_vehicle.act({
                "acceleration": self.acceleration_range[0],
                "steering": 0,
            })
        elif action == 1:
            self.controlled_vehicle.act({
                "acceleration": 0.0,
                "steering": 0,
            })
        else:
            self.controlled_vehicle.act({
                "acceleration": self.acceleration_range[1],
                "steering": 0,
            })

class HighwayEnvSeedable(HighwayEnvFast):

    def __init__(self, config = None, render_mode = None):
        super().__init__(config, render_mode)

    @classmethod
    def default_config(cls) -> dict:
        cfg = super().default_config()
        cfg.update(
            {
                "lanes_count": 1,  # (4)
                "collision_reward": -1,
                "right_lane_reward": 0.0, # (0.1),
                "reward_speed_range": [0,40],
                "high_speed_reward": 1,
                "render_agent": False,
                "real_time_rendering": False,
                "other_vehicles_type": "highway_env.vehicle.behavior.IDMVehicle",
                "action": {
                    "type": "DiscreteAction",
                    "acceleration_range": [-5.0, 5.0],
                    "longitudinal": True,
                    "lateral": False,
                    "speed_range": [0, 40],
                    "dynamical": False,
                    "clip": True}
            }
        )
        return cfg
    
    def set_observation_seed(self, observation_seed):
        self.config["observation_seed"] = observation_seed
        self.reset()

    def _create_vehicles(self) -> None:
        """Create some new random vehicles of a given type, and add them on the road."""
        #print("Creating vehicles...")
        if not "observation_seed" in self.config or self.config["observation_seed"] is None:
            super()._create_vehicles()
            return
        #print("Found observation seed")
        self.controlled_vehicles = []
        observation_seed = self.config["observation_seed"]
        other_vehicles_type = utils.class_from_path(self.config["other_vehicles_type"])
        other_per_controlled = near_split(
            self.config["vehicles_count"], num_bins=self.config["controlled_vehicles"]
        )
        assert observation_seed[0] == 1.0
        assert observation_seed[4] == 0.0
        vehicle = Vehicle.make_on_lane(
            self.road,
            self.road.network.get_closest_lane_index(np.array([observation_seed[1],0.0]),0),
            observation_seed[1]*5*40,
            observation_seed[3]*2*40
        )
        vehicle = self.action_type.vehicle_class(
            self.road, vehicle.position, vehicle.heading, vehicle.speed
        )
        #print(vehicle)
        self.controlled_vehicles.append(vehicle)
        self.road.vehicles.append(vehicle)
        #print("Ego Car: ")
        #print(vehicle)

        for other_i in range(1, 5):
            if observation_seed[5*other_i] == 0.0:
                continue
            assert observation_seed[5*other_i+4] == 0.0
            vehicle = other_vehicles_type(
                self.road,
                position=[
                    (observation_seed[1]+observation_seed[5*other_i+1])*5*40,
                    (observation_seed[2]+observation_seed[5*other_i+2])*5*40],
                heading=0,
                speed=(observation_seed[3]+observation_seed[5*other_i+3])*2*40
            )
            #print("Other Car: ")
            #print(vehicle)
            vehicle.randomize_behavior()
            #print(vehicle)
            self.road.vehicles.append(vehicle)
        # Disable collision check for uncontrolled vehicles
        for vehicle in self.road.vehicles:
            if vehicle not in self.controlled_vehicles:
                vehicle.check_collisions = False