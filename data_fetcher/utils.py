import subprocess
import time
import os
import pexpect
from dotenv import load_dotenv
import sys
import requests

def export_to_csv(df, file_name='data', cols_to_remove=None):
    """
    Method to export the data to a CSV file
    :param df: data to export
    :param file_name: name of the file to export
    :param cols_to_remove: columns to remove from the data before exporting
    :return: None
    """
    df = df.copy()
    if cols_to_remove and not isinstance(cols_to_remove, list):
        cols_to_remove = [cols_to_remove]
    current_dir = os.path.abspath(os.path.dirname(__file__))
    data_dir = os.path.join(current_dir, 'data')
    os.makedirs(data_dir, exist_ok=True) #create the directory if it doesn't exist
    file_path = os.path.join(data_dir, f'{file_name}.csv')
    if df.empty:
        print("Dataframe to export is empty")
        return None
    if cols_to_remove:
        df.drop(cols_to_remove, axis=1, level=1, inplace=True)
    df.to_csv(file_path, index=True)

# def check_ip():
#     # check the IP address after the connection is established
#     ip_command = "curl --silent https://api.ipify.org"
#     proc_ip = subprocess.Popen(ip_command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     output, error = proc_ip.communicate()
#     ip_address = output.decode("utf-8").strip()
#     print(f"IP address: {ip_address}")

# def vpn_connect():
#     from dotenv import load_dotenv
#     import os
#     # Load environment variables from the .env file
#     load_dotenv()
#     check_ip()
#     print("Connecting to VPN...")
#     password = os.environ.get('PROTONVPN_PASSWORD')
#     try:
#         # Disconnect from the current VPN connection, if any
#         disconnect_command = f"echo {password} | sudo -S protonvpn d"
#         print(disconnect_command)
#         process = subprocess.Popen(disconnect_command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#         print(process)
#         print(process.returncode)        
#         # if process.returncode != 0:
#         #     print(f"Error disconnecting from ProtonVPN")
#         #     return

#         # Connect to random ProtonVPN server
#         connect_command = f"echo {password} | sudo -S protonvpn c -r"
#         print(connect_command)
#         process = subprocess.Popen(connect_command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#         print(process)
#         print(process.returncode)
#         stdout, stderr = process.communicate()
#         if process.returncode != 0:
#             print(f"Error connecting to ProtonVPN: {stderr}")
#             return
#         print("Connected!")
#     except subprocess.CalledProcessError as e:
#         print("Error connecting to ProtonVPN:", e)

#     # check the IP address after the connection is established
#     check_ip()
    
def get_current_ip():
    connect_command = "protonvpn s"
    child = pexpect.spawn(connect_command)
    child.logfile_read = sys.stdout.buffer
    ip_pattern = r"IP:\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
    child.expect(ip_pattern)
    ip_address = child.match.group(1).decode("utf-8")
    return ip_address

def vpn_connect():    
    load_dotenv()
    sudo_password = os.environ.get('SUDO_PASSWORD')
    if not sudo_password:
        print("SUDO_PASSWORD environment variable not found.")
        return
    connected = False
    original_ip = get_current_ip()
    print("Original IP address:", original_ip) 
    while not connected:
        try:                         
            # Connect to a random ProtonVPN server
            connect_command = "sudo protonvpn c -r"
            child = pexpect.spawn(connect_command)
            child.logfile_read = sys.stdout.buffer  # Print terminal output
            child.expect("Password:")
            child.sendline(sudo_password)
            child.expect(pexpect.EOF)
            time.sleep(3)        
            new_ip = get_current_ip()
            print("\nIP address after Connect:", new_ip)
            if new_ip != original_ip:
                connected = True
                print("New IP address:", new_ip)
            
        except pexpect.exceptions.ExceptionPexpect as e:
            print("Error connecting to ProtonVPN:", e)
    