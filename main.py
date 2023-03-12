import math
import numpy as np
import matplotlib.pyplot as plt

from aco import ACO, Graph
from plot import plot
from mst import MST

# calculate the distance (cost) between two cities
def distance(city1: dict, city2: dict):
    return math.sqrt((city1['x'] - city2['x']) ** 2 + (city1['y'] - city2['y']) ** 2)


def main():

    # 1. GRAPH CONSTRUCTION

    # load cities
    cities = []
    points = [] # just for plot
    with open('./data/chn31.txt') as f:
        lines = f.readlines()
        for line in lines:
            city = line.split(' ')
            # doesn't need to be modeled with dictionaries, arrays are enough
            cities.append(dict(index=int(city[0]), x=int(city[1]), y=int(city[2])))
            points.append((int(city[1]), int(city[2])))
    rank = len(cities)
    print(f'Cities: {rank}')
    #print(cities)

    # cost matrix (aka graph): each entry will be the distance between city i and j
    cost_matrix = []
    for i in range(rank):
        row = []
        for j in range(rank):
            row.append(distance(cities[i], cities[j]))
        cost_matrix.append(row)


    # Graph instantiation: The Graph is just the Distance Matrix. The Graph instance includes a Pheromone Matrix that will be updated in each gen (iteration)
    graph = Graph(cost_matrix, rank)

    # 2. FIND SOLUTIONS

    # ACO instantiation
    aco = ACO(ant_count=80, iterations=100, alpha=1.0, beta=10.0, rho=0.5, q=10, strategy=2)

    # ACO Solver Call
    path, cost = aco.solve(graph)

    # Print and Plot Results
    print('cost: {}, path: {}'.format(cost, path))
    #plot(points, path)

    '''
    # To se performance based on number of ants (number of iterations doesn't seem to improve performance)
    avg_costs = np.zeros(15)
    ants = np.linspace(10, 150, 15).astype(int)
    for i in range(len(ants)):
        costs = np.zeros(10)
        for j in range(len(costs)): # 10 experiments      
            graph = Graph(cost_matrix, rank)
            aco = ACO(ant_count=ants[i], iterations=100, alpha=1.0, beta=10.0, rho=0.5, q=10, strategy=2)
            path, cost = aco.solve(graph)
            costs[j] = cost
            print(ants[i], costs[j])
        avg_costs[i] = np.mean(costs)
        print(f'AVG {ants[i]} {avg_costs[i]}')
    plt.plot(ants, avg_costs)
    plt.show()
    '''

    # 3. 1-TREE (MST) TO COMPARE ACCURACY OF SOLUTION
    mst = MST(cost_matrix) 
    parent = mst.primMST()
    mst_cost = 0
    for i in range(1, len(cost_matrix)):
        mst_cost += cost_matrix[i][parent[i]]
        #print(i, parent[i])

    print(f'MST Cost (Lower Bound): {mst_cost}')
    print(f'MST Performance Rate: {cost / mst_cost}')

    # Improved Lower Bound with 1-Tree
    one_tree_costs = []
    for i in range(len(cost_matrix)):
        new_matrix = np.array(cost_matrix)
        new_matrix = np.delete(new_matrix, i, axis=0)   # Remove the i-th row
        new_matrix = np.delete(new_matrix, i, axis=1)   # Remove the i-th column
        mst = MST(new_matrix) 
        parent = mst.primMST()
        mst_cost = 0
        for j in range(1, len(new_matrix)):
            mst_cost += new_matrix[j][parent[j]]
            #print(j, parent[j])
        row_i = np.array(cost_matrix[i]) # costs from ith node to every other node
        row_i = np.delete(row_i, i) # diagonal element is excluded since it's 0 always
        pidx = np.argpartition(row_i, 2) # 3 first indexes correspond to the smallest elements
        closest = row_i[pidx[:2]] # we get the two closest distances to node i
        mst_cost += np.sum(closest) # we add this two our mst_cost (1-tree cost)
        one_tree_costs.append(mst_cost)

    improved_lower_bound = np.max(one_tree_costs)

    print(f'Max 1-Tree Cost (Improved Lower Bound): {improved_lower_bound}')
    print(f'Max 1-Tree Performance Rate: {cost / improved_lower_bound}')   

if __name__ == '__main__':
    main()
