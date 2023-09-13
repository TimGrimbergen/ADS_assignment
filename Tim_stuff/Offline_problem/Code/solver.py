import numpy as np

def solve_offline(n, m, s, p, h):
    if sum(s) < n:
        raise RuntimeError(f"Total number of seats ({sum(s)}) is less than number of people ({n})")
    
    if not len(s) == len(p) == len(h) == m:
        raise RuntimeError(f"Mismatch between length of arrays and number of days: m={m}, L_s = {len(s)}, L_p = {len(p)}, L_h = {len(h)}")
    
    h_cum = np.cumsum(h)
    p_real = [p[0]] + [p[i] + h_cum[i-1] for i in range(1,m)]
    
    day_seats_prices = sorted([(i, s[i], p_real[i]) for i in range(m)], key = lambda x: -x[2])
    
    day_send = [0 for _ in range(m)]
    total_price = 0
    
    new_n = n
    
    while new_n > 0:
        day, seats, price = day_seats_prices.pop()
        send = min(new_n,seats)
        total_price += send * price
        day_send[day] = send
        new_n -= send
    
    ans = [[0,0] for _ in range(m)]
    
    for i,x in enumerate(day_send):
        ans[i] = [x, n-x]
        n -= x
    
    print(f"total_price = {total_price}")
    
    return ans