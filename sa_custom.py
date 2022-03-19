import time
import argparse
import tsplib95 as tsplib
from heuristics import SimulatedAnnealing, AntColony

def main():
    parser = argparse.ArgumentParser(
        description='Programa lê uma instância da tsplib '+
        ', gera uma solução inicial utilizando a heurística Ant Colony '+
        'e otimiza esta solução utilizando Simulated Annealing.'
    )
    parser.add_argument(
        '--file',
        '-f',
        type=str,
        required=True,
        help='Caminho até instância da tsplib.'
    )
    parser.add_argument(
        '-k',
        type=int,
        default=0,
        required=True,
        help='Número de entregas do Tspd.'
    )
    
    parser.add_argument(
        '-v',
        type=int,
        default=0,
        required=True,
        help='Valor de cada entrega do Tspd.'
    )

    parser.add_argument(
        '--t-max',
        type=float,
        default=0,
        required=True,
        help='Temperatura máxima do Simulated Annealing. Valores entre 0 e 1.'
    )

    parser.add_argument(
        '--t-min',
        type=float,
        default=0,
        required=True,
        help='Temperatura mínima do Simulated Annealing. Valores entre 0 e 1.'
    )

    parser.add_argument(
        '-c',
        type=float,
        default=0,
        required=True,
        help='SA Taxa de resfriamento. Valores entre 0 e 1.'
    )

    parser.add_argument(
        '-i',
        type=int,
        default=100,
        required=True,
        help='Valor máximo de iterações do ACO.'
    )

    parser.add_argument(
        '-n',
        type=int,
        default=10,
        required=True,
        help='Valor máximo de iterações sem melhora no ACO.'
    )
    
    parser.add_argument(
        '-p',
        type=float,
        default=0.3, required=True,
        help='Taxa de influência do feromômio. Valores entre 0 e 1.'
    )

    parser.add_argument(
        '-m',
        type=float,
        default=1, required=False,
        help='Limite para influência do feromômio. Valores entre 0 e 1.'
    )

    parser.add_argument(
        '-r',
        type=float,
        default=0.2, required=True,
        help='Taxa de Evaporação. Valores entre 0 e 1.'
    )

    parser.add_argument(
        '-a',
        type=int,
        default=20,
        required=True,
        help='Número de formigas no ACO.'
    )

    parser.add_argument(
        '-b',
        type=int,
        default=5,
        required=True,
        help='Número das k melhores formigas no ACO a serem usadas na atualização do feromônio.'
    )

    parser.add_argument(
        '--exec-data',
        '-e',
        action='store_true',
        required=False,
        help='Imprime dados de execução como os parâmetros de execução: k, v, solução, custo e tempo de execução',
        default=False
    )

    args = parser.parse_args()

    start = time.time()
    problem = tsplib.load(args.file)
    g = problem.get_graph()

    iter_max = 100
    iter_no_improv = 10
    p = 0.3
    pmax = 0.8
    evaporation_rate = 0.02
    k = 0
    v = 0
    nAnts = 20
    nBest = 5

    if args.i:
        iter_max = args.i

    if args.p:
        p = args.p

    if args.m:
        pmax = args.m

    if args.r:
        evaporation_rate = args.r

    if args.k:
        k = args.k
    
    if args.v:
        v = args.v

    if args.a:
        nAnts = args.a

    if args.b:
        nBest = args.b

    if args.n:
        iter_no_improv = args.n

    Tmax = 0.8
    if args.t_max:
        Tmax = args.t_max
    Tmin = 0.2
    if args.t_min:
        Tmax = args.t_max
    cooling_rate = 0.01
    if args.c:
        cooling_rate = args.c

    h0 = AntColony(g, k, v, p, pmax, evaporation_rate, nAnts, nBest, iter_max, iter_no_improv)
    s0, _ = h0.find_solution()
    h = SimulatedAnnealing(g, s0, k, v, Tmax, Tmin, cooling_rate)

    sol, cost = h.find_solution()
    if args.exec_data:
        print(k, v, p, pmax, evaporation_rate, nAnts, nBest, iter_max, iter_no_improv, Tmax, Tmin, cooling_rate)
        print(str(sol).replace(' ', ''), cost, '%s' % ((time.time() - start)))
    else:
        print(sol, cost)

if __name__ == '__main__':
    main()
