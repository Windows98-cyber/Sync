import sys
import os
import shutil
import filecmp
import time
import tempfile



def ops(file):   
    #delete content from tempfile               
    file.truncate(0)
    file.flush()
    file.seek(0)
    
    
    

def filesync(dirA, dirB):
    dirT=tempfile.gettempdir()+'\\sync.tmp'              #creating tempfile
    try:
        tmp = open(dirT, 'x')
    except:
        pass
    tmp = open(dirT, 'r+')
    fail_sync = tmp.readlines()                            #syncing files if transfer was failed
    if len(fail_sync) != 0:
        shutil.copy2(fail_sync[0].replace('\n', ''), fail_sync[1])
        ops(tmp)
                   
        
    #1st case syncing missing files for both directories 
    missing = set(os.listdir(dirA)).symmetric_difference(set(os.listdir(dirB)))
    for file in missing:
        if os.path.exists( os.path.join(dirA, file)):
            tmp.writelines([ os.path.join(dirA, file)+'\n',  os.path.join(dirB, file)])
            tmp.flush()
            shutil.copy2( os.path.join(dirA, file),  os.path.join(dirB, file))
            ops(tmp)
        else:
            tmp.writelines([ os.path.join(dirB, file)+'\n',  os.path.join(dirA, file)])
            tmp.flush()
            shutil.copy2( os.path.join(dirB, file),  os.path.join(dirA, file))
            ops(tmp)
            
            
    files = os.listdir(dirA)
    while True:
        time.sleep(1)
        common = set(os.listdir(dirA))
        common = common.union(set(os.listdir(dirB))) 
        match, mismatch, error = filecmp.cmpfiles(dirA, dirB, common, shallow=False)
        
        #syncing files with different modification date
        for file in mismatch:
            Amtime = os.path.getmtime( os.path.join(dirA, file))                                                           
            Bmtime = os.path.getmtime( os.path.join(dirB, file))
            if Amtime > Bmtime:
                shutil.copy2( os.path.join(dirA, file),  os.path.join(dirB, file))
            else:
                shutil.copy2( os.path.join(dirB, file),  os.path.join(dirA, file))
         #recognizing deletion or creation/rename
        for file in error:
            if file in files:
                files.remove(file)
                try:
                    os.remove( os.path.join(dirA, file))
                except OSError:
                    os.remove( os.path.join(dirB,file))
            else:
                files.append(file)
                if file in os.listdir(dirA):
                    tmp.writelines([ os.path.join(dirA, file)+'\n',  os.path.join(dirB, file)])
                    tmp.flush()
                    r=tmp.read()
                    shutil.copy2( os.path.join(dirA, file),  os.path.join(dirB, file))
                    ops(tmp)
                else:
                    tmp.writelines([ os.path.join(dirB, file)+'\n',  os.path.join(dirA, file)])
                    tmp.flush()
                    r=tmp.read()
                    shutil.copy2( os.path.join(dirB, file),  os.path.join(dirA, file))
                    ops(tmp)
                    
filesync(sys.argv[1], sys.argv[2])
