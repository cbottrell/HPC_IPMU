# Example Array Job Program 
import os,time

def serial_task(idx):
    # Simulated task taking 5s
    time.sleep(5)
    base = os.getenv('HPC_DIR')
    outdir = f'{base}/Output/Array'
    filename = f'{outdir}/Array.{idx}.txt'
    with open(filename,'w') as f:
    	for i in range(idx+1):
    		f.write(f'{i**2}\n')
    return 
    
def main():
    # Get subjob idx from env vars
    idx = os.getenv('PBS_ARRAY_INDEX')
    idx = int(idx)
    # Code performed for each subjob 
    start = time.time()
    serial_task(idx)
    runtime = time.time()-start
    print(f'Time: {runtime}s')

if __name__=='__main__':
    main()
