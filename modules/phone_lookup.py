import os
import time
import json
import requests
import re
import phonenumbers
from phonenumbers import geocoder, carrier, timezone

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def phone_lookup_menu():
    while True:
        clear_screen()
        basic_phone_lookup()
        return

def basic_phone_lookup():
    clear_screen()
    print("\n  === BASIC PHONE NUMBER LOOKUP ===")
    phone = input("  Enter phone number (with country code, e.g. +1234567890): ")
    
    if not phone:
        print("  Invalid phone number. Returning to menu...")
        time.sleep(2)
        return
        
    print(f"\n  Looking up phone number: {phone}")
    print("  " + "="*50)
    
    phone = clean_phone_number(phone)
    
    if not (phone.startswith('+') and len(phone) > 8 and len(phone) < 16 and phone[1:].isdigit()):
        print("  Invalid phone number format")
        input("\n  Press Enter to continue...")
        return
    
    try:
        parsed_number = phonenumbers.parse(phone)
        
        if not phonenumbers.is_valid_number(parsed_number):
            print("  Number is not valid according to E.164 standard")
            input("\n  Press Enter to continue...")
            return
        
        country_code = parsed_number.country_code
        country_iso = phonenumbers.region_code_for_number(parsed_number)
        country_name = get_country_name(country_iso)
        
        international_format = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        national_format = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)
        e164_format = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        
        carrier_name = carrier.name_for_number(parsed_number, "en")
        
        location = geocoder.description_for_number(parsed_number, "en")
        
        number_type = get_number_type(parsed_number)
        
        number_timezones = timezone.time_zones_for_number(parsed_number)
        tz_info = ", ".join(number_timezones) if number_timezones else "Unknown"
        
        print("\n  Phone Number Information:")
        print(f"  Valid: true")
        print(f"  Number: {phone}")
        print(f"  Local format: {national_format}")
        print(f"  International format: {international_format}")
        print(f"  E164 format: {e164_format}")
        print(f"  Country prefix: +{country_code}")
        print(f"  Country code: {country_iso}")
        print(f"  Country name: {country_name}")
        print(f"  Location: {location or 'Unknown'}")
        print(f"  Carrier: {carrier_name or 'Unknown'}")
        print(f"  Line type: {number_type}")
        print(f"  Timezone: {tz_info}")
        
    except Exception as e:
        print(f"  Error analyzing number: {e}")
    
    input("\n  Press Enter to continue...")
    return

def detailed_phone_analysis():
    clear_screen()
    print("\n  === DETAILED PHONE ANALYSIS ===")
    phone = input("  Enter phone number (with country code, e.g. +1234567890): ")
    
    if not phone:
        print("  Invalid phone number. Returning to menu...")
        time.sleep(2)
        return
        
    print(f"\n  Analyzing phone number: {phone}")
    print("  " + "="*50)
    
    phone = clean_phone_number(phone)
    
    try:
        parsed_number = phonenumbers.parse(phone)
        
        if not phonenumbers.is_valid_number(parsed_number):
            print("  Number is not valid")
            input("\n  Press Enter to continue...")
            return
        
        country_code = parsed_number.country_code
        country_iso = phonenumbers.region_code_for_number(parsed_number)
        country_name = get_country_name(country_iso)
        
        international_format = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        national_format = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)
        e164_format = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        
        carrier_name = carrier.name_for_number(parsed_number, "en")
        location = geocoder.description_for_number(parsed_number, "en")
        
        number_type = get_number_type(parsed_number)
        
        detailed_carrier = get_detailed_carrier_info(phone, country_iso)
        
        possible = phonenumbers.is_possible_number(parsed_number)
        valid_region = phonenumbers.is_valid_number_for_region(parsed_number, country_iso)
        
        print("\n  Phone Number Information:")
        print(f"  Valid: true")
        print(f"  Number: {phone}")
        print(f"  Local format: {national_format}")
        print(f"  International format: {international_format}")
        print(f"  E164 format: {e164_format}")
        print(f"  Country prefix: +{country_code}")
        print(f"  Country code: {country_iso}")
        print(f"  Country name: {country_name}")
        print(f"  Location: {location or 'Unknown'}")
        print(f"  Carrier: {carrier_name or detailed_carrier or 'Unknown'}")
        print(f"  Line type: {number_type}")
        
        print("\n  Additional Details:")
        print(f"  Possible number: {'Yes' if possible else 'No'}")
        print(f"  Valid for region {country_iso}: {'Yes' if valid_region else 'No'}")
        
        if country_iso == "US" or country_iso == "CA":
            area_code = national_format.split(" ")[0].replace("(", "").replace(")", "")
            print(f"\n  North American Numbering Plan Analysis:")
            print(f"  Area Code: {area_code}")
            print(f"  Exchange Code: {national_format.split(" ")[1].split("-")[0]}")
            print(f"  Subscriber Number: {national_format.split("-")[1]}")
        elif country_iso == "RU":
            print(f"\n  Russian Number Analysis:")
            print(f"  Mobile Provider Code: {national_format[2:5]}")
            if national_format.startswith("9"):
                print(f"  Network Type: Mobile")
        
        print("\n  OSINT Risk Assessment:")
        print("  • Phone number exposure on the internet may lead to spam calls")
        print("  • Numbers can be used for account verification (2FA)")
        print("  • Can be used to trace identity and location")
        
        print("\n  Best Practices:")
        print("  • Don't share your number publicly online")
        print("  • Consider using a secondary number for online services")
        print("  • Monitor for suspicious calls/SMS")
        
    except Exception as e:
        print(f"  Error analyzing number: {e}")
    
    input("\n  Press Enter to continue...")

def international_number_validation():
    clear_screen()
    print("\n  === INTERNATIONAL NUMBER VALIDATION ===")
    
    numbers_input = input("  Enter phone numbers to validate (comma separated): ")
    
    if not numbers_input:
        print("  No numbers provided. Returning to menu...")
        time.sleep(2)
        return
    
    numbers = [clean_phone_number(num.strip()) for num in numbers_input.split(",")]
    
    print("\n  Validating numbers...")
    print("  " + "="*50)
    
    for number in numbers:
        try:
            parsed_number = phonenumbers.parse(number)
            is_valid = phonenumbers.is_valid_number(parsed_number)
            is_possible = phonenumbers.is_possible_number(parsed_number)
            
            if is_valid:
                country_iso = phonenumbers.region_code_for_number(parsed_number)
                country_name = get_country_name(country_iso)
                international_format = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
                number_type = get_number_type(parsed_number)
                
                print(f"\n  Number: {number}")
                print(f"  Status: Valid")
                print(f"  Formatted: {international_format}")
                print(f"  Country: {country_name} ({country_iso})")
                print(f"  Type: {number_type}")
                
            else:
                error_msg = "Invalid format"
                if not is_possible:
                    error_msg = "Number not possible (wrong length or invalid format)"
                
                print(f"\n  Number: {number}")
                print(f"  Status: Invalid - {error_msg}")
        
        except Exception as e:
            print(f"\n  Number: {number}")
            print(f"  Status: Error - {str(e)}")
    
    input("\n  Press Enter to continue...")

                  

def clean_phone_number(phone):
    return phone.strip().replace(" ", "").replace("-", "").replace("(", "").replace(")", "")

def get_number_type(parsed_number):
    num_type = phonenumbers.number_type(parsed_number)
    
    type_map = {
        phonenumbers.PhoneNumberType.MOBILE: "mobile",
        phonenumbers.PhoneNumberType.FIXED_LINE: "landline",
        phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE: "landline or mobile",
        phonenumbers.PhoneNumberType.TOLL_FREE: "toll-free",
        phonenumbers.PhoneNumberType.PREMIUM_RATE: "premium rate",
        phonenumbers.PhoneNumberType.SHARED_COST: "shared cost",
        phonenumbers.PhoneNumberType.VOIP: "VoIP",
        phonenumbers.PhoneNumberType.PERSONAL_NUMBER: "personal",
        phonenumbers.PhoneNumberType.PAGER: "pager",
        phonenumbers.PhoneNumberType.UAN: "UAN",
        phonenumbers.PhoneNumberType.UNKNOWN: "unknown"
    }
    
    return type_map.get(num_type, "unknown")

def get_country_name(country_code):
    country_names = {
        "US": "United States",
        "CA": "Canada",
        "RU": "Russian Federation",
        "GB": "United Kingdom",
        "AU": "Australia",
        "DE": "Germany",
        "FR": "France",
        "IT": "Italy",
        "ES": "Spain",
        "JP": "Japan",
        "CN": "China",
        "IN": "India",
        "BR": "Brazil",
        "KR": "South Korea"
    }
    
    return country_names.get(country_code, country_code)

def get_detailed_carrier_info(phone, country_code):
    if phone.startswith('+7'):
        if any(phone.startswith(f'+79{prefix}') for prefix in ['00', '02', '04', '08', '50', '62', '69', '77', '85', '86', '88']):
            return "MegaFon"
        elif any(phone.startswith(f'+79{prefix}') for prefix in ['01', '02', '10', '13', '14', '15', '16', '19', '68', '84']):
            return "MTS"
        elif any(phone.startswith(f'+79{prefix}') for prefix in ['03', '05', '06', '09', '60', '61', '95', '96', '99']):
            return "Beeline"
        elif any(phone.startswith(f'+79{prefix}') for prefix in ['52', '53', '55', '57', '58', '59', '77', '78', '9']):
            return "Tele2"
        elif phone.startswith('+7800'):
            return "Toll-free number"
    
    elif phone.startswith('+1'):
        if phone[2:6] in ['3115', '3128', '3242']:
            return "Verizon"
        elif phone[2:6] in ['3145', '3235', '3256']:
            return "AT&T"
        elif phone[2:6] in ['3107', '3125', '3237']:
            return "T-Mobile"
    
    return None

if __name__ == "__main__":
    phone_lookup_menu() 