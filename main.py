import math

from aco import ACO, Graph
from plot import plot

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
    print(cities)

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
    aco = ACO(ant_count=10, iterations=10, alpha=1.0, beta=10.0, rho=0.5, q=10, strategy=2)

    # ACO Solver Call
    path, cost = aco.solve(graph)

    # Print and Plot Results
    print('cost: {}, path: {}'.format(cost, path))
    plot(points, path)


    # 3. 1-TREE (MST) TO COMPARE ACCURACY OF SOLUTION


if __name__ == '__main__':
    main()
