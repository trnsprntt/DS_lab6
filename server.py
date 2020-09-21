import socket
import tqdm
import os
from threading import Thread
from socketserver import ThreadingMixIn

TCP_IP = socket.gethostbyaddr("18.189.170.225")[0]
TCP_PORT = 60001
buffer = 1024

print (TCP_IP,":",TCP_PORT)

class ClientThread(Thread):

    def __init__(self,ip,port,sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock

    def run(self):
        conn, addr = tcpsock.accept()
        received = conn.recv(buffer).decode()
        filename, filesize = received.split(" ")
        # if such a file already exists, it would be removed by this command
        filename = os.path.basename(filename)
        progress = tqdm.tqdm(range(int(filesize)), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "wb") as f:
            for _ in progress:
                # read 1024 bytes from the socket (receive)
                bytes_read = tcpsock.recv(buffer)
                if not bytes_read:    
                    # nothing is received
                    # file transmitting is done
                    break
                # write to the file the bytes we just received
                f.write(bytes_read)
                # update the progress bar
                progress.update(len(bytes_read))


tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    tcpsock.listen(5)
    print ("Waiting for incoming connections...")
    (conn, (ip,port)) = tcpsock.accept()
    print ('Got connection from ', (ip,port))
    newthread = ClientThread(ip,port,conn)
    newthread.start()
    threads.append(newthread)

for t in threads:
    t.join()
