#!/usr/bin/env python3
import os
import time
import sys
import subprocess as sp

flag = False
if os.geteuid() != 0:
    sys.exit("Please Make Sure You're a Superuser Before Running This Program")    
try:
    import tqdm
except:
    if b'error' in sp.check_output(['pip3','install','tdqm']):
        flag = True
    else:
        print("There's been an error installing a necessary package for this client to work, attempting to update apt-get in 10 seconds...")
        time.sleep(10)
        os.system("sudo apt-get update -y")
        print("="*10 + "Update Complete, Now Upgrading apt-get" + "="*10)
        time.sleep(5)
        os.system("sudo apt-get upgrade -y")
        if flag:
            os.system("sudo apt-get -y install python3-pip")

        if b'error' in sp.check_output(['pip3','install','tqdm']):
            print("The error has occured again, please try something else, maybe switching python versions? Or attempt to manually install tqdm via pip")
            sys.exit()
        else:
            print("Everything has installed properly, happy file sharing!")
else:
    print("You've got everything you need, happy sharing!")
    os.remove(sys.argv[0])
