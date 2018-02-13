# Three sided coin

## Inspired by:

These Youtube videos!

* [How thick is a three-sided coin?](https://www.youtube.com/watch?v=-qqPKKOU-yY)
* [Help me find the thickness of a three-sided coin!](https://www.youtube.com/watch?v=xN5_VO7Nbu8)

## Question

What should be the size (height, or length) of coin edge so that the coin lands on edge with ~33% chance?

<p align="center">
  <img src="https://rawgit.com/iaroslav-ai/coin-experiment/master/media/coin_blueprint.svg", height="300px"/>
</p>

**Answer**:

~~Let the coin diameter be of size 2.0. Then the coin edge height should be around 1.043.~~

This depends on many parameters, for instance on how you toss the coin. 
Here are the results that you are expected to get if you follow 
[instructions on how to flip a coin](https://www.wikihow.com/Flip-a-Coin):

| Material of the coin  | Best thickness |
| --------------------- | -------------- |
| Plastic coin | 0.981 |
| Copper - Nickel alloy | 0.977 |

If you apply different range of random
rotation and linear speeds to coin, then thickness varies also. See table 
below - larger values of sigma in table correspond to larger speeds of coin.
A copper - nickel alloy coin of diameter 2.0 cm was simulated. 

| Angular speeds sigma  | Lin. speeds sigma  | Best thickness |
| --------------------- | ------------------ | -------------- |
| 0.0 | 0.0 | 1.000 |
| 0.0 | 2.0 | 0.970 |
| 4.0 | 0.0 | 0.910 |
| 4.0 | 2.0 | 0.903 |

Similar results are obtained with coin simulated to be made of plastic:

| Angular speeds sigma  | Lin. speeds sigma  | Best thickness |
| --------------------- | ------------------ | -------------- |
| 0.0 | 0.0 | 0.987 |
| 0.0 | 2.0 | 0.979 |
| 4.0 | 0.0 | 0.949 |
| 4.0 | 2.0 | 0.928 |

Find more experimental details below!

**Disclamer**:

Answer is based on a data from a simulator, so some differences with reality are possible :) 

If you think experimental setup could be better let me know.

## Approach

Use [Blender](https://www.blender.org/) as simulator for coin flipping!

You can find `coin.blend` which is a Blender file, where the environment for coin flipping is defiend. Every coin is a cylinder, "made" out of silver material. The radius of cylinder is 1.0.  

A script is used which generates 1000 coins with different rotations around x, y, z axes, and with fixed height above the "table" plane. These coins are dropped on the rigid surface, and the number of coins that are standing on the edge are counted.

In order to determine / confirm the restitution and friction values for 
simulated coins in blender, a minimalistic data collection was 
performed using the following setup:

<p align="center">
  <img src="https://github.com/iaroslav-ai/coin-experiment/blob/master/media/data_collection.jpg?raw=true", height="250px"/>
</p>

Two experiments were performed multiple times:

* Coin was dropped on the wooden plate from fixed height on its edge.
The height to which the coin bounced was recorded.

* Wooden plate was positioned at an angle, coin was placed at the top
of the plate, and allowed to slide. The time it took for coin to slide
was recorded.

A similar experiment was done in blender, where friction and restitution
were chosen such that simulation matches the observation, see 
`misc/check_restitution_friction.blend`:

<p align="center">
  <img src="https://github.com/iaroslav-ai/coin-experiment/blob/master/media/simulation.gif?raw=true", height="250px"/>
</p>

In order to determine the angular velocity of coin flipped according to
[instructions](https://www.wikihow.com/Flip-a-Coin), the following 
was used: 
[video](https://www.youtube.com/watch?v=sLJPLT9Dw04),
[video](https://www.youtube.com/watch?v=OF4WK2ICVN0).

## Visualization of full experimental data

Here you can find graphs with thickness values that were
tried. The thickness of coin was automatically optimized using
[scikit-optimize](https://github.com/scikit-optimize/scikit-optimize) package.


### Copper and plastic coins, flipping ~ according to instructions:
<p align="center">
  <img src="https://github.com/iaroslav-ai/coin-experiment/blob/master/media/flip_a_coin.png?raw=true", height="450px"/>
</p>

### Copper - nickel coin, uniform rotations

<p align="center">
  <img src="https://github.com/iaroslav-ai/coin-experiment/blob/master/media/cupronickel.png?raw=true", height="450px"/>
</p>

### Plastic coin, uniform rotations

<p align="center">
  <img src="https://github.com/iaroslav-ai/coin-experiment/blob/master/media/hardplastic.png?raw=true", height="450px"/>
</p>

## Unit conversion

Currently, the thickness of the coin is adjusted - the diameter of the coin is kept fixed at the value of 2.0. This is different to the videos where the diameter is adjusted. The conversion is summarized in the figure below:

<p align="center">
  <img src="https://rawgit.com/iaroslav-ai/coin-experiment/master/media/conversion.svg", height="450px"/>
</p>


## How to reproduce my results

A script `simulation.py` can be executed inside blender in order to run the experiment, using the following command line from terminal:

```bash
blender coin.blend --python simulation.py
```

Both `coin.blend` and `simulation.py` should be in the current folder where you are at in your terminal, as well as `config.json`.

The file `config.json` is a text file, where you can specify the height of the coin edge. After you run the command, the results of execution should appear in file called `result.json`. 

A **recommended** way of running a simulation is using `run_simulation.py` script. This script uses default
setting for coin experiment parameters from `coinfigurations/cupronickel.json`, as well as it allows
you to override some experimental settings in command line, for example:

```bash
python3 run_simulation.py coin_thickness=2.0 coin_grid_size=8 exit_when_done=false
```

Names of arguments should correspond to parameter names in `cupronickel.json`.

You can find example experimental settings in folder called `coinfigurations`. 

You can also run code which automatically adjusts the height of the coin using the `run_optimization.py`. For that, you need installed `scikit-optimize` python package. If you are not very familiar with python, see [here](https://www.learnpython.org/en/Modules_and_Packages) and [here](https://packaging.python.org/tutorials/installing-packages/).

By default, `run_optimization.py` copies the `config.json` from `cupronickel.json`
in `coinfigurations` folder. If you wish to override any of the simulation settings,
provide as argument to script pairs of setting name=value, for example:

```bash
python3 run_optimization.py angular_velocity_std=8.0 linear_velocity_std=0.0 coin_grid_size=8 exit_when_done=false
```

This is useful if you wish to experiment with different experimental settings.

## Screenshots

Example visualization of experiment with coins:

<p align="center">
  <img src="https://github.com/iaroslav-ai/coin-experiment/blob/master/media/coin_visualization.gif?raw=true", height="450px"/>
</p>

If you navigate in console to the folder with experiment code, you can start `python3.5` and
run experiments with different thickness yourself - see example below. Example below was run with only 64 coins, hence
fraction of standing coins is off and it is rather fast.

<p align="center">
  <img src="https://github.com/iaroslav-ai/coin-experiment/blob/master/media/run_blender.gif?raw=true", height="250px"/>
</p>

## Where this was tested

* Ubuntu 16.04
* python3.5
* Blender 2.76b

## Acknowledgments 

Thanks to [Epä Järjestys](https://www.youtube.com/channel/UCuhQxsF97vKnNMNnA5rmYYA)
 and [Rojetto](https://github.com/Rojetto) for pointing out the uniform rotation issue with coins.

## Got questions? 

Feel free to open an issue here or contact me in any other way.
