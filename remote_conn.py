import paramiko
import time
from paramiko.ssh_exception import *


class SSH(object):
    def __init__(self, ip_address, username, password, timeout=60, retries=2, interval=5):
        self.ip_address = ip_address
        self.username = username
        self.password = password
        self.timeout = timeout
        self.retries = retries
        self.interval = interval

    def connect_to_remote(self):
        ssh = None
        print "Connecting ......."
        for x in range(self.retries):
            print "Retry No. : ", str(x+1)
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(self.ip_address, username=self.username, password=self.password, timeout=self.timeout)
                break
            except (BadHostKeyException, AuthenticationException, SSHException, socket.error) as e:
                print e
                time.sleep(self.interval)
        return ssh

    def run_remote_cmd(self, commandList):
        output = err = None
        ssh = self.connect_to_remote()
        if ssh:
            try:
                stdin, stdout, stderr = ssh.exec_command(commandList, timeout=self.timeout)
                output = stdout.read()
                err = stderr.read()
            except Exception, e:
                print "Error in run remote command for command = " + str(commandList) + "\nError = ", e
            return output, err
        else:
            print "Connection failure for command = ", commandList
            return None, None


	
sobj = SSH('192.168.102.199','msys','master#123')
out, err = sobj.run_remote_cmd('ls /tmp/')
if err:
    print err
elif out:
    print out.split()
else:
    pass
