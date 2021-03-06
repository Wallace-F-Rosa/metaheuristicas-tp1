import time
import argparse
import tsplib95 as tsplib
from heuristics import Grasp

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
        '-i',
        type=int,
        default=100,
        required=True,
        help='Valor máximo de iterações do GRASP.'
    )
    
    parser.add_argument(
        '-a',
        type=float,
        default=0.2, required=True,
        help='Porcentagem da CL utilizada na RLC. Valores entre 0 e 1.'
    )

    parser.add_argument( '--solution',
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

    iter_max = 100
    a = 0.2
    if args.i:
        iter_max = args.i

    if args.a:
        a = args.a

    heuristic = Grasp(g, args.k, args.v, a, iter_max)
    sol, cost = heuristic.find_solution()
    if args.exec_data:
        print(args.k, args.v, iter_max, a)
        print(str(sol).replace(' ', ''), cost, '%s' % ((time.time() - start)))
    else:
        print(sol, cost)

if __name__ == '__main__':
    main()
