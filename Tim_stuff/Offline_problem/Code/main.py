from solver import solve_offline
from input_output_handler import transform_input, transform_output

input_file_directory = '../Input_files' 
output_file_directory = '../Output_files'

params = transform_input(f'{input_file_directory}/sample_input.txt')

if __name__ == '__main__':
    output = solve_offline(*params)
    print(output)
    
    transform_output(output, output_file_directory, 'sample_output')