import os
import boto3
from datetime import datetime
import time
import pandas as pd
import numpy as np
from pathlib import Path


from decentralizedroutines.worker_lib import send_command
import decentralizedroutines.defaults as defaults 
from SharedData.Logger import Logger
logger = Logger(__file__)


shareddata_version='shareddata==2.0.31'
decentralizedroutines_version='decentralizedroutines==2.0.31'
source_folder = Path(os.environ['SOURCE_FOLDER'])
paths = [Path(source_folder/f) for f in os.listdir(source_folder) if Path.is_dir(source_folder/f)]
path = paths[1]
for path in paths:
    req_path = path/'requirements.txt'
    if (req_path).is_file():
        print(req_path)
        f = open(req_path)        
        s = f.read()
        f.close()
        
        if ('shareddata==' in s) | ('decentralizedroutines' in s):
            f = open(req_path, 'w')
            lines = np.array(s.split('\n'))
            lidx = np.array(['shareddata==' in line for line in lines])
            lines[lidx] = shareddata_version
            hasshareddata = lidx.any()            
            lidx = np.array(['decentralizedroutines==' in line for line in lines])
            hasdecentralizedroutines = lidx.any()
            if hasdecentralizedroutines:
                lines[lidx] = decentralizedroutines_version                

            _s = '\n'.join(lines)
            f.write(_s)
            f.flush()
            f.close()
    
            cmd = 'git -C '+str(path)+' commit -a -m "'+shareddata_version+'"'
            send_command(cmd.split(' '))
            cmd = 'git -C '+str(path)+' push'
            send_command(cmd.split(' '))
            

            if os.name != 'posix':
                cmd = str(path/'venv\Scripts\python.exe')+' -m pip install '
            else:
                cmd = str(path/'venv/bin/python')+' -m pip install '
            
            if hasdecentralizedroutines:
                send_command(str(cmd+decentralizedroutines_version).split(' '))
            elif hasshareddata:
                send_command(str(cmd+shareddata_version).split(' '))
            
            
            

        


    