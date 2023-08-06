import argparse
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.validation import Validator, ValidationError
import ipaddress
from .utils import check_firewall_condition, get_dns_server, enable_ip_forwarding, get_ip_range, get_linux_distribution, get_required_dependencies, check_dependencies, install_missing_dependencies
from .firewall import configure_firewall
from .dnsmasq import configure_dnsmasq, check_dnsmasq_configs, restart_dnsmasq
from .network_interface import configure_interface

class IPValidator(Validator):
    def validate(self, document):
        try:
            ipaddress.IPv4Address(document.text)
        except ValueError:
            raise ValidationError(message="Please enter a valid IP address", cursor_position=len(document.text))

class IntValidator(Validator):
    def validate(self, document):
        if not document.text.isdigit():
            raise ValidationError(message="Please enter a valid integer", cursor_position=len(document.text))

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', help='the IP address')
    parser.add_argument('--netmask', help='the netmask')
    parser.add_argument('--dhcp-start-ip', help='the start IP of the DHCP range')
    parser.add_argument('--dhcp-ip-count', type=int, help='the number of IPs in the DHCP range')
    parser.add_argument('--wlan', help='the incoming network interface (WLAN)')
    parser.add_argument('--lan', help='the local network interface (LAN)')
    args = parser.parse_args()

    # Check and install dependencies
    linux_distribution = get_linux_distribution()
    required_dependencies = get_required_dependencies(linux_distribution)
    missing_dependencies = check_dependencies(required_dependencies)
    install_missing_dependencies(missing_dependencies)
    # Need to make sure firewalld is running and iptables is not running on 
    # rhel systems. 
    check_firewall_condition()
    # Enabling ipforwarding which is required for nat networks. 
    enable_ip_forwarding()

    # If arguments are not provided via command line, ask for user input
    ip = args.ip if args.ip else prompt("Please enter the IP address: ", validator=IPValidator())
    netmask = args.netmask if args.netmask else prompt("Please enter the netmask: ")  # add validation if desired
    dhcp_start_ip = args.dhcp_start_ip if args.dhcp_start_ip else prompt("Please enter the start IP of the DHCP range: ", validator=IPValidator())
    dhcp_ip_count = args.dhcp_ip_count if args.dhcp_ip_count else prompt("Please enter the number of IPs in the DHCP range: ", validator=IntValidator())
    wlan_interface = args.wlan if args.wlan else prompt("Please enter the incoming network interface (WLAN): ")
    lan_interface = args.lan if args.lan else prompt("Please enter the local network interface (LAN): ")

    # Setup network interface
    configure_interface(lan_interface, ip, netmask)

    # Setup dnsmasq
    check_dnsmasq_configs(lan_interface)
    ip_range = get_ip_range(dhcp_start_ip,dhcp_ip_count)
    dns_server_ip = get_dns_server()
    configure_dnsmasq(lan_interface,ip_range,dns_server_ip)
    restart_dnsmasq()

    # Setup firewall
    configure_firewall(wlan_interface, lan_interface)

if __name__ == "__main__":
    main()
