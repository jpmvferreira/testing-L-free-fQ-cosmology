#!/bin/bash

# path to cmdstan install
CMDSTAN=$HOME/cmdstan-2.31.0

# provide model path
MODEL=model/shift-LCDM.stan

# provide input data file
DATA=data/shift-parameters-mock-LCDM.json

# specifiy output folder
OUTPUT=output/shift-LCDM-mock

# provide init file
INIT=config/init.json

# create directory and subdirectories
mkdir -p $OUTPUT
mkdir $OUTPUT/data
mkdir $OUTPUT/model
mkdir $OUTPUT/chain
mkdir $OUTPUT/log
mkdir $OUTPUT/analysis

# compile the model
MODEL_BIN=$(readlink -f "$MODEL" | sed "s/.stan//g")
make -j -C $CMDSTAN $MODEL_BIN

# run the job(s) in the cluster using SLURM
for I in $(seq 1 10); do
  srun                          \
    --job-name=myMCMC           \
    --ntasks=1                  \
    --output=$OUTPUT/log/$I.log \
    --time=12-00:00:00          \
    --mem-per-cpu=512           \
  $MODEL_BIN                             \
    	sample                           \
    	adapt delta=0.9                  \
    	algorithm=hmc                    \
    	engine=nuts                      \
    	max_depth=20                     \
    	num_samples=7500                 \
    	num_warmup=2500                  \
    	save_warmup=1                    \
    	init=$INIT                       \
    	data file=$DATA                  \
    	output file=$OUTPUT/chain/$I.csv \
  &
done

# wait for all the chains to finish
wait

# copy data and model to output directory
cp $DATA $OUTPUT/data
cp $MODEL $OUTPUT/model

# run cmdstan diagnostics
$CMDSTAN/bin/diagnose $OUTPUT/chain/?.csv > $OUTPUT/analysis/diagnose.log
$CMDSTAN/bin/stansummary -c $OUTPUT/analysis/stansummary.csv $OUTPUT/chain/?.csv

# make plots
# (solucao de rabo, so o faco pq tenho que ativar environment antes)
echo """
import matplotlib.pyplot as plt
import arviz as az
posterior = az.from_cmdstan(posterior='$OUTPUT/chain/*.csv', save_warmup=True)
az.plot_trace(posterior, var_names=('h', 'Omega_b', 'Omega_c', 'Omega_r', 'Omega_L'), compact=False, combined=False)
plt.tight_layout()
plt.savefig('$OUTPUT/analysis/traceplot.png')
""" > $OUTPUT/gen-traceplot.py
