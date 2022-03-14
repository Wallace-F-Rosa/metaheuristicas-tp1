from evaluate import evaluate
from solutions import nearest_neighbor2, nearest_neighbor1
from neighborhoods import neighborhood_2opt
from search import local_search
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
    def __init__(self, graph, k, v, Tmax, Tmin, r):
        self.graph = graph
        self.k = k
        self.v = v
        self.Tmax = Tmax
        self.Tmin = Tmin
        self.r = r

    def candidate_cost(self, s):
        return evaluate(self.graph, s, self.k, self.v)

    def candidates(self, neighbors):
        return sorted(neighbors, key=self.candidate_cost)

    def candidate(self, neighbors):
        return max(neighbors, key=self.candidate_cost)

    def find_solution(self):
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
            delta = cCost - cost
            if cCost < cost or random.random() < exp(-delta/T): 
                s = candidate.copy()
                cost = cCost
            it +=1
            T = T*(1-self.r)
        return s, cost

class Grasp:
    """
    Classe que implementa a heurística GRASP. Solução inicial é construída via
    nearest neighbor e otimizada usando busca local. A busca Tabu é utilizada
    durante a construção da lista de candidatos.  Critério de parada é atingir
    o número máximo de iterações ou número máximo de iterações sem melhora da
    solução.

    Args:
        graph (NetworkX.Graph): grafo do TSPd.
        a (float): Porcentagem da CL utilizada na RCL. Valores entre 0 e 1
        iterMax (int): número máximo de iterações .
        iterNoImproveMax (int): número máximo de iterações sem melhora.
    """
    def __init__(self, graph, k, v, a, iterMax=100, iterNoImproveMax=10):
        self.graph = graph
        self.k = k
        self.v = v
        self.a = a
        self.iterMax = iterMax
        self.iterNoImproveMax = iterNoImproveMax
        self.tabu = {}
        self.nodes = list(graph.nodes())

    def candidate_cost(self, s):
        return evaluate(self.graph, s, self.k, self.v)

    def rcl(self, node, visited):
        g = self.graph
        cl = []
        clNotVisited = []
        for i in g[node]:
            notTabu = (node,i) not in self.tabu or self.tabu[(node,i)] == 0
            notVisisted = i not in visited
            if notVisisted:
                clNotVisited.append((node,i))
                if notTabu:
                    cl.append((i, g[node][i]['weight']))
        # ignore tabu if edge is needed
        if len(cl) == 0:
            cl = clNotVisited
        rclSize = ceil(len(cl)*self.a)
        if rclSize < 3:
            return sorted(cl, key=lambda i: i[1])

        return sorted(cl, key=lambda i: i[1])[:rclSize]

    def construct(self):
        s = []
        startNode = random.randint(0, len(self.nodes)-1)
        s.append(self.nodes[startNode])
        visited = { self.nodes[startNode]: True }
        while len(visited) != len(self.nodes):
            i = s[len(s)-1]
            candidates = self.rcl(i, visited)
            c = candidates[0]
            if len(candidates) > 1:
                c = random.choice(candidates)
            s.append(c[0])
            visited[c[0]] = True

        return s

    def update_tabu_list(self, s):
        t = random.randint(0, len(s)-1)
        for move in self.tabu:
            if self.tabu[move] > 0:
                self.tabu[move] -= 1
        self.tabu[(self.nodes[t], self.nodes[(t+1)%len(s)])] = 2

    def find_solution(self):
        """
        Executar heurística. Utiliza os parâmetros fornecidos
        para determinar as rotas construidas pelas formigas, atualizando
        a matrix de feromônios de forma off-line e elitista.

        Return:
            (list, float): solução (rota) com cidades a serem visitadas e custo da
            solução.
        """
        s = nearest_neighbor1(self.graph)
        cost = evaluate(self.graph, s, self.k, self.v)
        it = 0
        while it < self.iterMax:
            s1 = self.construct()
            s1, s1Cost = local_search(self.graph, s, self.k, self.v, self.iterMax, self.iterMax*0.1)


            if s1Cost < cost:
                s = s1
                cost = s1Cost

            self.update_tabu_list(s)
            it +=1

        return s, cost
