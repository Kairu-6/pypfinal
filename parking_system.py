from datetime import datetime

# BEGIN UNIVERSAL HELPER FUNCTIONS

def get_valid_date():
    while True:
        date_str = input("Enter date (DD/MM/YYYY) or q to cancel : ").strip()
        
        if date_str.lower() == "q":
            return "q"
        
        date_str = date_str.replace("-", "/")
        
        try:
            valid_date_object = datetime.strptime(date_str, "%d/%m/%Y")
            standardized_date_str = valid_date_object.strftime("%Y-%m-%d")
            
            return standardized_date_str 
            
        except ValueError:
            print("Invalid date or format. Please use exactly DD/MM/YYYY.")

def load_from_file(file_name):
    headers = []
    data_list = []

    try:
        with open(file_name, "r") as file:
            line = file.readline()
            if not line:                                                # Prevents error if file is empty
                return headers, data_list
            headers = line.strip().split(",")

            for line in file:
                clean_line = line.strip()
                if clean_line:                                          # Prevents error from empty lines
                    entry = line.strip().split(",")
                    data_list.append(entry)
                
            return headers, data_list

    except IOError:
        print(f"[Error] Could not read file {file_name}.")
        return headers, data_list

def get_valid_time():
    while True:
        time_str = input("Enter time (HH:MM) or q to cancel : ").strip()
        if time_str.lower() == "q":
            return "q"
        
        parts = time_str.split(":")
        if len(parts) == 2 and len(parts[0]) == 2 and len(parts[1]) == 2:

            if parts[0].isdigit() and parts[1].isdigit():

                if 0 <= int(parts[0]) <= 23 and 0 <= int(parts[1]) <= 59:
                    return time_str
                else:
                    print("Error: Please insert valid 24-hour time (00:00 - 23:59).")
            else:
                print("Error: Hours and minutes must be numeric.")
        else:
            print("Invalid format. Please use exactly HH:MM (24-hour).")

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
        print(f"[Error] Could not write to file {file_name}. Please check permissions.")
        return False

def get_id_number(record, index_of_id):
    full_id = record[index_of_id]
    return int(full_id[1:])

def enter_id(id_name):
    try:
        id_str = input(f"Enter ID (e.g. S12) of {id_name}, or q to cancel : ").strip()

        if id_str.lower() == "q":
            return "q", "q"
        
        if not id_str[0].isalpha():
            print("Invalid format. ID must start with a letter (e.g., S12).")
            return None, None

        elif len(id_str) > 2 and id_str[1] == "0":                      # To prevent id number with leading zeros (e.g. 02) from being considered invalid (02 != 2)
            id_number_str = id_str[2:]
        else:
            id_number_str = id_str[1:]
        return id_str[0], int(id_number_str)
    
    except ValueError:
        print("Invalid ID, please try again.")
        return None, None

def permit_types_sort_key(permit):
    permit_priority = {"D": 1, "M": 2, "A": 3} 

    full_id = permit[0]
    category = full_id[0]
    id_num = get_id_number(permit, 0)
    priority = permit_priority.get(category, 4)
    
    return (priority, id_num)

# END UNIVERSAL HELPER FUNCTIONS


# BEGIN PARKING STAFF FUNCTIONS

def staff_menu():
    while True:
        print("\n" + "="*45)
        print("   PARKING RECORD SYSTEM - PARKING STAFF MENU   ")
        print("="*45)
        print("[p] Parking Availability")
        print("[r] Vehicle Record (Entry/Exit)")
        print("[v] Visitors Temporary Passes")
        print("[d] Daily Logs")
        print("[b] Back to Main Menu")
        print("-"*45)

        staff_menu_choice = input("Enter your choice: ").strip().lower()
        if staff_menu_choice in ["p", "parking availability"]:
            staff_parking_available()
        elif staff_menu_choice in ["r", "vehicle record"]:
            staff_vehicle_record_menu()
        elif staff_menu_choice in ["v", "visitors temporary passes"]:
            staff_visitors_temporary_passes()
        elif staff_menu_choice in ["d", "daily logs"]:
            staff_daily_logs()
        elif staff_menu_choice in ["b", "back to main menu"]:
            print("Returning to Main Menu...")
            return
        else:
            print("Invalid selection.")

def staff_parking_available():
    parking_headers, parking_spaces = load_from_file("parking_spaces.txt")

    while True:
        print("\n" + "=" * 45)
        print("   AVAILABLE PARKING CHECKING ")
        print("=" * 45)
        print("[r] Regular")
        print("[s] Reserved")
        print("[e] Electric")
        print("[b] Back to Parking Staff Menu")
        print("-" * 45)

        choice = input("Enter your choice: ").strip().lower()
        if choice in ["r", "regular"]:
            target_type = "regular"
        elif choice in ["s", "reserved"]:
            target_type = "reserved"
        elif choice in ["e", "electric"]:
            target_type = "electric"
        elif choice in ["b", "back to parking staff menu"]:
            print("Back to Parking Staff Menu.....")
            return
        else:
            print("Invalid selection.")
            continue

        found_any = False  # This tracks if we found at least one spot

        print(f"\nSearching for available {target_type} spots...")
        print(f"Parking space available:")

        for space in parking_spaces:

            parkingID = space[0]
            parking_type = space[1].lower()  # The 'type' from the file
            status = space[2].lower()  # The 'status' from the file

            # Check if the type matches what the user wants AND it is available
            if parking_type  == target_type and status == "available":
                print(f"{parkingID}")
                found_any = True
        # Only print the error if we finished the loop and found nothing
        if not found_any:
            print(f"Sorry, no {target_type} spots are available right now.")

def staff_vehicle_record_menu(): #entry and exit vehicle
    while True:
        print("\n" + "=" * 45)
        print("   PARKING RECORD SYSTEM - VEHICLE RECORD  ")
        print("=" * 45)
        print("[r] Record New Vehicle Entry")
        print("[u] Update Vehicle Exit")
        print("[b] Back to Parking Staff Menu")
        print("-" * 45)
        vehicle_record_menu_choice = input("Enter your choice: ").strip().lower()

        if vehicle_record_menu_choice in ["r", "record new vehicle entry"]:
            staff_vehicle_entry()
        elif vehicle_record_menu_choice in ["u", "update vehicle exit"]:
            staff_vehicle_exit()
        elif vehicle_record_menu_choice in ["b", "back to parking staff menu"]:
            print("Back to Parking Staff Menu.....")
            return
        else:
            print("Invalid selection.")

def staff_vehicle_entry():
    parking_headers, parking_spaces = load_from_file("parking_spaces.txt")

    print("\n--- Parking Spaces Entry System ---")
    print(f"SpaceID | Type")
    space_available = []

    for space in parking_spaces:
        if len(space) >= 3 and space[2].capitalize() == "Available":
            print(f"{space[0]} | {space[1]}")
            space_available.append(space[0])

    if not space_available:
        print("No parking spaces are currently available.")
        return

    while True:
        entry_parking_SpaceID = input("Enter SpaceID choice: ").strip().upper()         # Prompts for SpaceID to occupy
        if entry_parking_SpaceID in space_available:
            break
        else:
            print(space_available)
            print("Error: invalid SpaceID. Please choose available space (e.g., S01)")

    entry_parking_plate = input("Enter vehicle plate number: ")

    print("Enter vehicle entry time:")          # Gets validated entry time
    vehicle_entry_time = get_valid_time()
    if vehicle_entry_time == "q": return

    print("Enter vehicle entry date:")          # Gets validated entry date
    vehicle_entry_date = get_valid_date()
    if vehicle_entry_date == "q": return

    space = get_record(entry_parking_SpaceID, parking_spaces)
    idx = parking_spaces.index(space)
    parking_spaces[idx] = [space[0], space[1], "Occupied", entry_parking_plate, vehicle_entry_time, vehicle_entry_date]

    
    #Write back all spaces
    save_to_file(parking_spaces, "parking_spaces.txt", parking_headers)
    print(f"Successfully added {entry_parking_plate} to parking space {entry_parking_SpaceID}.")

def staff_vehicle_exit():
    parking_headers, parking_spaces = load_from_file("parking_spaces.txt")
    logs_headers, parking_logs = load_from_file("parking_logs.txt")

    print("\n--- Parking Spaces Exit System ---")

    while True:
        exit_parking_plate = input("Enter vehicle plate number to exit: ").strip().upper()

        vehicle_plate_found = False
        target_vehicle_data = {}

        for space in parking_spaces:
            if len(space) >= 6 and space[3] == exit_parking_plate:
                exit_parking_index = parking_spaces.index(space)
                vehicle_plate_found = True
                target_vehicle_data = {
                    'plate': space[3],  # Added this so the log can find it!
                    'spaceID': space[0],
                    'type': space[1],
                    'entry_time': space[4],
                    'entry_date': space[5],
                }

        if not vehicle_plate_found:
            print(f"Vehicle with plate {exit_parking_plate} not found.")
            continue

        # --- Time & Date Validation ---
        print("\n--- Time and Date of Exit ---")
        print("Enter vehicle exit time:")
        exit_time_str = get_valid_time()
        if exit_time_str == "q": return
        
        print("Enter vehicle exit date:")
        exit_date_str = get_valid_date()
        if exit_date_str == "q": return

        try:
            # Convert user input strings into one single datetime object
            end_dt = datetime.strptime(f"{exit_date_str} {exit_time_str}", "%Y-%m-%d %H:%M")

            # Convert stored file strings into one single datetime object
            start_dt = datetime.strptime(f"{target_vehicle_data['entry_date']} {target_vehicle_data['entry_time']}", "%Y-%m-%d %H:%M")

            if end_dt < start_dt:
                print("Error: Exit time cannot be before entry time!")
                continue
        except ValueError:
            print("Error: Invalid Format. Use HH:MM and DD/MM/YYYY.")
            continue

        # hours calculation
        difference = end_dt - start_dt
        total_hours = difference.total_seconds() / 3600
        total_hours = round(total_hours, 2)

        if total_hours < 0.25: #no need to pay if under 15 minutes
            rounded_fee = 0.00
        else:
            # Fee rate
            vehicle_type = target_vehicle_data['type'].lower()
            if vehicle_type == 'electric' : #electric RM5
                rate = 5.00
            elif vehicle_type == 'regular' : #regular RM2
                rate = 2.00
            else : #reserved RM3
                rate = 3.00
            total_fee = total_hours * rate
            rounded_fee = round(total_fee, 2)

        # Logging
        if parking_logs:
                max_id = 0
                for log in parking_logs:
                    current_id = get_id_number(log, 1)

                    if current_id > max_id:
                        max_id = current_id

                log_id = f"L{max_id + 1}"
        else:
            log_id = "L101"

        # Now actually write to file
        with open('parking_logs.txt', 'a') as log_file:
            log_entry = (
                f"{exit_date_str},{log_id},{target_vehicle_data['plate']},{target_vehicle_data['spaceID']},"
                f"{target_vehicle_data['entry_time']},{exit_time_str},{rounded_fee}\n")
            log_file.write(log_entry)

        parking_spaces[exit_parking_index] = [space[0], space[1], "Available", "", "", ""]
        save_to_file(parking_spaces, "parking_spaces.txt", parking_headers)

        print(f"Successfully removed {target_vehicle_data['plate']} from {target_vehicle_data['spaceID']}")
        print(f"Total fee is RM{rounded_fee} ")
        break

def staff_visitors_temporary_passes():
    permit_headers, permit_types = load_from_file("permit_types.txt")
    permits_headers, permits = load_from_file("permits.txt")

    print("\n" + "=" * 60)
    print("   WELCOME TO VISITOR TEMPORARY PASSES MENU   ")
    print("=" * 60)
    print("[i] Issue temporary passes")
    print("[b] Back to Parking Staff Menu")
    print("-" * 60)
    visitors_temporary_choice = input("Enter your choice: ").strip().lower()

    if visitors_temporary_choice in ["i", "issue temporary passes"]:
        while True:
            print("----- Issue Temporary Passes -----")
            permit_plate = input("Enter permit plate number: ").strip().upper()

            print("\nAvailable Permit Types:")
            for pt in permit_types:
                print(f"{pt[0]} - {pt[1]} : RM{pt[2]}")
            permitID = input("\nEnter permit ID: ").strip().upper()

            # Validate permitID properly
            valid_permit = get_record(permitID, permit_types)
            if not valid_permit:
                print("Invalid permitID input. Please try again.")
                continue

            # Validate date input
            print("Enter permit expiry date:")
            permit_expiry_date = get_valid_date()
            if permit_expiry_date == "q": return

            
            # Determine the next IssueID in P001 format
            max_id = 0
            for p in permits:  # skip header if exists
                if p[0].startswith('P'):
                    try:
                        current_id = int(p[0][1:])
                        if current_id > max_id:
                            max_id = current_id
                    except ValueError:
                        pass

            # Generate new IssueID
            new_issue_id = f"P{max_id + 1:03d}"  # format as P001, P002, etc.
            permits.append([new_issue_id, permit_plate, permitID, permit_expiry_date])

            # Write header if file is empty
            if save_to_file(permits, "permits.txt", permits_headers):
                print(f"Temporary permit issued for {permit_plate} is {new_issue_id}")
            else:
                print("Error saving permit.")

    elif visitors_temporary_choice in ["b", "back to parking staff menu"]:
        print("Back to Parking Staff Menu.....")
        return
    else:
        print("Invalid choice. Please try again.")

def staff_daily_logs():  # read daily logs
    while True:
        print("\n" + "=" * 60)
        print("   WELCOME LOG READER SYSTEM MENU   ")
        print("=" * 60)
        print("[a] Read Daily Logs")
        print("[b] Back to Parking Staff Menu")
        print("-" * 60)
        daily_log_choice = input("Enter your choice: ")

        if daily_log_choice in ["a", "read daily logs"]:
            log_headers, logs = load_from_file("parking_logs.txt")

            print("\n--- Parking Daily Log Reader ---")

            # Convert user input to date object
            print("Enter date to view logs:")
            target_date_input = get_valid_date()
            if target_date_input == "q": return

            print(f"\nLog report for {target_date_input}")
            print("-" * 50)

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
                print(f"Sorry, no records found for {target_date_input}.")
            print("-" * 50)

        elif daily_log_choice in ["b", "back to parking staff menu"]:
            print("Back to Parking Staff Menu.....")
            return
        else:
            print("Error: Invalid choice. Please try again.")

# END PARKING STAFF FUNCTIONS


# BEGIN SYSTEM ADMIN FUNCTIONS

def admin_menu():
    while True:
        print("\n" + "="*45)
        print("   PARKING MANAGEMENT SYSTEM - ADMIN MENU   ")
        print("="*45)
        print("[e] Edit Parking Records (Add/Remove/Update)")
        print("[p] Edit Permit Pricing and Types")
        print("[r] Generate Revenue or Occupancy Reports")
        print("[v] View All Records and Violations")
        print("[b] Back to Main Menu")
        print("-"*45)
        
        admin_menu_options = ['e', 'p', 'r', 'v', 'b']
        admin_menu_option = ""

        while admin_menu_option not in admin_menu_options:
            admin_menu_option = input("Enter selection: ").strip().lower()

            if admin_menu_option not in admin_menu_options:
                print("Invalid selection, please try again.")

        if admin_menu_option == "b":
            break

        elif admin_menu_option == "e":                                  # Edit Parking Records
            admin_edit_records_menu()

        elif admin_menu_option == "p":                                  # Edit Permit pricing and types
            admin_edit_permit_menu()

        elif admin_menu_option == "r":                                  # Generate Revenue or Occupancy Reports
            admin_generate_records_menu()

        elif admin_menu_option == "v":                                  # View All Records and Violations
            admin_view_records_menu()

def admin_edit_records_menu():                                  # Edit Parking Records
    parking_space_types = ["Regular", "Reserved", "Electric"]

    while True:
        parking_headers, parking_spaces = load_from_file("parking_spaces.txt")

        print("\n" + "=" * 40)
        print("      EDIT PARKING RECORDS MENU      ")
        print("=" * 40)
        print("[a] Add New Parking Space")
        print("[r] Remove Existing Parking Space")
        print("[u] Update Space Information")
        print("[b] Back to System Admin Menu")
        print("-" * 40)
        
        current_line = ""
        for i in range(len(parking_spaces)):
            data = parking_spaces[i]
            current_line += f"{data[0]}({data[1]}) : {'[' + data[3] + ']' if data[3] else data[2]}".ljust(30)           # Parse into readable format (shows plate if occupied, else "available")

            if (i+1) % 5 == 0:
                print(current_line)
                current_line = ""
            elif i == len(parking_spaces)-1:
                print(current_line)
        
        edit_records_options = ['b', 'a', 'r', 'u']
        edit_records_option = ""

        while edit_records_option not in edit_records_options:
            edit_records_option = input("\nEnter selection: ").strip().lower()

            if edit_records_option not in edit_records_options:
                print("Invalid selection, please try again.")


        if edit_records_option == "b":                                      # Back To Main Menu
            break


        elif edit_records_option == "a":                                    # Add New Parking Space
            new_type = ""
            while new_type.capitalize() not in parking_space_types and new_type != "q":
                new_type = input(f"What type of parking? [{'/'.join(parking_space_types)}] (q to cancel): ").strip()

            if new_type == "q":
                continue
            else:
                existing_ids = []
                for space in parking_spaces:
                    existing_ids.append(get_id_number(space, 0))

                new_id_num = 1                                                  # Look for least non-existing id
                while new_id_num in existing_ids:
                    new_id_num += 1

                new_id = f"S{new_id_num:02d}"

                parking_spaces.append([new_id, new_type.capitalize(), "Available", "", "", ""])
                parking_spaces.sort(key=lambda space:get_id_number(space, 0))

                if save_to_file(parking_spaces, "parking_spaces.txt", parking_headers):
                    continue
                else:
                    print("error")

        elif edit_records_option == "r":                                    # Remove Existing Parking Space
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
                            print(f"\nParking space is occupied by {space[3]}. Please ask a Parking Staff to remove vehicle.")

                        else:
                            confirm = -1                                        # Confirmation to delete space
                                                                                    
                            while confirm not in ["y", "n"]:
                                confirm = input(f"\nDelete parking space {space[0]} ({space[1]})? y/n : ")

                            if confirm == "y":
                                found = 1
                                parking_spaces.remove(space)

                                save_to_file(parking_spaces, "parking_spaces.txt", parking_headers)
                            found = 1
                    else:
                        print("Invalid ID, please try again.")                  # Id was not found in the list

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

                        print("Manually altering spaces might cause inconsistencies or errors.")
                        while confirm not in ["y", "n"]:
                            confirm = input("Are you sure to proceed? (y/n) ")
                            
                        if confirm == "n":
                            break
                    
                        correct_format = -1

                        while correct_format == -1:
                            new_parking_details = input(f'\nInsert new details for parking space {space[0]} in the format of type/status/plate(blank if none), or q to cancel: ')
                            
                            if new_parking_details == "q": 
                                break

                            new_parking_details = new_parking_details.split("/")

                            if len(new_parking_details) != 3:
                                print("Invalid format, please try again.")
                                continue

                            elif new_parking_details[0].capitalize() not in parking_space_types:
                                print(f"Invalid parking type. Please choose from: {'/'.join(parking_space_types)}")
                                continue

                            elif new_parking_details[1].capitalize() not in ["Available", "Occupied"]:
                                print("Invalid status. Please enter 'Available' or 'Occupied'.")
                                continue

                            elif new_parking_details[1].capitalize() == "Occupied" and not new_parking_details[2]:
                                print("Invalid status. Please supply Plate if space is occupied.")
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
                                    new_time = space[4] if len(space) >= 5 and space[4] else "N/A"
                                    new_date = space[5] if len(space) >= 6 and space[5] else "N/A"

                                parking_spaces[update_id_number_index] = [space[0], new_type, new_status, new_plate, new_time, new_date]
                                save_to_file(parking_spaces, "parking_spaces.txt", parking_headers)
                                
                                found = 1
                    else:
                        print("ID not found, please try again.")

def admin_edit_permit_menu():
    permit_options = ["Daily", "Monthly", "Annual"]

    while True:
        permit_types_headers, permit_types = load_from_file("permit_types.txt")
        
        print("\n" + "=" * 40)
        print("      EDIT PERMIT TYPES MENU      ")
        print("=" * 40)
        print("[a] Add New Permit Type")
        print("[u] Update Permit Price/Availability")
        print("[b] Back to System Admin Menu")
        print("-" * 40)
        print("Available permit types")
        for type in permit_types:
            print(f"{type[0]} - {type[1].ljust(7)} : RM{type[2]}")
        
        edit_permit_types_option = ""
        edit_permit_types_options = ['b', 'a', 'u']
        
        while edit_permit_types_option not in edit_permit_types_options:
            edit_permit_types_option = input("\nEnter selection: ").strip().lower()

            if edit_permit_types_option not in edit_permit_types_options:
                print("Invalid selection, please try again.")

        if edit_permit_types_option == "b":
            break

        elif edit_permit_types_option == "a":                                           # Add new permit type
            new_permit_option = ""
            new_permit_price = -1

            while new_permit_option not in permit_options and new_permit_option != 'Q':
                new_permit_option = input("Enter new permit type [Daily/Monthly/Annual] or q to cancel : ").capitalize()
            
            if new_permit_option == 'Q':
                continue

            while new_permit_price < 0:
                try:
                    new_permit_price = float(input("Insert price of new permit : "))
                    if new_permit_price < 0:
                        print("Price cannot be negative.")
                except ValueError:
                    print("Invalid price, please try again.")

            new_permit_category = new_permit_option[0]                                  # First letter of option (D/M/A)

            existing_ids = []
            for p_type in permit_types:
                if p_type[0][0] == new_permit_category:
                    existing_ids.append(int(p_type[0][1:]))                             # Extract number id from already available permits in the same category

            new_id_num = 1
            while new_id_num in existing_ids:
                new_id_num += 1

            new_permit_type_id = f"{new_permit_category}{new_id_num:02d}"                                               # Combines letter (D/M/A) with id number (e.g. 12) to form a new unique id (D01)
            new_permit_type = [new_permit_type_id, new_permit_option.capitalize(), f"{new_permit_price:.2f}"]           # Puts together id, permit type, and price in a list
            permit_types.append(new_permit_type)
            
            permit_types.sort(key=permit_types_sort_key)
            save_to_file(permit_types, "permit_types.txt", permit_types_headers)

        elif edit_permit_types_option == "u":                                           # Update permit price/availability
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
                        print(f"\nCurrent Details for {permit_to_update[0]}: {permit_to_update[1]} @ RM{permit_to_update[2]}")

                        option = ""
                        while option not in ["p", "r", "q"]:
                            option = input("Insert option : p to update price, r to remove permit type, q to cancel : ").strip().lower()

                        if option == 'q':
                            break

                        elif option == 'p':
                            update_index = permit_types.index(permit_to_update)

                            new_price = -1
                            while new_price < 0:
                                try:
                                    new_price = float(input("Insert price of new permit : "))
                                    if new_price < 0:
                                        print("Price cannot be negative.")
                                except ValueError:
                                    print("Invalid price, please try again.")

                            permit_types[update_index] = [permit_to_update[0], permit_to_update[1], f"{new_price:.2f}"]
                                
                            if save_to_file(permit_types, "permit_types.txt", permit_types_headers):
                                print(f"Success! {permit_to_update[0]} updated to RM{new_price:.2f}.")
                                found = 1
                            else:
                                print("Error saving to file.")

                        elif option == 'r':
                            confirm = ""
                            while confirm not in ["y", "n"]:
                                confirm = input(f"Remove permit type {permit_to_update[0]} ({permit_to_update[1]})? y/n : ").strip().lower()

                            if confirm == "y":
                                permit_types.remove(permit_to_update)
                                
                                save_to_file(permit_types, "permit_types.txt", permit_types_headers)
                                found = 1
                            else:
                                print("Removal cancelled.")
                                break

                    else:
                        print("invalid permit ID, please try again")

def admin_generate_records_menu():
    while True:
        parking_headers, parking_spaces = load_from_file("parking_spaces.txt")
        permit_types_headers, permit_types = load_from_file("permit_types.txt")
        permits_headers, permits = load_from_file("permits.txt")

        print("\n" + "=" * 40)
        print("         GENERATE REPORTS MENU         ")
        print("=" * 40)
        print("[r] Generate Revenue Report")
        print("[o] Generate Occupancy Report")
        print("[b] Back to System Admin Menu")
        print("-" * 40)

        generate_report_option = ""
        generate_report_options = ['r', 'o', 'b']

        while generate_report_option not in generate_report_options:
            generate_report_option = input("Enter selection: ").strip().lower()

            if generate_report_option not in generate_report_options:
                print("Invalid selection, please try again.")

        if generate_report_option == "b":
            break

        report_date = get_valid_date()
        if report_date == 'q':
            continue

        report_time = get_valid_time()
        if report_time == 'q':
            continue

        if generate_report_option == "r":                                                   # Generate revenue report
        
            total_revenue = 0.0
            cat_totals = {"D": {"count": 0, "sum": 0.0}, "M": {"count": 0, "sum": 0.0}, "A": {"count": 0, "sum": 0.0}}
                
            id_stats = {}
            for p_type in permit_types:
                id_stats[p_type[0]] = {"type": p_type[1], "price": float(p_type[2]), "sold": 0, "subtotal": 0.0}        # Sets up dict for every permit type

            for p in permits:
                permit_id = p[2]

                if permit_id in id_stats:
                    price = id_stats[permit_id]["price"]                        # Gets corresponding price based on ID
                    permit_category = permit_id[0]                              # Extracts category from ID (D/M/A)
                        
                    id_stats[permit_id]["sold"] += 1
                    id_stats[permit_id]["subtotal"] += price                    # Adds to total count and price of each permit type
                        
                    cat_totals[permit_category]["count"] += 1
                    cat_totals[permit_category]["sum"] += price                 # Adds to total count and price of each category
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
                    
            print("\nRevenue report generated and appended to revenue.txt successfully.")

        elif generate_report_option == "o":                                                 # Generate occupancy report
            total_spaces = len(parking_spaces)
            occupied_spaces = 0
                
            space_stats = {"Regular": [0, 0], "Reserved": [0, 0], "Electric": [0, 0]}       # Format: [total, occupied]
                
            for space in parking_spaces:
                space_type = space[1].capitalize()
                space_status = space[2].capitalize()
                    
                if space_type in space_stats:                                               # Calculates total count and occupied spaces according to space type
                    space_stats[space_type][0] += 1
                    if space_status == "Occupied":
                        space_stats[space_type][1] += 1
                        occupied_spaces += 1

            available_spaces = total_spaces - occupied_spaces
            capacity_rate = (occupied_spaces / total_spaces * 100) if total_spaces > 0 else 0           # Percentage of occupied spaces

            active_permits = len(permits)
            permit_counts = {"D": 0, "M": 0, "A": 0}                                                         # Active permits by category
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
                    
            print("\nOccupancy report generated and appended to occupancy.txt successfully.")

def admin_view_records_menu():
    while True:
        parking_headers, parking_spaces = load_from_file("parking_spaces.txt")
        permit_types_headers, permit_types = load_from_file("permit_types.txt")
        permits_headers, permits = load_from_file("permits.txt")
        violations_headers, violations = load_from_file("violations.txt")

        print("\n" + "=" * 40)
        print("           VIEW RECORDS MENU           ")
        print("=" * 40)
        print("[ps] View All Parking Spaces")
        print("[pt] View All Permit Types")
        print("[p] View All Issued Permits")
        print("[v] View All Violations")
        print("[b] Back to System Admin Menu")
        print("-" * 40)
        
        view_options = ["ps", "pt", "p", "v", "b"]
        view_option = ""

        while view_option not in view_options:
            view_option = input("Enter selection: ").strip().lower()

            if view_option not in view_options:
                print("Invalid selection, please try again.")

        if view_option == "b":
            break
        
        elif view_option == "ps":                                    # View Parking Spaces
            print("\n" + "=" * 65)
            print("                  ALL PARKING SPACES                  ")
            print("=" * 65)
            print(f"{'ID':<5} | {'Type':<10} | {'Status':<10} | {'Plate':<10} | {'Time':<5} | {'Date'}")
            print("-" * 65)
            
            for space in parking_spaces:
                plate = space[3] if len(space) > 3 else ""
                time = space[4] if len(space) > 4 else ""
                date = space[5] if len(space) > 5 else ""
                print(f"{space[0]:<5} | {space[1]:<10} | {space[2]:<10} | {plate:<10} | {time:<5} | {date}")
            
            print("=" * 65)
            input("\nPress Enter to return...")

        elif view_option == "pt":                                    # View Permit Types
            print("\n" + "=" * 35)
            print("          ALL PERMIT TYPES         ")
            print("=" * 35)
            print(f"{'ID':<5} | {'Type':<10} | {'Price'}")
            print("-" * 35)
            
            for p_type in permit_types:
                print(f"{p_type[0]:<5} | {p_type[1]:<10} | RM {float(p_type[2]):>7.2f}")
            
            print("=" * 35)
            input("\nPress Enter to return...")

        elif view_option == "p":                                    # View Issued Permits
            print("\n" + "=" * 55)
            print("                 ALL ISSUED PERMITS                ")
            print("=" * 55)
            
            if not permits:
                print("No issued permits found.")
            else:
                print(f"{'Issue ID':<10} | {'Plate':<10} | {'Permit ID':<10} | {'Expiry Date'}")
                print("-" * 55)
                
                for p in permits:
                    print(f"{p[0]:<10} | {p[1]:<10} | {p[2]:<10} | {p[3]}")
                    
            print("=" * 55)
            input("\nPress Enter to return...")

        elif view_option == "v":                                    # View Violations
            print("\n" + "=" * 70)
            print("                           ALL VIOLATIONS                           ")
            print("=" * 70)
            
            if not violations:
                print("No violations found.")
            else:
                print(f"{'Violation ID':<12} | {'Plate':<10} | {'Date':<10} | {'Type':<15} | {'Status'}")
                print("-" * 70)
                
                for v in violations:
                    print(f"{v[0]:<12} | {v[1]:<10} | {v[2]:<10} | {v[3]:<15} | {v[4]}")
                    
            print("=" * 70)
            input("\nPress Enter to return...")

# END SYSTEM ADMIN FUNCTIONS


def main(): # main menu
    while True:
        print("\n" + "="*60)
        print("   WELCOME TO PARKING LOT & PERMIT MANAGEMENT SYSTEM MENU   ")
        print("="*60)
        print("[a] System Administrator")
        print("[s] Parking Staff")
        print("[v] Vehicle Owner")
        print("[o] Permit Officer")
        print("[q] Quit the Program")
        print("-"*60)

        main_menu_choice = input("Enter your choice: ")

        if main_menu_choice.lower() in ["a", "system administrator"]:
            admin_menu()

        elif main_menu_choice.lower() in ["s", "parking staff"]:
            staff_menu()
            
        else :
            print("Quiting the program.....")
            break

if __name__ == "__main__":
    main()