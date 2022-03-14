import time
import argparse
import tsplib95 as tsplib
from evaluate import evaluate
from solutions import nearest_neighbor2
from search import local_search

def main():
    parser = argparse.ArgumentParser(
        description='Programa lê uma instância da tsplib '+
        'e gera uma solução utilizando busca local. '+
        'Solução inicial fornecida pela versão 2 do Nearest Neighbor.'
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
    
    parser.add_argument(
        '--exec-data',
        '-e',
        action='store_true',
        required=False,
        help='Imprime dados de execução como os parâmetros de execução: k, v, solução, custo e tempo de execução',
        default=False
    )

    args = parser.parse_args()
    sol = []
    if args.solution is not None:
        sol = args.solution

    start = time.time()
    problem = tsplib.load(args.file)
    g = problem.get_graph()
    sol = nearest_neighbor2(g)
    cost = evaluate(g, sol, args.k, args.v)

    iter_max = 10**4
    iter_no_improve_max = 100
    sol, cost = local_search(g, sol, args.k, args.v, iter_max, iter_no_improve_max)
    if args.exec_data:
        print(args.k, args.v)
        print(str(sol).replace(' ', ''), cost, '%s' % (time.time() - start))
    else:
        print(sol, cost)

if __name__ == '__main__':
    main()
