import os
import json
from skopt import gp_minimize
from skopt.space import Real
import pickle as pc

def fraction_standing(x):
    cyllinder_height = x[0]

    # save experiment settings
    json.dump(
        {
            'cyllinder_height': cyllinder_height
        },
        open('config.json', 'w')
    )

    # run experiment!
    os.system('blender coin.blend --python run_simulation.py')

    # load the results
    js = json.load(open('result.json', 'r'))
    return js


def objective(x):
    fr = fraction_standing(x)
    total = fr['Edge'] + fr['Tails'] + fr['Heads']
    fraction_edge = fr['Edge'] / total
    return abs(fraction_edge - (1.0 / 3.0))


if __name__ == '__main__':
    # do the optimization!
    #print(fraction_standing([1.0]))
    sol = gp_minimize(objective, [Real(1.0, 1.3)], n_random_starts=4, n_calls=20)
    print(sol)
    pc.dump(sol, open('result.pc', 'wb'))