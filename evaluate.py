import argparse
import tsplib95 as tsplib

deliveriesDict = {}

def getDeliveries(k):
    deliveries = {}
    if k == 0:
        return deliveries

    for i in range(1,k+1):
        deliveries[i*2] = i*2+1

    return deliveries

def delivery(i, j, deliveries, v):
    if i+1 in deliveries and deliveries[i+1] == j+1:
        return v
    return 0

def evaluate(graph, solution, k, v):
    """
    Função que avalia solução para o TSPd.

    Args:
        graph (NetworkX.Graph): Grafo do problema. Estrutura suportada pela 
    NetworkX lib.
        k (int): Número de entregas no TSPd
        v (int): Número de entregas no TSPd.

    Return:
        int or float: avaliação da solução.
    """
    sCost = 0
    g = graph
    nodes = list(g.nodes)

    deliveries = getDeliveries(k)

    # sem solução. default é a solução em ordem
    if len(solution) == 0:
        for n in nodes:
            solution.append(n)
        solution.append(nodes[0])

    for n in range(len(solution)-1):
        i = solution[n]
        j = solution[n + 1]

        sCost += g[i][j]['weight'] 
        if k != 0:
            sCost -= delivery(i, j, deliveries, v)

    return sCost

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Programa lê uma instância da tsplib '+
        'e avalia a solução em ordem para o Tspd.'
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

    solution = []
    if args.solution is not None:
        solution = args.solution

    problem = tsplib.load(args.file)
    g = problem.get_graph()
    solEval = evaluate(g, solution, args.k, args.v)
    print(solEval)
