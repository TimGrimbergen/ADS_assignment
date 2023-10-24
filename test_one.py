import sys
import numpy as np
from algorithms.offline import solve_offline
from algorithms.online import qThresholdOnline, RandomizedQThresholdOnline, PredictionOnline
from input_output_handler import deserialize, validate_params, parse_output, serialize

input_file_directory = 'input' 
output_file_directory = 'output'

is_debug_run = False

# try to store program parameters to usable variables
if len(sys.argv) >= 3:
    case = sys.argv[1]
    algorithm = sys.argv[2]
    is_debug_run = len(sys.argv) == 4
else:
    print ("Please specify the case and algorithm, e.g. 'python main.py 1 offline'")
    exit()

# take input parameters from test case file
params = deserialize(f'{input_file_directory}/{case}')

# validate the parameters
validate_params(*params)
p_max = np.max(params[3])

# select algorithm function
if algorithm == "offline": # offline algorithm
    output = solve_offline(*params)

elif algorithm == "deterministic": # online deterministic algorithm
    output = qThresholdOnline(np.sqrt(1/p_max), p_max).solve_instance(params)

elif algorithm == "random": # online randomized algorithm
    output = RandomizedQThresholdOnline(np.sqrt(1/p_max), p_max).solve_instance(params)

elif algorithm == "prediction": # online randomized algorithm
    output = PredictionOnline().solve_instance(params)

else:
    output = solve_offline(*params) # default, fallback

schedule = output[0]
total_price = output[1]

# parse output to the desired format neat
parsedOutput = parse_output(schedule)

# store the parsed output in the output directory
serialize(f'{output_file_directory}/{case}', parsedOutput)

# if this run is a debug run, print the total price as well
if is_debug_run:
    print(f"Total cost: {total_price}\n")

# print the desired output
print(parsedOutput)