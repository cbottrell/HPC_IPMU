import sys
import numpy as np

from mpi4py import MPI

comm = MPI.COMM_WORLD
name = MPI.Get_processor_name()

print("Hello world fromp processor {}, rank {} out of {} processors"\
	.format(name, comm.rank, comm.size))

print("Now I will take up memory and waste computing power for demonstration purposes")

sys.stdout.flush()

nums = np.zeros((500,500,500))

nums[0,0,0] = 1.

while(1):

	nums[0,0,0] *= 3.14
	nums[0,0,0] /= 3.14

