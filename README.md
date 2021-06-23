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

This command creates a new python environment called `tf39_cpu` which runs the latest stable version of Python 3.9. Once you have created the new environment, you can view it and all other existing environments (including `base`) with `conda env list`. You can activate any of these environments as follows:

    conda activate tf39_cpu
    
Where you can replace `tf39_cpu` with the name of your environment. This installation will be fairly bare-bones. But you can now start installing packages. For example, the most recent `numpy` version can be installed using the `pip` version that is installed when you created your python environment. Type `which pip` and you will see that it is a specific pip installation for your python environment. Now install numpy:

    pip install numpy

`numpy` is one of many useful Python packages. Wouldn't it be nice if there is a stack of all the useful scientific packages so that you wouldn't have to install them all separately and think about dependencies? Oh yeah:

    pip install scipy-stack
    
 For more documentation on conda, including more management options and deletion of environments, go to the conda docs here:
 
    https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html
  
