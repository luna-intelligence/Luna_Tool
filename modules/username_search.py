import os
import time
import json
import requests
import re
import concurrent.futures
import random
import string
from bs4 import BeautifulSoup
from urllib.parse import urlparse

SITES_DATA = {
    "Twitter": {
        "url": "https://twitter.com/{}",
        "username_claimed": "<title>{} | X</title>",
        "username_unclaimed": "This account doesn't exist",
        "error_message": "Something went wrong",
        "username_pattern": "^[A-Za-z0-9_]{1,15}$"
    },
    "Instagram": {
        "url": "https://www.instagram.com/{}/",
        "username_claimed": "Profile picture of @{}",
        "username_unclaimed": "Sorry, this page isn't available",
        "error_message": "Please wait a few minutes before you try again",
        "username_pattern": "^[A-Za-z0-9_.]{1,30}$"
    },
    "GitHub": {
        "url": "https://github.com/{}",
        "username_claimed": "{} has",
        "username_unclaimed": "404 Not Found",
        "error_message": "Something went wrong",
        "username_pattern": "^[A-Za-z0-9-]{1,39}$"
    },
    "Reddit": {
        "url": "https://www.reddit.com/user/{}",
        "username_claimed": "u/{} - Reddit",
        "username_unclaimed": "Sorry, nobody on Reddit goes by that name",
        "error_message": "Something went wrong",
        "username_pattern": "^[A-Za-z0-9_-]{3,20}$"
    },
    "LinkedIn": {
        "url": "https://www.linkedin.com/in/{}/",
        "username_claimed": "{} - LinkedIn",
        "username_unclaimed": "Not found",
        "error_message": "Something went wrong",
        "username_pattern": "^[A-Za-z0-9_-]{3,100}$"
    },
    "Facebook": {
        "url": "https://www.facebook.com/{}",
        "username_claimed": "{} | Facebook",
        "username_unclaimed": "Page Not Found",
        "error_message": "Something went wrong",
        "username_pattern": "^[A-Za-z0-9.]{5,50}$"
    },
    "TikTok": {
        "url": "https://www.tiktok.com/@{}",
        "username_claimed": "{} (@{}) TikTok",
        "username_unclaimed": "Couldn't find this account",
        "error_message": "Something went wrong",
        "username_pattern": "^[A-Za-z0-9_.]{2,24}$"
    },
    "YouTube": {
        "url": "https://www.youtube.com/@{}",
        "username_claimed": "@{} - YouTube",
        "username_unclaimed": "404 Not Found",
        "error_message": "Something went wrong",
        "username_pattern": "^[A-Za-z0-9_-]{3,30}$"
    },
    "Pinterest": {
        "url": "https://www.pinterest.com/{}/",
        "username_claimed": "{} ({})",
        "username_unclaimed": "404: Not Found",
        "error_message": "Something went wrong",
        "username_pattern": "^[A-Za-z0-9_]{3,15}$"
    },
    "Tumblr": {
        "url": "https://{}.tumblr.com",
        "username_claimed": "{} -",
        "username_unclaimed": "There's nothing here.",
        "error_message": "Something went wrong",
        "username_pattern": "^[A-Za-z0-9-]{1,32}$"
    },
    "Medium": {
        "url": "https://medium.com/@{}",
        "username_claimed": "{} – Medium",
        "username_unclaimed": "404",
        "error_message": "Something went wrong",
        "username_pattern": "^[A-Za-z0-9_.]{1,50}$"
    },
    "Quora": {
        "url": "https://www.quora.com/profile/{}",
        "username_claimed": "{} - Quora",
        "username_unclaimed": "404 Not Found",
        "error_message": "Something went wrong",
        "username_pattern": "^[A-Za-z0-9_-]{3,50}$"
    },
    "DeviantArt": {
        "url": "https://{}.deviantart.com/",
        "username_claimed": "{} | DeviantArt",
        "username_unclaimed": "404 Not Found",
        "error_message": "Something went wrong",
        "username_pattern": "^[A-Za-z0-9-]{3,20}$"
    },
    "VKontakte": {
        "url": "https://vk.com/{}",
        "username_claimed": "{} | VK",
        "username_unclaimed": "404 Not Found",
        "error_message": "Something went wrong",
        "username_pattern": "^[A-Za-z0-9_-]{3,50}$"
    },
    "Twitch": {
        "url": "https://www.twitch.tv/{}",
        "username_claimed": "{} - Twitch",
        "username_unclaimed": "Sorry. Unless you've got a time machine",
        "error_message": "Something went wrong",
        "username_pattern": "^[A-Za-z0-9_]{4,25}$"
    },
    "SoundCloud": {
        "url": "https://soundcloud.com/{}",
        "username_claimed": "{} | Free Listening",
        "username_unclaimed": "404 Not Found",
        "error_message": "Something went wrong",
        "username_pattern": "^[A-Za-z0-9_-]{3,25}$"
    },
    "Snapchat": {
        "url": "https://www.snapchat.com/add/{}",
        "username_claimed": "{} on Snapchat",
        "username_unclaimed": "page not found",
        "error_message": "Something went wrong",
        "username_pattern": "^[A-Za-z0-9_.]{3,15}$"
    },
    "Spotify": {
        "url": "https://open.spotify.com/user/{}",
        "username_claimed": "{} | Spotify",
        "username_unclaimed": "404 Not Found",
        "error_message": "Something went wrong",
        "username_pattern": "^[A-Za-z0-9_-]{3,30}$"
    },
    "Telegram": {
        "url": "https://t.me/{}",
        "username_claimed": "Telegram: Contact",
        "username_unclaimed": "404 Not Found",
        "error_message": "Something went wrong",
        "username_pattern": "^[A-Za-z0-9_]{5,32}$"
    },
    "Patreon": {
        "url": "https://www.patreon.com/{}",
        "username_claimed": "{} is creating",
        "username_unclaimed": "404 Not Found",
        "error_message": "Something went wrong",
        "username_pattern": "^[A-Za-z0-9_]{1,30}$"
    },
    "WordPress": {
        "url": "https://{}.wordpress.com/",
        "username_claimed": "{} – ",
        "username_unclaimed": "doesn't exist",
        "error_message": "Something went wrong",
        "username_pattern": "^[A-Za-z0-9_-]{3,50}$"
    },
    "Slack": {
        "url": "https://{}.slack.com/",
        "username_claimed": "{}.slack.com",
        "username_unclaimed": "Not Found",
        "error_message": "Something went wrong",
        "username_pattern": "^[A-Za-z0-9-]{1,50}$"
    },
    "Behance": {
        "url": "https://www.behance.net/{}",
        "username_claimed": "{} on Behance",
        "username_unclaimed": "404 Not Found",
        "error_message": "Something went wrong",
        "username_pattern": "^[A-Za-z0-9_-]{1,30}$"
    },
    "GitLab": {
        "url": "https://gitlab.com/{}",
        "username_claimed": "{} · GitLab",
        "username_unclaimed": "404 Not Found",
        "error_message": "Something went wrong",
        "username_pattern": "^[A-Za-z0-9_.-]{1,255}$"
    },
    "Fiverr": {
        "url": "https://www.fiverr.com/{}",
        "username_claimed": "{} | Fiverr",
        "username_unclaimed": "404 Not Found",
        "error_message": "Something went wrong",
        "username_pattern": "^[A-Za-z0-9_]{3,30}$"
    },
    "Steam": {
        "url": "https://steamcommunity.com/id/{}",
        "username_claimed": "{} :: Steam Profile",
        "username_unclaimed": "The specified profile could not be found",
        "error_message": "Something went wrong",
        "username_pattern": "^[A-Za-z0-9_-]{3,32}$"
    },
    "Imgur": {
        "url": "https://imgur.com/user/{}",
        "username_claimed": "{} - Imgur",
        "username_unclaimed": "404 Not Found",
        "error_message": "Something went wrong",
        "username_pattern": "^[A-Za-z0-9_-]{3,30}$"
    },
    "Etsy": {
        "url": "https://www.etsy.com/shop/{}",
        "username_claimed": "{} - Etsy",
        "username_unclaimed": "Sorry, we couldn't find that page",
        "error_message": "Something went wrong",
        "username_pattern": "^[A-Za-z0-9-]{3,20}$"
    }
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def username_search_menu():
    while True:
        clear_screen()
        print("\n  === ADVANCED USERNAME SEARCH ===")
        print("  [1] Search Single Username")
        print("  [2] Search Multiple Usernames")
        print("  [3] Validate Username Formats")
        print("  [4] View Supported Platforms")
        print("  [0] Back to Main Menu")
        
        choice = input("\n  Select an option: ")
        
        if choice == "1":
            single_username_search()
        elif choice == "2":
            multi_username_search()
        elif choice == "3":
            validate_username_formats()
        elif choice == "4":
            view_supported_platforms()
        elif choice == "0":
            return
        else:
            print("  Invalid option. Please try again...")
            time.sleep(1)

def single_username_search():
    clear_screen()
    print("\n  === SINGLE USERNAME SEARCH ===")
    
    username = input("  Enter username to search: ")
    if not username:
        print("  Invalid username. Returning to menu...")
        time.sleep(2)
        return
    
    search_method = input("  Search method (1=Fast/Basic, 2=Thorough): ")
    if search_method not in ['1', '2']:
        search_method = '1'
        print("  Using fast search method")
    
    max_workers = 10 if search_method == '1' else 5
    
                                                  
    sites_to_check = {}
    for site_name, site_data in SITES_DATA.items():
        pattern = site_data.get("username_pattern", ".*")
        if re.match(pattern, username):
            sites_to_check[site_name] = site_data
    
    print(f"\n  Username '{username}' is valid for {len(sites_to_check)} out of {len(SITES_DATA)} sites")
    print("  " + "="*50)
    print("  Searching across platforms... This may take a while.")
    
                        
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    results = []
    def check_site(site_name, site_data):
        try:
            url = site_data["url"].format(username)
            response = requests.get(
                url, 
                headers=headers, 
                timeout=10,
                allow_redirects=True
            )
            
            if search_method == '2':
                                                                  
                claimed_text = site_data["username_claimed"].format(username)
                unclaimed_text = site_data["username_unclaimed"]
                
                if claimed_text.lower() in response.text.lower() and unclaimed_text.lower() not in response.text.lower():
                    return (site_name, url, True)         
                elif unclaimed_text.lower() in response.text.lower():
                    return (site_name, url, False)             
                else:
                                                             
                    soup = BeautifulSoup(response.text, 'html.parser')
                    if soup.title and username.lower() in soup.title.string.lower():
                        return (site_name, url, True)                
                    return (site_name, url, None)             
            else:
                                              
                if response.status_code == 200:
                    if "error_message" in site_data and site_data["error_message"].lower() in response.text.lower():
                        return (site_name, url, None)              
                    return (site_name, url, True)                     
                elif response.status_code == 404:
                    return (site_name, url, False)             
                else:
                    return (site_name, url, None)             

        except Exception as e:
            return (site_name, url, None)         
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_site = {executor.submit(check_site, site_name, site_data): site_name for site_name, site_data in sites_to_check.items()}
        
        for i, future in enumerate(concurrent.futures.as_completed(future_to_site)):
            site_name = future_to_site[future]
            try:
                result = future.result()
                if result:
                    results.append(result)
                print(f"  Checking {i+1}/{len(sites_to_check)} sites...", end="\r")
            except Exception as e:
                print(f"  Error checking {site_name}: {e}")
    
    print(" " * 50, end="\r")                       
    
                              
    found_results = [r for r in results if r[2] is True]
    not_found_results = [r for r in results if r[2] is False]
    uncertain_results = [r for r in results if r[2] is None]
    
    print(f"\n  Results for username '{username}':")
    print("  " + "="*50)
    print(f"  Found on {len(found_results)} sites:")
    
    if found_results:
        for site_name, url, _ in found_results:
            print(f"  - {site_name}: {url}")
    else:
        print("  None")
    
    print(f"\n  Not found on {len(not_found_results)} sites")
    
    if uncertain_results:
        print(f"\n  Uncertain results on {len(uncertain_results)} sites:")
        for site_name, url, _ in uncertain_results:
            print(f"  - {site_name}: {url}")
    
                                       
    save_results = input("\n  Save results to file? (y/n): ").lower() == 'y'
    if save_results:
        filename = f"username_search_{username}_{int(time.time())}.txt"
        with open(filename, "w") as f:
            f.write(f"Username Search Results for: {username}\n")
            f.write("="*50 + "\n\n")
            
            f.write(f"Found on {len(found_results)} sites:\n")
            for site_name, url, _ in found_results:
                f.write(f"- {site_name}: {url}\n")
            
            f.write(f"\nNot found on {len(not_found_results)} sites\n")
            
            if uncertain_results:
                f.write(f"\nUncertain results on {len(uncertain_results)} sites:\n")
                for site_name, url, _ in uncertain_results:
                    f.write(f"- {site_name}: {url}\n")
        
        print(f"  Results saved to {filename}")
    
    input("\n  Press Enter to continue...")

def multi_username_search():
    clear_screen()
    print("\n  === MULTIPLE USERNAME SEARCH ===")
    
                   
    print("  Enter usernames (one per line)")
    print("  Leave a blank line when done")
    
    usernames = []
    while True:
        username = input("  > ")
        if not username:
            break
        usernames.append(username)
    
    if not usernames:
        print("  No usernames entered. Returning to menu...")
        time.sleep(2)
        return
    
    print(f"\n  {len(usernames)} usernames to search")
    
                                   
    print("\n  Select platforms to search:")
    print("  [1] All platforms")
    print("  [2] Common platforms only (Twitter, Instagram, Facebook, etc.)")
    print("  [3] Select specific platforms")
    
    platform_choice = input("\n  Choice: ")
    
    if platform_choice == "1":
        sites_to_check = SITES_DATA
    elif platform_choice == "2":
        common_platforms = ["Twitter", "Instagram", "Facebook", "LinkedIn", "GitHub", "Reddit", "YouTube", "TikTok"]
        sites_to_check = {k: v for k, v in SITES_DATA.items() if k in common_platforms}
    elif platform_choice == "3":
        print("\n  Available platforms:")
        for i, site_name in enumerate(sorted(SITES_DATA.keys()), 1):
            print(f"  {i}. {site_name}")
        
        selected_platforms = input("\n  Enter platform numbers (comma-separated): ")
        try:
            selected_indices = [int(x.strip()) - 1 for x in selected_platforms.split(",")]
            sorted_platforms = sorted(SITES_DATA.keys())
            sites_to_check = {sorted_platforms[i]: SITES_DATA[sorted_platforms[i]] for i in selected_indices if 0 <= i < len(sorted_platforms)}
        except:
            print("  Invalid selection. Using common platforms.")
            common_platforms = ["Twitter", "Instagram", "Facebook", "LinkedIn", "GitHub", "Reddit", "YouTube", "TikTok"]
            sites_to_check = {k: v for k, v in SITES_DATA.items() if k in common_platforms}
    else:
        print("  Invalid choice. Using common platforms.")
        common_platforms = ["Twitter", "Instagram", "Facebook", "LinkedIn", "GitHub", "Reddit", "YouTube", "TikTok"]
        sites_to_check = {k: v for k, v in SITES_DATA.items() if k in common_platforms}
    
    print(f"\n  Searching across {len(sites_to_check)} platforms for {len(usernames)} usernames")
    print("  " + "="*50)
    
                        
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
                              
    all_results = {}
    for username in usernames:
        all_results[username] = []
    
                                        
    def check_username_on_site(username, site_name, site_data):
        try:
            url = site_data["url"].format(username)
            response = requests.get(
                url, 
                headers=headers, 
                timeout=10,
                allow_redirects=True
            )
            
                                          
            if response.status_code == 200:
                if "error_message" in site_data and site_data["error_message"].lower() in response.text.lower():
                    return (username, site_name, url, None)              
                return (username, site_name, url, True)                     
            elif response.status_code == 404:
                return (username, site_name, url, False)             
            else:
                return (username, site_name, url, None)             

        except Exception as e:
            return (username, site_name, url, None)         
    
                      
    total_checks = len(usernames) * len(sites_to_check)
    completed = 0
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_check = {}
        for username in usernames:
            for site_name, site_data in sites_to_check.items():
                                                        
                pattern = site_data.get("username_pattern", ".*")
                if not re.match(pattern, username):
                    completed += 1
                    continue
                
                future = executor.submit(check_username_on_site, username, site_name, site_data)
                future_to_check[future] = (username, site_name)
        
        for future in concurrent.futures.as_completed(future_to_check):
            completed += 1
            username, site_name = future_to_check[future]
            try:
                result = future.result()
                if result:
                    all_results[username].append((result[1], result[2], result[3]))
                print(f"  Progress: {completed}/{total_checks} checks completed ({(completed/total_checks)*100:.1f}%)", end="\r")
            except Exception as e:
                print(f"  Error checking {username} on {site_name}: {e}")
    
    print(" " * 60, end="\r")                       
    
                     
    print("\n  Search Results:")
    print("  " + "="*50)
    
    for username, results in all_results.items():
        found_results = [r for r in results if r[2] is True]
        print(f"\n  Username '{username}' found on {len(found_results)} sites:")
        
        if found_results:
            for site_name, url, _ in found_results:
                print(f"  - {site_name}: {url}")
        else:
            print("  None")
    
                                       
    save_results = input("\n  Save results to file? (y/n): ").lower() == 'y'
    if save_results:
        filename = f"multi_username_search_{int(time.time())}.txt"
        with open(filename, "w") as f:
            f.write(f"Multiple Username Search Results\n")
            f.write("="*50 + "\n\n")
            
            for username, results in all_results.items():
                found_results = [r for r in results if r[2] is True]
                f.write(f"Username '{username}' found on {len(found_results)} sites:\n")
                
                if found_results:
                    for site_name, url, _ in found_results:
                        f.write(f"- {site_name}: {url}\n")
                else:
                    f.write("None\n")
                
                f.write("\n")
        
        print(f"  Results saved to {filename}")
    
    input("\n  Press Enter to continue...")

def validate_username_formats():
    clear_screen()
    print("\n  === VALIDATE USERNAME FORMATS ===")
    
    username = input("  Enter username to validate: ")
    if not username:
        print("  Invalid username. Returning to menu...")
        time.sleep(2)
        return
    
    print(f"\n  Validating username format for '{username}'")
    print("  " + "="*50)
    
    valid_count = 0
    invalid_count = 0
    
    for site_name, site_data in sorted(SITES_DATA.items()):
        pattern = site_data.get("username_pattern", ".*")
        is_valid = bool(re.match(pattern, username))
        
        if is_valid:
            valid_count += 1
            status = "✓ Valid"
        else:
            invalid_count += 1
            status = "✗ Invalid"
        
        print(f"  {site_name}: {status}")
    
    print("  " + "="*50)
    print(f"  Username is valid for {valid_count} out of {len(SITES_DATA)} platforms")
    
    input("\n  Press Enter to continue...")

def view_supported_platforms():
    clear_screen()
    print("\n  === SUPPORTED PLATFORMS ===")
    print("  " + "="*50)
    
    for i, site_name in enumerate(sorted(SITES_DATA.keys()), 1):
        site_data = SITES_DATA[site_name]
        pattern = site_data.get("username_pattern", ".*")
        url_template = site_data["url"].format("<username>")
        
        print(f"  {i}. {site_name}")
        print(f"     URL: {url_template}")
        print(f"     Username Pattern: {pattern}")
        print()
    
    print(f"  Total supported platforms: {len(SITES_DATA)}")
    
    input("\n  Press Enter to continue...") 