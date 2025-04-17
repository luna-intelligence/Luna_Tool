import os
import time
import requests
import re
from bs4 import BeautifulSoup

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def discord_lookup():
    clear_screen()
    print("\n  === DISCORD USER/SERVER LOOKUP ===")
    user_input = input("  Enter Discord username, server invite code, or full invite URL: ")
    
    if not user_input:
        print("  Invalid input. Returning to menu...")
        time.sleep(2)
        return
        
    if "/" in user_input and ("discord.gg" in user_input or "discord.com/invite" in user_input):
        invite_code = user_input.split("/")[-1]
        lookup_discord_server(invite_code)
    elif user_input.startswith("https://") or user_input.startswith("http://"):
        print("  Invalid URL format. Please enter a valid Discord invite link")
        input("\n  Press Enter to continue...")
        return
    else:
        if len(user_input) >= 2 and len(user_input) <= 10 and re.match(r'^[a-zA-Z0-9]+$', user_input):
            lookup_discord_server(user_input)
        else:
            lookup_discord_user(user_input)

def lookup_discord_user(username):
    print(f"\n  Looking up Discord user: {username}")
    print("  " + "="*50)
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Referer": "https://www.google.com/",
            "DNT": "1"
        }
        
        discord_id_url = f"https://discord.id/?prefill={username}"
        
        print("  Note: Discord doesn't provide public profile pages like Telegram")
        print("  Checking third-party Discord directories instead...")
        print("\n  Possible matching users:")
        
        lookup_sites = [
            f"https://discordlookup.com/user/{username}",
            f"https://discord.com/users/{username}" if username.isdigit() else None
        ]
        
        found_any = False
        
        for site in lookup_sites:
            if site is None:
                continue
                
            try:
                response = requests.get(site, headers=headers, timeout=8)
                if response.status_code == 200:
                    print(f"  User may exist: {site}")
                    found_any = True
            except:
                pass
        
        known_bots = {
            "mee6": "MEE6 (Popular moderation bot)",
            "dyno": "Dyno (Popular moderation bot)",
            "carl-bot": "Carl-bot (Popular moderation bot)",
            "groovy": "Groovy (Music bot - discontinued)",
            "rythm": "Rythm (Music bot)",
            "fredboat": "FredBoat (Music bot)",
            "giveawaybot": "GiveawayBot (Giveaway management)",
            "tatsumaki": "Tatsumaki (Social bot)"
        }
        
        if username.lower() in known_bots:
            print(f"  Known Discord Bot: {known_bots[username.lower()]}")
            found_any = True
        
        print("\n  General Information:")
        print("  Username Format: [name]#[discriminator] (e.g. Username#1234)")
        
        if username.count('#') == 1:
            name, discriminator = username.split('#')
            if discriminator.isdigit() and len(discriminator) == 4:
                print("  Valid username format detected")
                print(f"  Name: {name}")
                print(f"  Discriminator: #{discriminator}")
            else:
                print("  Note: Discriminator should be a 4-digit number")
        elif username.isdigit():
            print(f"  Appears to be a Discord User ID: {username}")
            print("  Discord User IDs are 18-20 digit numbers")
        else:
            print("  Note: Full Discord username includes a 4-digit discriminator after a #")
            
        print("\n  Ways to find a user:")
        print("  1. Must be in a mutual server with the user")
        print("  2. Need to know their exact username with discriminator")
        print("  3. Discord ID number can be used to add a friend")
        
        if not found_any:
            print("\n  No definitive user information could be found")
            print("  Discord does not provide public user profiles without authentication")
        
        print("\n  Discord.ID URL (may have information if user is indexed):")
        print(f"  {discord_id_url}")
        
    except Exception as e:
        print(f"  Error occurred: {str(e)}")
        
    input("\n  Press Enter to continue...")

def lookup_discord_server(invite_code):
    print(f"\n  Looking up Discord server with invite: {invite_code}")
    print("  " + "="*50)
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Referer": "https://www.google.com/",
            "DNT": "1"
        }
        
        invite_url = f"https://discord.com/invite/{invite_code}"
        response = requests.get(invite_url, headers=headers, timeout=10)
        
        server_info = {}
        found = False
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            if "This invite is invalid or has expired" not in response.text:
                found = True
                
                meta_title = soup.find('meta', property='og:title')
                if meta_title:
                    server_info['name'] = meta_title['content'].replace('Discord | ', '')
                
                meta_desc = soup.find('meta', property='og:description')
                if meta_desc:
                    server_info['description'] = meta_desc['content']
                    
                meta_image = soup.find('meta', property='og:image')
                if meta_image:
                    server_info['icon_url'] = meta_image['content']
                
                member_info = re.search(r'(\d+,?\d*) Members', response.text)
                if member_info:
                    server_info['member_count'] = member_info.group(1)
                
                online_info = re.search(r'(\d+,?\d*) Online', response.text)
                if online_info:
                    server_info['online_count'] = online_info.group(1)
                
                if 'Discord Partner' in response.text or 'Verified' in response.text:
                    server_info['verified'] = True
                
        if found:
            print(f"  Server Invite: {invite_code}")
            print(f"  Invite Link: {invite_url}")
            
            if 'name' in server_info:
                print(f"  Server Name: {server_info['name']}")
            
            if 'description' in server_info:
                print(f"  Description: {server_info['description']}")
            
            if 'member_count' in server_info:
                print(f"  Member Count: {server_info['member_count']}")
            
            if 'online_count' in server_info:
                print(f"  Online Count: {server_info['online_count']}")
            
            if 'verified' in server_info:
                print("  Verified: Yes")
            else:
                print("  Verified: No")
            
            if 'icon_url' in server_info:
                print("  Server Icon: Yes")
                print(f"  Icon URL: {server_info['icon_url']}")
            else:
                print("  Server Icon: No")
            
            print("\n  Additional Information:")
            
            if 'nsfw' in response.text.lower() or 'age-restricted' in response.text.lower():
                print("  NSFW: Yes (Age-restricted)")
            else:
                print("  NSFW: No")
            
            bot_patterns = ['MEE6', 'Dyno', 'Carl-bot', 'Groovy', 'Rythm', 'FredBoat', 'GiveawayBot', 'Tatsumaki']
            detected_bots = []
            
            for bot in bot_patterns:
                if bot in response.text:
                    detected_bots.append(bot)
            
            if detected_bots:
                print("  Popular Bots Detected: " + ", ".join(detected_bots))
                
            vanity_pattern = re.search(r'discord\.gg/([a-zA-Z0-9]+)', response.text)
            if vanity_pattern and vanity_pattern.group(1) != invite_code:
                print(f"  Vanity URL: discord.gg/{vanity_pattern.group(1)}")
                
        else:
            print("  Invalid or expired invite code")
            print("  Discord server could not be found with this invite")
            
    except requests.exceptions.Timeout:
        print("  Error: Request timed out. Please try again later.")
    except requests.exceptions.ConnectionError:
        print("  Error: Connection error. Please check your internet connection.")
    except Exception as e:
        print(f"  Error occurred: {str(e)}")
        
    input("\n  Press Enter to continue...")

if __name__ == "__main__":
    discord_lookup() 