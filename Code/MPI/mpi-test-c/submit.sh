#!/bin/bash
#PBS -q small
#PBS -l nodes=2:ppn=3
#PBS -l walltime=01:00:00
#PBS -N test
#PBS -o OUT
#PBS -e ERR
#PBS -k eo

cd ${PBS_O_WORKDIR}

mpirun -n 6 ./test

