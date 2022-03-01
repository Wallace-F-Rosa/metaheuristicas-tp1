from evaluate import evaluate

class AntColonyOptimization:
    """
    Classe que implementa a otimização por colônia de formigas com atualização
    de feromônio off-line baseada em ranqueamento. Critério de parada é atingir
    o número máximo de iterações ou número máximo de iterações sem melhora da
    solução.

    Args:
        graph (NetworkX.Graph): grafo do TSPd.
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
    def __init__(self, graph, pheromone_rate=0.8, heuristic_rate=0.2,
                     evaporation_rate=0.2, nAnts=20, nBest=3, iterMax = 10**4,
                 iterNoImproveMax = 100):
        self.pheromone_matrix = {}
        self.graph = graph
        self.pheromone_rate = pheromone_rate
        self.heuristic_rate = heuristic_rate
        self.evaporation_rate = evaporation_rate
        self.nAnts = nAnts
        self.nBest = nBest
        self.iterMax = iterMax
        self.iterNoImproveMax = iterNoImproveMax
        self.pop = [] # solutions found by the ants

    def evaporation(self):
        pass

    def reinforcement(self):
        pass

    def construct(self):
        pass

    def init_pheromone_matrix(self):
        pass

    def optimization(self):
        """
        Otimização por colônia de formigas. Utiliza os parâmetros fornecidos
        para determinar as rotas construidas pelas formigas, atualizando
        a matrix de feromônios de forma off-line e elitista.

        Return:
            (list, int): solução (rota) com cidades a serem visitadas e custo da
            solução.
        """
        self.init_pheromone_matrix()
        best_sol = None
        iterNoImprove = 0
        for it in range(self.iterMax):
            for ant in self.nAnts:
                self.pop.append(([], 0))
            for ant in self.nAnts:
                sol, cost = self.construct()
                self.pop[ant][0] = sol
                self.pop[ant][1] = cost

            improv_rate = 0.0
            if best_sol == None:
                best_sol = self.pop[0]

            new_best = ([],0)
            for sol in self.pop:
                if sol[1] < best_sol[1]:
                    new_best = sol

            improv_rate = abs(new_best[1]/best_sol[1] - 1)
            if improv_rate < 0.01:
                iterNoImprove +=1
            self.reinforcement()
            self.evaporation()

            if iterNoImprove >= self.iterNoImproveMax:
                break

        return best_sol
