#!/usr/bin/env bash

N=$(ls $1/chain/*.csv | wc -l)
for ID in $(seq 1 $N); do
  echo "Chain Nº" $ID

  # display number of steps
  cat $1/log/$ID.log | grep % | tail -n 1

  # get all steps so far
  # () estava a meter um erro aqui algures
  #STEPS=$(cat $1/chain/$ID.csv | sed "s/^#/d" | wc -l)
  #STEPS=$((STEPS-1))

  # get running time of corresponding chain
  # () meter fallback para o caso de ja estar completed
  # () nao sei como fzr isto :(

  # compute number of steps per second

  echo ""
done
