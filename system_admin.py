parking_space_types = ["Regular", "Reserved", "Electric"]
permit_priority = {"D": 1, "M": 2, "A": 3}

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
    id_number = int(full_id[1:])
    return id_number

def get_space(id_number, data_list):
    for item in data_list:
        if get_id_number(item) == id_number:
            return item
    return False

def enter_parking_id_num():                                 
    try:
        id_number_str = input("Enter ID number (e.g. 12) of parking space, or q to cancel : ").strip()

        if id_number_str.lower() == "q":
            return "q"
        
        elif len(id_number_str) > 1 and id_number_str[0] == "0":                      # To prevent id with leading zeros (e.g. 02) from being considered invalid (02 != 2)
            id_number_str = id_number_str[1:]
        return int(id_number_str)
    
    except ValueError:
        print("Invalid input, please enter a numeric ID.")

def permit_types_sort_key(permit):
    full_id = permit[0]
    category = full_id[0]
    id_num = get_id_number(permit)
    priority = permit_priority.get(category, 4)
    
    return (priority, id_num)

def main():
    while True:
        parking_headers, parking_spaces = load_from_file("parking_spaces.txt")
        permit_types_headers, permit_types = load_from_file("permit_types.txt")

        print_admin_menu()

        admin_menu_option = input("Enter selection: ")

        if admin_menu_option == "q":
            print("Exiting Menu...")
            break


        elif admin_menu_option == "e":                                      # Edit Parking Records
            
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
                
                edit_records_option = input("\nEnter selection: ")


                if edit_records_option == "b":                                      # Back To Main Menu
                    break


                elif edit_records_option == "a":                                    # Add New Parking Space
                    new_type = -1
                    while new_type.capitalize() not in parking_space_types and new_type != "q":
                        new_type = input(f"What type of parking? [{"/".join(parking_space_types)}] (q to cancel): ").strip()

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
                        delete_id_number = enter_parking_id_num()

                        if delete_id_number is None:
                            continue

                        elif delete_id_number == "q":
                            break
                        
                        else:
                            space = get_space(delete_id_number, parking_spaces)
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
                                    break
                            else:
                                print("Invalid ID, please try again.")                  # Id was not found in the list

                elif edit_records_option == "u":
                    found = -1

                    while found == -1:
                        update_id_number = enter_parking_id_num()

                        if update_id_number is None:
                            continue

                        elif update_id_number == "q":
                            break

                        else:
                            space = get_space(update_id_number, parking_spaces)
                            if space:
                                update_id_index = parking_spaces.index(get_space(update_id_number, parking_spaces))

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

                                    parking_spaces[update_id_index] = [space[0], new_type, new_status, new_plate]
                                    save_to_file(parking_spaces, "parking_spaces.txt", parking_headers)
                                    
                                    found = 1


        elif admin_menu_option == "p":                                  # Edit Permit pricing and types
            permit_options = ["Daily", "Monthly", "Annual"]

            while True:
                
                print_edit_permit_types_menu()
                print("Available permit types")
                for type in permit_types:
                    print(f"{type[0]} - {type[1].ljust(7)} : RM{type[2]}")
                
                edit_permit_types_option = input("\nEnter selection: ")

                if edit_permit_types_option == "b":
                    break

                elif edit_permit_types_option == "a":
                    new_permit_option = -1
                    new_permit_price = -1

                    while new_permit_option not in permit_options:
                        new_permit_option = input("Enter new permit type [Daily/Monthly/Annual] : ").capitalize()
                    
                    while new_permit_price < 0:
                        try:
                            new_permit_price = float(input("Insert price of new permit : "))
                            if new_permit_price < 0:
                                print("Price cannot be negative.")
                        except ValueError:
                            print("Invalid price, please try again.")

                    new_permit_category = new_permit_option[0]                                  # First letter of option (D/M/A)

                    counter = 0
                    for p_type in permit_types:                                                 # Look for first non-existent id number in the same category (Daily, Monthly, Annual)
                        if p_type[0][0] == new_permit_category:
                            counter += 1
                    counter += 1

                    new_permit_type_id = f"{new_permit_category}{counter:02d}"                                              # Combines letter (D/M/A) with id number (e.g. 12) to form a new unique id (D01)
                    new_permit_type = [new_permit_type_id, new_permit_option.capitalize(), f"{new_permit_price:.2f}"]       # Puts together id, permit type, and price in a list
                    permit_types.append(new_permit_type)
                    
                    permit_types.sort(key=permit_types_sort_key)
                    save_to_file(permit_types, "permit_types.txt", permit_types_headers)

if __name__ == "__main__":
    main()