## Overview

This Python script is designed for conducting WiFi deauthentication attacks on wireless networks. The script automates the process of putting your WiFi interface into monitor mode, scanning for networks, and performing a deauthentication attack on selected networks. It uses tools like `airmon-ng` and `aireplay-ng` to perform the attack.

### Features:
- **Auto-monitor mode setup**: Automatically switches the selected WiFi interface to monitor mode.
- **Network scanning**: Scans for nearby access points (APs) and displays available networks.
- **Deauthentication Attack**: Performs a deauthentication attack to disconnect clients from a selected access point.
- **Backup of CSV files**: Automatically backs up any existing `.csv` files generated during network scanning before each attack.
- **Customizable attack parameters**: Includes options for attack packet count, interval between packets, and task priority.
- **Two operation modes**: Standard mode (simplified) and Expert mode (customizable).

### Usage

The script must be run as **sudo** to interact with the WiFi interfaces and to change the mode of the network adapter.

### Prerequisites

Before running the script, ensure that:
- You are using a **Linux** system with tools like `airmon-ng` and `aireplay-ng` installed.
- You have a compatible **WiFi adapter** that supports monitor mode.
- The script relies on Python 3 and some standard libraries (`subprocess`, `re`, `csv`, `os`, `shutil`, `time`, `datetime`).

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/h3xvo1dnull/WI-DOS.git
   cd wifi-deauth-script
   ```

2. Install the necessary dependencies:

   ```bash
   sudo apt update
   sudo apt install aircrack-ng
   ```

### How It Works

1. **Monitor Mode Setup**: The script detects the available WiFi interfaces and enables monitor mode using `airmon-ng`. If there are any conflicting processes, it will terminate them automatically.
   
2. **Network Scanning**: The script runs `airodump-ng` in the background to scan for available networks. Detected networks are saved in CSV files.
   
3. **Display Networks**: Once scanning is completed, the script will list nearby networks with details like **BSSID**, **ESSID**, and **channel**.

4. **Deauthentication Attack**: The user selects a network to attack. The script sends deauthentication packets using `aireplay-ng`, effectively disconnecting clients from the target access point.

5. **Backup CSV Files**: Before starting the scan, the script backs up any existing `.csv` files to prevent overwriting previous data.

### Running the Script

Run the script using **sudo**:

```bash
sudo python3 WI-DOS.py
```

### Interaction Flow

1. **Interface Selection**: The script will first check for available WiFi interfaces. If none are found, it will prompt you to connect a compatible adapter.

2. **Monitor Mode Setup**: It will automatically put the selected interface into monitor mode.

3. **Mode Selection**:
   - **Standard Mode (S)**: Default mode with predefined settings.
   - **Expert Mode (E)**: Allows customization of various parameters like the channel, packet count, attack interval, and priority.

4. **Network Scanning**: The script continuously scans for available networks and displays them. You can stop scanning by pressing `Ctrl+C`.

5. **Attack Configuration**: In Expert mode, you can customize:
   - **Channel**: Choose a specific channel to scan (or leave empty to scan all channels).
   - **Packet Count**: Number of deauthentication packets to send (1-100).
   - **Interval**: Time interval (in seconds) between each deauthentication packet (1-60).
   - **Priority**: Task priority for the attack process (-20 to 19).

6. **Deauthentication**: After selecting the target network, the script sends deauthentication packets, disconnecting clients from the selected AP.

### Example Workflow

```bash
$ sudo python3 WI-DOS.py
  _         _    _  _  _ _ _  _  _       _  _  
|   |     |   |  \     _  _/  \   \     /   /   
|   | _ _ |   |   \   \        \     V     /     
|     _ _     |     >   >       >    x    <       
|   |     |   |   /   / _ _    /     Λ     \       
| _ |     | _ |  /_  _  _ _\  /_  _/   \_  _\       
****************************************************************
*   This script was developed by Hex and remains the            *
*   property of Tenebris.                                        *
****************************************************************

Available WiFi interfaces:
0 - wlan0
1 - wlan1

Please select the interface you want to use for the deauthentication attack: 0
WiFi adapter connected.
Killing conflicting processes...
WiFi interface in monitor mode.

Select mode (S/standard or E/expert): E
Enter the channel to scan (leave empty to scan all channels): 6
Enter the number of deauthentication packets to send (1-100): 50
Enter the interval between deauthentication packets in seconds (1-60): 2
Enter the task manager priority (-20 to 19): 10

Scanning... Ctrl+C to select a network.
No |    BSSID              |  Channel | ESSID        
---|-----------------------|----------|---------------
0  | AA:BB:CC:DD:EE:FF     |  6       | MyWiFiNetwork
1  | 00:11:22:33:44:55     |  11      | AnotherNetwork

Please select a SSID from above: 0

Deauthenticating clients on selected network, Ctrl+C to terminate.
```

### Legal Disclaimer
This script is intended **only for ethical use** in penetration testing and network security auditing. **Do not use it** to attack networks without explicit permission from the network owner. Unauthorized use may be illegal.

### License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
