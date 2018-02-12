"""This takes a results json, and makes visualizations
of results out of it."""
import json
import os
from collections import defaultdict
import numpy as np


def fraction_edge(r):
    """Calculate fraction of coins that landed on edge"""
    total = r['Edge'] + r['Tails'] + r['Heads']
    fraction_edge = r['Edge'] / total
    return fraction_edge


def best_fit(results):
    """Fit GP model, and find point which is most close to 1/3"""
    x = list([x['coin_thickness'] for x, y in results])
    y = list([fraction_edge(y) for x, y in results])

    from skopt.utils import cook_estimator
    from skopt.space import Real

    # single feature dataset
    X = np.array(x)[:, np.newaxis]

    # fit gaussian process model
    model = cook_estimator('GP', [Real(0.1, 2.0)])
    model.fit(X, y)

    fnc = lambda V: model.predict(V[:, np.newaxis])
    # find here also the best fit to 1/3
    obj = lambda x: (fnc(np.array(x)) - 1.0 / 3.0) ** 2

    from scipy.optimize import minimize
    thickness = minimize(obj, [1.0], bounds=[(0.1, 2.0)]).x[0]

    return fnc, thickness


def visualize_results(results, name, fit_res=None):
    """results is a list of [config, result] pairs"""
    import matplotlib.pyplot as plt

    x = list([x['coin_thickness'] for x, y in results])
    y = list([fraction_edge(y) for x, y in results])

    # make the figure

    # set the title of the figure
    plt.title(name)

    # plot the data points
    plt.scatter(x, y, label='Simulator data')

    # plot fitted data
    if fit_res is not None:
        fnc, x_best = fit_res
        xv = np.linspace(min(x), max(x))
        plt.plot(xv, fnc(xv), c='green', label='Fit curve')

        # plot the vertical and horizontal lines
        plt.axvline(x_best, label='Best match to 1/3', dashes=[5, 5], c='r')
        plt.axhline(1.0 / 3.0, dashes=[5, 5], c='r')

        # add the text of best matching thickness
        plt.text(x_best + 0.01, 0.125, str(x_best))

    # add labels to the axes
    plt.xlabel('Thickness of a coin')
    plt.ylabel('Fraction of coins that land on edge')

    plt.xlim([0.0, 2.1])
    plt.ylim([-0.1, 1.0])

    # add legends and grid
    plt.legend()
    plt.grid()
    #plt.show()

def plot_multiple(params):
    import matplotlib.pyplot as plt
    plt.figure(figsize=(16, 10))

    idx = 1
    for p in params:
        plt.subplot(2,2,idx)
        idx += 1
        visualize_results(*p)
    plt.show()


#results_file = 'hardplastic_results.json'
results_file = 'cupronickel_results.json'

# load and process data here
data_file = os.path.join('results', results_file)
js = json.load(open(data_file, 'r'))

# determine changing parameters
base = js[0][0]
changing_params = set()
for x, y in js[1:]:
    might_change = {k for (k, v) in x.items() if k not in changing_params}
    changing_params |= {k for k in might_change if x[k] != base[k]}

# remove coin thickness - it was optimized
changing_params -= {'coin_thickness'}

# sort the evaluations into different configurations
setups = defaultdict(list)

for x, y in js:
    signature = ", ".join([p + "=" + str(x[p]) for p in changing_params])
    setups[signature].append([x, y])

for_plotting = []

for setup, results in setups.items():
    # find best result
    fnc, best_x  = best_fit(results)
    print(setup, best_x)
    for_plotting.append((results, setup, (fnc, best_x)))

plot_multiple(for_plotting)
