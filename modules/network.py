import os
import time
import socket
import subprocess
import random
import threading
import ipaddress
import struct
import nmap
import requests
import dns.resolver
import scapy.all as scapy
from scapy.layers import http
from datetime import datetime

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def network_menu():
    while True:
        clear_screen()
        print("\n  === NETWORK RECONNAISSANCE ===")
        print("  [1] Port Scanner")
        print("  [2] Network Sniffer")
        print("  [3] Router Analysis")
        print("  [4] DNS Enumeration")
        print("  [5] Vulnerability Scanner")
        print("  [0] Back to Main Menu")

        choice = input("\n  Select an option: ")

        if choice == "1":
            port_scanner()
        elif choice == "2":
            network_sniffer()
        elif choice == "3":
            router_analysis()
        elif choice == "4":
            dns_enumeration()
        elif choice == "5":
            vulnerability_scanner()
        elif choice == "0":
            return
        else:
            print("  Invalid option. Please try again...")
            time.sleep(1)

def port_scanner():
    clear_screen()
    print("\n  === PORT SCANNER ===")
    target = input("  Enter target IP address or hostname: ")
    
    if not target:
        print("  Invalid target. Returning to menu...")
        time.sleep(2)
        return
    
    port_range = input("  Enter port range (e.g. 1-1000): ")
    try:
        start_port, end_port = map(int, port_range.split('-'))
    except:
        start_port, end_port = 1, 1000
        print(f"  Using default port range: {start_port}-{end_port}")
    
    scan_type = input("  Scan type (1=Basic, 2=Service Detection): ")
    
    print(f"\n  Scanning {target} on ports {start_port}-{end_port}")
    print("  " + "="*50)
    print("  This may take some time...\n")
    
    try:
        scanner = nmap.PortScanner()
        
        if scan_type == "2":
            args = f"-sV -p {start_port}-{end_port}"
            print("  Running service detection scan...")
        else:
            args = f"-sS -p {start_port}-{end_port}"
            print("  Running basic TCP scan...")
        
        scanner.scan(hosts=target, arguments=args)
        
        for host in scanner.all_hosts():
            print(f"\n  Host: {host} ({scanner[host].hostname()})")
            print(f"  State: {scanner[host].state()}")
            
            for proto in scanner[host].all_protocols():
                print(f"\n  Protocol: {proto}")
                
                lport = sorted(scanner[host][proto].keys())
                for port in lport:
                    service = scanner[host][proto][port]
                    print(f"  Port {port}: {service['state']}", end=" ")
                    
                    if 'product' in service and service['product']:
                        print(f"- {service['product']} {service.get('version', '')}")
                    else:
                        print()
    
    except nmap.PortScannerError as e:
        print(f"  Error during scan: {e}")
        print("  Make sure nmap is installed on your system.")
    except Exception as e:
        print(f"  Error during scan: {e}")
    
    print("\n  Scan complete.")
    input("  Press Enter to continue...")

def packet_callback(packet, counter, stop_event):
    if stop_event.is_set():
        return
    
    counter[0] += 1
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    if packet.haslayer(scapy.IP):
        src_ip = packet[scapy.IP].src
        dst_ip = packet[scapy.IP].dst
        proto = packet[scapy.IP].proto
        
        proto_name = {1: "ICMP", 6: "TCP", 17: "UDP"}.get(proto, str(proto))
        
        packet_details = f"  [{timestamp}] {counter[0]}: {src_ip} -> {dst_ip} | {proto_name}"
        
        if packet.haslayer(scapy.TCP):
            src_port = packet[scapy.TCP].sport
            dst_port = packet[scapy.TCP].dport
            flags = packet[scapy.TCP].flags
            flag_str = ''
            
            if flags & 0x01: flag_str += 'F'
            if flags & 0x02: flag_str += 'S'
            if flags & 0x04: flag_str += 'R'
            if flags & 0x08: flag_str += 'P'
            if flags & 0x10: flag_str += 'A'
            if flags & 0x20: flag_str += 'U'
            
            packet_details += f" | TCP {src_port} -> {dst_port} [{flag_str}]"
            
            if packet.haslayer(http.HTTPRequest):
                http_layer = packet.getlayer(http.HTTPRequest)
                url = http_layer.Host + http_layer.Path
                packet_details += f" | HTTP GET {url}"
                
                if packet.haslayer(scapy.Raw):
                    payload = packet[scapy.Raw].load.decode('utf-8', 'ignore')
                    keywords = ['username', 'user', 'login', 'password', 'pass', 'email']
                    for keyword in keywords:
                        if keyword in payload.lower():
                            packet_details += f" | POSSIBLE LOGIN DATA: {payload[:50]}..."
                            break
        
        elif packet.haslayer(scapy.UDP):
            src_port = packet[scapy.UDP].sport
            dst_port = packet[scapy.UDP].dport
            packet_details += f" | UDP {src_port} -> {dst_port}"
            
            if packet.haslayer(scapy.DNSQR):
                qname = packet[scapy.DNSQR].qname.decode('utf-8')
                packet_details += f" | DNS Query: {qname}"
        
        elif packet.haslayer(scapy.ICMP):
            icmp_type = packet[scapy.ICMP].type
            icmp_code = packet[scapy.ICMP].code
            
            type_str = {0: "Echo Reply", 8: "Echo Request"}.get(icmp_type, str(icmp_type))
            packet_details += f" | ICMP {type_str} (type:{icmp_type}/code:{icmp_code})"
        
        print(packet_details)

def sniff_thread_function(interface, stop_event, packet_counter):
    try:
        scapy.sniff(
            iface=interface,
            prn=lambda pkt: packet_callback(pkt, packet_counter, stop_event),
            store=0,
            stop_filter=lambda pkt: stop_event.is_set()
        )
    except Exception as e:
        if not stop_event.is_set():
            print(f"\n  Error in sniffer: {e}")
            stop_event.set()

def network_sniffer():
    clear_screen()
    print("\n  === NETWORK SNIFFER ===")
    print("  This tool captures network packets in real-time")
    
    interfaces = []
    try:
        if os.name == 'nt':
            from scapy.arch.windows import get_windows_if_list
            interfaces = [iface.get('name', '') for iface in get_windows_if_list()]
        else:
            interfaces = scapy.get_if_list()
    except Exception as e:
        print(f"  Error getting interfaces: {e}")
        interfaces = []
        
    if interfaces:
        print("\n  Available interfaces:")
        for i, iface in enumerate(interfaces):
            print(f"  [{i}] {iface}")
    
    interface = input("\n  Enter interface name or number (leave empty for default): ")
    
    if interface.isdigit() and interfaces and int(interface) < len(interfaces):
        interface = interfaces[int(interface)]
    elif not interface and interfaces:
        interface = interfaces[0]
    elif not interface:
        interface = None
    
    if interface:
        print(f"\n  Starting network sniffer on interface: {interface}")
    else:
        print("\n  Starting network sniffer on default interface")
    
    print("  " + "="*50)
    print("  Capturing packets... Press Ctrl+C to stop.")
    print("  [Time] #: Source -> Destination | Protocol | Details")
    print("  " + "="*50)
    
    stop_event = threading.Event()
    packet_counter = [0]
    
    sniffer_thread = threading.Thread(
        target=sniff_thread_function,
        args=(interface, stop_event, packet_counter)
    )
    sniffer_thread.daemon = True
    
    try:
        sniffer_thread.start()
        
        while not stop_event.is_set():
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n\n  Stopping packet capture...")
    finally:
        stop_event.set()
        sniffer_thread.join(2)
    
    print(f"\n  Sniffing stopped. Captured {packet_counter[0]} packets.")
    input("  Press Enter to continue...")

def get_gateway():
    try:
        gateway = scapy.conf.route.route("0.0.0.0")[2]
        return gateway
    except:
        if os.name == 'nt':
            try:
                output = subprocess.check_output("ipconfig", shell=True).decode('utf-8')
                for line in output.split('\n'):
                    if "Default Gateway" in line:
                        gateway = line.split(":")[-1].strip()
                        if gateway and gateway != "None":
                            return gateway
            except:
                pass
        else:
            try:
                output = subprocess.check_output("ip route | grep default", shell=True).decode('utf-8')
                gateway = output.split("via")[-1].split()[0].strip()
                return gateway
            except:
                pass
    
    return None

def get_my_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def router_analysis():
    clear_screen()
    print("\n  === ROUTER ANALYSIS ===")
    
    gateway = get_gateway()
    
    if gateway:
        print(f"  Default gateway detected: {gateway}")
    
    router_ip = input("  Enter router IP (or hit Enter to use detected gateway): ")
    
    if not router_ip and gateway:
        router_ip = gateway
    elif not router_ip:
        router_ip = "192.168.1.1"
    
    print(f"\n  Analyzing router: {router_ip}")
    print("  " + "="*50)
    
    my_ip = get_my_ip()
    print(f"  Local IP: {my_ip}")
    
    try:
        arp_request = scapy.ARP(pdst=router_ip)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast/arp_request
        answered_list = scapy.srp(arp_request_broadcast, timeout=2, verbose=False)[0]
        
        if answered_list:
            router_mac = answered_list[0][1].hwsrc
            print(f"  Router MAC: {router_mac}")
        else:
            print("  Router MAC: Not discovered")
    except Exception as e:
        print(f"  Error getting router MAC: {e}")
    
    print("\n  Running traceroute to 8.8.8.8...")
    try:
        if os.name == 'nt':
            output = subprocess.check_output("tracert -d -h 5 8.8.8.8", shell=True).decode('utf-8', 'ignore')
        else:
            output = subprocess.check_output("traceroute -n -m 5 8.8.8.8", shell=True).decode('utf-8', 'ignore')
        
        for line in output.splitlines()[:10]:
            print(f"  {line}")
    except Exception as e:
        print(f"  Error running traceroute: {e}")
    
    print("\n  Checking for common open ports on router...")
    common_ports = [80, 443, 22, 23, 53, 8080, 8443, 21]
    for port in common_ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((router_ip, port))
        if result == 0:
            service = socket.getservbyport(port) if port < 1024 else "Unknown"
            print(f"  Port {port} ({service}): OPEN")
        sock.close()
    
    input("\n  Press Enter to continue...")

def dns_enumeration():
    clear_screen()
    print("\n  === DNS ENUMERATION ===")
    domain = input("  Enter domain to enumerate: ")
    
    if not domain:
        print("  Invalid domain. Returning to menu...")
        time.sleep(2)
        return
    
    print(f"\n  Enumerating DNS records for {domain}")
    print("  " + "="*50)
    
    record_types = ["A", "AAAA", "MX", "NS", "TXT", "SOA", "CNAME"]
    
    for record_type in record_types:
        print(f"\n  {record_type} Records:")
        try:
            answers = dns.resolver.resolve(domain, record_type)
            for rdata in answers:
                print(f"  {domain}. IN {record_type} {rdata}")
        except dns.resolver.NoAnswer:
            print(f"  No {record_type} records found")
        except dns.resolver.NXDOMAIN:
            print(f"  Domain {domain} does not exist")
            break
        except Exception as e:
            print(f"  Error retrieving {record_type} records: {e}")
    
    print("\n  Attempting to discover subdomains:")
    common_subdomains = ['www', 'mail', 'remote', 'blog', 'webmail', 'server', 'ns1', 'ns2', 
                         'smtp', 'secure', 'vpn', 'admin', 'mx', 'ftp', 'dev', 'test',
                         'cloud', 'api', 'cdn', 'shop', 'app']
    
    found_subdomains = []
    for subdomain in common_subdomains:
        try:
            full_domain = f"{subdomain}.{domain}"
            answers = dns.resolver.resolve(full_domain, "A")
            ips = [rdata.address for rdata in answers]
            print(f"  {full_domain}: {', '.join(ips)}")
            found_subdomains.append(full_domain)
        except:
            pass
    
    if not found_subdomains:
        print("  No common subdomains discovered")
    
    input("\n  Press Enter to continue...")

def vulnerability_scanner():
    clear_screen()
    print("\n  === VULNERABILITY SCANNER ===")
    target = input("  Enter target IP or hostname: ")
    
    if not target:
        print("  Invalid target. Returning to menu...")
        time.sleep(2)
        return
    
    scan_type = input("  Scan type (1=Basic, 2=Service Detection, 3=Vuln Scripts): ")
    
    print(f"\n  Scanning {target} for vulnerabilities")
    print("  " + "="*50)
    print("  This may take some time...\n")
    
    try:
        scanner = nmap.PortScanner()
        
        if scan_type == "3":
            print("  Running vulnerability scripts scan...")
            args = "-sV --script vuln"
        elif scan_type == "2":
            print("  Running service detection scan...")
            args = "-sV -p 21,22,23,25,53,80,110,111,135,139,143,443,445,993,995,1723,3306,3389,5900,8080"
        else:
            print("  Running basic scan...")
            args = "-sV -F"
        
        scanner.scan(hosts=target, arguments=args)
        
        for host in scanner.all_hosts():
            print(f"\n  Host: {host} ({scanner[host].hostname()})")
            print(f"  State: {scanner[host].state()}")
            
            for proto in scanner[host].all_protocols():
                print(f"\n  Protocol: {proto}")
                
                lport = sorted(scanner[host][proto].keys())
                for port in lport:
                    service = scanner[host][proto][port]
                    print(f"  Port {port}: {service['state']}", end=" ")
                    
                    if 'product' in service and service['product']:
                        print(f"- {service['product']} {service.get('version', '')}")
                        
                        if scan_type == "3" and 'script' in service:
                            for script_name, output in service['script'].items():
                                if output.strip():
                                    print(f"    [VULN] {script_name}:")
                                    for line in output.strip().split('\n'):
                                        print(f"      {line}")
                    else:
                        print()
    
    except nmap.PortScannerError as e:
        print(f"  Error during scan: {e}")
        print("  Make sure nmap is installed on your system.")
    except Exception as e:
        print(f"  Error during scan: {e}")
    
    print("\n  Scan complete.")
    input("  Press Enter to continue...") 