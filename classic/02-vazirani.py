def classical_bernstein_vazirani(n, f):
    """
    Solves the Bernstein-Vazirani problem classically.
    
    :param n: Number of bits in the hidden string s.
    :param f: Function that represents f(x) = s . x mod 2.
    :return: The hidden string s as a binary string.
    """
    s = ""
    for i in range(n):
        # Create an input with a single bit set at position i
        x = 1 << i  # Binary representation with only the i-th bit set
        # Query the function f(x) to determine the i-th bit of s
        s = str(f(x)) + s
    return s

# Example usage:
# Define a hidden string s = "101"
hidden_s = "101"
n = len(hidden_s)

# Define the function f(x) using the hidden string s
def f(x):
    # Convert hidden_s to a list of integers
    s_bits = [int(bit) for bit in hidden_s]
    # Convert x to a binary list
    x_bits = [int(bit) for bit in format(x, f"0{n}b")]
    # Compute the dot product mod 2
    return sum(s_bit * x_bit for s_bit, x_bit in zip(s_bits, x_bits)) % 2

# Solve the Bernstein-Vazirani problem classically
recovered_s = classical_bernstein_vazirani(n, f)
print("Hidden string s:", recovered_s)
