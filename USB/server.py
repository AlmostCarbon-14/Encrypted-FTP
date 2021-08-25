#!/usr/bin/env python3

import PrinterFileServer as PFS
import sys
import os

'''
-l File Location
-p Server Port
'''

args = {}
for x in range(1, len(sys.argv), 2):
    args[sys.argv[x][1]] = sys.argv[x + 1]

server = PFS.PrinterFileServer('0.0.0.0', args['p'], args['l'])

server.run_server()


