import os
import json
from skopt import gp_minimize
from skopt.space import Real
from run_simulation import settings_ranges, fraction_standing, get_config

if __name__ == '__main__':
    all_results = []
    setup = get_config()

    def objective(x):
        # run experiment with coin height
        fr = fraction_standing(setup, x, all_results)

        # save the record of all results to file
        json.dump(all_results, open('results.json', 'w'), indent=1, sort_keys=True)

        # calculate objective - deviation from 0.33333... of edge landing coin fraction
        total = fr['Edge'] + fr['Tails'] + fr['Heads']
        fraction_edge = fr['Edge'] / total
        return abs(fraction_edge - (1.0 / 3.0))

    # do the optimization!
    th = settings_ranges['coin_thickness']
    sol = gp_minimize(objective, [Real(low=th[0], high=th[1])], n_random_starts=4, n_calls=64)