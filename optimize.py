from evaluate import evaluate
from solutions import nearest_neighbor2
from neighborhoods import neighborhood_2opt
import random
from math import exp, ceil

class AntColony:
    """
    Classe que implementa a otimização por colônia de formigas com atualização
    de feromônio off-line baseada em ranqueamento. Critério de parada é atingir
    o número máximo de iterações ou número máximo de iterações sem melhora da
    solução.

    Args:
        graph (NetworkX.Graph): grafo do TSPd.
        k (int): Número de entregas no TSPd
        v (int): Valor das entregas no TSPd.
        pheromone_rate (float): influência do feromônio na escolha da
        solução.
        heuristic_rate (float): influência da heurística na escolha da
        solução.
        evaporation_rate (float): taxa de evaporação do feromônio.
        nAnts (int): number of ants to be used in optimization.
        nBest (int): número das melhores formigas que influenciam na
        atualização do feromônio.
        iterMax (int): número máximo de iterações .
        iterNoImproveMax (int): número máximo de iterações sem melhora.
    """
    def __init__(self, graph, k, v, pheromone_rate=0.8, heuristic_rate=0.2,
                     evaporation_rate=0.2, nAnts=20, nBest=3, iterMax = 10**4,
                 iterNoImproveMax = 100):
        self.pheromone_matrix = {}
        self.graph = graph
        self.k = k
        self.v = v
        self.pheromone_rate = pheromone_rate
        self.heuristic_rate = heuristic_rate
        self.evaporation_rate = evaporation_rate
        self.nAnts = nAnts
        self.nBest = nBest
        self.iterMax = iterMax
        self.iterNoImproveMax = iterNoImproveMax

    def evaporation(self):
        pass

    def reinforcement(self):
        pass

    def construct(self):
        pass

    def init_pheromone_matrix(self):
        for e in self.graph.edges():
            self.pheromone_matrix[e] = 1

    def evaluate_sol(self, s):
        return evaluate(self.graph, s, self.k, self.v)

    def optimization(self):
        """
        Otimização por colônia de formigas. Utiliza os parâmetros fornecidos
        para determinar as rotas construidas pelas formigas, atualizando
        a matrix de feromônios de forma off-line e elitista.

        Return:
            (list, float): solução (rota) com cidades a serem visitadas e custo da
            solução.
        """
        self.init_pheromone_matrix()
        best_sol = None
        iterNoImprove = 0
        S = []
        for ant in range(self.nAnts):
            S.append([])
        for it in range(self.iterMax):
            for ant in self.nAnts:
                S[ant] = self.construct()
            
            # improv_rate = abs(new_best[1]/best_sol[1] - 1)
            # if improv_rate < 0.01:
            #     iterNoImprove +=1
            self.reinforcement()
            self.evaporation()

            if iterNoImprove >= self.iterNoImproveMax:
                break

        return best_sol

class SimulatedAnnealing:
    """
    Classe que implementa a otimização por utilizando Simulated Annealing.
    Critério de parada é atingir o número máximo de iterações ou número máximo
    de iterações sem melhora da solução.

    Args:
        graph (NetworkX.Graph): grafo do TSPd.
        Tmax (float): Temperatura máxima. Entre 0  e 1.
        Tmin (float): Temperatura mínima. Valor entre 0 e 1.
        r (float): Taxa de resfriamento. Valor entre 0 e 1.
        iterMax (int): número máximo de iterações .
        iterNoImproveMax (int): número máximo de iterações sem melhora.
    """
    def __init__(self, graph, k, v, Tmax, Tmin, r, iterMax=10**4, iterNoImproveMax=100):
        self.graph = graph
        self.k = k
        self.v = v
        self.Tmax = Tmax
        self.Tmin = Tmin
        self.r = r
        self.iterMax = iterMax
        self.iterNoImproveMax = iterNoImproveMax

    def candidate_cost(self, s):
        return evaluate(self.graph, s, self.k, self.v)

    def candidates(self, neighbors):
        return sorted(neighbors, key=self.candidate_cost)

    def candidate(self, neighbors):
        return max(neighbors, key=self.candidate_cost)

    def optimize(self):
        """
        Executar otimização. Utiliza os parâmetros fornecidos
        para determinar as rotas construidas pelas formigas, atualizando
        a matrix de feromônios de forma off-line e elitista.

        Return:
            (list, float): solução (rota) com cidades a serem visitadas e custo da
            solução.
        """
        s = nearest_neighbor2(self.graph)
        cost = evaluate(self.graph, s, self.k, self.v)
        T = self.Tmax
        it = 0
        while T >= self.Tmin:
            candidate = self.candidate(neighborhood_2opt(self.graph, s))
            cCost = evaluate(self.graph, candidate, self.k, self.v)
            if cCost < cost or random.randint(0,99)/100 < exp((cCost - cost)/T): 
                s = candidate.copy()
                cost = cCost
            it +=1
            T = T*self.r
        return s
