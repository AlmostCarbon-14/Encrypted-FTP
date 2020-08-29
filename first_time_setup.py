#!/usr/bin/env python3

import os
import time
import sys

try:
    os.rename('/etc/foo', '/etc/bar')
except IOError as e:
    if (e[0] == errno.EPERM):
        sys.exit("Please Make Sure You're a Superuser Before Running This Program")

try:
    import tqdm
except:
    ret = os.system("pip3 install tdqm")
    if ret != 0:
        print("There's been an error installing a necessary package for this client to work, attempting to update apt-get in 10 seconds...")
        time.sleep(10)
        os.system("sudo apt-get update")
        os.system("sudo apt-get upgrade")
        ret = os.system("sudo apt-get install tqdm")
        if ret != 0:
            print("The error has occured again, please try something else, maybe switching python versions? Or attempt to manually install tqdm via pip")
            sys.exit()
    else:
        print("Everything has installed properly, happy file sharing!")
