import os
import json
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
    'coin_density': [0.9, 19.3], # Plastic - Gold
    'coin_friction': [0.1, 0.9],
    'coin_restitution': [0.1, 0.9],
    'table_friction': 0.5,
    'table_restitution': 0.1,
    # size of coin grid in every dimension
    'coin_grid_size': 32,
    # distance between every coin in a grid, cm
    'coin_grid_step': 10.0,
    # whether to close blender when done simulating.
    # if False, you can take a look at simulation when done.
    'exit_when_done': True,
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


def run(setup, tape=None):
    """Runs the experiment with given settings"""
    setup = deepcopy(setup)

    # save experiment settings
    json.dump(
        setup,
        open('config.json', 'w'),
        indent=1,
        sort_keys=True
    )

    run_back = ' -b' if setup['exit_when_done'] else ""

    # run experiment!
    os.system('blender coin.blend' + run_back + ' --python simulation.py')

    # load the results
    js = json.load(open('result.json', 'r'))

    if isinstance(tape, list):
        tape.append([setup, js])

    return js


def fraction_standing(setup, x, tape=None):
    setup = deepcopy(setup)
    setup['coin_thickness'] = x[0]
    return run(setup, tape)


def get_config():
    """Reads default configuration and update it according
     to command line arguments given by user"""
    import sys

    # read user override of parameters from console
    user_override = {}
    for k, v in ((k.lstrip('-'), v) for k, v in (a.split('=') for a in sys.argv[1:])):
        user_override[k] = json.loads(v)

    # get the configuration file that is to be used
    cfg_file = 'cupronickel.json'
    if 'config_file' in user_override:
        cfg_file = user_override['config_file']

    # read the predefined coin configuration
    setup = json.load(open(os.path.join('coinfigurations', cfg_file), 'r'))

    # here results for all evaluations will be stored
    for k, v in user_override.items():
        setup[k] = v

    return setup


if __name__ == '__main__':
    setup = get_config()
    result = run(setup)
    print(result)

