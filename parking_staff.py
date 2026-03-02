from datetime import datetime

def main_menu(): # main menu
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

def staff_menu(): #staff main menu
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
        staff_menu_choice = input("Enter your choice: ")
        if staff_menu_choice.lower() == "p" or staff_menu_choice.lower() == "parking availability":
            parking_available()
        elif staff_menu_choice.lower() == "r" or staff_menu_choice.lower() == "vehicle record":
            vehicle_record_menu()
        elif staff_menu_choice.lower() == "v" or staff_menu_choice.lower() == "visitors temporary passes":
            visitors_temporary_passes()
        elif staff_menu_choice.lower() == "d" or staff_menu_choice.lower() == "daily logs":
            daily_logs()
        elif staff_menu_choice.lower() == "b" or staff_menu_choice.lower() == "back to main menu":
            print("Back to Main Menu.....")
            return
        else :
            print("Invalid selection.")

def parking_available():
    try:
        while True:
            with open('parking_spaces.txt', 'r') as file:
                print("\n" + "=" * 45)
                print("   AVAILABLE PARKING CHECKING ")
                print("=" * 45)
                print("[r] Regular")
                print("[s] Reserved")
                print("[e] Electric")
                print("[b] Back to Parking Staff Menu")
                print("-" * 45)
                choice = input("Enter your choice: ").lower()
                if choice == "r" or choice == "regular":
                    target_type = "regular"
                elif choice == "s" or choice == "reserved":
                    target_type = "reserved"
                elif choice == "e" or choice == "electric":
                    target_type = "electric"
                elif choice == "b" or choice == "back to parking staff menu":
                    print("Back to Parking Staff Menu.....")
                    break
                else:
                    print("Invalid selection.")
                    continue

                found_any = False  # This tracks if we found at least one spot

                print(f"\nSearching for {target_type} spots...")
                print(f"Parking space available:")

                for line in file:
                    parting = [p.strip() for p in line.strip().split(',')]
                    if len(parting) < 3:
                        continue

                    parkingID = parting[0]
                    parking_type = parting[1].lower()  # The 'type' from the file
                    status = parting[2].lower()  # The 'status' from the file

                    # Check if the type matches what the user wants AND it is available
                    if parking_type  == target_type and status == "available":
                        print(f"{parkingID}")
                        found_any = True
                # Only print the error if we finished the loop and found nothing
                if not found_any:
                    print(f"Sorry, no {target_type} spots are available right now.")
    except FileNotFoundError:
        print("Error: 'parking_spaces.txt' not found.")

def vehicle_record_menu(): #entry and exit vehicle
    while True:
        print("\n" + "=" * 45)
        print("   PARKING RECORD SYSTEM - VEHICLE RECORD  ")
        print("=" * 45)
        print("[r] Record New Vehicle Entry")
        print("[u] Update Vehicle Exit")
        print("[b] Back to Parking Staff Menu")
        print("-" * 45)
        vehicle_record_menu_choice = input("Enter your choice: ")
        if vehicle_record_menu_choice == "r" or vehicle_record_menu_choice.lower() == "record new vehicle entry":
            vehicle_entry()
        elif vehicle_record_menu_choice == "u" or vehicle_record_menu_choice.lower() == "update vehicle exit":
            vehicle_exit()
        elif vehicle_record_menu_choice == "b" or vehicle_record_menu_choice.lower() == "back to parking staff menu":
            print("Back to Parking Staff Menu.....")
            return
        else:
            print("Invalid selection.")

def vehicle_entry():
    try:
        with open('parking_spaces.txt', 'r') as file: #read available parking slot
            header = file.readline()
            print("--- Parking Spaces Entry System ---")
            print(f"SpaceID | Type")
            spaces = []
            space_available = []
            for line in file:
                parts = [p.strip() for p in line.strip().split(',')]
                # Ensure the list has enough slots to prevent index errors
                if len(parts) < 3:
                    continue

                spaceID = parts[0]
                space_type = parts[1]
                status = parts[2]
                spaces.append([spaceID, space_type, status, *parts[3:]])
                if status.lower() == "available":
                    print(f"{spaceID} | {space_type}")
                    space_available.append(spaceID)
                # user input
            while True:
                entry_parking_SpaceID = input("Enter SpaceID choice: ")
                if entry_parking_SpaceID in space_available:
                    break
                else:
                    print (space_available)
                    print("Error: invalid SpaceID. Please choose available space (e.g., S01)")
        entry_parking_plate = input("Enter vehicle plate number: ")
        while True:
            vehicle_entry_time = input("Enter vehicle entry time (HH:MM): ")
            if ":" in vehicle_entry_time:
                parts = vehicle_entry_time.split(":")
                if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                    hour, minute = int(parts[0]), int(parts[1])
                    if 0 <= hour < 24 and 0 <= minute < 60:
                        # Valid input
                        break  # exit the loop
                    else:
                        print("Error: Please insert valid 24-hour time (00:00 - 23:59).")
                else:
                    print("Error: Hours and minutes must be numeric.")
            else:
                print("Error: Wrong time format. Please use HH:MM (e.g., 14:30).")
        while True:
            from datetime import datetime
            vehicle_entry_date = input("Enter vehicle entry date (DD/MM/YYYY): ")
            if "/" in vehicle_entry_date:
                break
            else :
                print("Error: Wrong date format. Please use DD/MM/YYYY (e.g., 12/12/2026).")
        #doublechecking
        updated = False
        for i, space in enumerate(spaces):
            if space[0] == entry_parking_SpaceID:
                if space[2] == "Available":
                    space[2] = "Occupied"
                    # Ensure the list has enough slots to prevent index errors
                    while len(space) < 6:
                        space.append("")

                    #Assign values to specific indices
                    space[3] = entry_parking_plate
                    space[4] = vehicle_entry_time
                    space[5] = vehicle_entry_date

                    updated = True
                else:
                    print("Error: That space is already occupied.")
                    return
        if updated:
            #Write back all spaces
            with open("parking_spaces.txt", "w") as f:
                f.write(header)
                for space in spaces:
                    f.write(", ".join(space) + "\n")
            print(f"Successfully added {entry_parking_plate} to parking space {entry_parking_SpaceID}.")
            return
    except FileNotFoundError:
        print("Error: 'parking_spaces.txt' not found.")

def vehicle_exit():
    print("\n--- Parking Spaces Exit System ---")

    while True:
        exit_parking_plate = input("Enter vehicle plate number: ").strip().upper()

        try:
            with open('parking_spaces.txt', 'r') as file:
                lines = file.readlines()
        except FileNotFoundError:
            print("Error: parking_spaces.txt not found.")
            return

        vehicle_plate_found = False
        updated_lines = []
        target_vehicle_data = {}

        for line in lines:
            parts = [p.strip() for p in line.split(',')]
            if len(parts) >= 6 and parts[3] == exit_parking_plate:
                vehicle_plate_found = True
                target_vehicle_data = {
                    'plate': parts[3],  # Added this so the log can find it!
                    'spaceID': parts[0],
                    'type': parts[1],
                    'entry_time': parts[4],
                    'entry_date': parts[5],
                }
                updated_lines.append(f"{parts[0]}, {parts[1]}, Available, \n")
            else:
                updated_lines.append(line)

        if not vehicle_plate_found:
            print(f"Vehicle with plate {exit_parking_plate} not found.")
            continue

        # --- Time & Date Validation ---
        while True:
            try:
                exit_time_str = input("Enter vehicle exit time (HH:MM): ")
                exit_date_str = input("Enter vehicle exit date (DD/MM/YYYY): ")

                # Convert user input strings into one single datetime object
                end_dt = datetime.strptime(f"{exit_date_str} {exit_time_str}", "%d/%m/%Y %H:%M")

                # Convert stored file strings into one single datetime object
                start_dt = datetime.strptime(f"{target_vehicle_data['entry_date']} {target_vehicle_data['entry_time']}",
                                             "%d/%m/%Y %H:%M")

                if end_dt < start_dt:
                    print("Error: Exit time cannot be before entry time!")
                    continue
                break
            except ValueError:
                print("Error: Invalid Format. Use HH:MM and DD/MM/YYYY.")

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
            total_fee = (total_hours * rate)
            rounded_fee = round (total_fee, 2)

        # --- Logging ---
        try:
            with open('parking_logs.txt', 'r') as log_file:
                log_lines = [line.strip() for line in log_file if line.strip()]

                max_id = 0
                for line in log_lines[1:]:  # skip header
                    parts = [p.strip() for p in line.split(',')]
                    if len(parts) > 1 and parts[1].startswith('L'):
                        try:
                            current_id = int(parts[1][1:])
                            if current_id > max_id:
                                max_id = current_id
                        except ValueError:
                            continue

                log_id = f"L{max_id + 1}"

        except FileNotFoundError:
            log_id = "L101"

        # Now actually write to file
        with open('parking_logs.txt', 'a') as log_file:
            log_entry = (
                f"{exit_date_str},{log_id},{target_vehicle_data['plate']},{target_vehicle_data['spaceID']},"
                f"{target_vehicle_data['entry_time']},{exit_time_str},{rounded_fee}\n")
            log_file.write(log_entry)

        with open('parking_spaces.txt', 'w') as file:
            file.writelines(updated_lines)

        print(f"Successfully remove {target_vehicle_data['plate']} from {target_vehicle_data['spaceID']}")
        print(f"Total fee is RM{rounded_fee} ")
        break

def visitors_temporary_passes():
    try:
        while True:
            print("\n" + "=" * 60)
            print("   WELCOME TO VISITOR TEMPORARY PASSES MENU   ")
            print("=" * 60)
            print("[i] Issue temporary passes")
            print("[b] Back to Parking Staff Menu")
            print("-" * 60)
            visitors_temporary_choice = input("Enter your choice: ")
            if visitors_temporary_choice == "i" or visitors_temporary_choice.lower() == "issue temporary passes":
                while True:
                    print("----- Issue Temporary Passes -----")
                    permit_plate = input("Enter permit plate number: ").strip()
                    permitID = input("Enter permit ID: ").strip()

                    # Validate permitID properly
                    if permitID not in {'D01','A01','A02','A03','M01','M02'}:
                        print("Invalid permitID input. Please try again.")
                        continue

                    # Validate date input
                    while True:
                        permit_expiry_date = input("Enter permit expiry date (YYYY-MM-DD): ").strip()
                        try:
                            permit_expiry_date = datetime.strptime(permit_expiry_date, "%Y-%m-%d").date()
                            break
                        except ValueError:
                            print("Invalid date! Please enter a valid date in YYYY-MM-DD format.")

                    with open("permits.txt", 'a+') as f:
                        f.seek(0)
                        permit_lines = [line.strip() for line in f if line.strip()]

                        # Determine the next IssueID in P001 format
                        max_id = 0
                        for line in permit_lines[1:]:  # skip header if exists
                            parts = [p.strip() for p in line.split(',')]
                            if len(parts) > 0 and parts[0].startswith('P'):
                                try:
                                    current_id = int(parts[0][1:])
                                    if current_id > max_id:
                                        max_id = current_id
                                except ValueError:
                                    continue

                        # Generate new IssueID
                        new_issue_id = f"P{max_id + 1:03d}"  # format as P001, P002, etc.

                        # Write header if file is empty
                        if not permit_lines:
                            f.write("IssueID,Plate,PermitID,ExpiryDate\n")

                        # Write the new permit
                        f.write(f"{new_issue_id},{permit_plate},{permitID},{permit_expiry_date}\n")
                        print(f"Temporary permit issued for {permit_plate} is {new_issue_id}")
            elif visitors_temporary_choice == "b" or visitors_temporary_choice.lower() == "back to parking staff menu":
                print("Back to Parking Staff Menu.....")
                return
            else:
                print("Invalid choice. Please try again.")
    except FileNotFoundError:
        print("Error: 'permits.txt' not found.")

def daily_logs():  # read daily logs
    try:
        while True:
            print("\n" + "=" * 60)
            print("   WELCOME LOG READER SYSTEM MENU   ")
            print("=" * 60)
            print("[a] Read Daily Logs")
            print("[b] Back to Parking Staff Menu")
            print("-" * 60)
            daily_log_choice = input("Enter your choice: ")
            if daily_log_choice == "a" or daily_log_choice.lower() == "read daily logs":
                with open("parking_logs.txt", "r") as f:
                    print("\n--- Parking Daily Log Reader ---")

                    # Convert user input to date object
                    while True:
                        target_date_input = input("Enter date (DD/MM/YYYY): ")
                        try:
                            date_obj = datetime.strptime(target_date_input, "%d/%m/%Y").date()
                            break  # success
                        except ValueError:
                            print("Error: Wrong date format. Please use DD/MM/YYYY (e.g., 02/12/2026).")

                    print(f"\nLog report for {target_date_input}")
                    print("-" * 50)

                    found_any = False

                    for line in f:
                        parting = [p.strip() for p in line.strip().split(',')]
                        if len(parting) < 7:
                            continue

                        # Convert log date to date object
                        try:
                            log_date = datetime.strptime(parting[0], "%d/%m/%Y").date()
                        except ValueError:
                            continue  # skip invalid date formats in file

                        if log_date == date_obj:
                            logID = parting[1]
                            log_plate = parting[2]
                            log_spaceID = parting[3]
                            log_entry_time = parting[4]
                            log_exit_time = parting[5]
                            log_fee = parting[6]
                            print(f"{logID}, {log_plate}, {log_spaceID}, "
                                  f"{log_entry_time}, {log_exit_time}, RM{log_fee}")
                            found_any = True
                    if not found_any:
                        print(f"Sorry, no records found for {target_date_input}.")
            elif daily_log_choice == "b" or daily_log_choice.lower() == "back to parking staff menu":
                print("Back to Parking Staff Menu.....")
                return
            else:
                print("Error: Invalid choice. Please try again.")
    except FileNotFoundError:
        print("Error: 'parking_logs.txt' not found.")

main_menu()