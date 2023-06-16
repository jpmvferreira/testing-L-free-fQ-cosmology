# path to cmdstan install
CMDSTAN=$HOME/projects/cmdstan

# provide model path
MODEL_STAN=model/shift.stan

# provide input data file
DATA=data/shift-mock.json

# specifiy output folder
OUTPUT=output/shift_mock

# provide init file
INIT=config/init.json

# create directory and subdirectories
# (!) devia dar exit se ja tivessem preenchidas as diretorias
mkdir -p $OUTPUT
mkdir $OUTPUT/data
mkdir $OUTPUT/model
mkdir $OUTPUT/chain
mkdir $OUTPUT/log
mkdir $OUTPUT/analysis

# compile the model
# cmdstan directory is hardcoded
# (!) devia dar exit se der erro a compilar
MODEL=$(realpath "$MODEL_STAN" | sed "s/.stan//g")
MODEL_BIN=$(realpath "$MODEL_STAN" | sed "s/.stan/.out/g")
make -j -C $CMDSTAN $MODEL
mv $MODEL $MODEL_BIN

# run the model
# warning: the order of the arguments matter!
for i in {1..4}; do
	time $MODEL_BIN                      \
		sample                           \
		num_samples=2500                 \
		num_warmup=2500                  \
		save_warmup=1                    \
		init=$INIT                       \
		data file=$DATA                  \
		output file=$OUTPUT/chain/$i.csv \
	&> $OUTPUT/log/$i.log                &
	sleep 2  # for some reason both the initial values and the seed are the same for all chains... this is a workaround
done

# wait for all chains to finish
wait

# copy stuff to output directory
cp $DATA $OUTPUT/data
cp $MODEL_STAN $OUTPUT/model

# run cmdstan diagnostics
$CMDSTAN/bin/diagnose $OUTPUT/chain/?.csv > $OUTPUT/analysis/diagnose.log
$CMDSTAN/bin/stansummary -c $OUTPUT/analysis/stansummary.csv $OUTPUT/chain/?.csv 

# make plots
# (mete esta gaita a ativar o environment pah)
echo """
import os
import matplotlib.pyplot as plt
import arviz as az
posterior = az.from_cmdstan(posterior=os.path.dirname(__file__) + '/chain/*.csv', save_warmup=True)
az.plot_trace(posterior, var_names=('h', 'Omega_b', 'Omega_c', 'Omega_r'), compact=False, combined=False)
plt.tight_layout()
plt.savefig(os.path.dirname(__file__) + '/analysis/traceplot.png')
""" > $OUTPUT/gen-traceplot.py
