from __future__ import division, print_function

import numpy as np


dbname = 'all_ratings_file.csv'
def save_db(combos):
    with open(dbname, 'wb') as fobj:
        ls = ["{0},{1}".format(k, v) for k, v in combos.items()]
        fobj.write("\n".join(ls))

def load_db():
    combos = []
    with open(dbname, 'rb') as fobj:
        for line in fobj.readlines():
            k, v = line.strip().split(',')
            combos.append((k, float(v)))
    return dict(combos)

def R_score(rating):
    
    return 10 ** (rating / 400)

def E_value(R1, R2):
    
    return R1 / (R1 + R2)

def update_rating(r_old, S, E):
    K = 32
    return r_old + K * (S - E)

def process(left, right, response, combos):

    left_r = combos[left]
    right_r = combos[right]
    left_R = R_score(left_r)
    right_R = R_score(right_r)
    left_E = E_value(left_R, right_R)
    right_E = E_value(right_R, left_R)
    
    if response == 'L':
        new_left = update_rating(left_r, 1, left_E)
        new_right = update_rating(right_r, 0, right_E)
    elif response == 'R':
        new_left = update_rating(left_r, 0, left_E)
        new_right = update_rating(right_r, 1, right_E)
    else: #D for draw
        new_left = update_rating(left_r, 0.5, left_E)
        new_right = update_rating(right_r, 0.5, right_E)
        
    combos[left] = new_left
    combos[right] = new_right
        
    
if __name__ == "__main__":
    
    combos = load_db()
    while True:
        left, right = np.random.choice(combos.keys(), size=2, replace=False)
        text = "L: {0} vs R: {1}".format(left, right)
        response = raw_input(text)
        if response not in ['L', 'R', 'S', 'D']:
            print('bad input')
            continue
        elif response == 'S':
            print('DONE')
            break
        else:
            process(left, right, response, combos)
            
    save_db(combos)
    print(sorted(combos.items(), key=lambda k: k[1], reverse=True)[:10])
    