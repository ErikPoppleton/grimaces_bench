import os
import argparse
import json

def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

def cli_parser():
    parser = argparse.ArgumentParser(description="Analyze a set of GROMACS test runs and find the optimal parameters")
    parser.add_argument('-f', '--field', type=str, nargs='+', help='Show the values of these parameters in the output table.')
    parser.add_argument('-n', '--n_return', type=int, default=10, help='List the top n simulations')
    return parser

# Get command line arguments
parser = cli_parser()
args = parser.parse_args()
test_field = args.field
n_ret = args.n_return

if test_field is None:
    test_field = []

# Get list of directories
dirs = get_immediate_subdirectories('.')

ns_per_day = {}
field_value = {}
print()
print('Failed runs:')
for d in dirs:
    # you might have, for example a force field directory...
    if not d.startswith('run'):
        continue
    
    # Parse the log file and get performance
    try:
        with open(d+'/md.log', 'r') as f:
            lines  = f.readlines()
            for l in lines:
                if "Performance" in l:
                    l = l.split()
                    ns_per_day[d] = float(l[1])
        if test_field:
            with open(d+'/param_dict.json', 'r') as f:
                params = json.loads(f.read())
                field_value[d] = [params[f] for f in test_field] # extract variables of interest
        else:
            field_value[d] = []
    except:
        print(d)

if n_ret > len(ns_per_day.keys()):
    n_ret = len(ns_per_day.keys())

# Get the best-performing simulations and print
ns_per_day = {k: v for k, v in sorted(ns_per_day.items(), key=lambda item: item[1], reverse=True)}
print()
print('Best runs:')
print('run#\tns/day\t', end='')
print(*test_field)
for i in range(n_ret):
    k = list(ns_per_day.keys())[i]
    print(k, ns_per_day[k], *field_value[k], sep='\t')

