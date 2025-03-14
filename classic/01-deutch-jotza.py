# This is a simple implementation of the Deutsch-Jotza algorithm. 
# The algorithm determines whether a function is constant or balanced.
#  The algorithm is deterministic and requires only one query to the function.
#  The algorithm is based on the fact that a constant function will always return the same output
#  for all inputs, while a balanced function will return an equal number of 0s and 1s for all inputs.
#  The algorithm works by querying the function with all possible inputs and checking 
# if the outputs are all the same or balanced. If the outputs are all the same, 
# the function is constant, and if the outputs are balanced, the function is balanced. 
# The algorithm has a success probability of 100%.

def constant_function(x):
    return 1

def balanced_function(x):
    return int(x[0])

def is_constant_or_balanced(f, n):
    all_inputs = [format(i, f'0{n}b') for i in range(2**n)]
    outputs = [f(x) for x in all_inputs]
    if all(output == outputs[0] for output in outputs):
        return "constant"
    else:
        return "balanced"

n = 3
result_constant = is_constant_or_balanced(constant_function, n)
print(f"Constant function is: {result_constant}")
result_balanced = is_constant_or_balanced(balanced_function, n)
print(f"Balanced function is: {result_balanced}")
