# Kavli IPMU HPC documentation 
Useful tips and tricks for high-performance computing using Kavli IPMU clusters (specifically iDark).

## Python

The code examples used in this tutorial use Python 3. Never fear, installation of Python 3 is not required as it is already installed on the idark cluster. To activate Python 3, login to idark and write the following from the command line:

    source /home/anaconda3/bin/activate

or 

    conda activate base

if you have already done `conda init` (default for new accounts, check your ~/.bashrc file). Once you have activated the conda base python environment, do:

    python

and you will see that the version that has been activated is Python 3.8.5. 

## Conda

Conda is a python environment manager. Suppose you start a new project and want to use all of the up-to-date versions of your favorite python modules -- but want to keep older versions available for compatibility with previous projects. This is the rationale of conda. With conda you can create a library of separate python environments that you can activate anywhere on the cluster -- from the login node or compute nodes (either in interactive mode or directly inside your job scripts!). 

<p>If you have not yet used conda, start by writing:</p>

    conda init
    
which will add the initialization script to your `~/.bashrc` that is executed whenever you login to the cluster or allocate to a compute node. When you use `conda init`, the next time you login to the cluster you will see `(base)` next your credentials on the command line. This means that your `base` conda environment is active. You can turn off automatic activation of this environment by doing:

    conda config --set auto_activate_base false
    
You can create your own environments with conda with any specified python version:

    conda create -n tf39_cpu python=3.9

This command creates a new python environment called `tf39_cpu` which runs the latest stable version of Python 3.9. Once you have created the new environment, you can view it and all other existing environments (including `base`) with `conda env list`. You can activate any of these environments as follows:

    conda activate tf39_cpu
    
Where you can replace `tf39_cpu` with the name of your environment. This installation will be fairly bare-bones. But you can now start installing packages. For example, to install numpy, you can do:
    
    conda install numpy
    
If a package you want is unavailable from conda, you can also use `pip` within a conda environment. Type `which pip` and you will see that it is a specific pip installation for your python environment. Note, however, that this can sometimes lead to conflicts; see [here](https://www.anaconda.com/blog/using-pip-in-a-conda-environment) for detals. To install numpy using pip, do:

    pip install numpy

`numpy` is one of many useful Python packages. Wouldn't it be nice if there is a stack of all the useful scientific packages so that you wouldn't have to install them all separately and think about dependencies? Oh yeah:

    pip install scipy-stack
    
 For more documentation on conda, including more management options and deletion of environments, go to the conda docs here:
 
    https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html
  
## Python in Interactive jobs

An interactive job is useful for debugging. But all large jobs should be executed through the main queue for peak efficiency. You can submit an interactive job on any of the queues. Here is an example:

    qsub -l select=1:ncpus=1:mem=4gb -l walltime=3:0:0 -q tiny -I
    
You can also copy/paste this into an executable shell script instead of memorizing the syntax. This submission requests an allocation of 1 task with 1 CPU per task with 4GB of memory per task (i.e. 1 CPU on some node with at least 4GB of available memory). By executing, you will be put into the queue until the resources are available. Once you have been allocated to the resources, you can conduct your tests. Let's see if we can access our conda environment:

    conda activate tf39_cpu
    
## Python in Batch jobs

The same principle applies to job scripts in batch mode. In your job script, simply activate the conda environment before execution of your program. For example, after creating a path for your output and error files at /home/username/PBS, you could execute the following job script:

    #!/bin/bash 
    #PBS -N Demo
    #PBS -o /home/username/PBS 
    #PBS -e /home/username/PBS
    #PBS -l select=1:ncpus=1:mem=4gb
    #PBS -l walltime=0:0:30
    #PBS -u username
    #PBS -M username@ipmu.jp
    #PBS -m ae
    #PBS -q tiny

    # activate conda environment
    conda activate tf39_cpu
    python my_program.py
    
# Where to work on iDark

The `/home` file system has very limited space and may rapidly get congested if too many users are working and storing files there. As with previous clusters, iDark has a designated file system for work:

    /lustre/work/username
    
The snag is that the output files from job scripts will not save to this file system -- could be quite inconvenient. I have raised this issue with IT. For now, you should create a directory in the `/home` file system (e.g. `/home/username/tmp/pbs/` where those files can be directed in the `#PBS -o` and `#PBS -e` lines of your job scripts.

# Updates

If you have any comments or suggestions for this goodie bag of tips and tricks, please send them my way (`connor.bottrell 'at' ipmu 'dot' jp`) with a description and I will consider adding them to the list.

