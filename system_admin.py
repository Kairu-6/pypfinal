def print_admin_menu():
    print("\n" + "="*45)
    print("   PARKING MANAGEMENT SYSTEM - ADMIN MENU   ")
    print("="*45)
    print("[e] Edit Parking Records (Add/Remove/Update)")
    print("[p] Edit Permit Pricing and Types")
    print("[r] Generate Revenue or Occupancy Reports")
    print("[v] View All Records and Violations")
    print("[q] Quit the Program")
    print("-"*45)

def print_edit_parking_records_menu():
    print("\n" + "=" * 40)
    print("      EDIT PARKING RECORDS MENU      ")
    print("=" * 40)
    print("[a] Add New Parking Space")
    print("[r] Remove Existing Parking Space")
    print("[u] Update Space Information")
    print("[b] Back to Main Admin Menu")
    print("-" * 40)

def print_edit_permit_types_menu():
    print("\n" + "=" * 40)
    print("      EDIT PERMIT TYPES MENU      ")
    print("=" * 40)
    print("[a] Add New Permit Type")
    print("[u] Update Permit Price/Availability")
    print("[b] Back to Main Admin Menu")
    print("-" * 40)

def print_generate_records_menu():
    print("\n" + "=" * 40)
    print("         GENERATE REPORTS MENU         ")
    print("=" * 40)
    print("[r] Generate Revenue Report")
    print("[o] Generate Occupancy Report")
    print("[b] Back to Main Admin Menu")
    print("-" * 40)

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

def get_id_number(space):
    full_id = space[0]
    return int(full_id[1:])

def get_record(full_id, data_list):
    target = full_id.strip().upper()

    for item in data_list:
        if item[0].upper() == target:
            return item
    return False

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
    id_num = get_id_number(permit)
    priority = permit_priority.get(category, 4)
    
    return (priority, id_num)

def get_valid_date():
    while True:
        date_str = input("Enter date (DD-MM-YYYY) or q to cancel : ").strip()
        if date_str.lower() == "q":
            return "q"
        
        parts = date_str.split("-")
        if len(parts) == 3 and len(parts[0]) == 2 and len(parts[1]) == 2 and len(parts[2]) == 4:   

            if parts[0].isdigit() and parts[1].isdigit() and parts[2].isdigit():
                return date_str
        
        print("Invalid format. Please use exactly DD-MM-YYYY.")

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
                
        print("Invalid format. Please use exactly HH:MM (24-hour).")

def print_view_records_menu():
    print("\n" + "=" * 40)
    print("           VIEW RECORDS MENU           ")
    print("=" * 40)
    print("[ps] View All Parking Spaces")
    print("[pt] View All Permit Types")
    print("[p] View All Issued Permits")
    print("[v] View All Violations")
    print("[b] Back to Main Admin Menu")
    print("-" * 40)

def main():
    while True:
        parking_headers, parking_spaces = load_from_file("parking_spaces.txt")
        permit_types_headers, permit_types = load_from_file("permit_types.txt")
        permits_headers, permits = load_from_file("permits.txt")
        violations_headers, violations = load_from_file("violations.txt")

        print_admin_menu()
        admin_menu_options = ['e', 'p', 'r', 'v', 'q']
        admin_menu_option = ""

        while admin_menu_option not in admin_menu_options:
            admin_menu_option = input("Enter selection: ").strip().lower()

            if admin_menu_option not in admin_menu_options:
                print("Invalid selection, please try again.")

        if admin_menu_option == "q":
            print("Exiting Menu...")
            break


        elif admin_menu_option == "e":                                  # Edit Parking Records
            parking_space_types = ["Regular", "Reserved", "Electric"]

            while True:
                
                print_edit_parking_records_menu()
                
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
                            existing_ids.append(get_id_number(space))

                        new_id_num = 1                                                  # Look for least non-existing id
                        while new_id_num in existing_ids:
                            new_id_num += 1

                        new_id = f"S{new_id_num:02d}"

                        parking_spaces.append([new_id, new_type.capitalize(), "Available", ""])
                        parking_spaces.sort(key=get_id_number)

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

                                        parking_spaces[update_id_number_index] = [space[0], new_type, new_status, new_plate]
                                        save_to_file(parking_spaces, "parking_spaces.txt", parking_headers)
                                        
                                        found = 1
                            else:
                                print("ID not found, please try again.")


        elif admin_menu_option == "p":                                  # Edit Permit pricing and types
            permit_options = ["Daily", "Monthly", "Annual"]

            while True:
                
                print_edit_permit_types_menu()
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


        elif admin_menu_option == "r":                                  # Generate Revenue or Occupancy Reports
            while True:
                print_generate_records_menu()

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


        elif admin_menu_option == "v":                                  # View All Records and Violations
            while True:
                print_view_records_menu()
                view_options = ["ps", "pt", "p", "v", "b"]
                view_option = ""

                while view_option not in view_options:
                    view_option = input("Enter selection: ").strip().lower()

                    if view_option not in view_options:
                        print("Invalid selection, please try again.")

                if view_option == "b":
                    break
                
                elif view_option == "ps":                                    # View Parking Spaces
                    print("\n" + "=" * 45)
                    print("             ALL PARKING SPACES             ")
                    print("=" * 45)
                    print(f"{'ID':<5} | {'Type':<10} | {'Status':<10} | {'Plate'}")
                    print("-" * 45)
                    
                    for space in parking_spaces:
                        print(f"{space[0]:<5} | {space[1]:<10} | {space[2]:<10} | {space[3]}")
                    
                    print("=" * 45)
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


if __name__ == "__main__":
    main()