# gromacs_bench
Generate SLURM submit scripts to test a set of resource allocations for GROMACS simulations

### Creating GROMACS run directories
`generate_test_runs.py` will generate a .tpr file and a set of run directories containing all permutations of the parameters defined in `example_params.json`.  It assumes the following names (defaults for the '[Lysozyme in water](http://www.mdtutorials.com/gmx/lysozyme/index.html)' example) for your grompp input:  
* mdp : md.mdp
* structure : npt.gro
* topology : topol.top
* index : index.ndx

If you use other file names or need additional options, edit the grompp command in `generate_test_runs.py`.

`generate_test_runs.py` has a default set of parameters to vary and a default submission script which will be used if no arguments are provided.  If you would like to vary different parameters or use a different submission script template, copy and modify `example_params.json` and `example_submit.sh` and run `generate_test_runs.py` with the `-p` and `-f` options for the params and submit file, respectivley.  The params file should be a json where each key has an easy-to-remember name and each value is a list of possible (string) values.  The submit file is a standard Slurm submit file where the parameters to be varied are replaced with `{key_name}` where `key_name` matches the keys in the params json file.  These will be replaced using Python string formatting by `generate_test_runs.py`.

If you would like to have the script submit your jobs for you, add the `-s` option.  Otherwise jobs can be submitted with:
```bash
for x in run*; do
  sbatch $x\/submit.sh
done
```

#### `generate_test_runs.py` options
```
-h Show the help and exit
-p <filename.json> Read the variable parameters from the provided json file.
-f <filename.sh> Use the provided file as the template for the Slurm submit file.
-s If set, automatically submit the jobs to Slurm once all run directories are created.
```

### GROMACS simulations
Each submit directory is set to run for 5 minutes, once the queue has cleared and all simulations finished you can move on to analysis.

### Analyzing simulation performance
`analyze.py` will read the GROMACS log files in each of the run directories and report the best performing simulations (in ns/day).  It will also report if any of the runs failed (performance not reported).  It defaults to just printing the run number and performance, however you can add additional columns to the output with the `-f` option followed by any of the key names from your parameter file used for `generate_test_runs.py`.  By default it will report the best 10 simulations (or all simulations if fewer than 10 were run).  This can be changed by setting the `-n` option.

#### `analyze.py` options
```
-h Show the help and exit
-f <key1 key2 ... > Append columns to the output table with the values of each key used in each simulation.
-n <number> Show the top <number> simulations
```
