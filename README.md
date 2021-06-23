# Kavli IPMU HPC documentation 
Useful tips and tricks for high-performance computing using Kavli IPMU clusters (specifically idark, which uses the PBS Professional queue system).

## Python

<p>The code examples used in this tutorial use Python 3. Never fear, installation of Python 3 is not required as it is already installed on the idark cluster. To activate Python 3, login to idark and write the following from the command line:</p>

    source /home/anaconda3/bin/activate

or 

    conda activate base

if you have already done `conda init` (default for new accounts, check your ~/.bashrc file). Once you have activated the conda base python environment, do:

    python

<p>and you will see that the version that has been activated is Python 3.8.5. Conda is a python environment manager. Suppose you start a new project and want to use all of the new versions of each module -- but want to keep older versions available for compatibility with previous projects. This is the rationale of conda. Suppose you want to create a new python environment that you can activate anywhere on the cluster -- from the login node or compute nodes (either in batch or interactive mode). </p>

The gw and gfarm clusters use older versions of python which may not be compatible with some of the Python programs in this documentation. However, once you are famililar with the concepts, they can be easily applied with older versions of Python. 
  
