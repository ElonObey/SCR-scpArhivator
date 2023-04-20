import zipfile
import os
import datetime
from dotenv import load_dotenv, find_dotenv
import shutil
from paramiko import SSHClient
from scp import SCPClient


config = load_dotenv(find_dotenv())

PASS = os.environ.get("PASS")
DOMAIN = os.environ.get("DOMAIN")
USER = os.environ.get("USER")
PATH = os.environ.get("CLOUD_PATH")
PREFIX = os.environ.get("PREFIX")

dataTime = datetime.datetime.now()
nowDate = dataTime.date().strftime("%Y-%m-%d")
nowTime = dataTime.time().strftime("%H-%M-%S")

arhiveName = str(PREFIX) + "-" + str(nowDate) + "-" + str(nowTime)+".zip"

def scpDowloadFile(PASS, DOMAIN, USER, remotePath):
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.connect(hostname=f"{DOMAIN}",
                username=f"{USER}",
                password=f"{PASS}")
    scp = SCPClient(ssh.get_transport())
    scp.get(remotePath, recursive=True)

    scp.close()

def arhive(name, path):
    zip = zipfile.ZipFile(name, mode="w")

    for root, dirs, files in os.walk(path):
        for file in files:
            print(os.path.join(root, file))
            zip.write(os.path.join(root, file))

    zip.close()


scpDowloadFile(PASS, DOMAIN, USER, PATH)
path = PATH.split("/")[-1]
arhive(arhiveName, path)
shutil.rmtree(path)
