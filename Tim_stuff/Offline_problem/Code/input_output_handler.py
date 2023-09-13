def transform_input(file):
    '''
        Loads in a file and returns an list of length 5 with the problem
        parameters.
    '''
    
    with open(file, 'r') as f:
        lines = [line for line in f]
        n = int(lines[0])
        m = int(lines[1])
        s = [int(x) for x in lines[2].split(', ')]
        p = [int(x) for x in lines[3].split(', ')]
        h = [int(x) for x in lines[4].split(', ')]
    
    return [n, m, s, p, h]

def transform_output(output, save_location, name):
    with open(f"{save_location}/{name}.txt", 'w') as g:
        for (f, l) in output:
            g.write(f"{f}, {l}\n")
            
    return
