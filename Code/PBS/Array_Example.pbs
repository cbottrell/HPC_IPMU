#!/bin/bash 
#PBS -N Array_Example
#PBS -o /lustre/work/tutorial/scratch
#PBS -e /lustre/work/tutorial/scratch
#PBS -l select=1:ncpus=1:mem=32mb
#PBS -l walltime=00:30:00
#PBS -J 0-127:1
#PBS -u tutorial
#PBS -M connor.bottrell@ipmu.jp
#PBS -m ae
#PBS -V
#PBS -q tiny

# activate Python 3
source /home/anaconda3/bin/activate
# you can set environment variables in the job script
export HPC_DIR=/lustre/work/tutorial/HPC_IPMU
cd $HPC_DIR/Code/Array
# run program
python Array_Example.py
