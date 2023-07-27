import sys

def classify_player(L):
    t_avr, sl_avr, obp_avr = L[0], L[1], L[2]
    #print(t_avr ,sl_avr , obp_avr)
    avg = (t_avr + sl_avr + obp_avr) / 3.0

    # 보다 낮은지, 보다 높은지, 또는 비슷한지를 판단하는 함수
    def compare_to_average(value, avg):
        if value < avg - 0.6:
            return -1
        elif value > avg + 0.3:
            return 1
        else:
            return 0

    # 분류를 위한 각 지표를 판단
    A = compare_to_average(t_avr, avg)
    B = compare_to_average(sl_avr, avg)
    C = compare_to_average(obp_avr, avg)

    count_ones = [A, B, C].count(1)
    count_zeros = [A, B, C].count(0)
    count_neg_ones = [A, B, C].count(-1)

    # print([A, B, C])
    # print([count_ones, count_zeros, count_neg_ones])

    if count_ones == 1 and (count_zeros + count_neg_ones) == 2:
        return f'+{[A, B, C].index(1)+1}'
    elif count_neg_ones == 1 and (count_zeros + count_ones) == 2:
        return f'-{[A, B, C].index(-1)+1}'
    else:
        return '0'



def convert_to_float(lst):
    return [float(x) for x in lst]



#sys.argv = ['경로', '0.999','0.487', '0.111']

playerinput = sys.argv[1:]


playerinput = convert_to_float(playerinput)

max = [ 0.300, 0.478, 0.376]
min = [ 0.214, 0.288, 0.272]

sc = []
for i, n in enumerate(playerinput):
    if n < min[i]:
        n = min[i]
    elif n > max[i]:
        n = max[i]
    
    x = round((n- min[i]) * (8 / (max[i] - min[i])) + 1, 2)
    sc.append(x)

print(classify_player(sc))