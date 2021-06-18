# Example Serial Job
import time

# Serial task
def serial_task(idx):
    time.sleep(0.5)
    filename = f'../../Output/Serial/Serial.{idx}.txt'
    with open(filename,'w') as f:
    	for i in range(idx+1):
    		f.write(f'{i**2}\n')
    return 
    
def main():
    # Main code 
    start = time.time()
    for i in range(16):
    	serial_task(i)
    runtime = time.time()-start
    print(f'Time: {runtime}s')
	
if __name__=='__main__':
    main()
