# Example Serial Job
import os,time

# Serial task
def serial_task(idx):
    # Simulated task taking 5s
    time.sleep(5)
    base = os.getenv('HPC_DIR')
    outdir = f'{base}/Output/Serial'
    filename = f'{outdir}/Serial.{idx}.txt'
    with open(filename,'w') as f:
    	for i in range(idx+1):
    		f.write(f'{i**2}\n')
    return 
    
def main():
    # Main code
    start = time.time()
    for idx in range(128):
    	serial_task(idx)
    runtime = time.time()-start
    print(f'Time: {runtime}s')
	
if __name__=='__main__':
    main()
