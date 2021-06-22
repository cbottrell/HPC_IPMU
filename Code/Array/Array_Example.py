# Example Array Job Program 
import time
# To access $PBS_ARRAY_INDEX 
import sys

# subjob task 
def serial_task(idx):
    time.sleep(0.5)
    filename = f'../../Output/Array/Array.{idx}.txt'
    with open(filename,'w') as f:
    	for i in range(idx+1):
    		f.write(f'{i**2}\n')
    return 
    
def main():
    # Get subjob idx from python arg vars
    program_name, pbs_array_idx = sys.argv
    pbs_array_idx = int(pbs_array_idx)
    # Code performed for each subjob 
    start = time.time()
    serial_task(pbs_array_idx)
    runtime = time.time()-start
    print(f'Time: {runtime}s')

if __name__=='__main__':
    main()
