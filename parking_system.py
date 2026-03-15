from datetime import datetime

PARKING_SPACE_TYPES = ("Regular", "Reserved", "Electric")
PERMIT_OPTIONS = ("Daily", "Monthly", "Annual")
PERMIT_PRIORITY = {"D": 1, "M": 2, "A": 3}

# ANSI COLOR CODES
RESET = "\033[0m"
BLUE = "\033[94m"     # Borders and Dividers
CYAN = "\033[96m"     # Titles and Headers
GREEN = "\033[92m"    # Success messages and 'Yes'
YELLOW = "\033[93m"   # User Prompts
RED = "\033[91m"      # Errors and 'No'
MAGENTA = "\033[95m"  # Admin Menu Theme

# BEGIN UNIVERSAL HELPER FUNCTIONS

def get_valid_date():
    while True:
        date_str = input(f"{YELLOW}Enter date (DD/MM/YYYY) or q to cancel : {RESET}").strip()
        
        if date_str.lower() == "q":
            return "q"
        
        date_str = date_str.replace("-", "/")
        
        try:
            valid_date_object = datetime.strptime(date_str, "%d/%m/%Y")
            standardized_date_str = valid_date_object.strftime("%Y-%m-%d")
            
            return standardized_date_str 
            
        except ValueError:
            print(f"{RED}Invalid date or format. Please use exactly DD/MM/YYYY.{RESET}")

def load_from_file(file_name):
    headers = []
    data_list = []

    try:
        with open(file_name, "r") as file:
            line = file.readline()
            if not line:                                                
                return headers, data_list
            headers = line.strip().split(",")

            for line in file:
                clean_line = line.strip()
                if clean_line:                                          
                    entry = line.strip().split(",")
                    data_list.append(entry)
                
            return headers, data_list

    except IOError:
        print(f"{RED}[Error] Could not read file {file_name}.{RESET}")
        return headers, data_list

def get_valid_time():
    while True:
        time_str = input(f"{YELLOW}Enter time (HH:MM) or q to cancel : {RESET}").strip()
        if time_str.lower() == "q":
            return "q"
        
        parts = time_str.split(":")
        if len(parts) == 2 and len(parts[0]) == 2 and len(parts[1]) == 2:

            if parts[0].isdigit() and parts[1].isdigit():

                if 0 <= int(parts[0]) <= 23 and 0 <= int(parts[1]) <= 59:
                    return time_str
                else:
                    print(f"{RED}Error: Please insert valid 24-hour time (00:00 - 23:59).{RESET}")
            else:
                print(f"{RED}Error: Hours and minutes must be numeric.{RESET}")
        else:
            print(f"{RED}Invalid format. Please use exactly HH:MM (24-hour).{RESET}")

def get_record(full_id, data_list):
    target = full_id.strip().upper()

    for item in data_list:
        if item[0].upper() == target:
            return item
    return False

def save_to_file(data_list, file_name, headers):
    try:
        with open(file_name, "w") as file:
            file.write(",".join(headers) + '\n')
            for entry in data_list:
                file.write(",".join(entry) + '\n')
        return True
            
    except IOError:
        print(f"{RED}[Error] Could not write to file {file_name}. Please check permissions.{RESET}")
        return False

def get_id_number(record, index_of_id):
    full_id = record[index_of_id]
    return int(full_id[1:])

def enter_id(id_name):
    try:
        id_str = input(f"{YELLOW}Enter ID (e.g. S12) of {id_name}, or q to cancel : {RESET}").strip()

        if id_str.lower() == "q":
            return "q", "q"
        
        if not id_str[0].isalpha():
            print(f"{RED}Invalid format. ID must start with a letter (e.g., S12).{RESET}")
            return None, None

        elif len(id_str) > 2 and id_str[1] == "0":                      
            id_number_str = id_str[2:]
        else:
            id_number_str = id_str[1:]
        return id_str[0], int(id_number_str)
    
    except ValueError:
        print(f"{RED}Invalid ID, please try again.{RESET}")
        return None, None

def permit_types_sort_key(permit): 

    full_id = permit[0]
    category = full_id[0]
    id_num = get_id_number(permit, 0)
    priority = PERMIT_PRIORITY.get(category, 4)
    
    return (priority, id_num)

# END UNIVERSAL HELPER FUNCTIONS


# BEGIN PARKING STAFF FUNCTIONS

def staff_menu():
    while True:
        print(f"\n{BLUE}" + "="*45 + f"{RESET}")
        print(f"{CYAN}   PARKING RECORD SYSTEM - PARKING STAFF MENU   {RESET}")
        print(f"{BLUE}" + "="*45 + f"{RESET}")
        print("[p] Parking Availability")
        print("[r] Vehicle Record (Entry/Exit)")
        print("[v] Visitors Temporary Passes")
        print("[d] Daily Logs")
        print("[b] Back to Main Menu")
        print(f"{BLUE}" + "-"*45 + f"{RESET}")

        staff_menu_choice = input(f"{YELLOW}Enter your choice: {RESET}").strip().lower()
        if staff_menu_choice in ["p", "parking availability"]:
            staff_parking_available()
        elif staff_menu_choice in ["r", "vehicle record"]:
            staff_vehicle_record_menu()
        elif staff_menu_choice in ["v", "visitors temporary passes"]:
            staff_visitors_temporary_passes()
        elif staff_menu_choice in ["d", "daily logs"]:
            staff_daily_logs()
        elif staff_menu_choice in ["b", "back to main menu"]:
            print(f"{CYAN}Returning to Main Menu...{RESET}")
            return
        else:
            print(f"{RED}Invalid selection.{RESET}")

def staff_parking_available():
    parking_headers, parking_spaces = load_from_file("parking_spaces.txt")

    while True:
        print(f"\n{BLUE}" + "=" * 45 + f"{RESET}")
        print(f"{CYAN}   AVAILABLE PARKING CHECKING {RESET}")
        print(f"{BLUE}" + "=" * 45 + f"{RESET}")
        print("[r] Regular")
        print("[s] Reserved")
        print("[e] Electric")
        print("[b] Back to Parking Staff Menu")
        print(f"{BLUE}" + "-" * 45 + f"{RESET}")

        choice = input(f"{YELLOW}Enter your choice: {RESET}").strip().lower()
        if choice in ["r", "regular"]:
            target_type = "regular"
        elif choice in ["s", "reserved"]:
            target_type = "reserved"
        elif choice in ["e", "electric"]:
            target_type = "electric"
        elif choice in ["b", "back to parking staff menu"]:
            print(f"{CYAN}Back to Parking Staff Menu.....{RESET}")
            return
        else:
            print(f"{RED}Invalid selection.{RESET}")
            continue

        found_any = False  

        print(f"\n{CYAN}Searching for available {target_type} spots...{RESET}")
        print(f"Parking space available:")

        for space in parking_spaces:

            parkingID = space[0]
            parking_type = space[1].lower()  
            status = space[2].lower()  

            if parking_type  == target_type and status == "available":
                print(f"{GREEN}{parkingID}{RESET}")
                found_any = True
                
        if not found_any:
            print(f"{RED}Sorry, no {target_type} spots are available right now.{RESET}")

def staff_vehicle_record_menu(): 
    while True:
        print(f"\n{BLUE}" + "=" * 45 + f"{RESET}")
        print(f"{CYAN}   PARKING RECORD SYSTEM - VEHICLE RECORD  {RESET}")
        print(f"{BLUE}" + "=" * 45 + f"{RESET}")
        print("[r] Record New Vehicle Entry")
        print("[u] Update Vehicle Exit")
        print("[b] Back to Parking Staff Menu")
        print(f"{BLUE}" + "-" * 45 + f"{RESET}")
        vehicle_record_menu_choice = input(f"{YELLOW}Enter your choice: {RESET}").strip().lower()

        if vehicle_record_menu_choice in ["r", "record new vehicle entry"]:
            staff_vehicle_entry()
        elif vehicle_record_menu_choice in ["u", "update vehicle exit"]:
            staff_vehicle_exit()
        elif vehicle_record_menu_choice in ["b", "back to parking staff menu"]:
            print(f"{CYAN}Back to Parking Staff Menu.....{RESET}")
            return
        else:
            print(f"{RED}Invalid selection.{RESET}")

def staff_vehicle_entry():
    parking_headers, parking_spaces = load_from_file("parking_spaces.txt")

    print(f"\n{CYAN}--- Parking Spaces Entry System ---{RESET}")
    print(f"SpaceID | Type")
    space_available = []

    for space in parking_spaces:
        if len(space) >= 3 and space[2].capitalize() == "Available":
            print(f"{space[0]} | {space[1]}")
            space_available.append(space[0])

    if not space_available:
        print(f"{RED}No parking spaces are currently available.{RESET}")
        return

    while True:
        entry_parking_SpaceID = input(f"{YELLOW}Enter SpaceID choice: {RESET}").strip().upper()         
        if entry_parking_SpaceID in space_available:
            break
        else:
            print(space_available)
            print(f"{RED}Error: invalid SpaceID. Please choose available space (e.g., S01){RESET}")

    entry_parking_plate = input(f"{YELLOW}Enter vehicle plate number: {RESET}")

    print(f"{CYAN}Enter vehicle entry time:{RESET}")          
    vehicle_entry_time = get_valid_time()
    if vehicle_entry_time == "q": return

    print(f"{CYAN}Enter vehicle entry date:{RESET}")          
    vehicle_entry_date = get_valid_date()
    if vehicle_entry_date == "q": return

    space = get_record(entry_parking_SpaceID, parking_spaces)
    idx = parking_spaces.index(space)
    parking_spaces[idx] = [space[0], space[1], "Occupied", entry_parking_plate, vehicle_entry_time, vehicle_entry_date]
    
    save_to_file(parking_spaces, "parking_spaces.txt", parking_headers)
    print(f"{GREEN}Successfully added {entry_parking_plate} to parking space {entry_parking_SpaceID}.{RESET}")

def staff_vehicle_exit():
    parking_headers, parking_spaces = load_from_file("parking_spaces.txt")
    logs_headers, parking_logs = load_from_file("parking_logs.txt")

    print(f"\n{CYAN}--- Parking Spaces Exit System ---{RESET}")

    while True:
        exit_parking_plate = input(f"{YELLOW}Enter vehicle plate number to exit: {RESET}").strip().upper()

        vehicle_plate_found = False
        target_vehicle_data = {}

        for space in parking_spaces:
            if len(space) >= 6 and space[3] == exit_parking_plate:
                exit_parking_index = parking_spaces.index(space)
                vehicle_plate_found = True
                target_vehicle_data = {
                    'plate': space[3],  
                    'spaceID': space[0],
                    'type': space[1],
                    'entry_time': space[4],
                    'entry_date': space[5],
                }

        if not vehicle_plate_found:
            print(f"{RED}Vehicle with plate {exit_parking_plate} not found.{RESET}")
            continue

        print(f"\n{CYAN}--- Time and Date of Exit ---{RESET}")
        print(f"{CYAN}Enter vehicle exit time:{RESET}")
        exit_time_str = get_valid_time()
        if exit_time_str == "q": return
        
        print(f"{CYAN}Enter vehicle exit date:{RESET}")
        exit_date_str = get_valid_date()
        if exit_date_str == "q": return

        try:
            end_dt = datetime.strptime(f"{exit_date_str} {exit_time_str}", "%Y-%m-%d %H:%M")
            start_dt = datetime.strptime(f"{target_vehicle_data['entry_date']} {target_vehicle_data['entry_time']}", "%Y-%m-%d %H:%M")

            if end_dt < start_dt:
                print(f"{RED}Error: Exit time cannot be before entry time!{RESET}")
                continue
        except ValueError:
            print(f"{RED}Error: Invalid Format. Use HH:MM and DD/MM/YYYY.{RESET}")
            continue

        difference = end_dt - start_dt
        total_hours = difference.total_seconds() / 3600
        total_hours = round(total_hours, 2)

        if total_hours < 0.25: 
            rounded_fee = 0.00
        else:
            vehicle_type = target_vehicle_data['type'].lower()
            if vehicle_type == 'electric' : 
                rate = 5.00
            elif vehicle_type == 'regular' : 
                rate = 2.00
            else : 
                rate = 3.00
            total_fee = total_hours * rate
            rounded_fee = round(total_fee, 2)

        if parking_logs:
                max_id = 0
                for log in parking_logs:
                    current_id = get_id_number(log, 1)
                    if current_id > max_id:
                        max_id = current_id
                log_id = f"L{max_id + 1}"
        else:
            log_id = "L101"

        with open('parking_logs.txt', 'a') as log_file:
            log_entry = (
                f"{exit_date_str},{log_id},{target_vehicle_data['plate']},{target_vehicle_data['spaceID']},"
                f"{target_vehicle_data['entry_time']},{exit_time_str},{rounded_fee}\n")
            log_file.write(log_entry)

        parking_spaces[exit_parking_index] = [space[0], space[1], "Available", "", "", ""]
        save_to_file(parking_spaces, "parking_spaces.txt", parking_headers)

        print(f"{GREEN}Successfully removed {target_vehicle_data['plate']} from {target_vehicle_data['spaceID']}{RESET}")
        print(f"{CYAN}Total fee is RM{rounded_fee}{RESET}")
        break

def staff_visitors_temporary_passes():
    permit_headers, permit_types = load_from_file("permit_types.txt")
    permits_headers, permits = load_from_file("permits.txt")

    print(f"\n{BLUE}" + "=" * 60 + f"{RESET}")
    print(f"{CYAN}   WELCOME TO VISITOR TEMPORARY PASSES MENU   {RESET}")
    print(f"{BLUE}" + "=" * 60 + f"{RESET}")
    print("[i] Issue temporary passes")
    print("[b] Back to Parking Staff Menu")
    print(f"{BLUE}" + "-" * 60 + f"{RESET}")
    visitors_temporary_choice = input(f"{YELLOW}Enter your choice: {RESET}").strip().lower()

    if visitors_temporary_choice in ["i", "issue temporary passes"]:
        while True:
            print(f"{CYAN}----- Issue Temporary Passes -----{RESET}")
            permit_plate = input(f"{YELLOW}Enter permit plate number: {RESET}").strip().upper()

            print(f"\n{CYAN}Available Permit Types:{RESET}")
            for pt in permit_types:
                print(f"{pt[0]} - {pt[1]} : RM{pt[2]}")
            permitID = input(f"\n{YELLOW}Enter permit ID: {RESET}").strip().upper()

            valid_permit = get_record(permitID, permit_types)
            if not valid_permit:
                print(f"{RED}Invalid permitID input. Please try again.{RESET}")
                continue

            print(f"{CYAN}Enter permit expiry date:{RESET}")
            permit_expiry_date = get_valid_date()
            if permit_expiry_date == "q": return
            
            max_id = 0
            for p in permits:  
                if p[0].startswith('P'):
                    try:
                        current_id = int(p[0][1:])
                        if current_id > max_id:
                            max_id = current_id
                    except ValueError:
                        pass

            new_issue_id = f"P{max_id + 1:03d}"  
            permits.append([new_issue_id, permit_plate, permitID, permit_expiry_date])

            if save_to_file(permits, "permits.txt", permits_headers):
                print(f"{GREEN}Temporary permit issued for {permit_plate} is {new_issue_id}{RESET}")
            else:
                print(f"{RED}Error saving permit.{RESET}")
            break

    elif visitors_temporary_choice in ["b", "back to parking staff menu"]:
        print(f"{CYAN}Back to Parking Staff Menu.....{RESET}")
        return
    else:
        print(f"{RED}Invalid choice. Please try again.{RESET}")

def staff_daily_logs():  
    while True:
        print(f"\n{BLUE}" + "=" * 60 + f"{RESET}")
        print(f"{CYAN}   WELCOME LOG READER SYSTEM MENU   {RESET}")
        print(f"{BLUE}" + "=" * 60 + f"{RESET}")
        print("[a] Read Daily Logs")
        print("[b] Back to Parking Staff Menu")
        print(f"{BLUE}" + "-" * 60 + f"{RESET}")
        daily_log_choice = input(f"{YELLOW}Enter your choice: {RESET}")

        if daily_log_choice in ["a", "read daily logs"]:
            log_headers, logs = load_from_file("parking_logs.txt")

            print(f"\n{CYAN}--- Parking Daily Log Reader ---{RESET}")
            print(f"{CYAN}Enter date to view logs:{RESET}")
            target_date_input = get_valid_date()
            if target_date_input == "q": return

            print(f"\n{CYAN}Log report for {target_date_input}{RESET}")
            print(f"{BLUE}" + "-" * 50 + f"{RESET}")

            found_any = False
            for log in logs:
                if len(log) >= 7 and log[0] == target_date_input:
                    logID = log[1]
                    log_plate = log[2]
                    log_spaceID = log[3]
                    log_entry_time = log[4]
                    log_exit_time = log[5]
                    log_fee = log[6]
                    print(f"{logID}, {log_plate}, {log_spaceID}, "
                            f"{log_entry_time}, {log_exit_time}, RM{log_fee}")
                    found_any = True

            if not found_any:
                print(f"{RED}Sorry, no records found for {target_date_input}.{RESET}")
            print(f"{BLUE}" + "-" * 50 + f"{RESET}")

        elif daily_log_choice in ["b", "back to parking staff menu"]:
            print(f"{CYAN}Back to Parking Staff Menu.....{RESET}")
            return
        else:
            print(f"{RED}Error: Invalid choice. Please try again.{RESET}")

# END PARKING STAFF FUNCTIONS


# BEGIN SYSTEM ADMIN FUNCTIONS

def admin_menu():
    while True:
        print(f"\n{BLUE}" + "="*45 + f"{RESET}")
        print(f"{MAGENTA}   PARKING MANAGEMENT SYSTEM - ADMIN MENU   {RESET}")
        print(f"{BLUE}" + "="*45 + f"{RESET}")
        print("[e] Edit Parking Records (Add/Remove/Update)")
        print("[p] Edit Permit Pricing and Types")
        print("[r] Generate Revenue or Occupancy Reports")
        print("[v] View All Records and Violations")
        print("[b] Back to Main Menu")
        print(f"{BLUE}" + "-"*45 + f"{RESET}")
        
        admin_menu_options = ['e', 'p', 'r', 'v', 'b']
        admin_menu_option = ""

        while admin_menu_option not in admin_menu_options:
            admin_menu_option = input(f"{YELLOW}Enter selection: {RESET}").strip().lower()

            if admin_menu_option not in admin_menu_options:
                print(f"{RED}Invalid selection, please try again.{RESET}")

        if admin_menu_option == "b":
            break
        elif admin_menu_option == "e":                                  
            admin_edit_records_menu()
        elif admin_menu_option == "p":                                  
            admin_edit_permit_menu()
        elif admin_menu_option == "r":                                  
            admin_generate_records_menu()
        elif admin_menu_option == "v":                                  
            admin_view_records_menu()

def admin_edit_records_menu():                                  

    while True:
        parking_headers, parking_spaces = load_from_file("parking_spaces.txt")

        print(f"\n{BLUE}" + "=" * 40 + f"{RESET}")
        print(f"{MAGENTA}      EDIT PARKING RECORDS MENU      {RESET}")
        print(f"{BLUE}" + "=" * 40 + f"{RESET}")
        print("[a] Add New Parking Space")
        print("[r] Remove Existing Parking Space")
        print("[u] Update Space Information")
        print("[b] Back to System Admin Menu")
        print(f"{BLUE}" + "-" * 40 + f"{RESET}")
        
        current_line = ""
        for i in range(len(parking_spaces)):
            data = parking_spaces[i]
            current_line += f"{data[0]}({data[1]}) : {'[' + data[3] + ']' if data[3] else data[2]}".ljust(30)          

            if (i+1) % 5 == 0:
                print(current_line)
                current_line = ""
            elif i == len(parking_spaces)-1:
                print(current_line)
        
        edit_records_options = ['b', 'a', 'r', 'u']
        edit_records_option = ""

        while edit_records_option not in edit_records_options:
            edit_records_option = input(f"\n{YELLOW}Enter selection: {RESET}").strip().lower()

            if edit_records_option not in edit_records_options:
                print(f"{RED}Invalid selection, please try again.{RESET}")


        if edit_records_option == "b":                                      
            break

        elif edit_records_option == "a":                                    
            new_type = ""
            while new_type.capitalize() not in PARKING_SPACE_TYPES and new_type != "q":
                new_type = input(f"{YELLOW}What type of parking? [{'/'.join(PARKING_SPACE_TYPES)}] (q to cancel): {RESET}").strip()

            if new_type == "q":
                continue
            else:
                existing_ids = []
                for space in parking_spaces:
                    existing_ids.append(get_id_number(space, 0))

                new_id_num = 1                                                  
                while new_id_num in existing_ids:
                    new_id_num += 1

                new_id = f"S{new_id_num:02d}"

                parking_spaces.append([new_id, new_type.capitalize(), "Available", "", "", ""])
                parking_spaces.sort(key=lambda space:get_id_number(space, 0))

                if save_to_file(parking_spaces, "parking_spaces.txt", parking_headers):
                    continue
                else:
                    print(f"{RED}Error{RESET}") 

        elif edit_records_option == "r":                                    
            found = -1

            while found == -1:
                id_code, delete_id_number = enter_id("parking space")

                if delete_id_number is None:
                    continue
                elif delete_id_number == "q":
                    break
                else:
                    space = get_record(f"{id_code}{delete_id_number:02d}", parking_spaces)
                    if space:
                        if space[2] == "Occupied":
                            print(f"\n{RED}Parking space is occupied by {space[3]}. Please ask a Parking Staff to remove vehicle.{RESET}")
                        else:
                            confirm = -1                                                        
                                                                                                
                            while confirm not in ["y", "n"]:
                                confirm = input(f"\n{YELLOW}Delete parking space {space[0]} ({space[1]})? ({GREEN}y{YELLOW}/{RED}n{YELLOW}): {RESET}").lower()

                            if confirm == "y":
                                found = 1
                                parking_spaces.remove(space)
                                save_to_file(parking_spaces, "parking_spaces.txt", parking_headers)
                            found = 1
                    else:
                        print(f"{RED}Invalid ID, please try again.{RESET}")                  

        elif edit_records_option == "u":
            found = -1

            while found == -1:
                id_code, update_id_number = enter_id("parking space")

                if update_id_number is None:
                    continue
                elif update_id_number == "q":
                    break
                else:
                    space = get_record(f"{id_code}{update_id_number:02d}", parking_spaces)
                    if space:
                        update_id_number_index = parking_spaces.index(space)
                        confirm = -1

                        print(f"{RED}Manually altering spaces might cause inconsistencies or errors.{RESET}")
                        while confirm not in ["y", "n"]:
                            confirm = input(f"{YELLOW}Are you sure to proceed? ({GREEN}y{YELLOW}/{RED}n{YELLOW}): {RESET}").lower()
                            
                        if confirm == "n":
                            break
                    
                        correct_format = -1

                        while correct_format == -1:
                            new_parking_details = input(f'\n{YELLOW}Insert new details for parking space {space[0]} in the format of type/status/plate(blank if none), or q to cancel: {RESET}').strip()
                            
                            if new_parking_details == "q": 
                                break

                            new_parking_details = new_parking_details.split("/")

                            if len(new_parking_details) != 3:
                                print(f"{RED}Invalid format, please try again.{RESET}")
                                continue
                            elif new_parking_details[0].capitalize() not in PARKING_SPACE_TYPES:
                                print(f"{RED}Invalid parking type. Please choose from: {'/'.join(PARKING_SPACE_TYPES)}{RESET}")
                                continue
                            elif new_parking_details[1].capitalize() not in ["Available", "Occupied"]:
                                print(f"{RED}Invalid status. Please enter 'Available' or 'Occupied'.{RESET}")
                                continue
                            elif new_parking_details[1].capitalize() == "Occupied" and not new_parking_details[2]:
                                print(f"{RED}Invalid status. Please supply Plate if space is occupied.{RESET}")
                                continue
                            else:
                                correct_format = 1

                                new_type = new_parking_details[0].capitalize()
                                new_status = new_parking_details[1].capitalize()
                                new_plate = new_parking_details[2].upper()

                                if new_status == "Available" and new_plate != "":
                                    new_plate = ""
                                    new_time = ""
                                    new_date = ""
                                else:
                                    new_time = space[4] if len(space) >= 5 and space[4] else ""
                                    new_date = space[5] if len(space) >= 6 and space[5] else ""

                                parking_spaces[update_id_number_index] = [space[0], new_type, new_status, new_plate, new_time, new_date]
                                save_to_file(parking_spaces, "parking_spaces.txt", parking_headers)
                                
                                found = 1
                    else:
                        print(f"{RED}ID not found, please try again.{RESET}")

def admin_edit_permit_menu():

    while True:
        permit_types_headers, permit_types = load_from_file("permit_types.txt")
        
        print(f"\n{BLUE}" + "=" * 40 + f"{RESET}")
        print(f"{MAGENTA}      EDIT PERMIT TYPES MENU      {RESET}")
        print(f"{BLUE}" + "=" * 40 + f"{RESET}")
        print("[a] Add New Permit Type")
        print("[u] Update Permit Price/Availability")
        print("[b] Back to System Admin Menu")
        print(f"{BLUE}" + "-" * 40 + f"{RESET}")
        print(f"{CYAN}Available permit types{RESET}")
        for type in permit_types:
            print(f"{type[0]} - {type[1].ljust(7)} : RM{type[2]}")
        
        edit_permit_types_option = ""
        edit_permit_types_options = ['b', 'a', 'u']
        
        while edit_permit_types_option not in edit_permit_types_options:
            edit_permit_types_option = input(f"\n{YELLOW}Enter selection: {RESET}").strip().lower()

            if edit_permit_types_option not in edit_permit_types_options:
                print(f"{RED}Invalid selection, please try again.{RESET}")

        if edit_permit_types_option == "b":
            break

        elif edit_permit_types_option == "a":                                           
            new_permit_option = ""
            new_permit_price = -1

            while new_permit_option not in PERMIT_OPTIONS and new_permit_option != 'Q':
                new_permit_option = input(f"{YELLOW}Enter new permit type [Daily/Monthly/Annual] or q to cancel : {RESET}").capitalize()
            
            if new_permit_option == 'Q':
                continue

            while new_permit_price < 0:
                try:
                    new_permit_price = float(input(f"{YELLOW}Insert price of new permit : {RESET}"))
                    if new_permit_price < 0:
                        print(f"{RED}Price cannot be negative.{RESET}")
                except ValueError:
                    print(f"{RED}Invalid price, please try again.{RESET}")

            new_permit_category = new_permit_option[0]                                  

            existing_ids = []
            for p_type in permit_types:
                if p_type[0][0] == new_permit_category:
                    existing_ids.append(int(p_type[0][1:]))                             

            new_id_num = 1
            while new_id_num in existing_ids:
                new_id_num += 1

            new_permit_type_id = f"{new_permit_category}{new_id_num:02d}"                                               
            new_permit_type = [new_permit_type_id, new_permit_option.capitalize(), f"{new_permit_price:.2f}"]           
            permit_types.append(new_permit_type)
            
            permit_types.sort(key=permit_types_sort_key)
            save_to_file(permit_types, "permit_types.txt", permit_types_headers)

        elif edit_permit_types_option == "u":                                           
            found = -1

            while found == -1:
                id_code, update_id_number = enter_id("permit type")

                if update_id_number is None:
                    continue
                elif update_id_number == "q":
                    break
                else:
                    permit_to_update = get_record(f"{id_code}{update_id_number:02d}", permit_types)

                    if permit_to_update:
                        print(f"\n{CYAN}Current Details for {permit_to_update[0]}: {permit_to_update[1]} @ RM{permit_to_update[2]}{RESET}")

                        option = ""
                        while option not in ["p", "r", "q"]:
                            option = input(f"{YELLOW}Insert option : p to update price, r to remove permit type, q to cancel : {RESET}").strip().lower()

                        if option == 'q':
                            break
                        elif option == 'p':
                            update_index = permit_types.index(permit_to_update)

                            new_price = -1
                            while new_price < 0:
                                try:
                                    new_price = float(input(f"{YELLOW}Insert price of new permit : {RESET}"))
                                    if new_price < 0:
                                        print(f"{RED}Price cannot be negative.{RESET}")
                                except ValueError:
                                    print(f"{RED}Invalid price, please try again.{RESET}")

                            permit_types[update_index] = [permit_to_update[0], permit_to_update[1], f"{new_price:.2f}"]
                                
                            if save_to_file(permit_types, "permit_types.txt", permit_types_headers):
                                print(f"{GREEN}Success! {permit_to_update[0]} updated to RM{new_price:.2f}.{RESET}")
                                found = 1
                            else:
                                print(f"{RED}Error saving to file.{RESET}")

                        elif option == 'r':
                            confirm = ""
                            while confirm not in ["y", "n"]:
                                confirm = input(f"{YELLOW}Remove permit type {permit_to_update[0]} ({permit_to_update[1]})? ({GREEN}y{YELLOW}/{RED}n{YELLOW}): {RESET}").strip().lower()

                            if confirm == "y":
                                permit_types.remove(permit_to_update)
                                save_to_file(permit_types, "permit_types.txt", permit_types_headers)
                                found = 1
                            else:
                                print(f"{YELLOW}Removal cancelled.{RESET}")
                                break
                    else:
                        print(f"{RED}Invalid permit ID, please try again.{RESET}")

def admin_generate_records_menu():
    while True:
        parking_headers, parking_spaces = load_from_file("parking_spaces.txt")
        permit_types_headers, permit_types = load_from_file("permit_types.txt")
        permits_headers, permits = load_from_file("permits.txt")

        print(f"\n{BLUE}" + "=" * 40 + f"{RESET}")
        print(f"{MAGENTA}         GENERATE REPORTS MENU         {RESET}")
        print(f"{BLUE}" + "=" * 40 + f"{RESET}")
        print("[r] Generate Revenue Report")
        print("[o] Generate Occupancy Report")
        print("[b] Back to System Admin Menu")
        print(f"{BLUE}" + "-" * 40 + f"{RESET}")

        generate_report_option = ""
        generate_report_options = ['r', 'o', 'b']

        while generate_report_option not in generate_report_options:
            generate_report_option = input(f"{YELLOW}Enter selection: {RESET}").strip().lower()

            if generate_report_option not in generate_report_options:
                print(f"{RED}Invalid selection, please try again.{RESET}")

        if generate_report_option == "b":
            break

        print(f"{CYAN}Enter Report Date:{RESET}")
        report_date = get_valid_date()
        if report_date == 'q': continue

        print(f"{CYAN}Enter Report Time:{RESET}")
        report_time = get_valid_time()
        if report_time == 'q': continue

        if generate_report_option == "r":                                                   
            total_revenue = 0.0
            cat_totals = {"D": {"count": 0, "sum": 0.0}, "M": {"count": 0, "sum": 0.0}, "A": {"count": 0, "sum": 0.0}}
                
            id_stats = {}
            for p_type in permit_types:
                id_stats[p_type[0]] = {"type": p_type[1], "price": float(p_type[2]), "sold": 0, "subtotal": 0.0}        

            for p in permits:
                permit_id = p[2]
                if permit_id in id_stats:
                    price = id_stats[permit_id]["price"]                        
                    permit_category = permit_id[0]                              
                        
                    id_stats[permit_id]["sold"] += 1
                    id_stats[permit_id]["subtotal"] += price                    
                        
                    cat_totals[permit_category]["count"] += 1
                    cat_totals[permit_category]["sum"] += price                 
                    total_revenue += price

            with open("revenue.txt", "a") as report:
                report.write(f"\n============================================================\n")
                report.write(f"PARKING SYSTEM REVENUE REPORT\n")
                report.write(f"Generated on: {report_date} {report_time}\n")
                report.write(f"============================================================\n\n")
                report.write(f"--- OVERALL REVENUE SUMMARY ---\n")
                report.write(f"Total Revenue Generated: RM {total_revenue:,.2f}\n\n")
                report.write(f"--- REVENUE BY PERMIT CATEGORY ---\n")
                report.write(f"[D] Daily Permits    ({cat_totals['D']['count']:>2} Sold)    : RM {cat_totals['D']['sum']:>9,.2f}\n")
                report.write(f"[M] Monthly Permits  ({cat_totals['M']['count']:>2} Sold)    : RM {cat_totals['M']['sum']:>9,.2f}\n")
                report.write(f"[A] Annual Permits   ({cat_totals['A']['count']:>2} Sold)    : RM {cat_totals['A']['sum']:>9,.2f}\n\n")
                report.write(f"--- DETAILED PERMIT BREAKDOWN ---\n")
                report.write(f"Permit ID | Type    | Price (RM) | Sold | Subtotal (RM)\n")
                report.write(f"------------------------------------------------------------\n")
                for permit_id, data in id_stats.items():
                    report.write(f"{permit_id:<9} | {data['type']:<7} | {data['price']:>10,.2f} | {data['sold']:>4} | {data['subtotal']:>13,.2f}\n")
                report.write(f"============================================================")
                report.write(f"\n\n\n")
                    
            print(f"\n{GREEN}Revenue report generated and appended to revenue.txt successfully.{RESET}")

        elif generate_report_option == "o":                                                 
            total_spaces = len(parking_spaces)
            occupied_spaces = 0
                
            space_stats = {"Regular": [0, 0], "Reserved": [0, 0], "Electric": [0, 0]}       
                
            for space in parking_spaces:
                space_type = space[1].capitalize()
                space_status = space[2].capitalize()
                    
                if space_type in space_stats:                                               
                    space_stats[space_type][0] += 1
                    if space_status == "Occupied":
                        space_stats[space_type][1] += 1
                        occupied_spaces += 1

            available_spaces = total_spaces - occupied_spaces
            capacity_rate = (occupied_spaces / total_spaces * 100) if total_spaces > 0 else 0           

            active_permits = len(permits)
            permit_counts = {"D": 0, "M": 0, "A": 0}                                                   
            for p in permits:
                permit_counts[p[2][0]] += 1

            with open("occupancy.txt", "a") as report:
                report.write(f"\n============================================================\n")
                report.write(f"PARKING SYSTEM OCCUPANCY & USAGE REPORT\n")
                report.write(f"Generated on: {report_date} {report_time}\n")
                report.write(f"============================================================\n\n")
                report.write(f"--- OVERALL PARKING SPACE UTILIZATION ---\n")
                report.write(f"Total Parking Spaces : {total_spaces}\n")
                report.write(f"Occupied Spaces      : {occupied_spaces}\n")
                report.write(f"Available Spaces     :  {available_spaces}\n")
                report.write(f"Current Capacity     : {capacity_rate:.1f}%\n\n")
                    
                report.write(f"--- UTILIZATION BY SPACE TYPE ---\n")
                report.write(f"Type       | Total | Occupied | Available | Occupancy %\n")
                report.write(f"------------------------------------------------------------\n")
                for space_type, counts in space_stats.items():
                    t_count = counts[0]
                    o_count = counts[1]
                    a_count = t_count - o_count
                    percentage = (o_count / t_count * 100) if t_count > 0 else 0
                    report.write(f"{space_type:<10} | {t_count:>5} | {o_count:>8} | {a_count:>9} | {percentage:>10.1f}%\n")
                        
                report.write(f"\n--- ACTIVE PERMITS SUMMARY ---\n")
                report.write(f"Total Active Permits : {active_permits}\n")
                report.write(f"Daily Permits        :  {permit_counts['D']}\n")
                report.write(f"Monthly Permits      :  {permit_counts['M']}\n")
                report.write(f"Annual Permits       :  {permit_counts['A']}\n")
                report.write(f"============================================================")
                report.write(f"\n\n\n")
                    
            print(f"\n{GREEN}Occupancy report generated and appended to occupancy.txt successfully.{RESET}")

def admin_view_records_menu():
    while True:
        parking_headers, parking_spaces = load_from_file("parking_spaces.txt")
        permit_types_headers, permit_types = load_from_file("permit_types.txt")
        permits_headers, permits = load_from_file("permits.txt")
        violations_headers, violations = load_from_file("violations.txt")

        print(f"\n{BLUE}" + "=" * 40 + f"{RESET}")
        print(f"{MAGENTA}           VIEW RECORDS MENU           {RESET}")
        print(f"{BLUE}" + "=" * 40 + f"{RESET}")
        print("[ps] View All Parking Spaces")
        print("[pt] View All Permit Types")
        print("[p] View All Issued Permits")
        print("[v] View All Violations")
        print("[b] Back to System Admin Menu")
        print(f"{BLUE}" + "-" * 40 + f"{RESET}")
        
        view_options = ["ps", "pt", "p", "v", "b"]
        view_option = ""

        while view_option not in view_options:
            view_option = input(f"{YELLOW}Enter selection: {RESET}").strip().lower()

            if view_option not in view_options:
                print(f"{RED}Invalid selection, please try again.{RESET}")

        if view_option == "b":
            break
        
        elif view_option == "ps":                                    
            print(f"\n{BLUE}" + "=" * 65 + f"{RESET}")
            print(f"{MAGENTA}                  ALL PARKING SPACES                  {RESET}")
            print(f"{BLUE}" + "=" * 65 + f"{RESET}")
            print(f"{CYAN}{'ID':<5} | {'Type':<10} | {'Status':<10} | {'Plate':<10} | {'Time':<5} | {'Date'}{RESET}")
            print(f"{BLUE}" + "-" * 65 + f"{RESET}")
            
            for space in parking_spaces:
                plate = space[3] if len(space) > 3 else ""
                time = space[4] if len(space) > 4 else ""
                date = space[5] if len(space) > 5 else ""
                print(f"{space[0]:<5} | {space[1]:<10} | {space[2]:<10} | {plate:<10} | {time:<5} | {date}")
            
            print(f"{BLUE}" + "=" * 65 + f"{RESET}")
            input(f"{YELLOW}\nPress Enter to return...{RESET}")

        elif view_option == "pt":                                    
            print(f"\n{BLUE}" + "=" * 35 + f"{RESET}")
            print(f"{MAGENTA}         ALL PERMIT TYPES          {RESET}")
            print(f"{BLUE}" + "=" * 35 + f"{RESET}")
            print(f"{CYAN}{'ID':<5} | {'Type':<10} | {'Price'}{RESET}")
            print(f"{BLUE}" + "-" * 35 + f"{RESET}")
            
            for p_type in permit_types:
                print(f"{p_type[0]:<5} | {p_type[1]:<10} | RM {float(p_type[2]):>7.2f}")
            
            print(f"{BLUE}" + "=" * 35 + f"{RESET}")
            input(f"{YELLOW}\nPress Enter to return...{RESET}")

        elif view_option == "p":                                    
            print(f"\n{BLUE}" + "=" * 55 + f"{RESET}")
            print(f"{MAGENTA}                 ALL ISSUED PERMITS                {RESET}")
            print(f"{BLUE}" + "=" * 55 + f"{RESET}")
            
            if not permits:
                print(f"{RED}No issued permits found.{RESET}")
            else:
                print(f"{CYAN}{'Issue ID':<10} | {'Plate':<10} | {'Permit ID':<10} | {'Expiry Date'}{RESET}")
                print(f"{BLUE}" + "-" * 55 + f"{RESET}")
                
                for p in permits:
                    print(f"{p[0]:<10} | {p[1]:<10} | {p[2]:<10} | {p[3]}")
                    
            print(f"{BLUE}" + "=" * 55 + f"{RESET}")
            input(f"{YELLOW}\nPress Enter to return...{RESET}")

        elif view_option == "v":                                    
            print(f"\n{BLUE}" + "=" * 70 + f"{RESET}")
            print(f"{MAGENTA}                           ALL VIOLATIONS                           {RESET}")
            print(f"{BLUE}" + "=" * 70 + f"{RESET}")
            
            if not violations:
                print(f"{RED}No violations found.{RESET}")
            else:
                print(f"{CYAN}{'Violation ID':<12} | {'Plate':<10} | {'Date':<10} | {'Type':<15} | {'Status'}{RESET}")
                print(f"{BLUE}" + "-" * 70 + f"{RESET}")
                
                for v in violations:
                    print(f"{v[0]:<12} | {v[1]:<10} | {v[2]:<10} | {v[3]:<15} | {v[4]}")
                    
            print(f"{BLUE}" + "=" * 70 + f"{RESET}")
            input(f"{YELLOW}\nPress Enter to return...{RESET}")

# END SYSTEM ADMIN FUNCTIONS


# BEGIN VEHICLE OWNER FUNCTIONS

def owner_menu(): 
    while True:
        print(f"\n{BLUE}" + "="*45 + f"{RESET}")
        print(f"{GREEN}   PARKING RECORD SYSTEM - VEHICLE OWNER MENU   {RESET}")
        print(f"{BLUE}" + "="*45 + f"{RESET}")
        print("[r] Register Vehicle")
        print("[s] Permit Status")
        print("[p] Request Permit")
        print("[h] Parking History")
        print("[b] Back to Main Menu")
        print(f"{BLUE}" + "-"*45 + f"{RESET}")
        vehicle_menu_choice = input(f"{YELLOW}Enter your choice: {RESET}").lower().strip()
        if vehicle_menu_choice in ["r", "register vehicle"]:
            owner_register_vehicle()
        elif vehicle_menu_choice in ["s", "permit status"]:
            owner_permit_status()
        elif vehicle_menu_choice in ["p", "request permit"]:
            owner_request_permit()
        elif vehicle_menu_choice in ["h", "parking history"]:
            owner_parking_history()
        elif vehicle_menu_choice in ["b", "back to main menu"]:
            print(f"{GREEN}Back to Main Menu.....{RESET}")
            return
        else:
            print(f"{RED}Invalid selection.{RESET}")

def owner_register_vehicle():
    print(f"\n{BLUE}" + "="*45 + f"{RESET}")
    print(f"{GREEN}   VEHICLE REGISTRATION   {RESET}")
    print(f"{BLUE}" + "="*45 + f"{RESET}")
    plate = input(f"{YELLOW}Enter a plate number: {RESET}")
    model = input(f"{YELLOW}Enter car model: {RESET}")
    color = input(f"{YELLOW}Enter car color: {RESET}")

    if not plate or not model or not color:
        print(f"{RED}Error: All fields are required!{RESET}")
        return
    
    vehicle_headers, vehicles = load_from_file("vehicles.txt")

    count = 0
    for vehicle in vehicles:
        count += 1
        if len(vehicle) > 1 and vehicle[0] == plate:
            print(f"{RED}Error: This vehicle is already registered.{RESET}")
            return
            
    new_id = f"USR{100 + count + 1}"
    new_record = [plate,model,color,new_id]

    vehicles.append(new_record)
    if save_to_file(vehicles, "vehicles.txt", vehicle_headers):
        print(f"{GREEN}Vehicle registered succesfully!{RESET}")

def owner_permit_status():
    print(f"\n{BLUE}" + "="*45 + f"{RESET}")
    print(f"{GREEN}      VIEW PERMIT STATUS       {RESET}")
    print(f"{BLUE}" + "="*45 + f"{RESET}")
    user_plate = input(f"{YELLOW}Enter your plate number: {RESET}").strip().upper()    

    permits_headers, permits = load_from_file("permits.txt")

    permit_info = None
    for data in permits:
        if len(data) >= 4 and data[1] == user_plate:
            permit_info = data
            break
        
    if not permit_info:
        print(f"{RED}No active permit found for this plate.{RESET}")
        return 

    pt_headers, permit_types = load_from_file("permit_types.txt")
    p_type_name = "Unknown"
    
    type_data = get_record(permit_info[2], permit_types) 
    if type_data:
        p_type_name = type_data[1]

        privileges = "General Parking"
        if permit_info[2] == "D01": 
            privileges = "Regular"
        elif permit_info[2] == "M01": 
            privileges = "Regular"
        elif permit_info[2] == "M02": 
            privileges = "Electric or Reserved"
        elif permit_info[2] == "A01": 
            privileges = "Electric"
        elif permit_info[2] == "A02": 
            privileges = "Reserved"
        else:  
            privileges = "Electric or Reserved"

        print(f"{BLUE}" + "-" * 30 + f"{RESET}")
        print(f"Permit Type: {CYAN}{p_type_name} ({permit_info[2]}){RESET}")
        print(f"Expiration:  {CYAN}{permit_info[3]}{RESET}")
        print(f"Privileges:  {CYAN}{privileges}{RESET}")
        print(f"{BLUE}" + "-" * 30 + f"{RESET}")

def owner_request_permit():
    print(f"\n{BLUE}" + "="*45 + f"{RESET}")
    print(f"{GREEN}      REQUEST NEW PERMIT       {RESET}")
    print(f"{BLUE}" + "="*45 + f"{RESET}")
    user_plate = input(f"{YELLOW}Enter your plate number: {RESET}").strip().upper()
    if not user_plate:
        print(f"{RED}Error: Plate number cannot be empty{RESET}")
        return 
    
    expiry_date = get_valid_date()
        
    if expiry_date == "q":
        return

    print(f"{CYAN}Permit types : Daily(D01)")
    print("               Monthly(M01,M02)")
    print(f"               Annual(A01,A02,A03){RESET}")
    permit_type = input(f"{YELLOW}Enter permit type (e.g, DO1): {RESET}").strip().upper()
        
    permit_count = 0

    permits_headers, permits = load_from_file("permits.txt")
    for permit_data in permits:
        permit_count += 1
        if len(permit_data) > 1 and permit_data[1] == user_plate:
            print(f"{RED}Error: This permit is already registered.{RESET}")
            return
        
    new_permit_id = f"P{ permit_count + 1:03d}"
    new_permit_record = [new_permit_id,user_plate,permit_type,expiry_date]

    requests_headers, requests = load_from_file("permit_requests.txt")
    requests.append(new_permit_record)
    if save_to_file(requests, "permit_requests.txt", requests_headers):
        print(f"{GREEN}Permit submitted succesfully!{RESET}")

def owner_parking_history():
    print(f"\n{BLUE}" + "="*45 + f"{RESET}")
    print(f"{GREEN}         VIEW PARKING HISTORY          {RESET}")
    print(f"{BLUE}" + "="*45 + f"{RESET}")
    
    user_plate = input(f"{YELLOW}Enter your plate number: {RESET}").strip().upper()
    if not user_plate:
        print(f"{RED}Error: Plate number cannot be empty.{RESET}") 
        return
    
    log_headers, logs = load_from_file("parking_logs.txt")

    found = False
    print(f"\n{CYAN}Records for {user_plate}:{RESET}")
    print(f"{CYAN}{'Space ID':<10} | {'Entry Time':<20} | {'Exit Time':<20}{RESET}")
    print(f"{BLUE}" + "-" * 55 + f"{RESET}")
    
    for info in logs:
        if len(info) >= 4 and info[2] == user_plate:
            print(f"{info[3]:<10} | {info[4]:<20} | {info[5]:<20}")
            found = True
    
    if not found:
        print(f"{RED}No parking records found for this vehicle.{RESET}")

# END VEHICLE OWNER FUNCTIONS


# BEGIN PERMIT OFFICER FUNCTIONS

def officer_menu():
    while True:
        print(f"\n{BLUE}" + "=" * 50 + f"{RESET}")
        print(f"{CYAN}      PARKING SYSTEM - PERMIT OFFICER MENU      {RESET}")
        print(f"{BLUE}" + "=" * 50 + f"{RESET}")
        print("[i] Issue New Parking Permit")
        print("[v] View All Permit Status")
        print("[u] Update / Renew / Cancel Permit")
        print("[s] System Statistics & Reports")
        print("[b] Back to Main Menu")
        print(f"{BLUE}" + "-" * 50 + f"{RESET}")
        
        choice = input(f"{YELLOW}Enter your selection: {RESET}").lower().strip()
        
        if choice == 'i':
            officer_issue_new_permit()
        elif choice == 'v':
            officer_view_permit_status()
        elif choice == 'u':
            officer_manage_existing_records()
        elif choice == 's':
            officer_system_statistics()
        elif choice == 'b':
            print(f"{CYAN}Logging out Permit Officer...{RESET}")
            break
        else:
            print(f"{RED}>> Invalid input. Please select i, v, u, s, or b.{RESET}")

def officer_issue_new_permit():
    print(f"\n{BLUE}" + "=" * 50 + f"{RESET}")
    print(f"{CYAN}          [i] ISSUE NEW PARKING PERMIT          {RESET}")
    print(f"{BLUE}" + "=" * 50 + f"{RESET}")
    
    plate = input(f"{YELLOW}Enter Vehicle Plate: {RESET}").upper().strip()
    if not plate:
        print(f"{RED}>> Error: Plate number is required.{RESET}")
        return

    print(f"\n{CYAN}Available Types:{RESET}")
    print(f"{BLUE}" + "-" * 35 + f"{RESET}")
    print(f"{CYAN}{'ID':<8} | {'Category':<12} | {'Price'}{RESET}")
    print(f"{BLUE}" + "-" * 35 + f"{RESET}")

    pt_headers, permit_types = load_from_file("permit_types.txt")
    if not pt_headers:
        print(f"{RED}Critical Error: 'permit_types.txt' missing.{RESET}")
        return
    
    for p_type in permit_types:
        if len(p_type) >= 3:
            p_id = p_type[0]
            p_cat = p_type[1]
            p_price = p_type[2]
            print(f"{p_id:<8} | {p_cat:<12} | RM{p_price}")
    print(f"{BLUE}" + "-" * 35 + f"{RESET}")

    p_choice = input(f"{YELLOW}Select Permit ID: {RESET}").upper().strip()

    selected_type = get_record(p_choice, permit_types)
    if not selected_type:
        print(f"{RED}>> Error: Invalid Permit Type selected.{RESET}")
        return
    price = selected_type[2]

    print(f"{CYAN}Set Expiry Date:{RESET}")
    exp_date_str = get_valid_date()
    if exp_date_str == "q": 
        return
  
    print(f"\n{CYAN}Confirm Issuance for {plate}?{RESET}")
    print(f"{CYAN}Total Charge: RM{price}{RESET}")
    confirm = input(f"{YELLOW}Proceed? ({GREEN}y{YELLOW}/{RED}n{YELLOW}): {RESET}").lower()

    if confirm == 'y':
        p_headers, permits = load_from_file("permits.txt")
        if not permits:
            new_id = "P001"
        else:
            last_id = permits[-1][0]
            if last_id.startswith("P"):
                try:
                    next_num = int(last_id[1:]) + 1
                    new_id = f"P{next_num:03d}"
                except ValueError:
                    new_id = "P001"
            else:
                new_id = "P001"
        permits.append([new_id, plate, p_choice, exp_date_str])
        save_to_file(permits, "permits.txt", p_headers)
        
        print(f"\n{GREEN}>>> SUCCESS: Permit {new_id} is now ACTIVE.{RESET}")
    else:
        print(f"\n{YELLOW}>>> Transaction cancelled.{RESET}")
    
    input(f"\n{YELLOW}Press Enter to return...{RESET}")

def officer_view_permit_status():
    today = datetime.now().date()
    
    print(f"\n{BLUE}" + "=" * 80 + f"{RESET}")
    print(f"{CYAN}                PERMIT STATUS REPORT (TODAY: {today}){RESET}")
    print(f"{BLUE}" + "=" * 80 + f"{RESET}")
    print(f"{CYAN}{'Issue ID':<10} | {'Plate':<12} | {'Type':<8} | {'Expiry Date':<15} | {'Status'}{RESET}")
    print(f"{BLUE}" + "-" * 80 + f"{RESET}")

    p_headers, permits = load_from_file("permits.txt")

    if not permits:
        print(f"{RED}No permits found in database.{RESET}")

    else:
        for parts in permits:
            if len(parts) < 4:
                continue
                
            p_id, plate, p_type, exp_str = parts[0], parts[1], parts[2], parts[3]
            
            try:
                exp_date = datetime.strptime(exp_str, "%Y-%m-%d").date()
                if exp_date >= today:
                    status = f"{GREEN}ACTIVE{RESET}"
                else:
                    status = f"{RED}EXPIRED{RESET}"
            except ValueError:
                status = f"{RED}ERROR{RESET}"
                exp_str = "Invalid Format"

            print(f"{p_id:<10} | {plate:<12} | {p_type:<8} | {exp_str:<15} | {status}")

    print(f"{BLUE}" + "=" * 80 + f"{RESET}")
    input(f"\n{YELLOW}Press Enter to return...{RESET}")

def officer_manage_existing_records():
    print(f"\n{BLUE}" + "=" * 50 + f"{RESET}")
    print(f"{CYAN}          [u] UPDATE / RENEW / DELETE          {RESET}")
    print(f"{BLUE}" + "=" * 50 + f"{RESET}")
    target = input(f"{YELLOW}Enter Permit ID to modify: {RESET}").upper().strip()

    p_headers, permits = load_from_file("permits.txt")
    
    found_record = None
    found = False
    
    if not p_headers:
        return

    for p in permits:
        if p[0] == target:
            found_record = p
            found = True
            break

    if found == True:
        idx = permits.index(found_record)

        print(f"\n{CYAN}RECORD FOUND: {found_record[1]} (Type: {found_record[2]}){RESET}")
        print(f"{BLUE}" + "-" * 30 + f"{RESET}")
        print("[1] Renew Permit (New Expiry)")
        print("[2] Correct Plate Number")
        print("[3] Cancel (Delete) Permit")
        print("[4] Back")

        choice = input(f"\n{YELLOW}Action: {RESET}")

        if choice == '1':
            print(f"{CYAN}Enter New Expiry Date:{RESET}")
            new_date = get_valid_date()
            if new_date != "q":
                permits[idx][3] = new_date
                print(f"{GREEN}>> Record Renewed.{RESET}")
        elif choice == '2':
            permits[idx][1] = input(f"{YELLOW}Enter New Plate: {RESET}").upper().strip()
            print(f"{GREEN}>> Plate Updated.{RESET}")
        elif choice == '3':
            confirm = input(f"{YELLOW}Confirm Delete? ({GREEN}y{YELLOW}/{RED}n{YELLOW}): {RESET}").lower()
            if confirm == 'y':
                permits.remove(found_record)
                print(f"{GREEN}>> Permit {target} Deleted.{RESET}")
        else:
            print(f"{YELLOW}>> No changes applied.{RESET}")

        save_to_file(permits, "permits.txt", p_headers)
        
    else:
        print(f"{RED}>> Error: ID not found.{RESET}")
        
    input(f"\n{YELLOW}Press Enter to return...{RESET}")

def officer_system_statistics():
    print(f"\n{BLUE}" + "=" * 50 + f"{RESET}")
    print(f"{CYAN}          PERMIT SYSTEM ANALYTICS          {RESET}")
    print(f"{BLUE}" + "=" * 50 + f"{RESET}")
    
    active, expired, total = 0, 0, 0
    today = datetime.now().date()
    
    p_headers, permits = load_from_file("permits.txt")

    for parts in permits:
        if len(parts) >= 4:
            try:
                exp_date = datetime.strptime(parts[3], "%Y-%m-%d").date()
                if exp_date >= today: active += 1
                else: expired += 1
                total += 1
            except ValueError:
                continue 

    print(f"Total Permit Records: {CYAN}{total}{RESET}")
    print(f"Active Permits:      {GREEN}{active}{RESET}")
    print(f"Expired Permits:     {RED}{expired}{RESET}")
    if total > 0:
        rate = (active / total) * 100
        print(f"System Health Rate:  {CYAN}{rate:.1f}%{RESET}")
        
    print(f"{BLUE}" + "=" * 50 + f"{RESET}")
    input(f"\n{YELLOW}Press Enter to return...{RESET}")

# END PERMIT OFFICER FUNCTIONS


def main(): # main menu
    while True:
        print(f"\n{BLUE}" + "="*60 + f"{RESET}")
        print(f"{GREEN}   WELCOME TO PARKING LOT & PERMIT MANAGEMENT SYSTEM MENU   {RESET}")
        print(f"{BLUE}" + "="*60 + f"{RESET}")
        print(f"[a] System Administrator")
        print(f"[s] Parking Staff")
        print(f"[v] Vehicle Owner")
        print(f"[o] Permit Officer")
        print(f"[q] Quit the Program")
        print(f"{BLUE}" + "-"*60 + f"{RESET}")

        main_menu_choice = input(f"{YELLOW}Enter your choice: {RESET}").lower().strip()

        if main_menu_choice in ["a", "system administrator"]:
            admin_menu()

        elif main_menu_choice in ["s", "parking staff"]:
            staff_menu()

        elif main_menu_choice in ["v", "vehicle owner"]:
            owner_menu()

        elif main_menu_choice in ["o", "permit officer"]:
            officer_menu()

        elif main_menu_choice in ["q", "quit the program"]:
            print(f"{CYAN}Quitting the program.....{RESET}")
            break

        else :
            print(f"{RED}Invalid option, please try again.{RESET}")

if __name__ == "__main__":
    main()