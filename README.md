# Three sided coin
What should be the size (height, or length) of coin edge so that the coin lands on edge with ~33% chance?

<p align="center">
  <img src="https://github.com/iaroslav-ai/coin-experiment/blob/master/media/coin_blueprint.png?raw=true", height="250px"/>
</p>

**Answer**:

Let the coin diameter be of size 2.0. Then the coin edge height should be around **1.043 (x≈1.043 in figure above)**. 

Find more experimental details below!

**Disclamer**:

Answer is based on a data from a simulator, so some differences with reality are possible :)

## Inspired by:

These Youtube videos!

* [How thick is a three-sided coin?](https://www.youtube.com/watch?v=-qqPKKOU-yY)
* [Help me find the thickness of a three-sided coin!](https://www.youtube.com/watch?v=xN5_VO7Nbu8)

## Experimental results

Data from standupmaths et al. (converted):

| Coin thickness        | Fraction of coins landing on edge |
| ---------------- |:---------------------------------:|
| 0.707            | 0.132                             |
| 1.154            | 0.410                             |

Data from my simulator:

| Coin thickness        | Fraction of coins landing on edge |
| ---------------- |:---------------------------------:|
| 0.707            | 0.128                             |
| 1.043            | 0.335                             |
| 1.154            | 0.446                             |

Complete experimental data in a graph (use `make_exp_plot.py` to reproduce):

<p align="center">
  <img src="https://github.com/iaroslav-ai/coin-experiment/blob/master/media/coin_size_plot.png?raw=true", height="350px"/>
</p>

## Approach

Use [Blender](https://www.blender.org/) as simulator for coin flipping!

You can find `coin.blend` which is a Blender file, where the environment for coin flipping is defiend. Every coin is a cylinder, "made" out of silver material. The radius of cylinder is 1.0.  

A script is used which generates 1000 coins with different rotations around x, y, z axes, and with fixed height above the "table" plane. These coins are dropped on the rigid surface, and the number of coins that are standing on the edge are counted.

## Unit conversion

Currently, the thickness of the coin is adjusted - the diameter of the coin is kept fixed at the value of 2.0. This is different to the videos where the diameter is adjusted. The conversion is summarized in the figure below:

<p align="center">
  <img src="https://github.com/iaroslav-ai/coin-experiment/blob/master/media/conversion.png?raw=true", height="450px"/>
</p>


## How to reproduce my results

A script `run_simulation.py` can be executed inside blender in order to run the experiment, using the following command line from terminal:

```bash
blender coin.blend --python run_simulation.py
```

Both `coin.blend` and `run_simulation.py` should be in the current folder where you are at in your terminal, as well as `config.json`.

The file `config.json` is a text file, where you can specify the height of the coin edge. After you run the command, the results of execution should appear in file called `result.json`. 

You can also run code which automatically adjusts the height of the coin using the `run_optimization.py`. For that, you need installed `scikit-optimize` python package. If you are not very familiar with python, see [here](https://www.learnpython.org/en/Modules_and_Packages) and [here](https://packaging.python.org/tutorials/installing-packages/).

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

## Got questions? 

Feel free to open an issue here or contact me in any other way.
