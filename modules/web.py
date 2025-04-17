import os
import time
import random
import string
from datetime import datetime

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def web_menu():
    while True:
        clear_screen()
        print("\n  === WEB INTELLIGENCE ===")
        print("  [1] Website Analyzer")
        print("  [0] Back to Main Menu")
        
        choice = input("\n  Select an option: ")
        
        if choice == "1":
            website_analyzer()
        elif choice == "0":
            return
        else:
            print("  Invalid option. Please try again...")
            time.sleep(1)

def website_analyzer():
    clear_screen()
    print("\n  === WEBSITE ANALYZER ===")
    
    url = input("  Enter website URL to analyze: ")
    if not url:
        print("  Invalid URL. Returning to menu...")
        time.sleep(2)
        return
    
    if not url.startswith('http'):
        url = 'https://' + url
    
    print(f"\n  Analyzing website: {url}")
    print("  " + "="*50)
    
    try:
                                                             
        import requests
        from bs4 import BeautifulSoup
        import socket
        from urllib.parse import urlparse
        
                                          
        print("  Fetching website content...")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        
                                         
        if response.status_code != 200:
            print(f"  Website returned status code: {response.status_code}")
                                                     
    
                                      
        
                                
        soup = BeautifulSoup(response.text, 'html.parser')
        
                           
        print("\n  Basic Information:")
        title = soup.title.string if soup.title else "No title found"
        print(f"  Title: {title}")
        
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        description = meta_desc['content'] if meta_desc and 'content' in meta_desc.attrs else "No description found"
        if len(description) > 100:
            description = description[:97] + "..."
        print(f"  Description: {description}")
        
                                             
        server = response.headers.get('Server', 'Not disclosed')
        print(f"  Server: {server}")
        
                                
        parsed_uri = urlparse(url)
        domain = parsed_uri.netloc
        try:
            ip_address = socket.gethostbyname(domain)
            print(f"  IP Address: {ip_address}")
        except:
            print(f"  IP Address: Unable to resolve")
        
                           
        print("\n  Security Analysis:")
        is_https = url.startswith('https://')
        print(f"  HTTPS: {'Yes' if is_https else 'No'}")
        
        security_headers = {
            'Strict-Transport-Security': 'HSTS',
            'Content-Security-Policy': 'CSP',
            'X-Content-Type-Options': 'Content Type Options',
            'X-Frame-Options': 'Frame Options',
            'X-XSS-Protection': 'XSS Protection'
        }
        
        for header, name in security_headers.items():
            value = response.headers.get(header, 'Not implemented')
            if value != 'Not implemented':
                value = 'Implemented'
            print(f"  {name}: {value}")
        
                          
        print("\n  Content Analysis:")
        links = soup.find_all('a', href=True)
        print(f"  Links: {len(links)}")
        
        images = soup.find_all('img')
        print(f"  Images: {len(images)}")
        
        scripts = soup.find_all('script')
        print(f"  JavaScript Files: {len(scripts)}")
        
        styles = soup.find_all('link', rel='stylesheet')
        print(f"  CSS Files: {len(styles)}")
        
                                           
        technologies = []
        
                                                
        js_frameworks = {
            'jQuery': ['jquery'],
            'React': ['react', 'reactjs'],
            'Vue.js': ['vue'],
            'Angular': ['angular'],
            'Bootstrap': ['bootstrap']
        }
        
        for script in scripts:
            script_src = script.get('src', '')
            script_text = script.string if script.string else ''
            
            for framework, keywords in js_frameworks.items():
                for keyword in keywords:
                    if (script_src and keyword in script_src.lower()) or                       (script_text and keyword in script_text.lower()):
                        technologies.append(framework)
        
                           
        technologies = list(set(technologies))
        
        if technologies:
            print(f"  Detected Technologies: {', '.join(technologies)}")
        else:
            print("  Detected Technologies: None identified")
        
    except requests.exceptions.RequestException as e:
        print(f"  Error connecting to website: {str(e)}")
    except Exception as e:
        print(f"  Error analyzing website: {str(e)}")
    
    input("\n  Press Enter to continue...")
    return
