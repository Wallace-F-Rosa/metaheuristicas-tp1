# Resolvendo problema TSPd usando metaheurísticas
Este projeto é resultado de um trabalho prático da disciplina de Metaheurísticas
oferecida no curso de Ciência da Computação da UFV. Aqui são implementadas
soluções para resolver o problema do Caixeiro viajante com um pequeno ajuste
considerando a possibilidade de fazer entregas entre as cidades (TSPd
: Travelling Salesman with deliveries)

## Instalando requerimentos
`pip install -r requirements.txt`

## Rodando projeto 
Usamos o comando abaixo para compilar o código pytho utilizando [Cython](https://cython.readthedocs.io/en/latest/index.html):

`python setup.py build_ext --inplace`

Agora é possível executar alguma das soluções:

| Solução | Descrição |
|---------|-----------|
| local_search1 | Solução utilizando busca local com solução inicial obtida pelo método guloso do vizinho mais próximo considerando modificação somente no final da solução |
| local_search2 | Solução utilizando busca local com solução inicial obtida pelo método guloso do vizinho mais próximo considerando modificação tanto no inicio como no final da solução |

Será usada como exemplo a solução `local_search2` mas o processo é análogo para
todas as soluções aqui contidas:

`python local_search2.py -f data/gr17.tsp -k 0 -v 0`

Parâmetros de execução:
```
usage: local_search2.py [-h] --file FILE -k K -v V [--solution SOLUTION]

Programa lê uma instância da tsplib e gera solução inicial utilizando a heurística do vizinho mais próximo. Versão 1: adiciona cidades
somente no final da solução.

options:
  -h, --help            show this help message and exit
  --file FILE, -f FILE  Caminho até instância da tsplib.
  -k K                  Número de entregas do Tspd.
  -v V                  Valor de cada entrega do Tspd.
  --solution SOLUTION, -s SOLUTION
                        Solução para o problema(lista de vértices a serem visitados). Default: solução em ordem.
```

