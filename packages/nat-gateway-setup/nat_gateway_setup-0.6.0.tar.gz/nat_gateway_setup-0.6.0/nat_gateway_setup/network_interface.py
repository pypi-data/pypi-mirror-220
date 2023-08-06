import os
import shutil
import subprocess
import uuid
from time import sleep
from .utils import CustomException

def backup_existing_configuration(interface_name, connection_folder='/etc/NetworkManager/system-connections'):
    """
    Back up the existing configuration of the network interface if it exists.

    :raise: CustomException if the backup fails
    """
    try:
        connection_file = os.path.join(connection_folder, interface_name)
        if os.path.exists(connection_file):
            backup_file = connection_file + '.bak'
            shutil.copyfile(connection_file, backup_file)
            os.remove(connection_file)
    except Exception as e:
        raise CustomException(f"Backup of existing configuration failed with error: {str(e)}") from None


def create_nm_connection(interface_name, ip, netmask, connection_folder='/etc/NetworkManager/system-connections'):
    """
    Create a new NetworkManager connection file for the interface.

    :raise: CustomException if the file creation fails
    """
    try:
        interface_file_name = interface_name + ".nmconnection"
        connection_file = os.path.join(connection_folder, interface_file_name)
        with open(connection_file, 'w') as f:
            f.write(f"""[connection]
id={interface_name}
uuid={str(uuid.uuid4())}
type=ethernet
interface-name={interface_name}

[ipv4]
method=manual
addresses={ip}/{netmask}

[ipv6]
method=disabled
""")
        # After writing the file, change the file permissions to 0600
        os.chmod(connection_file, 0o600)

    except Exception as e:
        raise CustomException(f"Creation of NetworkManager connection file failed with error: {str(e)}") from None

def enable_network_manager():
    """
    Reload NetworkManager to apply the new configuration.

    :raise: CustomException if the reload fails
    """
    try:
        subprocess.check_call(['systemctl', 'enable', 'NetworkManager'])
    except subprocess.CalledProcessError as e:
        raise CustomException(f"Reloading NetworkManager failed with error: {str(e)}") from None


def restart_network_manager():
    """
    Reload NetworkManager to apply the new configuration.

    :raise: CustomException if the reload fails
    """
    try:
        subprocess.check_call(['systemctl', 'restart', 'NetworkManager'])
    except subprocess.CalledProcessError as e:
        raise CustomException(f"Reloading NetworkManager failed with error: {str(e)}") from None


def configure_interface(interface_name, ip, netmask, connection_folder='/etc/NetworkManager/system-connections'):
    """
    Configure the network interface for NAT.

    :raise: CustomException if the network interface configuration fails
    """
    try:
        backup_existing_configuration(interface_name, connection_folder)
        create_nm_connection(interface_name, ip, netmask, connection_folder)
        enable_network_manager()
        restart_network_manager()
        print("Restarting network services")
        sleep(2)

    except subprocess.CalledProcessError as e:
        raise CustomException(f"Network interface configuration failed with error: {str(e)}") from None
