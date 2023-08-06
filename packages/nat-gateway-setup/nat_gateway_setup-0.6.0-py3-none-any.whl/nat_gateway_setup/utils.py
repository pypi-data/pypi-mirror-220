import os
import subprocess
import distro
import ipaddress
import re

def check_firewall_condition():
    """
    Check and set the correct firewall conditions for redhat systems.

    :raise: CustomException if the configuration fails
    """
    try:
        # First check if we are on a redhat system
        if get_linux_distribution() in ['centos', 'redhat']:
            # Disable iptables
            try:
                subprocess.check_call(['systemctl', 'stop', 'iptables'])
            except subprocess.CalledProcessError:
                pass # This is ok to get an error here... we just want to make sure
            try:
                subprocess.check_call(['systemctl', 'disable', 'iptables'])
            except subprocess.CalledProcessError:
                pass # same here. 

            # Unmask firewalld
            subprocess.check_call(['systemctl', 'unmask', 'firewalld'])

            # Enable and start firewalld
            subprocess.check_call(['systemctl', 'enable', 'firewalld'])
            subprocess.check_call(['systemctl', 'start', 'firewalld'])
        else:
            print("check_firewall_condition is only applicable to redhat-based distributions.")
    except subprocess.CalledProcessError as e:
        raise CustomException(f"Firewall condition check and setup failed with error: {str(e)}") from None

def get_dns_server():
    """
    Get the DNS server 
    
    :return: The DNS server IP address
    """
    with open('/etc/resolv.conf', 'r') as f:
        contents = f.read()
    match = re.search(r'nameserver (\b(?:\d{1,3}\.){3}\d{1,3}\b)', contents)
    if match:
        return match.group(1)
    else:
        return None

def enable_ip_forwarding():
    """
    Enable IP forwarding.
    
    :raise: CustomException if the configuration fails
    """
    try:
        if get_linux_distribution() in ['centos', 'redhat']:
            with open('/etc/sysctl.d/99-ipforward.conf', 'w') as f:
                f.write('net.ipv4.ip_forward = 1\n')
            subprocess.check_call(['sysctl', '-p', '/etc/sysctl.d/99-ipforward.conf'])
        elif get_linux_distribution() in ['ubuntu', 'debian']:
            with open('/etc/sysctl.conf', 'a') as f:
                f.write('\nnet.ipv4.ip_forward=1\n')
            subprocess.check_call(['sysctl', '-p'])
        else:
            raise CustomException("Unsupported Linux distribution for IP forwarding configuration.")
    except subprocess.CalledProcessError as e:
        raise CustomException(f"IP forwarding configuration failed with error: {str(e)}") from None

def get_ip_range(start_ip: str, count: int):
    start_ip_int = int(ipaddress.IPv4Address(start_ip))
    end_ip_int = start_ip_int + count - 1
    end_ip = ipaddress.IPv4Address(end_ip_int)
    return f"{start_ip},{end_ip}"

def get_linux_distribution():
    """
    Detect the Linux distribution.

    :return: String identifier for the detected Linux distribution
    """
    try:
        return distro.id()
    except:
        return "unknown"


class CustomException(Exception):
    pass

DEPENDENCIES = {
    'ubuntu': {'firewall': 'ufw', 'dnsmasq': 'dnsmasq', 'network_manager': 'network-manager', 'systemd': 'systemd'},
    'redhat': {'firewall': 'firewalld', 'dnsmasq': 'dnsmasq', 'network_manager': 'NetworkManager', 'systemd': 'systemd'}
}

def get_required_dependencies(linux_distribution):
    return DEPENDENCIES.get(linux_distribution, {})

def check_dependencies(dependencies):
    return [dep for dep in dependencies if not is_installed(dep)]

def install_missing_dependencies(missing_dependencies):
    for dep in missing_dependencies:
        install_dependency(dep)

def is_installed(dependency):
    try:
        subprocess.check_call(['which', dependency])
        return True
    except subprocess.CalledProcessError:
        return False

def install_dependency(dependency):
    try:
        if os.path.isfile('/usr/bin/yum'):
            subprocess.check_call(['yum', 'install', '-y', dependency])
        elif os.path.isfile('/usr/bin/apt-get'):
            subprocess.check_call(['apt-get', 'install', '-y', dependency])
        else:
            raise CustomException("Unsupported package manager. Cannot install dependencies.")
    except subprocess.CalledProcessError as e:
        raise CustomException(f"Dependency installation failed with error: {str(e)}") from None
