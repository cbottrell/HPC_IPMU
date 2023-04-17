# Example Parellel OpenMP Job
import os,time
from multiprocessing import Pool

# Serial task 
def serial_task(idx):
    # Simulated task taking 5s
    time.sleep(5)
    base = os.getenv('HPC_DIR')
    outdir = f'{base}/Output/OpenMP'
    filename = f'{outdir}/OpenMP.{idx}.txt'
    with open(filename,'w') as f:
        for i in range(idx+1):
            f.write(f'{i**2}\n')
    return

def main():
    # Main code 
    start = time.time()
    args = range(128)
    nthreads = os.getenv('OMP_NUM_THREADS')
    nthreads = int(nthreads)
    with Pool(nthreads) as pool:
        pool.map(serial_task,args)
    runtime = time.time()-start
    print(f'Time: {runtime}s')
	
if __name__=='__main__':
    main()
