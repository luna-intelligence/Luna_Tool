import os
import sys
import time
import sqlite3
import csv
import threading
import glob
from tkinter import Tk, filedialog
from tkinter.ttk import Progressbar
import tkinter as tk

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def db_search_menu():
    while True:
        clear_screen()
        print("\n  === SEARCH BY YOUR OWN DB ===")
        print("  Supported formats: .db (SQLite) and .csv files")
        print("  [1] Search in databases")
        print("  [0] Back to Main Menu")

        choice = input("\n  Select an option: ")

        if choice == "1":
            search_in_databases()
        elif choice == "0":
            return
        else:
            print("  Invalid option. Please try again...")
            time.sleep(1)

def get_directory_path():
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    
    print("\n  Please select a directory with your databases (.db and .csv files)...")
    
    directory_path = filedialog.askdirectory(title="Select Directory with Databases")
    
    if directory_path:
        return directory_path
    else:
        print("  No directory selected. Returning to menu...")
        time.sleep(2)
        return None

def find_database_files(directory_path):
    db_files = glob.glob(os.path.join(directory_path, "*.db"))
    csv_files = glob.glob(os.path.join(directory_path, "*.csv"))
    
    return db_files + csv_files

def load_sqlite_db(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        all_data = []
        table_schemas = {}
        
        for table in tables:
            table_name = table[0]
            
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [col[1] for col in cursor.fetchall()]
            
            table_schemas[table_name] = columns
            
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            
            for row in rows:
                all_data.append((table_name, row))
        
        conn.close()
        return all_data, table_schemas
    
    except sqlite3.Error as e:
        print(f"  Error loading SQLite database {db_path}: {e}")
        return [], {}

def load_csv_file(csv_path):
    try:
        with open(csv_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            headers = next(reader)
            
            all_data = []
            for row in reader:
                all_data.append(("csv_data", row))
            
            table_schemas = {"csv_data": headers}
            return all_data, table_schemas
    
    except Exception as e:
        print(f"  Error loading CSV file {csv_path}: {e}")
        return [], {}

def binary_search(data, target):
    left, right = 0, len(data) - 1
    
    while left <= right:
        mid = (left + right) // 2
        mid_value = str(data[mid][1][0]) if len(data[mid][1]) > 0 else ""
        
        if mid_value == target:
            return mid
        elif mid_value < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1

def linear_search(data, target, schemas):
    results = []
    
    for i, (table_name, row) in enumerate(data):
        for j, value in enumerate(row):
            if str(target).lower() in str(value).lower():
                column_name = schemas.get(table_name, [])[j] if j < len(schemas.get(table_name, [])) else f"Column {j}"
                results.append((i, table_name, column_name, row))
                break
    
    return results

def search_database(db_path, target, progress_callback=None):
    file_ext = os.path.splitext(db_path)[1].lower()
    
    if file_ext == '.db':
        data, schemas = load_sqlite_db(db_path)
    elif file_ext == '.csv':
        data, schemas = load_csv_file(db_path)
    else:
        return []
    
    if not data:
        return []
    
    try:
        sorted_data = sorted(data, key=lambda x: int(x[1][0]) if str(x[1][0]).isdigit() else float('inf'))
        index = binary_search(sorted_data, target)
        
        if index != -1:
            table_name = sorted_data[index][0]
            row = sorted_data[index][1]
            column_name = schemas.get(table_name, [])[0] if schemas.get(table_name, []) else "ID"
            return [(index, table_name, column_name, row)]
    except:
        pass
    
    results = linear_search(data, target, schemas)
    
    if progress_callback:
        progress_callback()
    
    return results

def create_progress_window(total_files):
    progress_window = tk.Tk()
    progress_window.title("Search Progress")
    progress_window.geometry("400x100")
    progress_window.attributes('-topmost', True)
    
    label = tk.Label(progress_window, text="Searching databases...")
    label.pack(pady=10)
    
    progress_bar = Progressbar(progress_window, orient="horizontal", length=300, mode="determinate")
    progress_bar.pack(pady=10)
    progress_bar["maximum"] = total_files
    progress_bar["value"] = 0
    
    return progress_window, progress_bar

def search_in_databases():
    clear_screen()
    print("\n  === SEARCH IN DATABASES ===")
    
    directory_path = get_directory_path()
    if not directory_path:
        return
    
    db_files = find_database_files(directory_path)
    
    if not db_files:
        print(f"  No database (.db) or CSV (.csv) files found in {directory_path}")
        input("\n  Press Enter to continue...")
        return
    
    print(f"\n  Found {len(db_files)} database/CSV files in {directory_path}")
    
    target = input("\n  Enter value to search for: ")
    if not target:
        print("  Invalid search term. Returning to menu...")
        time.sleep(2)
        return
    
    print(f"\n  Searching for '{target}' in {len(db_files)} files...")
    start_time = time.time()
    
    progress_window, progress_bar = create_progress_window(len(db_files))
    current_progress = 0
    
    all_results = []
    
    def update_progress():
        nonlocal current_progress
        current_progress += 1
        progress_bar["value"] = current_progress
        progress_window.update()
    
    try:
        for db_file in db_files:
            print(f"  Searching in {os.path.basename(db_file)}...", end="\r")
            
            results = search_database(db_file, target, update_progress)
            
            if results:
                for _, table_name, column_name, row in results:
                    all_results.append((db_file, table_name, column_name, row))
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        progress_window.destroy()
        
        clear_screen()
        print(f"\n  Search Results for '{target}':")
        print("  " + "="*50)
        
        if all_results:
            print(f"  Found {len(all_results)} matches in {len(set(r[0] for r in all_results))} files")
            
            for i, (db_file, table_name, column_name, row) in enumerate(all_results, 1):
                print(f"\n  Result #{i}:")
                print(f"  Database: {os.path.basename(db_file)}")
                print(f"  Table/Sheet: {table_name}")
                print(f"  Row data: {row}")
                
                if i >= 20:
                    print(f"\n  ... and {len(all_results) - 20} more results (showing first 20)")
                    break
        else:
            print(f"  No matches found for '{target}'")
        
        print(f"\n  Search completed in {elapsed_time:.2f} seconds")
    
    except Exception as e:
        try:
            progress_window.destroy()
        except:
            pass
        
        print(f"\n  Error during search: {e}")
    
    input("\n  Press Enter to continue...")

if __name__ == "__main__":
    db_search_menu() 