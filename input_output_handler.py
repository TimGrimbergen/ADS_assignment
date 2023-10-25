# Loads an input file assuming a certain format, returns a list of parameters.
def deserialize(file):
    with open(file, 'r') as f:
        s = []
        p = []
        h = []

        lines = [line for line in f]
    
        n = int(lines[0])
        m = int(lines[1])
        for i in range(2, len(lines)):
            sph = lines[i].split(', ')
            s.append(int(sph[0]))
            p.append(int(sph[1]))
            h.append(int(sph[2]))
    
    return [n, m, s, p, h]

def validate_params(n, m, s, p, h):
    if sum(s) < n:
        raise RuntimeError(f"Total number of seats ({sum(s)}) is less than number of people ({n})")
    
    if not len(s) == len(p) == len(h) == m:
        raise RuntimeError(f"Mismatch between length of arrays and number of days: m={m}, L_s = {len(s)}, L_p = {len(p)}, L_h = {len(h)}")

# Parses the output array to the desired format.
def parse_output(output):
    return ''.join([f"{flying}, {hotel}\n" for flying, hotel in output])

# Saves a certain input to a file
def serialize(file, input):
    with open(file, 'w') as g:
        g.write(input)
            
    return