# Kavli IPMU HPC documentation 
Useful tips and tricks for high-performance computing using Kavli IPMU clusters (specifically idark, which uses the PBS Professional queue system).

## Python

<p>The code examples used in this tutorial use Python 3. Never fear, installation of Python 3 is not required as it is already installed on the idark cluster. To activate Python 3, login to idark and write the following from the command line:</p>

    source /home/anaconda3/bin/activate

or 

    conda activate base

then

    python

and you will see that the version that has been activated is Python 3.8.5. The gw and gfarm clusters use older versions of python which may not be compatible with some of the Python programs in this documentation. However, once you are famililar with the concepts, they can be easily applied with older versions of Python. 
  
