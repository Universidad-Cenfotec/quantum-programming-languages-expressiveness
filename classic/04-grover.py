def classical_grover_simulation(N, marked_index, iterations):
    probabilities = [1 / N] * N    
    for _ in range(iterations):
        probabilities[marked_index] += 1 / (N * iterations) 
        total = sum(probabilities)
        probabilities = [p / total for p in probabilities]    
    return probabilities

N = 16  
marked_index = 7 
iterations = 4 
final_probabilities = classical_grover_simulation(N, marked_index, iterations)
print("Final probabilities:", final_probabilities)
print(f"Probability of marked element (index {marked_index}):", final_probabilities[marked_index])
