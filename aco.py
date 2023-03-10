import random


class Graph(object):
    def __init__(self, cost_matrix: list, rank: int):
        """
        :param cost_matrix:
        :param rank: rank of the cost matrix
        """
        self.matrix = cost_matrix
        self.rank = rank # could be internal variable only
        # pheromone matrix will indicate amount of pheromone in each link
        self.pheromone = [[1 / (rank * rank) for j in range(rank)] for i in range(rank)]


class ACO(object):
    def __init__(self, ant_count: int, iterations: int, alpha: float, beta: float, rho: float, q: int,
                 strategy: int):
        """
        :param ant_count:
        :param iterations:
        :param alpha: relative importance of pheromone
        :param beta: relative importance of heuristic information
        :param rho: pheromone residual coefficient
        :param q: pheromone intensity
        :param strategy: pheromone update strategy. 0 - ant-cycle, 1 - ant-quality, 2 - ant-density
        """
        self.Q = q
        self.rho = rho
        self.beta = beta
        self.alpha = alpha
        self.ant_count = ant_count
        self.iterations = iterations
        self.update_strategy = strategy

    def _update_pheromone(self, graph: Graph, ants: list):
        # can be re-written to not use enumerate
        for i, row in enumerate(graph.pheromone):
            for j, col in enumerate(row):
                # see pheromone update formula
                graph.pheromone[i][j] *= self.rho
                for ant in ants:
                    graph.pheromone[i][j] += ant.pheromone_delta[i][j]

    def solve(self, graph: Graph):
        """
        :param graph:
        """
        best_cost = float('inf')
        best_solution = []
        for iter in range(self.iterations):
            ants = [_Ant(self, graph) for i in range(self.ant_count)]
            for ant in ants:
                for i in range(graph.rank - 1):
                    ant._select_next()
                ant.total_cost += graph.matrix[ant.tabu[-1]][ant.tabu[0]] # to close the loop
                if ant.total_cost < best_cost:
                    best_cost = ant.total_cost # new minimum cost
                    best_solution = [] + ant.tabu # new best solution is this ant solution
                # update pheromone delta of each ant
                ant._update_pheromone_delta()
            # update pheromone matrix at the end of the iteration
            self._update_pheromone(graph, ants)
            print('iteration #{}, best cost: {}, path: {}'.format(iter, best_cost, best_solution))
        return best_solution, best_cost


class _Ant(object):
    def __init__(self, aco: ACO, graph: Graph):
        self.colony = aco
        self.graph = graph
        self.total_cost = 0.0
        self.tabu = []  # ant solution
        self.pheromone_delta = []  # the local increase of pheromone
        self.allowed = [i for i in range(graph.rank)]  # nodes which are allowed for the next selection
        # eta matrix for edge selection: see edge selection formula
        self.eta = [[0 if i == j else 1 / graph.matrix[i][j] for j in range(graph.rank)] for i in range(graph.rank)]  # heuristic information
        start = random.randint(0, graph.rank - 1)  # start from any node: starting city
        self.tabu.append(start)
        self.current = start
        self.allowed.remove(start) # cities that can be visited: each city is visited only once

    def _select_next(self):
        # see edge selection formula
        denominator = 0
        for i in self.allowed:
            denominator += self.graph.pheromone[self.current][i] ** self.colony.alpha * self.eta[self.current][i] ** self.colony.beta
        probabilities = [0 for i in range(self.graph.rank)]  # probabilities for moving to a node in the next step
        for i in range(self.graph.rank):
            # no need to use try and catch: use if instead
            try:
                self.allowed.index(i)  # test if allowed list contains i
                probabilities[i] =  (self.graph.pheromone[self.current][i] ** self.colony.alpha * \
                                    self.eta[self.current][i] ** self.colony.beta) / denominator
            except ValueError:
                pass  # do nothing
        # select next node by probability roulette
        # see if other probabilistic method can be used (youtube video?)
        selected = 0
        rand = random.random()
        for i, probability in enumerate(probabilities):
            rand -= probability
            if rand <= 0:
                selected = i
                break
        # update allowed, tabu (ant solution), ant cost and current city
        self.allowed.remove(selected)
        self.tabu.append(selected)
        self.total_cost += self.graph.matrix[self.current][selected]
        self.current = selected

    def _update_pheromone_delta(self):
        self.pheromone_delta = [[0 for j in range(self.graph.rank)] for i in range(self.graph.rank)]
        for _ in range(1, len(self.tabu)):
            i = self.tabu[_ - 1]
            j = self.tabu[_]

            # maybe we can remove this (and remove strategy parameter)
            if self.colony.update_strategy == 1:  # ant-quality system
                self.pheromone_delta[i][j] = self.colony.Q
            elif self.colony.update_strategy == 2:  # ant-density system
                self.pheromone_delta[i][j] = self.colony.Q / self.graph.matrix[i][j]

            # this is the wikipedia one
            else:  # ant-cycle system
                self.pheromone_delta[i][j] = self.colony.Q / self.total_cost
