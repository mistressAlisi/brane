import ipaddress
import re


def validate_network_block(input_string):
    pattern = r'^10\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})/24$'
    match = re.match(pattern, input_string)
    if match:
        # Check if each octet is within the valid range (0-255)
        octets = match.groups()
        if all(0 <= int(octet) <= 255 for octet in octets):
            return True
    return False

def extract_ips(cidr):
        """
        Given a /24 CIDR (e.g., '10.31.159.0/24'), returns:
        - first usable IP
        - second usable IP
        - last usable IP (excluding broadcast)
        """
        network = ipaddress.ip_network(cidr, strict=True)

        # Generate all usable hosts (excludes network and broadcast)
        hosts = list(network.hosts())

        if len(hosts) < 2:
            raise ValueError("CIDR block too small to provide required IPs.")

        return str(hosts[0]), str(hosts[1]), str(hosts[-1])