# Example Parellel OpenMP Job
import time
from multiprocessing import Pool

# Serial task 
def serial_task(idx):
    time.sleep(0.5)
    filename = f'../../Output/OpenMP/OpenMP.{idx}.txt'
    with open(filename,'w') as f:
        for i in range(idx+1):
            f.write(f'{i**2}\n')
    return

def main():
    # Main code 
    start = time.time()
    args = range(16)
    nthreads = 8
    with Pool(nthreads) as pool:
        pool.map(serial_task,args)
    runtime = time.time()-start
    print(f'Time: {runtime}s')
	
if __name__=='__main__':
    main()