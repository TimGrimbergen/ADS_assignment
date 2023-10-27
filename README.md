# ADS Assignment
By Tim Grimbergen, Agostino Sorbo, Daan van Dongen, Timo Post and Jesse Flikweert.

*** THE PAPER CAN BE FOUND IN THE "PAPER" FOLDER ***

Run a single algorithm against a single instance with python `>=3.10.0`, using `python test_one.py {case} {algorithmName}`.
* Replace `{case}` with the name of the input file you want to use within our program, e.g. `1` or `2`.
* Replace `{algorithmName}` with the name of the algorithm you want to use, e.g. `offline`, `deterministic` or `random`.
* If debugging, use an additional parameter 'debug', so `python test_one.py {case} {algorithmName} debug`, this will also print the totalCost value.

To run a larger test script, run `python test_all.py`. This will run and compare the qThreshold and Random Online Algorithms to the optimal offline algorithm.
