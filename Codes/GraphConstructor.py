import math
from aco import Graph

def distance(city1: tuple, city2: tuple):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def main():
    # 1. GRAPH CONSTRUCTION

    # load cities
    with open('./data/chn31.txt') as f:
        lines = f.readlines()
        cities = [0] * len(lines)
        for i in range(len(lines)):
            city = lines[i].split(' ')
            cities[i] = (int(city[1]), int(city[2]))
    rank = len(cities)
    print(f'Cities: {rank}')

    # cost matrix (aka graph): each entry will be the distance between city i and j
    cost_matrix = []
    for i in range(rank):
        row = []
        for j in range(rank):
            row.append(distance(cities[i], cities[j]))
        cost_matrix.append(row)

    # Graph instantiation: The Graph is just the Distance Matrix. The Graph instance includes a Pheromone Matrix that will be updated in each gen (iteration)
    graph = Graph(cost_matrix, rank)