def classical_simon(n, f):
    """
    Solves Simon's problem classically.
    
    :param n: Number of bits in the inputs.
    :param f: Function that maps n-bit strings to n-bit strings.
    :return: The secret s as a binary string.
    """
    # Generate all possible n-bit inputs
    inputs = [format(i, f'0{n}b') for i in range(2**n)]
    output_map = {}

    # Map each input to its corresponding output
    for x in inputs:
        output = f(x)
        if output in output_map:
            # If we find two different inputs with the same output, we can determine s
            x_prev = output_map[output]
            x_current = int(x, 2)
            x_previous = int(x_prev, 2)
            # s = x ⊕ y
            s = x_current ^ x_previous
            return format(s, f'0{n}b')
        else:
            output_map[output] = x

    # If no collision is found, the function does not match the Simon problem constraints
    return None


# Example usage:
# Define the hidden string s = "101"
hidden_s = "101"
n = len(hidden_s)

# Define the function f(x) using the hidden string s
def f(x):
    # Convert x to integer and apply the XOR with the secret
    x_int = int(x, 2)
    s_int = int(hidden_s, 2)
    # Return the same output for x and x ⊕ s
    if x_int < s_int:
        return format(x_int, f'0{n}b')
    else:
        return format(x_int ^ s_int, f'0{n}b')

# Solve Simon's problem classically
recovered_s = classical_simon(n, f)
if recovered_s:
    print("Hidden string s:", recovered_s)
else:
    print("No valid secret found.")
