import os
import time
import requests
import json
import re
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def custom_requests_menu():
    while True:
        clear_screen()
        print("\n  === CUSTOM HTTP REQUESTS ===")
        print("  [1] GET Request")
        print("  [2] POST Request")
        print("  [3] PUT Request")
        print("  [4] DELETE Request")
        print("  [5] HEAD Request")
        print("  [6] OPTIONS Request")
        print("  [7] Custom Request Builder")
        print("  [0] Back to Main Menu")
        
        choice = input("\n  Select an option: ")
        
        if choice == "1":
            make_request("GET")
        elif choice == "2":
            make_request("POST")
        elif choice == "3":
            make_request("PUT")
        elif choice == "4":
            make_request("DELETE")
        elif choice == "5":
            make_request("HEAD")
        elif choice == "6":
            make_request("OPTIONS")
        elif choice == "7":
            custom_request_builder()
        elif choice == "0":
            return
        else:
            print("  Invalid option. Please try again...")
            time.sleep(1)

def make_request(method):
    clear_screen()
    print(f"\n  === {method} REQUEST ===")
    
    url = input("  Enter URL: ")
    if not url:
        print("  Invalid URL. Returning to menu...")
        time.sleep(2)
        return
    
    if not url.startswith('http'):
        url = 'https://' + url
    
    print("\n  === HEADERS ===")
    print("  Enter headers (one per line, format 'Key: Value')")
    print("  Leave a blank line when done")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    while True:
        header_line = input("  > ")
        if not header_line:
            break
        
        if ":" in header_line:
            key, value = header_line.split(":", 1)
            headers[key.strip()] = value.strip()
    
    data = None
    if method in ["POST", "PUT"]:
        print("\n  === PAYLOAD ===")
        content_type = headers.get("Content-Type", "").lower()
        
        if "json" in content_type:
            print("  Enter JSON payload:")
            json_str = input("  > ")
            try:
                data = json.loads(json_str)
            except json.JSONDecodeError:
                print("  Invalid JSON. Using as raw data.")
                data = json_str
        elif "x-www-form-urlencoded" in content_type:
            print("  Enter form data (one per line, format 'key=value')")
            print("  Leave a blank line when done")
            form_data = {}
            while True:
                form_line = input("  > ")
                if not form_line:
                    break
                if "=" in form_line:
                    key, value = form_line.split("=", 1)
                    form_data[key.strip()] = value.strip()
            data = form_data
        else:
            print("  Enter raw data:")
            data = input("  > ")
    
    print("\n  === QUERY PARAMETERS ===")
    print("  Enter query parameters (one per line, format 'key=value')")
    print("  Leave a blank line when done")
    
    params = {}
    while True:
        param_line = input("  > ")
        if not param_line:
            break
        if "=" in param_line:
            key, value = param_line.split("=", 1)
            params[key.strip()] = value.strip()
    
    timeout = input("\n  Enter request timeout in seconds (default: 10): ")
    try:
        timeout = int(timeout) if timeout else 10
    except:
        timeout = 10
    
    verify_ssl = input("  Verify SSL certificate? (y/n, default: y): ").lower()
    verify_ssl = verify_ssl != 'n'
    
    print(f"\n  Making {method} request to {url}...")
    print("  " + "="*50)
    
    try:
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            data=data,
            timeout=timeout,
            verify=verify_ssl
        )
        
        print(f"  Status Code: {response.status_code} ({response.reason})")
        print(f"  Response Time: {response.elapsed.total_seconds():.2f} seconds")
        
        print("\n  Response Headers:")
        for key, value in response.headers.items():
            print(f"  {key}: {value}")
        
        if method != "HEAD":
            content_type = response.headers.get('Content-Type', '')
            
            if 'application/json' in content_type:
                try:
                    json_data = response.json()
                    print("\n  Response Body (JSON):")
                    print("  " + json.dumps(json_data, indent=2).replace('\n', '\n  '))
                except:
                    print("\n  Response Body:")
                    print(f"  {response.text[:2000]}")
                    if len(response.text) > 2000:
                        print("  ... (truncated)")
            elif 'text/html' in content_type:
                print("\n  Response Body (HTML):")
                print(f"  Length: {len(response.text)} characters")
                
                try:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    title = soup.title.string if soup.title else "No title found"
                    print(f"  Title: {title}")
                    
                    forms = soup.find_all('form')
                    if forms:
                        print(f"\n  Found {len(forms)} form(s):")
                        for i, form in enumerate(forms, 1):
                            method = form.get('method', 'GET').upper()
                            action = form.get('action', '')
                            print(f"  Form #{i}: Method={method}, Action={action}")
                            
                            inputs = form.find_all(['input', 'textarea', 'select'])
                            if inputs:
                                print("  Fields:")
                                for input_field in inputs:
                                    field_type = input_field.get('type', input_field.name)
                                    field_name = input_field.get('name', 'unnamed')
                                    print(f"    - {field_name} ({field_type})")
                except Exception as e:
                    print(f"  Error parsing HTML: {e}")
                
                show_html = input("\n  Show full HTML? (y/n): ").lower() == 'y'
                if show_html:
                    print("\n  HTML Content:")
                    print("  " + response.text.replace('\n', '\n  '))
            else:
                print("\n  Response Body:")
                if len(response.text) > 2000:
                    print(f"  {response.text[:2000]}")
                    print("  ... (truncated)")
                else:
                    print(f"  {response.text}")
        
        save_response = input("\n  Save response to file? (y/n): ").lower() == 'y'
        if save_response:
            filename = input("  Enter filename: ")
            if not filename:
                filename = f"response_{int(time.time())}"
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write(response.text)
            print(f"  Response saved to {filename}")
    
    except Exception as e:
        print(f"  Error making request: {e}")
    
    input("\n  Press Enter to continue...")

def custom_request_builder():
    clear_screen()
    print("\n  === CUSTOM REQUEST BUILDER ===")
    
    print("\n  Available HTTP Methods:")
    methods = ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS", "PATCH", "TRACE", "CONNECT"]
    for i, method in enumerate(methods, 1):
        print(f"  {i}. {method}")
    
    method_choice = input("\n  Select method (1-9): ")
    try:
        method = methods[int(method_choice) - 1]
    except:
        print("  Invalid choice. Using GET.")
        method = "GET"
    
    make_request(method)

def parse_url(url):
    """Parse URL and extract components"""
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)
    
                                                             
    for key, value in query_params.items():
        if isinstance(value, list) and len(value) == 1:
            query_params[key] = value[0]
    
    return {
        "scheme": parsed.scheme,
        "netloc": parsed.netloc,
        "path": parsed.path,
        "params": parsed.params,
        "query": parsed.query,
        "fragment": parsed.fragment,
        "query_params": query_params
    }