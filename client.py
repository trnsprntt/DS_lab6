import socket
import os
import tqdm
import sys
[program, filename, TCP_IP, TCP_PORT] = sys.argv

BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, int(TCP_PORT)))
filesize = os.path.getsize(filename)
s.send(f"{filename} {filesize}".encode())

# start sending the file
progress = tqdm.tqdm(range(int(filesize)), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "rb") as f:
    for _ in progress:
        # read the bytes from the file
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            # file transmitting is done
            break
        # we use sendall to assure transimission in 
        # busy networks
        s.sendall(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))


print('Successfully transfered the file')
s.close()
print('connection closed')
