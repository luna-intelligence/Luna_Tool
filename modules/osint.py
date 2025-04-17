import os
import time
import requests
import socket
import whois
import re
import json
import dns.resolver
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def osint_menu():
    while True:
        clear_screen()
        print("  === OSINT Menu ===")
        print("  [1] Email Verification")
        print("  [2] Username Search")
        print("  [3] Phone Number Lookup")
        print("  [4] IP Geolocation")
        print("  [5] Metadata Extraction")
        print("  [6] Search by your own DB")
        print("  [0] Back to Main Menu")

        choice = input("\n  Select an option: ")

        if choice == '1':
            email_verification()
        elif choice == '2':
            username_search()
        elif choice == '3':
            phone_lookup()
        elif choice == '4':
            ip_geolocation()
        elif choice == '5':
            metadata_extraction()
        elif choice == '6':
            from modules.db_search import db_search_menu
            db_search_menu()
        elif choice == '0':
            return
        else:
            print("  Invalid option. Please try again...")
            time.sleep(1)

def email_verification():
    clear_screen()
    print("\n  === EMAIL INTELLIGENCE ===")
    email = input("\n  Enter email address: ")
    
    if not email or '@' not in email:
        print("  Invalid email format. Returning to menu...")
        time.sleep(2)
        return
        
    print(f"\n  Analyzing: {email}")
    print("  " + "="*60)
    
                           
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        print("  Invalid email format")
        input("\n  Press Enter to continue...")
        return
    
                                 
    username, domain = email.split('@', 1)
    
    print(f"  Username: {username}")
    print(f"  Domain: {domain}")
    
                                 
    print("\n  DOMAIN VERIFICATION")
    print("  " + "-"*60)
    
                                
    domain_exists = False
    try:
        domain_ip = socket.gethostbyname(domain)
        domain_exists = True
        print(f"  Domain resolves to IP: {domain_ip}")
        
                                    
        try:
            ptr_record = socket.gethostbyaddr(domain_ip)[0]
            print(f"  Reverse DNS: {ptr_record}")
        except:
            print("  No reverse DNS record found")
            
    except socket.gaierror:
        print(f"  Domain does not exist or cannot be resolved")

                                       
    print("\n  EMAIL SERVER VERIFICATION")
    print("  " + "-"*60)
    
    if domain_exists:
        try:
            mx_records = dns.resolver.resolve(domain, 'MX')
            if mx_records:
                print("  Mail servers (MX records):")
                for mx in sorted(mx_records, key=lambda x: x.preference):
                    print(f"  - {mx.exchange} (Priority: {mx.preference})")
                
                                                             
                mx_servers = [str(mx.exchange).lower() for mx in mx_records]
                
                provider_found = False
                provider_signatures = {
                    'Google': ['google', 'gmail', 'googlemail', 'aspmx.l.google.com'],
                    'Microsoft': ['outlook.com', 'hotmail.com', 'microsoft.com'],
                    'ProtonMail': ['protonmail', 'proton.ch'],
                    'Yahoo': ['yahoo', 'yahoodns', 'yahoomail'],
                    'Zoho': ['zoho'],
                    'Yandex': ['yandex'],
                    'Mail.ru': ['mail.ru'],
                    'Mailchimp': ['mailchimp'],
                    'GoDaddy': ['secureserver.net', 'godaddy'],
                    'Amazon SES': ['amazonses'],
                    'Fastmail': ['fastmail'],
                    'Rackspace': ['emailsrvr.com', 'rackspace']
                }
                
                for provider, signatures in provider_signatures.items():
                    if any(any(sig in mx_server for sig in signatures) for mx_server in mx_servers):
                        print(f"  Provider identified: {provider}")
                        provider_found = True
                        break
                        
                if not provider_found:
                    print("  Provider: Custom/self-hosted mail server")
            else:
                print("  No mail servers found - domain cannot receive email")
        except Exception as e:
            print(f"  MX record lookup failed: {str(e)}")
    
                                    
    print("\n  EMAIL SECURITY CONFIGURATION")
    print("  " + "-"*60)
    
    if domain_exists:
                                    
        security_records = {
            'SPF': ('TXT', domain, lambda r: any('v=spf1' in str(txt) for txt in r)),
            'DMARC': ('TXT', f'_dmarc.{domain}', lambda r: any('v=dmarc1' in str(txt) for txt in r)),
        }
        
        for record_type, (dns_type, lookup_domain, check_func) in security_records.items():
            try:
                records = dns.resolver.resolve(lookup_domain, dns_type)
                if check_func(records):
                    print(f"  {record_type}: Present")
                    
                                                             
                    if record_type == 'SPF':
                        for txt in records:
                            spf_record = str(txt)
                            if 'v=spf1' in spf_record:
                                print(f"  SPF Record: {spf_record}")
                                
                                if '-all' in spf_record:
                                    print("  SPF Policy: Strict (-all)")
                                elif '~all' in spf_record:
                                    print("  SPF Policy: Soft Fail (~all)")
                                elif '?all' in spf_record:
                                    print("  SPF Policy: Neutral (?all)")
                                elif '+all' in spf_record:
                                    print("  SPF Policy: Permissive (+all)")
                    
                                                               
                    elif record_type == 'DMARC':
                        for txt in records:
                            dmarc_record = str(txt)
                            if 'v=dmarc1' in dmarc_record:
                                print(f"  DMARC Record: {dmarc_record}")
                                
                                                      
                                if 'p=none' in dmarc_record:
                                    print("  DMARC Policy: None (Monitoring only)")
                                elif 'p=quarantine' in dmarc_record:
                                    print("  DMARC Policy: Quarantine")
                                elif 'p=reject' in dmarc_record:
                                    print("  DMARC Policy: Reject")
                else:
                    print(f"  {record_type}: Not found")
            except Exception:
                print(f"  {record_type}: Lookup failed")
    
                           
    print("\n  WEBSITE VERIFICATION")
    print("  " + "-"*60)
    
    if domain_exists:
        website_found = False
        try:
            response = requests.get(f"https://{domain}", timeout=3)
            print(f"  Website found: https://{domain}")
            print(f"  Status code: {response.status_code}")
            website_found = True
        except:
            try:
                response = requests.get(f"http://{domain}", timeout=3)
                print(f"  Website found: http://{domain}")
                print(f"  Status code: {response.status_code}")
                website_found = True
            except:
                print(f"  No website found at http(s)://{domain}")
    
                            
    print("\n  VERIFICATION RESULTS")
    print("  " + "-"*60)
    
                                  
    technical_status = []
    
    if domain_exists:
        technical_status.append("Domain exists")
    else:
        technical_status.append("Domain does not exist")
        
    if 'mx_records' in locals() and mx_records:
        technical_status.append("Email server configured")
    elif domain_exists:
        technical_status.append("No email server configured")
        
    if website_found:
        technical_status.append("Website exists")
    elif domain_exists:
        technical_status.append("No website found")
    
                                           
    print(f"  Email address: {email}")
    print(f"  Status: {', '.join(technical_status)}")
    
    if domain_exists and 'mx_records' in locals() and mx_records:
        print("  Result: Email address is properly configured to receive messages")
    elif domain_exists:
        print("  Result: Domain exists but cannot receive email (no mail servers)")
    else:
        print("  Result: Email address cannot receive messages (domain does not exist)")
    
    print("\n  " + "="*60)
    input("\n  Press Enter to continue...")

def phone_lookup():
    from modules.phone_lookup import phone_lookup_menu
    phone_lookup_menu()

def get_country_iso_code(country_name):
    country_map = {
        'United States/Canada': 'US',
        'Russia/Kazakhstan': 'RU',
        'United Kingdom': 'GB',
        'Australia': 'AU',
        'Germany': 'DE',
        'France': 'FR',
        'Italy': 'IT',
        'Spain': 'ES',
        'China': 'CN',
        'Japan': 'JP',
        'India': 'IN',
        'Brazil': 'BR',
        'Russian Federation': 'RU'
    }
    
    if country_name in country_map:
        return country_map[country_name]
    
    for name, code in country_map.items():
        if country_name in name or name in country_name:
            return code
    
    if '/' in country_name:
        first_country = country_name.split('/')[0]
        if first_country in country_map:
            return country_map[first_country]
    
    if len(country_name) >= 2:
        return country_name[:2].upper()
    
    return "??"

def get_carrier_info(phone_number):
    """Get carrier information based on number patterns"""
                                                                         
    
                      
    if phone_number.startswith('+7'):
        if any(phone_number.startswith(f'+79{prefix}') for prefix in ['00', '02', '04', '08', '50', '62', '69', '77', '85', '86', '88']):
            return "MegaFon"
        elif any(phone_number.startswith(f'+79{prefix}') for prefix in ['01', '02', '10', '13', '14', '15', '16', '19', '68', '84']):
            return "MTS"
        elif any(phone_number.startswith(f'+79{prefix}') for prefix in ['03', '05', '06', '09', '60', '61', '95', '96', '99']):
            return "Beeline"
        elif any(phone_number.startswith(f'+79{prefix}') for prefix in ['52', '53', '55', '57', '58', '59', '77', '78', '9']):
            return "Tele2"
        elif phone_number.startswith('+7800'):
            return "Toll-free number"
    
                                       
    elif phone_number.startswith('+1'):
        if phone_number[2:6] in ['3115', '3128', '3242']:
            return "Verizon"
        elif phone_number[2:6] in ['3145', '3235', '3256']:
            return "AT&T"
        elif phone_number[2:6] in ['3107', '3125', '3237']:
            return "T-Mobile"
    
    return "Unknown"

def get_location_info(phone_number, country_code):
    """Get location information based on number patterns"""
    
                           
    if country_code == "RU":
        if phone_number.startswith('+7495') or phone_number.startswith('+7499'):
            return "Moscow"
        elif phone_number.startswith('+7812'):
            return "Saint Petersburg"
        elif phone_number.startswith('+7383'):
            return "Novosibirsk"
        elif phone_number.startswith('+7863'):
            return "Rostov-on-Don"
                                                          
        elif phone_number.startswith('+79'):
            return "Mobile (Russia-wide)"
    
                                                 
    elif country_code == "US":
        area_code = phone_number[2:5]
        us_area_codes = {
            '212': 'New York, NY',
            '213': 'Los Angeles, CA',
            '312': 'Chicago, IL',
            '404': 'Atlanta, GA',
            '415': 'San Francisco, CA',
            '305': 'Miami, FL',
            '702': 'Las Vegas, NV',
            '202': 'Washington, DC'
        }
        if area_code in us_area_codes:
            return us_area_codes[area_code]
    
    return "Unknown"

def determine_line_type(phone_number, country_code):
    """Determine line type based on number patterns"""
    
                     
    if country_code == "RU":
        if phone_number.startswith('+79'):
            return "mobile"
        elif phone_number.startswith('+78'):
            return "toll-free"
        else:
            return "landline"
    
                
    elif country_code == "US":
        if phone_number.startswith('+1800') or phone_number.startswith('+1844') or phone_number.startswith('+1855') or phone_number.startswith('+1866') or phone_number.startswith('+1877') or phone_number.startswith('+1888'):
            return "toll-free"
        else:
            return "unknown"                                                                    
    
                                                                                               
    return "unknown"

def username_search():
    clear_screen()
    print("\n  === USERNAME SEARCH ===")
    username = input("  Enter username to search: ")
    
    if not username:
        print("  Invalid username. Returning to menu...")
        time.sleep(2)
        return
        
    print(f"\n  Searching for username: {username}")
    print("  " + "="*50)
    print("  Checking popular platforms...")
    
                                                       
    platforms = {
        "Twitter/X": f"https://twitter.com/{username}",
        "Instagram": f"https://www.instagram.com/{username}/",
        "Facebook": f"https://www.facebook.com/{username}",
        "LinkedIn": f"https://www.linkedin.com/in/{username}/",
        "GitHub": f"https://github.com/{username}",
        "Reddit": f"https://www.reddit.com/user/{username}",
        "YouTube": f"https://www.youtube.com/@{username}",
        "TikTok": f"https://www.tiktok.com/@{username}",
        "Pinterest": f"https://www.pinterest.com/{username}/",
        "Twitch": f"https://www.twitch.tv/{username}",
        "Medium": f"https://medium.com/@{username}",
        "Vimeo": f"https://vimeo.com/{username}",
        "Flickr": f"https://www.flickr.com/people/{username}/",
        "Behance": f"https://www.behance.net/{username}",
        "Dribbble": f"https://dribbble.com/{username}",
        "Patreon": f"https://www.patreon.com/{username}",
        "DeviantArt": f"https://{username}.deviantart.com/",
        "Quora": f"https://www.quora.com/profile/{username}",
        "Steam": f"https://steamcommunity.com/id/{username}",
        "Soundcloud": f"https://soundcloud.com/{username}"
    }
    
                                             
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    results = []
    
    for platform, url in platforms.items():
        try:
            response = requests.get(url, headers=headers, timeout=5, allow_redirects=True)
            
                                                                              
            if platform == "Twitter/X":
                if response.status_code == 200 and f"@{username}" in response.text:
                    results.append((platform, url, True))
                else:
                    results.append((platform, url, False))
            
            elif platform == "Instagram":
                if response.status_code == 200 and not "Page Not Found" in response.text:
                    results.append((platform, url, True))
                else:
                    results.append((platform, url, False))
            
            elif platform == "GitHub":
                if response.status_code == 200 and not "Not Found" in response.text:
                    results.append((platform, url, True))
                else:
                    results.append((platform, url, False))
                    
            elif platform == "Reddit":
                if response.status_code == 200 and "u/" + username in response.text:
                    results.append((platform, url, True))
                else:
                    results.append((platform, url, False))
                    
            else:
                                                         
                if response.status_code == 200:
                    results.append((platform, url, True))
                else:
                    results.append((platform, url, False))
            
            print(f"  Checking {platform}...", end="\r")
            
        except Exception as e:
            results.append((platform, url, None))                            
    
    print(" " * 40, end="\r")                              
    
                   
    print("\n  Results:")
    print("  " + "-"*50)
    
    found_count = 0
    for platform, url, found in results:
        if found is True:
            status = "FOUND"
            found_count += 1
        elif found is False:
            status = "NOT FOUND"
        else:
            status = "ERROR CHECKING"
        
        print(f"  {platform}: {status}")
        if found:
            print(f"    URL: {url}")
    
    print("  " + "-"*50)
    print(f"  Total platforms where username was found: {found_count}")
    
    input("\n  Press Enter to continue...")

def ip_geolocation():
    clear_screen()
    print("\n  === IP GEOLOCATION ===")
    ip = input("  Enter IP address: ")
    
    if not ip:
        print("  Invalid IP address. Returning to menu...")
        time.sleep(2)
        return
        
    print(f"\n  Geolocating IP: {ip}")
    print("  " + "="*50)
    
                                
    ip_pattern = r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$'
    match = re.match(ip_pattern, ip)
    
    if not match:
        print("  Invalid IP address format")
        input("\n  Press Enter to continue...")
        return
    
                              
    for octet in match.groups():
        if int(octet) > 255:
            print("  Invalid IP address (octet > 255)")
            input("\n  Press Enter to continue...")
            return
    
                                
    private_ranges = [
        (re.compile(r'^10\.'), "Private IP (Class A)"),
        (re.compile(r'^172\.(1[6-9]|2[0-9]|3[0-1])\.'), "Private IP (Class B)"),
        (re.compile(r'^192\.168\.'), "Private IP (Class C)"),
        (re.compile(r'^127\.'), "Localhost"),
        (re.compile(r'^169\.254\.'), "Link-local address")
    ]
    
    for pattern, label in private_ranges:
        if pattern.match(ip):
            print(f"  {label}")
            print("  Cannot geolocate private IP addresses")
            input("\n  Press Enter to continue...")
            return
    
                                               
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        data = response.json()
        
        if "bogon" in data and data["bogon"]:
            print("  This is a bogon (reserved/private) IP address")
            input("\n  Press Enter to continue...")
            return
        
        print("  Location Information:")
        if "city" in data and "region" in data and "country" in data:
            print(f"  City: {data.get('city', 'Unknown')}")
            print(f"  Region: {data.get('region', 'Unknown')}")
            print(f"  Country: {data.get('country', 'Unknown')}")
        
        if "loc" in data:
            print(f"  Coordinates: {data.get('loc', 'Unknown')}")
            
        if "org" in data:
            print(f"  ISP/Organization: {data.get('org', 'Unknown')}")
            
        if "timezone" in data:
            print(f"  Timezone: {data.get('timezone', 'Unknown')}")
            
        if "postal" in data:
            print(f"  Postal Code: {data.get('postal', 'Unknown')}")
            
                            
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            print(f"  Hostname: {hostname}")
        except:
            print("  Hostname: Not available")
        
    except Exception as e:
        print(f"  Error retrieving geolocation data: {e}")
    
    input("\n  Press Enter to continue...") 

def metadata_extraction():
    """Extract metadata from files by importing from the metadata_extraction module"""
    try:
        from modules.metadata_extraction import metadata_extractor
        metadata_extractor()
    except ImportError as e:
        print(f"\n  Error: {e}")
        print("  Make sure the metadata_extraction.py module is available.")
    input("\n  Press Enter to continue...") 