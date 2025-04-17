import os
import sys
import time
import random
import string
from datetime import datetime
from colorama import *
from pystyle import *

                  
VERSION = f"0.0.1 | {Fore.YELLOW}Beta{Style.RESET_ALL}"
CODENAME = f"{Fore.CYAN}Luna OSINT{Style.RESET_ALL}"
DEVELOPER = f"{Fore.GREEN}https://t.me/luna_intelligence{Style.RESET_ALL}"
LAUNCH_AT = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_animated_loading():
    message = "Luna starting"
    animation_chars = string.ascii_letters + string.digits + string.punctuation
    width = os.get_terminal_size().columns
    
    delay = 0.1
    
    for pos in range(len(message) + 1):
        animated_text = ""
        for i in range(len(message)):
            if i < pos:
                animated_text += message[i]
            else:
                animated_text += random.choice(animation_chars)
        
        clear_screen()
        print("\n" * (os.get_terminal_size().lines // 3))
        print(animated_text.center(width))
        
        time.sleep(delay)
    
    time.sleep(0.3)

def display_banner():
    banner = f'''
                   ____           
              .--""___ ""-,       
            .' .-"" __:-' ;       
          /__:.--""      :       
          \              _`-'\   
            \_..--""    ""     :  
            /      ______..,   ;  
        _gd$$$$$$$$$$$$$$$P===;               Tool:       {CODENAME} 
      ,g$$$$$$P^^^^T$$$$$P'    ;  
      T^": ,-.       """  \    :              Version:    {VERSION}
          ;;  d.   .-"""d. \ ,-:  
        : '.:$$'-"    :$$  '.-,;              Developer:  {DEVELOPER}
        ;   :^"    "-._T'  ') :: 
        /   /      \         ._.'             Launch at:  {LAUNCH_AT}
      .   :        ; \       \;  
      ;    \      /   :       :  
      ;     '-..-'            ;  
      :     ,---.    ,       /   
      '    '  -. "--"      .'    
        `.              _.-"      
          "-.       _.-"          
            "-._.-"     
    '''
    print(Center.XCenter(banner))
                   
                                                  
                                           
                                                                         
                          

def display_menu():
    menu = f'''
    [1] Osint Search                    [4] Web Intelligence
    [2] Network Reconnaissance          [5] Custom HTTP Requests
    [3] DDOS Tools                      

    [e] Exit
    '''

    print(Center.XCenter(menu))

def main_menu():
    while True:
        clear_screen()
        display_banner()
        
        display_menu()

                                              
                                                  
                                      
                                                 
                                            
                                                
                                                      
                                    
                                
        
        choice = input("\n╔═══[Select an option]\n╚══> ")
        
        if choice == "1":
            from modules.osint import osint_menu
            osint_menu()
        elif choice == "2":
            from modules.network import network_menu
            network_menu()
        elif choice == "3":
            from modules.ddos import ddos_menu
            ddos_menu()
        elif choice == "4":
            from modules.web import web_menu
            web_menu()
        elif choice == "5":
            from modules.custom_requests import custom_requests_menu
            custom_requests_menu()
                             
                                                                      
                                    
                             
                                                        
                             
        elif choice == "e":
            clear_screen()
            sys.exit(0)
        else:
            print("  Invalid option. Please try again...")
            time.sleep(1)

if __name__ == "__main__":
    if not os.path.exists("modules"):
        print("  Initial setup in progress...")
        os.makedirs("modules", exist_ok=True)
    
    try:
        display_animated_loading()
        main_menu()
    except KeyboardInterrupt:
        print("\n\n  Exiting...")
        sys.exit(0)