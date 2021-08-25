#!/usr/bin/env python3

import PrinterFileServer as PFS
import sys
import os

'''
-l File Location
-p Server Port
'''

ADDR = '0.0.0.0'

args = {}
for x in range(1, len(sys.argv), 2):
    args[sys.argv[x][1]] = sys.argv[x + 1]

if 'l' in args.keys():
    server = PFS.PrinterFileServer(ADDR, args['p'], args['l'])
else:
    server = PFS.PrinterFileServer(ADDR, args['p'])
while True:
    try:
        server.run_server()
    except Exception as e:
        print(e)

