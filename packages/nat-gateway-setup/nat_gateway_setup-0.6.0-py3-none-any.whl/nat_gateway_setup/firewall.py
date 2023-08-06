import os
import subprocess
from datetime import datetime
from .utils import CustomException, get_linux_distribution
import glob
import shutil

def configure_firewall(wlan_interface, lan_interface):
    """
    Configure the firewall to forward traffic from the wlan interface to the eth interface.

    :raise: CustomException if the firewall configuration fails
    """
    backup_folder = "/var/cache/nat-linux-gateway"
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)
    
    backup_time = datetime.now().strftime('%Y%m%d%H%M%S')
    
    try:
        if get_linux_distribution() in ['centos', 'redhat']:
            # Backup firewall rules
            with open(os.path.join(backup_folder, f'firewall_rules.bak.{backup_time}'), 'w') as f:
                subprocess.check_call(['firewall-cmd', '--list-all-zones'], stdout=f)
            
            subprocess.check_call(['firewall-cmd', '--zone=public', '--add-masquerade', '--permanent'])
            subprocess.check_call(['firewall-cmd', '--zone=public', '--add-interface', wlan_interface, '--permanent'])
            subprocess.check_call(['firewall-cmd', '--zone=internal', '--add-interface', lan_interface, '--permanent'])
            subprocess.check_call(['firewall-cmd', '--zone=internal', '--add-port=53/udp', '--permanent']) # DNS
            subprocess.check_call(['firewall-cmd', '--zone=internal', '--add-port=53/tcp', '--permanent']) # DNS
            subprocess.check_call(['firewall-cmd', '--zone=internal', '--add-port=67/udp', '--permanent']) # DHCP
            subprocess.check_call(['firewall-cmd', '--zone=internal', '--add-port=68/udp', '--permanent']) # DHCP
            # Add additional ports as necessary
            subprocess.check_call(['firewall-cmd', '--reload'])
        elif get_linux_distribution() in ['ubuntu', 'debian']:
            # Backup sysctl.conf and before.rules
            for conf_file in ['/etc/ufw/sysctl.conf', '/etc/ufw/before.rules']:
                if os.path.exists(conf_file):
                    shutil.copyfile(conf_file, os.path.join(backup_folder, os.path.basename(conf_file) + f'.bak.{backup_time}'))

            with open('/etc/ufw/sysctl.conf', 'a') as f:
                f.write("\n# Enable IP forwarding\nnet/ipv4/ip_forward=1\nnet/ipv6/conf/default/forwarding=1\nnet/ipv6/conf/all/forwarding=1\n")
            with open('/etc/ufw/before.rules', 'a') as f:
                f.write("\n# Enable forwarding from " + lan_interface + " to " + wlan_interface + "\n*nat\n:POSTROUTING ACCEPT [0:0]\n-A POSTROUTING -s 192.168.1.0/24 -o " + wlan_interface + " -j MASQUERADE\nCOMMIT\n")
            subprocess.check_call(['ufw', 'allow', '53/udp'])  # DNS
            subprocess.check_call(['ufw', 'allow', '53/tcp'])  # DNS
            subprocess.check_call(['ufw', 'allow', '67/udp'])  # DHCP
            subprocess.check_call(['ufw', 'allow', '68/udp'])  # DHCP
            # Add additional ports as necessary
            subprocess.check_call(['ufw', 'enable'])
        else:
            raise CustomException("Unsupported Linux distribution for firewall configuration.")
    except subprocess.CalledProcessError as e:
        raise CustomException(f"Firewall configuration failed with error: {str(e)}") from None


def restore_firewall_configuration(backup_time=None):
    """
    Restore the firewall configuration to a previous state.

    :param backup_time: The timestamp of the backup to restore. If None, restore the most recent backup.
    :raise: CustomException if the restore fails
    """
    backup_folder = "/var/cache/nat-linux-gateway"

    try:
        if get_linux_distribution() in ['centos', 'redhat']:
            if backup_time is None:
                # Find the most recent backup
                list_of_files = glob.glob(os.path.join(backup_folder, 'firewall_rules.bak.*'))
                backup_file = max(list_of_files, key=os.path.getctime)
            else:
                backup_file = os.path.join(backup_folder, f'firewall_rules.bak.{backup_time}')

            # TODO: Restore firewall-cmd configuration from backup file
            # Unfortunately, firewall-cmd does not support a straightforward way to import settings.
            # It may be necessary to write a parser for the backup file and call firewall-cmd commands accordingly.
            # Please consider using other methods to backup and restore firewall-cmd configurations.
        elif get_linux_distribution() in ['ubuntu', 'debian']:
            for conf_file in ['sysctl.conf', 'before.rules']:
                if backup_time is None:
                    # Find the most recent backup
                    list_of_files = glob.glob(os.path.join(backup_folder, conf_file + '.bak.*'))
                    backup_file = max(list_of_files, key=os.path.getctime)
                else:
                    backup_file = os.path.join(backup_folder, conf_file + f'.bak.{backup_time}')

                # Restore from backup
                shutil.copyfile(backup_file, '/etc/ufw/' + conf_file)
        else:
            raise CustomException("Unsupported Linux distribution for firewall configuration restore.")
    except Exception as e:
        raise CustomException(f"Firewall configuration restore failed with error: {str(e)}") from None
