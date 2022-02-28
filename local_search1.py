import argparse
import tsplib95 as tsplib
from evaluate import evaluate
from neighborhoods import nearest_neighbor1
from search import local_search

def main():
    parser = argparse.ArgumentParser(
        description='Programa lê uma instância da tsplib '+
        'e gera solução inicial utilizando a heurística do vizinho mais '+
        'próximo. Versão 1: adiciona cidades somente no final da solução.'
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
        '--solution',
        '-s',
        type=list,
        action='append',
        required=False,
        help='Solução para o problema(lista de vértices a serem visitados).'+
        ' Default: solução em ordem.'
    )
    
    args = parser.parse_args()
    sol = []
    if args.solution is not None:
        sol = args.solution

    problem = tsplib.load(args.file)
    g = problem.get_graph()
    sol = nearest_neighbor1(g)
    cost = evaluate(g, sol, args.k, args.v)

    iter_max = 10**4
    iter_no_improve_max = 100
    sol, cost = local_search(g, sol, args.k, args.v, iter_max, iter_no_improve_max)
    print(sol)
    print(cost)

if __name__ == '__main__':
    main()
