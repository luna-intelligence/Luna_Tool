import os
import time
import requests
from bs4 import BeautifulSoup

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def telegram_lookup():
    clear_screen()
    print("\n  === TELEGRAM USER LOOKUP ===")
    username = input("  Enter Telegram username: ")
    
    if not username:
        print("  Invalid input. Returning to menu...")
        time.sleep(2)
        return
        
    print(f"\n  Looking up Telegram user: {username}")
    print("  " + "="*50)
    
    if username.startswith('@'):
        username = username[1:]
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Referer": "https://www.google.com/",
            "DNT": "1"
        }
        
        web_url = f"https://t.me/{username}"
        response = requests.get(web_url, headers=headers, timeout=10)
        
        found = False
        account_type = "Unknown"
        profile_info = {}
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            if "tgme_page" in response.text:
                found = True
                
                if "tgme_page_channel" in response.text:
                    account_type = "Channel"
                elif "tgme_page_user" in response.text:
                    account_type = "User"
                elif "tgme_page_group" in response.text:
                    account_type = "Group"
                
                title_tag = soup.find('div', class_='tgme_page_title')
                if title_tag:
                    profile_info["name"] = title_tag.get_text(strip=True)
                
                description_tag = soup.find('div', class_='tgme_page_description')
                if description_tag:
                    profile_info["bio"] = description_tag.get_text(strip=True)
                
                if account_type in ["Channel", "Group"]:
                    extra_tag = soup.find('div', class_='tgme_page_extra')
                    if extra_tag:
                        profile_info["member_count"] = extra_tag.get_text(strip=True)
                
                verified = soup.find('i', class_='verified-icon')
                if verified:
                    profile_info["verified"] = True
                
                photo = soup.find('img', class_='tgme_page_photo_image')
                if photo and photo.get('src'):
                    profile_info["photo_url"] = photo['src']
        
        if found:
            print(f"  Username: @{username}")
            print(f"  Account Type: {account_type}")
            
            if "name" in profile_info:
                print(f"  Name: {profile_info['name']}")
            
            if "bio" in profile_info:
                print(f"  Bio: {profile_info['bio']}")
            else:
                print("  Bio: Not available")
            
            if "member_count" in profile_info:
                print(f"  {account_type} Size: {profile_info['member_count']}")
            
            if "verified" in profile_info:
                print("  Verified: Yes")
            else:
                print("  Verified: No")
            
            if "photo_url" in profile_info:
                print("  Profile Photo: Yes")
                print(f"  Photo URL: {profile_info['photo_url']}")
            else:
                print("  Profile Photo: No")
            
            print(f"  Public Link: {web_url}")
            
            if account_type in ["Channel", "Group"]:
                posts_visible = "Posts are publicly visible" if "tgme_widget_message_wrap" in response.text else "Posts are not publicly visible"
                print(f"  Content Status: {posts_visible}")
            
            if account_type == "Channel":
                last_activity = soup.find('time', class_='time')
                if last_activity:
                    print(f"  Last Activity: {last_activity.get_text(strip=True)}")

            related = soup.find_all('a', class_='tgme_widget_message_link_preview')
            if related:
                print("\n  Related Links:")
                for link in related[:5]:
                    href = link.get('href')
                    if href:
                        print(f"    {href}")
        else:
            print(f"  Username '@{username}' not found or not publicly accessible")
            print("  Note: This could be due to privacy settings or the user doesn't exist")
            
    except requests.exceptions.Timeout:
        print("  Error: Request timed out. Please try again later.")
    except requests.exceptions.ConnectionError:
        print("  Error: Connection error. Please check your internet connection.")
    except Exception as e:
        print(f"  Error occurred: {str(e)}")
        
    input("\n  Press Enter to continue...")

if __name__ == "__main__":
    telegram_lookup()