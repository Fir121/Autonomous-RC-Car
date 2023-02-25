import os
import paramiko 
import time
ssh = paramiko.SSHClient()
from detection import *

ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('172.20.10.5', username="firas", password="firas")
sftp = ssh.open_sftp()
print("connected")

remotepath = '/home/firas/Desktop/Autonomous-RC-Car/Raspberry Pi'
i = 0
t = time.time()
os.makedirs(f"outputimages/{t}")

while True:
    s = time.time()
    while True:
        try:
            sftp.stat(remotepath+"/test.jpg")
            break
        except Exception as e:
            time.sleep(0.00001)
    localpath = f'outputimages/{t}/{i}-Base.jpg'
    i += 1
    sftp.get(remotepath+"/test.jpg", localpath)
    op = process(localpath)
    with open("op.txt", "w") as f:
        f.write(str(op))
    sftp.remove(remotepath+"/test.jpg")
    sftp.put("op.txt", remotepath+"/op.txt", confirm=False)
    print(time.time()-s)