import time
import os
import pexpect
from dotenv import load_dotenv
from termcolor import colored

class Utils:
    def __init__(self):
        self.id_ = 1
            
    def export_to_csv(self, df, file_name='data', cols_to_remove=None):
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
        
    def get_current_ip(self):
        connect_command = "protonvpn s"
        child = pexpect.spawn(connect_command)
        # child.logfile_read = sys.stdout.buffer # Print terminal output
        ip_pattern = r"IP:\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
        child.expect(ip_pattern)
        ip_address = child.match.group(1).decode("utf-8")
        return ip_address

    def vpn_connect(self):    
        load_dotenv()
        sudo_password = os.environ.get('SUDO_PASSWORD')
        if not sudo_password:
            print("SUDO_PASSWORD environment variable not found.")
            return
        connected = False
        original_ip = self.get_current_ip()
        print(f"Original IP address: {colored(original_ip, 'yellow')}")
        while not connected:
            try:                         
                # Connect to a random ProtonVPN server
                connect_command = "sudo protonvpn c -r"
                child = pexpect.spawn(connect_command)
                # child.logfile_read = sys.stdout.buffer  # Print terminal output
                child.expect("Password:")
                child.sendline(sudo_password)
                child.expect(pexpect.EOF)
                time.sleep(3)        
                new_ip = self.get_current_ip()
                print(f"\nNew IP address: {colored(new_ip, 'yellow')}")
                if new_ip != original_ip:
                    connected = True
                    print(colored("IP changed successfully", 'yellow'))
                
            except pexpect.exceptions.ExceptionPexpect as e:
                print(f"{colored('Error connecting to ProtonVPN', 'red')}: {e}")
        