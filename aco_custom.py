import time
import argparse
import tsplib95 as tsplib
from heuristics import AntColony
from search import local_search

def main():
    parser = argparse.ArgumentParser(
        description='Programa lê uma instância da tsplib '+
        'e gera solução inicial utilizando a heurística de colônia de formigas'+
        'combinada com a busca tabu.'
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
    r = 0.02
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
        r = args.r

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

    heuristic = AntColony(g, k, v, p, pmax, r, nAnts, nBest, iter_max, iter_no_improv)
    sol, cost = heuristic.find_solution()
    if args.exec_data:
        print(args.k, args.v, p, pmax, r, nAnts, nBest, iter_max, iter_no_improv)
        print(str(sol).replace(' ', ''), cost, '%s' % ((time.time() - start)))
    else:
        print(sol, cost)

if __name__ == '__main__':
    main()
