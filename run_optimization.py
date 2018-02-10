import os
import json
from skopt import gp_minimize
from skopt.space import Real
import pickle as pc
import random
from copy import deepcopy

settings_ranges = {
        # cm, height of coin cylinder
        'coin_thickness': [0.1, 2.0],
        'coin_diameter': 2.0,
        # cm/s, standard deviation of normal distribution of angular speeds
        'angular_velocity_std': [0.0, 3.33],
        # cm/s, standard deviation of normal distribution of linear speeds
        'linear_velocity_std': [0.0, 3.33],
        # grams / cm^3
        'coin_density': [1.0, 20.0], #~Plastic - ~Gold
        'coin_friction': [0.1, 0.9],
        'coin_restitution': [0.1, 0.9],
        'table_friction': 0.5,
        'table_restitution': 0.1,
        # size of coin grid in every dimension
        'coin_grid_size': 32,
        # distance between every coin in a grid, cm
        'coin_grid_step': 10.0,
    }

def random_setup():
    """Generate a random setup for experimentation"""
    result = {}
    for k, v in settings_ranges.items():
        if isinstance(v, list):
            result[k] = random.uniform(v[0], v[1])
        else:
            result[k] = v
    return result

def make_coin_config(coin_thickness=1.0,
        angular_velocity_std=1.0,
        linear_velocity_std=1.0,
        coin_density=8.9, # ~Nickel
        coin_friction=0.5,
        coin_restitution=0.5,
        table_friction=0.5,
        table_restitution=0.5,
        coin_grid_size=8,
        coin_grid_step=10.0):
    """Generates the configuration for blender script.
    """
    return {
        # cm, height of coin cylinder
        'coin_thickness': coin_thickness,
        # cm/s, standard deviation of normal distribution of angular speeds
        'angular_velocity_std': angular_velocity_std,
        # cm/s, standard deviation of normal distribution of linear speeds
        'linear_velocity_std': linear_velocity_std,
        # grams / cm^3
        'coin_density': coin_density,
        'coin_friction': coin_friction,
        'coin_restitution': coin_restitution,
        'table_friction': table_friction,
        'table_restitution': table_restitution,
        # size of coin grid in every dimension
        'coin_grid_size': coin_grid_size,
        # distance between every coin in a grid, cm
        'coin_grid_step': coin_grid_step,
    }

def fraction_standing(setup, x, tape=None):
    setup = deepcopy(setup)
    setup['coin_thickness'] = x[0]

    # save experiment settings
    json.dump(
        setup,
        open('config.json', 'w'),
        indent=1,
        sort_keys=True
    )

    # run experiment!
    os.system('blender coin.blend -b --python run_simulation.py')

    # load the results
    js = json.load(open('result.json', 'r'))

    if isinstance(tape, list):
        tape.append([setup, js])

    return js


if __name__ == '__main__':
    all_results = []
    setup = json.load(open('coinfigurations/cupronickel.json', 'r'))

    def objective(x):
        fr = fraction_standing(setup, x, all_results)
        json.dump(all_results, open('results.json', 'w'), indent=1, sort_keys=True)

        total = fr['Edge'] + fr['Tails'] + fr['Heads']
        fraction_edge = fr['Edge'] / total
        return abs(fraction_edge - (1.0 / 3.0))

    # do the optimization!
    th = settings_ranges['coin_thickness']
    sol = gp_minimize(objective, [Real(low=th[0], high=th[1])], n_random_starts=4, n_calls=64)