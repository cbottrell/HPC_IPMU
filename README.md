# Kavli IPMU HPC documentation 
Useful tips and tricks for high-performance computing using Kavli IPMU clusters (specifically iDark).

## Python

The code examples used in this tutorial use Python 3. Never fear, installation of Python 3 is not required as it is already installed on the idark cluster. To activate Python 3, login to idark and write the following from the command line:

    source /home/anaconda3/bin/activate

or 

    conda activate base

if you have already done `conda init` (default for new accounts, check your ~/.bashrc file). Once you have activated the conda base python environment, do:

    python

and you will see that the version that has been activated is Python 3.8.5. Conda is a python environment manager. Suppose you start a new project and want to use all of the up-to-date versions of your favorite python modules -- but want to keep older versions available for compatibility with previous projects. This is the rationale of conda. With conda you can create python environments that you can activate anywhere on the cluster -- from the login node or compute nodes (either in interactive mode or directly inside your job scripts!). 

<p>If you have not yet used conda, start by writing:</p>

    conda init
    
which will add the initialization script to your `~.bashrc` that is executed whenever you login to the cluster or allocate to a compute node. When you use `conda init`, the next time you login to the cluster you will see `(base)` next your credentials on the command line. This means that your `base` conda environment is active. You can turn off automatic activation of this environment by doing:

    conda config --set auto_activate_base false
    
You can create your own environments with conda with any specified python version:

    conda create -n tf39_cpu python=3.9

Once you have created the environment `tf39_cpu` (or a less boring name), you can view existing environments with `conda env list`. There, you will see the `base` environment and any other environments. 

  
