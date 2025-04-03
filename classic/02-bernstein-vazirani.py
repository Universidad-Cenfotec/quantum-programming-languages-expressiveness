def classical_bernstein_vazirani(n, f):
    s = ""
    for i in range(n):
        x = 1 << i         
        s = str(f(x)) + s
    return s

hidden_s = "101"
n = len(hidden_s)

def f(x):    
    s_bits = [int(bit) for bit in hidden_s]
    x_bits = [int(bit) for bit in format(x, f"0{n}b")]
    return sum(s_bit * x_bit for s_bit, x_bit in zip(s_bits, x_bits)) % 2

recovered_s = classical_bernstein_vazirani(n, f)
print("Hidden string s:", recovered_s)
