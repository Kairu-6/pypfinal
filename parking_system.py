


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
            pass
        else :
            print("Quiting the program.....")
            break

if __name__ == "__main__":
    main()