def classical_grover_simulation(N, marked_index, iterations):
    """
    Simulates the logic of Grover's algorithm in a classical manner.
    
    :param N: Total number of elements in the search space.
    :param marked_index: The index of the "marked" element we want to find.
    :param iterations: Number of iterations to simulate.
    :return: Approximation of how likely we are to identify the marked element.
    """
    # Start with a uniform probability distribution
    probabilities = [1 / N] * N
    
    for _ in range(iterations):
        # "Mark" the desired element: classically, just adjust its probability
        probabilities[marked_index] += 1 / (N * iterations)  # Increment its "weight"
        
        # Normalize probabilities (simulate the effect of interference)
        total = sum(probabilities)
        probabilities = [p / total for p in probabilities]
    
    return probabilities


# Example usage:
N = 16  # Number of possible elements
marked_index = 7  # The "marked" element
iterations = 4  # Number of iterations

final_probabilities = classical_grover_simulation(N, marked_index, iterations)
print("Final probabilities:", final_probabilities)
print(f"Probability of marked element (index {marked_index}):", final_probabilities[marked_index])
