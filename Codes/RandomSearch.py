import random
from aco import ACO

def random_search(param_ranges, num_iterations, objective_function):
    best_params = None
    best_objective = float('inf')
    
    for i in range(num_iterations):
        params = [random.uniform(param_ranges[j][0], param_ranges[j][1]) for j in range(len(param_ranges))]
        objective = objective_function(params)
        
        if objective < best_objective:
            best_params = params
            best_objective = objective
    
    return best_params, best_objective

# define the parameter ranges
param_ranges = [(50, 100), (50, 500), (0.5, 1.5), (5, 20), (0.1, 0.9), (5, 15), (1, 3)]

# define the objective function to be optimized
def objective_function(params):
    ant_count, iterations, alpha, beta, rho, q, strategy = params
    # run your ACO algorithm with the given parameters and return the objective function value
    objective_value = ACO(ant_count=ant_count, iterations=iterations, alpha=alpha, beta=beta, rho=rho, q=q, strategy=strategy)
    return objective_value

# run the random search algorithm
num_iterations = 100
best_params, best_objective = random_search(param_ranges, num_iterations, objective_function)

print('Best parameters found:', best_params)
print('Best objective value:', best_objective)
