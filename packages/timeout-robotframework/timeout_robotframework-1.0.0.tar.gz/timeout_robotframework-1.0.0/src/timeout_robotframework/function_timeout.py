import multiprocessing as mp
import os
import getpass
import sys
import importlib

def timeout(func, timeout = 1):
    pool = mp.Pool(processes = 1)
    result = pool.apply_async(func)
    try:
        val = result.get(timeout = timeout)
    except mp.TimeoutError:
        print(str(timeout) + " Second timeout exceed")
        os.system('taskkill /F /IM excel.exe /FI "USERNAME eq '+getpass.getuser())
        pool.terminate()
        return True
    else:
        pool.close()
        pool.join()
        return False

if __name__ == '__main__':
    try :
        # Add the directory to the search path
        sys.path.append(os.getcwd())
        
        func = str(sys.argv[2]).split('.')
        mod =  importlib.import_module(func[0])
        met = getattr(mod, func[1])
        
        if len(sys.argv)>2 :
            print(timeout(met, timeout = int(sys.argv[1])))
        else :
            print(timeout(met, timeout = 10))
    except :
        print('Error in calling function please follow this order')
        print('python timeout.py [Timeout In Seconds] [File].[Method]')
        print('True')
    

    
        
    
    
