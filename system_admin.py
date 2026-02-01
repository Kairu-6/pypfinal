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
    id = space[0]
    id_number = int(id[1:])
    return id_number

parking_space_types = ["Regular", "Reserved", "Electric"]


def main():
    while True:
        parking_headers, parking_spaces = load_from_file("parking_spaces.txt")

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
                    current_line += f"{data[0]}({data[1]}) : {data[2]}" + "    "             # Parse into readable format

                    if (i+1) % 5 == 0:
                        print(current_line)
                        current_line = ""
                    elif i == len(parking_spaces)-1:
                        print(current_line)
                
                print("")
                edit_records_option = input("Enter selection: ")


                if edit_records_option == "b":                                      # Back To Main Menu
                    break


                elif edit_records_option == "a":                                    # Add New Parking Space
                    new_type = -1
                    while new_type not in parking_space_types:
                        new_type = input(f"What type of parking? [{"/".join(parking_space_types)}] : ")

                    existing_ids = []
                    for space in parking_spaces:
                        existing_ids.append(get_id_number(space))

                    new_id_num = 1                                                  # Look for least non-existing id
                    while new_id_num in existing_ids:
                        new_id_num += 1

                    if len(str(new_id_num)) > 1:                                    # Creation of new id based on id number(one digit or more)
                        new_id = "S" + str(new_id_num)
                    else:
                        new_id = "S0" + str(new_id_num)

                    parking_spaces.append([new_id, new_type, "Available"])
                    parking_spaces.sort(key=get_id_number)

                    if save_to_file(parking_spaces, "parking_spaces.txt", parking_headers):
                        continue
                    else:
                        print("error")

if __name__ == "__main__":
    main()