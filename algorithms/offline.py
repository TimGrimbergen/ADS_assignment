import numpy as np

# returns tuple ['schedule array', 'total_price']
def solve_offline(n, m, s, p, h):
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
    
    return [ans, total_price]