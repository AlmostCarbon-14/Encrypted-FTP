#!/usr/bin/env python3

import PrinterFileServer as PFS
import sys
import os

'''
-a Server Address
-p Server Port
-f Filename / Foldername
-r IsFolder
'''

args = {}
for x in range(1, len(sys.argv), 2):
    args[sys.argv[x][1]] = sys.argv[x + 1]

client = PFS.PrinterFileServer(args['a'], args['p'])



if args['r'].upper() == 'T' or args['r'].upper() == 'TRUE':
    if os.path.isdir(args['f']):
        files = os.listdir(args['f'])
        for f in files:
            if not os.path.isdir(f):
                print(f)
                client_run_client(f)
    

else:
    if os.path.isfile(args['f']):
        client.run_client(args['f'].strip())

    else:
        print("file not found")



