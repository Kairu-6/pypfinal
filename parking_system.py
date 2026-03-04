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
        if main_menu_choice.lower() == "s" or main_menu_choice.lower() == "parking staff":
            staff_menu()
        else :
            print("Quiting the program.....")
            break

if __name__ == "__main__":
    main()