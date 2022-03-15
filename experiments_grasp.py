from datetime import datetime
import subprocess
import argparse
import csv
import os

def create_data_dir(instance):
    instance_dir = 'experiments_grasp/{0}'.format(instance)
    if not os.path.isdir(instance_dir):
        os.makedirs(instance_dir)

def get_instance_data_file(instance, k, v):
    create_data_dir(instance)
    instance_csv = 'experiments_grasp/{0}/{0}_{1}_{2}.csv'.format(instance, k, v)
    if not os.path.isfile(instance_csv):
        with open(instance_csv, 'w+') as csvf:
            csvW = csv.DictWriter(csvf, fieldnames=['instance', 'k', 'v',
                                                    'iterMax',
                                                    'a',
                                                    'solution',
                                                    'cost',
                                                    'exec_time',
                                                    'timestamp'])
            csvW.writeheader()
            pass
    return instance_csv

def run_instances(instances, no_delivery=False, only_delivery=False, repeat=10):
    # each instance has args with delivery or not
    args = {
        'gr17': {
            True: [{'k': 3, 'v': 80, 'iter_max': 10, 'a': 0.1}],
            False: [{'k': 0, 'v': 0, 'iter_max': 10, 'a': 0.1}],
        },
        'gr21': {
            True: [],
            False: [{'k': 0, 'v': 0, 'iter_max': 10, 'a': 0.2}] 
        },
        'gr48': {
            True: [
                {'k': 6, 'v': 80, 'iter_max': 10, 'a': 0.1},
                {'k': 10, 'v': 80, 'iter_max': 10, 'a': 0.1}
            ],
            False:[{'k': 0, 'v': 0, 'iter_max': 10, 'a': 0.1}]
        },
        'gr120': {
            True: [],
            False: [{'k': 0, 'v': 0, 'iter_max': 10, 'a': 0.1}]
        },
        'brazil58': {
            True: [
                {'k': 5, 'v': 300, 'iter_max': 10, 'a': 0.1},
                {'k': 8, 'v': 100, 'iter_max': 10, 'a': 0.1},
                {'k': 8, 'v': 250, 'iter_max': 10, 'a': 0.1}
            ],
            False: [
                {'k': 0, 'v': 0, 'iter_max': 10, 'a': 0.2}
            ]
        },
        'berlin52': {
            True: [{'k': 3, 'v': 90, 'iter_max': 10, 'a': 0.2}],
            False: [{'k': 0, 'v': 0, 'iter_max': 10, 'a': 0.2}]
        },
        'fri26': {
            True: [],
            False: [{'k': 0, 'v': 0, 'iter_max': 10, 'a': 0.2}]
        },
        'eil51': {
            True: [],
            False: [{'k': 0, 'v': 0, 'iter_max': 10, 'a': 0.2}]
        },
        'eil76': {
            True: [],
            False: [{'k': 0, 'v': 0, 'iter_max': 10, 'a': 0.2}]
        },
        'eil101': {
            True: [{'k': 10, 'v': 5, 'iter_max': 10, 'a': 0.2}],
            False: [{'k': 0, 'v': 0, 'iter_max': 10, 'a': 0.2}]
        },
        'a280': {
            True: [{'k': 10, 'v': 10, 'iter_max': 10, 'a': 0.2}],
            False: [{'k': 0, 'v': 0, 'iter_max': 10, 'a': 0.2}]
        },
    }

    for instance in instances:
        delivery = [False,True]
        if no_delivery:
            delivery.pop(1)
        elif only_delivery:
            delivery.pop(0)

        for d in delivery:
            for arg in args[instance][d]:
                for r in range(repeat):
                    k = arg['k']
                    v = arg['v']
                    iter_max = arg['iter_max']
                    a = arg['a']
                    # create instance csv to hold data
                    instancef = get_instance_data_file(instance, k, v)
                    now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                    row = {
                        'instance': instance,
                        'timestamp': now
                    }
                    with open(instancef, 'a') as csvf:
                        fields = ['instance', 'k', 'v',
                                    'iterMax',
                                    'a',
                                    'solution',
                                    'cost',
                                    'exec_time',
                                    'timestamp']                        
                        csvW = csv.DictWriter(csvf, fieldnames=fields.copy())
                        instance_path = 'data/{0}.tsp'.format(instance)
                        # run heuristic
                        result = subprocess.run(['python',
                                                 'grasp_custom.py',
                                                 '-f', instance_path,
                                                 '-k', str(k),
                                                 '-v', str(v),
                                                 '-i', str(iter_max),
                                                 '-a', str(a),
                                                 '-e'],
                                                capture_output=True)
                        # get data from output
                        lines = result.stdout.decode('utf-8').split("\n")
                        values = lines[0].split(' ') + lines[1].split(' ')
                        fields.pop(0)
                        fields.pop(len(fields)-1)
                        for i in range(len(fields)):
                            row[fields[i]] = values[i]
                        csvW.writerow(row)

if __name__ == '__main__':
    argparse = argparse.ArgumentParser(description='Experimentos do TP1'+
                                       'utilizando heurística customizada')
    argparse.add_argument('--all',
                          '-a',
                          action='store_true',
                          help='Roda o experimento em todas as instâncias.',
                          default=True
                          )
    argparse.add_argument('--no-delivery',
                          '-nd',
                          action='store_true',
                          help='Roda o experimento em todas as instâncias'+
                          'somente sem os valores de entrega.',
                          default=False)

    argparse.add_argument('--delivery',
                          '-d',
                          action='store_true',
                          help='Roda o experimento em todas as instâncias'+
                          'somente com os valores de entrega.',
                          default=False)
    
    argparse.add_argument('--repeat',
                          '-r',
                          type=int,
                          help='Informa quantas vezes rodar cada instâncias.',
                          default=10)
    instances = [
        'gr17',
        'gr21',
        'gr48',
        'gr120',
        'brazil58',
        'berlin52',
        'fri26',
        'eil51',
        'eil76',
        'eil101',
        'a280',
    ]

    argparse.add_argument('--instances', '-i', nargs='+', default=['gr17'])
    args = argparse.parse_args()

    if args.instances:
        instances = args.instances
    run_instances(instances, args.no_delivery, args.delivery, args.repeat)
