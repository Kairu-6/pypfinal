def print_admin_menu():
    print("\n" + "="*45)
    print("   PARKING MANAGEMENT SYSTEM - ADMIN MENU   ")
    print("="*45)
    print("[e] Edit Parking Records (Add/Remove/Update)")
    print("[p] Edit Permit Pricing and Types")
    print("[r] Generate Revenue or Occupancy Reports")
    print("[v] View All Records and Violations")
    print("[q] Quits the Program")
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


while True:
    print_admin_menu()

    choice1 = input("Enter selection: ")

    parking_spaces = []
    with open("parking_spaces.txt", "r+") as ps:
        header = ps.readline()
        for line in ps.readlines():
            entry = line.strip().split(",")
            parking_spaces.append(entry)

    if choice1 == "e":
        parking_spaces = []
        with open("parking_spaces.txt", "r+") as ps:
            header = ps.readline()
            for line in ps.readlines():
                entry = line.strip().split(",")
                parking_spaces.append(entry)

        
        finish = -1
        while finish != 1:
            
            print_edit_parking_records_menu()
            currentline = ""
            for i in range(len(parking_spaces)):
                data = parking_spaces[i]
                currentline += f"{data[0]}({data[1]}) : {data[2]}" + "    "

                if (i+1) % 5 == 0:
                    print(currentline)
                    currentline = ""
                elif i == len(parking_spaces)-1:
                    print(currentline)
            
            print("")
            choice2 = input("Enter selection: ")

            if choice2 == "b":
                finish = 1

    elif choice1 == "q":
        print("Exiting Menu...")
        break