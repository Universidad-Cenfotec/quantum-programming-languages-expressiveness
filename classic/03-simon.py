def classical_simon(n, f):
    inputs = [format(i, f'0{n}b') for i in range(2**n)]
    output_map = {}
    for x in inputs:
        output = f(x)
        if output in output_map:
            x_prev = output_map[output]
            x_current = int(x, 2)
            x_previous = int(x_prev, 2)
            s = x_current ^ x_previous
            return format(s, f'0{n}b')
        else:
            output_map[output] = x
    return None

hidden_s = "101"
n = len(hidden_s)
def f(x):
    x_int = int(x, 2)
    s_int = int(hidden_s, 2)
    if x_int < s_int:
        return format(x_int, f'0{n}b')
    else:
        return format(x_int ^ s_int, f'0{n}b')

recovered_s = classical_simon(n, f)
if recovered_s:
    print("Hidden string s:", recovered_s)
else:
    print("No valid secret found.")
