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
[username@idark ~]$ conda create -n project-env python=3.9
```

This command creates a new python environment called `project-env` which runs the latest stable version of Python 3.9. Once you have created the new environment, you can view it and all other existing environments (including `base`) with `conda env list`. You can activate any of these environments as follows:
```bash
[username@idark ~]$ conda activate project-env
``` 
replacing `project-env` with the name of your environment. 

The default installation will be fairly bare-bones, but you can now start installing packages. To install numpy, for example, you can do:
```bash
(project-env) [username@idark ~]$ conda install numpy
```

If a package you want is unavailable from the conda package manager, you can use `pip` within a conda environment instead. Type `which pip` and you will see that it is a specific pip installation for your python environment. Note, however, that this can sometimes lead to conflicts; see [here](https://www.anaconda.com/blog/using-pip-in-a-conda-environment) for details. 

`numpy` is one of many useful Python packages. Wouldn't it be nice if there is a stack of all the useful scientific packages so that you wouldn't have to install them all separately and think about dependencies? Oh yeah:
```bash
(project-env) [username@idark ~]$ pip install scipy-stack
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
[username@idark ~]$ 
CPPFLAGS=-I/usr/include/openssl11 \
LDFLAGS=-L/usr/lib64/openssl11 \
PYTHON_CONFIGURE_OPTS="--enable-shared" \
pyenv install -v 3.11.3 # or something different
```

The new version will now show up if you run `pyenv versions`, and you can set it as your global python version using 

```bash
[username@idark ~]$ pyenv global 3.11.3

[username@idark ~]$ python --version
# Python 3.11.3

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

The basic pattern for a PBS job on idark is

```bash
#!/bin/bash
#PBS -N demo
#PBS -o /home/username/PBS/
#PBS -e /home/username/PBS/
#PBS -l select=1:ncpus=1:mem=4gb
#PBS -l walltime=0:0:30
#PBS -u username
#PBS -M username@ipmu.jp
#PBS -m ae
#PBS -q tiny

# activate python environment
source ~/.bashrc 
conda activate project-env
# for pyenv/virtualenv instead use
# source /home/username/project/project-venv/bin/activate

python my_program.py
```

For a  job on gpgpu, make sure to first run `nvidia-smi` and identify GPUs which are not being used. Then a typical slurm file looks like

```
#!/bin/bash
#SBATCH --job-name=demo
#SBATCH --account=username
#SBATCH --output=/home/username/log/%j.out  
#SBATCH --error=/home/username/log/%j.err  
#SBATCH --time==0+00:01:00
#SBATCH --gres=gpu:1
#SBATCH --mem=32G
#SBATCH --cpus-per-gpu=6
#SBATCH --mail-user=username@ipmu.jp
#SBATCH --mail-type=END,FAIL

export CUDA_DEVICE_ORDER=PCI_BUS_ID
export CUDA_VISIBLE_DEVICES=X # where X is the GPU id of an available GPU

# activate python environment
conda activate project-env
# for pyenv/virtualenv instead use
# source /home/username/project/project-venv/bin/activate

python my_program.py
```

Please use only one GPU at a time, to prevent congestion.

## Accessing the compute nodes

On idark, you can directly access the compute node that is running your job. First identify the node by running

``` bash
[username@idark] $ qstat -nrt -u username
```
The node will have a name of the format `ansysNN` where `NN` in a 2-digit number between 01 and 40. 

Then use `rsh` to connect to it

```bash
[username@idark ~]$ rsh ansysNN
[username@ansysNN ~]$
```

## Using Jupyter and port forwarding

Using jupyter is a great way to make working remotely a little easier and more seamless.

You should always run jupyter in a job. Make a job script which runs the command 

```bash
jupyter lab --no-browser --ip=0.0.0.0 --port=X
```

where X is some port you choose, e.g 1337. Each port can only be used by one application at a time so make sure your jupyter session chooses a unique port number.

Now you just need to forward some port Y on your local computer to the remote port X. On gpgpu, this is as simple as running

```bash
$ ssh -NfL Y:localhost:X username@192.168.156.71 #for gpgpu
```
Now opening your browser to localhost:Y will give you direct access to jupyter on gpgpu. This same kind of port forwarding is used if you want to use MLFlow or tensorboard to track your ML experiments. 

On idark, you first need to find node your jupyter is running on by running `qstat -nrt -u username`.

Then on your local computer just run
```bash
$ ssh -NfL Y:ansysNN:X username@idark.ipmu.jp #for idark
```
where ansysNN is the node name. You'll now be able to access jupyter by pointing your browser to localhost:Y . The first time you connect to a jupyter session, it may prompt you for a connection token. You can get the token by connecting to the compute node using `rsh ansysNN` from the head node, and then running `jupyter server list`. You can use that token on the connection page to set a jupyter password which you can use to connect to future jupyter sessions on any node.


<!-- On gpgpu, to give GPUs to your jupyter instance you should put the jupyter lab command in a job script. -->

<!-- If you get an ssl error running jupyter lab, then either make sure you activate conda in your job script or if using pyenv find the missing libraries mentioned in the error message using `locate libssl.so.1.1`, copy library from the login node to a folder `/home/username/mylibs/`, and and then in your job script add the line `export LD_LIBRARY_PATH=/home/username/mylibs/:$LD_LIBRARY_PATH` .  -->

To register a python environment with jupyter, just activate the environment and then run
```bash
python -m ipykernel install --name project-venv --user
```
and you'll see a kernel with name project-venv next time you launch jupyter.

## Connecting your IDE 

Most IDEs you run on your local computer can be connected to the cluster to allow you to edit your files there seamlessly. For vscode, for example, follow the instructions [here](https://code.visualstudio.com/docs/remote/ssh).

# Where to work on idark

The `/home` file system has very limited space and may rapidly get congested if too many users are working and storing files there. As with previous clusters, iDark has a designated file system for work:

    /lustre/work/username
    
The snag is that the output files from job scripts will not save to this file system -- could be quite inconvenient. This issue has been raised with IT, but for now you should create a directory in the `/home` file system (e.g. `/home/username/tmp/pbs/` where those files can be directed in the `#PBS -o` and `#PBS -e` lines of your job scripts.

# Updates

If you have any comments or suggestions for this goodie bag of tips and tricks, please send them to `connor.bottrell 'at' ipmu 'dot' jp` with a description or make a pull request directly to this repo.

