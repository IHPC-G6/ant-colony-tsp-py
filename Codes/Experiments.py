from aco import ACO, graph

# Define the number of runs to perform
num_runs = 10

# These parameters should be taken from Random Search results
ant_count = 80
iteration_count = 100
alpha = 1.0
beta = 10.0
rho = 0.5
q = 10
strategy = 2

# Define lists to store the results
costs = []
paths = []

# Loop over the number of runs
for i in range(num_runs):
    
    # Instantiate the ACO solver
    aco = ACO(ant_count=ant_count, iterations=iteration_count, alpha=alpha, beta=beta, rho=rho, q=q, strategy=strategy)
    
    # Run the solver on the graph
    path, cost = aco.solve(graph)
    
    # Store the results
    costs.append(cost)
    paths.append(path)

# Calculate the average and standard deviation of the costs
avg_cost = sum(costs) / num_runs
#std_dev_cost = statistics.stdev(costs)