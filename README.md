# High Performance Computing at Kavli IPMU

Useful tips and tricks for high-performance computing on the IPMU cluster.

## Accessing the machines

There are two main machines at IPMU:

- `idark` is the main computer cluster.
- `gpgpu` is a box with 8 GPUs.

These machines are managed by IPMU's IT team, who can be reached at  `it 'at' ipmu 'dot' jp`. See the [internal webpage](https://www.ipmu.jp/en/employees-internal/computing) (ask the IT team for access) for technical details and specifications. 

The machines can only be accessed from within the campus intranet. To use them from home, ask the IT team for VPN connection information.

You will need an account on the machines you wish to access. Follow the IT team's instructions, which will involve sending them your ssh public key.

Once you're all set up you can connect to the servers with
```bash
$ ssh [username]@idark.ipmu.jp # for idark
$ ssh [username]@192.168.156.71 # for gpgpu
```

## Seeing what's going on

Once you ssh onto the cluster, you'll want to see what everyone else is doing.

The job manager on idark is PBS. To see what jobs are running, run

```bash
[username@idark ~]$ qstat
```

On gpgpu, the job manager is slurm. The equivalent command is

```bash
[username@gpgpu ~]$ squeue
```

It's important to know that there is no central system to allocate the GPUs on gpgpu, so you need to check which are available using the command

```bash
[username@gpgpu ~]$ nvidia-smi
```

## Setting up a Python environment

Before running your own jobs, you may wish to set up your Python environment. Python 3 is already installed on the cluster, and there are two main approaches to managing your python installation: `conda` and `pyenv`. Choose whichever you prefer.

### Conda

Conda is a python package and environment manager. Suppose you start a new project and want to use all of the up-to-date versions of your favorite python modules -- but want to keep older versions available for compatibility with previous projects. This is the rationale of conda. With conda you can create a library of separate python environments that you can activate anywhere on the cluster -- from the login node or compute nodes, either in interactive mode or directly inside your job scripts. 

The first time you log on to the cluster, run
```bash
[username@idark ~]$ conda init
```
This will add an initialization script to your `~/.bashrc` that is executed whenever you login to the cluster or allocate to a compute node. The next time you login, you will see `(base)` next to your credentials on the command line, indicating that your `base` conda environment is active. When you run python,
```bash
(base) [username@idark ~]$ python
```
and you will see that the version that has been activated is Python 3.8.10.

If you prefer, you can always turn off automatic activation of the environment by doing:
```bash
[username@idark ~]$ conda config --set auto_activate_base false
```
and instead manually activate the environment using 
```bash
[username@idark ~]$ source /home/anaconda3/bin/activate
```
or
```bash
[username@idark ~]$ conda activate base
```

To deactivate a conda environment, just run `conda deactivate`.

You can also create your own environments with conda with any specified python version:

```bash
[username@idark ~]$ conda create -n tf39_cpu python=3.9
```

This command creates a new python environment called `tf39_cpu` which runs the latest stable version of Python 3.9. Once you have created the new environment, you can view it and all other existing environments (including `base`) with `conda env list`. You can activate any of these environments as follows:
```bash
[username@idark ~]$ conda activate tf39_cpu
``` 
replacing `tf39_cpu` with the name of your environment. 

The default installation will be fairly bare-bones, but you can now start installing packages. To install numpy, for example, you can do:
```bash
(tf39_cpu) [username@idark ~]$ conda install numpy
```

If a package you want is unavailable from the conda package manager, you can use `pip` within a conda environment instead. Type `which pip` and you will see that it is a specific pip installation for your python environment. Note, however, that this can sometimes lead to conflicts; see [here](https://www.anaconda.com/blog/using-pip-in-a-conda-environment) for details. 

`numpy` is one of many useful Python packages. Wouldn't it be nice if there is a stack of all the useful scientific packages so that you wouldn't have to install them all separately and think about dependencies? Oh yeah:
```bash
(tf39_cpu) [username@idark ~]$ pip install scipy-stack
```

Later, we will see how to use this python environment for jobs. For more documentation on conda, including more management options and deletion of environments, check out the [conda docs](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html).

### pyenv

Unlike conda, which is a full package manager, pyenv is a simpler tool that just manages your different python versions. The idea is to use pip as the package manager and python's built in virtual environment feature to separate dependencies for different projects.

pyenv does not come pre-installed on the cluster machines. To install it, we use the [pyenv-installer](https://github.com/pyenv/pyenv-installer.
). First run 

```bash
[username@idark ~]$ curl https://pyenv.run | bash
```

and then add the following lines to your bash profile `~/.bashrc`:

```bash
export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
```

After restarting your terminal, pyenv should now be in your path and you can see the list of installable python versions:
```bash
[username@idark ~]$ pyenv install --list # see a list of installable versions
```
and then install one using
```bash
[username@idark ~]$ CPPFLAGS=-I/usr/include/openssl11 \
LDFLAGS=-L/usr/lib64/openssl11 \
pyenv install -v 3.11.3 # or something different
```

The new version will now show up if you run `pyenv versions`, and you can set it as your global python version using 

```bash
[username@idark ~]$ pyenv global 3.11.3

[username@idark ~]$ python --version
# Python 3.11.1

[username@idark ~]$ which python
# ~/.pyenv/shims/python

[username@idark ~]$ which pip
# ~/.pyenv/shims/pip
```

You can also set local python versions for different projects using `pyenv local`. Then to manage dependencies for different projects, you use python's built in `venv` feature. Here is a [tutorial](https://docs.python.org/3/tutorial/venv.html), and the tldr is as follows. Starting from your project folder, initialize a new virtual environment and activate it with

```bash
[username@idark project]$ python -m venv project-venv
[username@idark project]$ source project-venv/bin/activate
```

At which point you will see (project-venv) in the command prompt. If you now install dependencies or projects with pip, they will be installed in the local virtual environment.

## Running jobs on the cluster

Anytime you want to run code on the cluster, you should do so in a job. There are a lot of different types of jobs.

The basic pattern for a job in PBS (idark) is

```bash
#!/bin/bash 
#PBS -N demo # job name
#PBS -o /home/username/PBS/  # (path for stdout)
#PBS -e /home/username/PBS/  # (path for stderr)
#PBS -l select=1:ncpus=1:mem=4gb
#PBS -l walltime=0:0:30
#PBS -u username
#PBS -M username@ipmu.jp
#PBS -m ae # (email notification when job (a)borts or (e)nds)
#PBS -q tiny # which queue

# activate python environment
conda activate tf39_cpu
# for pyenv/virtualenv instead use
# source /home/username/project/project-venv/bin/activate

python my_program.py
```

## Python in Batch jobs

The same principle applies to job scripts in batch mode. In your job script, simply activate the conda environment before execution of your program. For example, after creating a path for your output and error files at /home/username/PBS, you could execute the following job script:

### Assigning GPUs to a job

1. Run "nvidia-smi" and identify GPUs which are NOT used.
2. Specify GPU you want use.
   $ export CUDA_DEVICE_ORDER=PCI_BUS_ID
   $ export CUDA_VISIBLE_DEVICES=X    # where X is GPU id
3. Run your process.

### Using Jupyter lab

job script

ssh port forwarding

function gpubridge(){
    if [ $# -eq 0 ]
    then
        localport=8000
        clusterport=9000
    else
        localport=($1)
        clusterport=($2)
    fi
    echo "$localport"
    echo "$clusterport"
    ssh -NfL ${localport}:localhost:${clusterport} passaglia@192.168.156.71
}

TODO: connecting your venv to jupyter 
jupytervenv:
	source venv/bin/activate && \
	pip install ipykernel && \
	pip install jupyter && \
	python -m ipykernel install --name venv-japandata --user

<!-- ## Python in Interactive jobs

An interactive job is useful for debugging. But all large jobs should be executed through the main queue for peak efficiency. You can submit an interactive job on any of the queues. Here is an example:

    qsub -l select=1:ncpus=1:mem=4gb -l walltime=3:0:0 -q tiny -I
    
You can also copy/paste this into an executable shell script instead of memorizing the syntax. This submission requests an allocation of 1 task with 1 CPU per task with 4GB of memory per task (i.e. 1 CPU on some node with at least 4GB of available memory). By executing, you will be put into the queue until the resources are available. Once you have been allocated to the resources, you can conduct your tests. Let's see if we can access our conda environment:

    conda activate tf39_cpu -->
    
# Where to work on iDark

The `/home` file system has very limited space and may rapidly get congested if too many users are working and storing files there. As with previous clusters, iDark has a designated file system for work:

    /lustre/work/username
    
The snag is that the output files from job scripts will not save to this file system -- could be quite inconvenient. This issue has been raised with IT, but for now you should create a directory in the `/home` file system (e.g. `/home/username/tmp/pbs/` where those files can be directed in the `#PBS -o` and `#PBS -e` lines of your job scripts.

# Updates

If you have any comments or suggestions for this goodie bag of tips and tricks, please send them to `connor.bottrell 'at' ipmu 'dot' jp` with a description or make a pull request directly to this repo.

