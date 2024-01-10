import subprocess
import sys
import os
import json
import argparse
from pathlib import Path
from itertools import product

def cli_parser():
    parser = argparse.ArgumentParser(description="Generate SLURM submission files to test GROMACS performance for various resource allocations.")
    parser.add_argument('-p', '--params', type=str, default=os.path.join(os.path.dirname(__file__), "example_params.json"), help='If set, read parameter set to vary from a json file. If not set the program will use the default file provided.')
    parser.add_argument('-f', '--submit_file', type=str, default=os.path.join(os.path.dirname(__file__), "example_submit.sh"), help='If set, use this file as the submit file template. The file should contain a single format-ready python string (see example).')
    parser.add_argument('-s', '--submit', dest='submit', action='store_const', const=True, default=False, help='If provided, submit the jobs.')
    return parser

# Get options, variable parameters and submit template
parser = cli_parser()
args = parser.parse_args()
with open(args.params, 'r') as f:
    cli_options = json.loads(f.read())
        
with open(args.submit_file, 'r') as f:
    slurm_example = f.read()

# Create permutations of the parameters
keys, values = zip(*cli_options.items())
cli_permutations = [dict(zip(keys, v)) for v in product(*values)]

# Create tpr file
env = os.environ.copy()
subprocess.run(f'gmx grompp -f md.mdp -c npt.gro -p topol.top -n index.ndx -o start.tpr', shell=True, env=env)

# Create a simulation directory for each permutation
i = 0
for cp in cli_permutations:
    # skip invalid configurations
    if 'nb' in cp.keys() and 'pme' in cp.keys():
        if cp['nb'] == 'cpu' and cp['pme'] == 'gpu':
            continue
    
    # Create directory for the run
    p = Path(f"./run{i}")
    p.mkdir(exist_ok=True)

    # Create submit file for each run
    # You can add more parameters programatically here if you want.
    cp['jobid'] = str(i)
    cp['wd'] = str(os.path.join(os.getcwd(), f'run{i}'))
    with open(f'run{i}/submit.sh', 'w+') as f:
        f.write(slurm_example.format(**cp))

    # Dump the directory's variables in a readable format
    with open(f'run{i}/param_dict.json', 'w+') as f:
        json.dump(cp, f)

    i += 1

print(f"Created {i} directories.")

# Submit the jobs
if args.submit:
    for j in range(i):
        subprocess.run(f'sbatch run{j}/submit.sh', shell=True, env=env)

print(f"Submitted {i} runs.")
