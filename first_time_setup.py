#!/usr/bin/env python3
import os
import time
import sys
import subprocess as sp

if os.geteuid() != 0:
    sys.exit("Please Make Sure You're a Superuser Before Running This Program")    
try:
    import tqdm
except:
    sp.check_output(['pip3','install','tdqm'])
    #if error add flag to install pip3 after
    if ret != 0:
        print("There's been an error installing a necessary package for this client to work, attempting to update apt-get in 10 seconds...")
        time.sleep(10)
        os.system("sudo apt-get update -y")
        os.system("sudo apt-get upgrade -y")
        if flag:
            os.system("sudo apt-get -y install python3-pip")

        sp.check_output(['pip3','install','tqdm'])
        #if error
            print("The error has occured again, please try something else, maybe switching python versions? Or attempt to manually install tqdm via pip")
            sys.exit()
        else:
            print("Everything has installed properly, happy file sharing!")

print("You've got everything you need, happy sharing!")
os.remove(sys.argv[0])
