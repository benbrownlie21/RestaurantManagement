import sys


def main():
    try:
        menu()
    except KeyboardInterrupt:
        print("\nProgram ended. Exiting now...")
        sys.exit(0)


def menu():
    print("-----Welcome to The Institute-----")

    choice = input(
        """
    W: Waitlist
    A: Restaurant
    B: Kitchen
    M: Manager
    Q: Quit
    
    Please enter your choice: """
    ).lower()

    if choice == "a":
        restaurant()
    elif choice == "b":
        kitchen()
    elif choice == "m":
        manager()
    elif choice == "w":
        waitlist()
    elif choice == "q":
        print("Restaurant Management shutting down, goodbye!")
        sys.exit()
    else:
        print("You must only select either A, B, M or Q")
        print("Please try again")
        menu()


def restaurant():
    from restaurant_api import RestaurantChoices

    print("-----The Institute Restaurant-----")

    choice = input(
        """
    A: Show Menu
    B: Take Order
    C: Change Order
    D: Cancel Order
    E: Pay for Order
    R: Return
    Q: Quit

    Please enter your choice: """
    ).lower()
    if choice == "a":
        RestaurantChoices.view()
    elif choice == "b":
        RestaurantChoices.insert()
    elif choice == "c":
        RestaurantChoices.update()
    elif choice == "d":
        RestaurantChoices.cancelled()
    elif choice == "e":
        RestaurantChoices.complete()
    elif choice == "r":
        menu()
    elif choice == "q":
        print("Restaurant Management shutting down, goodbye!")
        sys.exit()
    else:
        print("You must only select either A, B, C, D or Q")
        print("Please try again")


def kitchen():
    from kitchen_api import KitchenChoices

    print("-----The Institute Kitchen-----")

    choice = input(
        """
    A: Show Orders 
    B: Prepare Food
    C: Food Availability
    D: Mark as Ready
    E: Mark as Delivered
    R: Return
    Q: Quit

    Please enter your choice: """
    ).lower()

    if choice == "a":
        KitchenChoices.show_orders()
    elif choice == "b":
        KitchenChoices.update_pf()
    elif choice == "c":
        KitchenChoices.update_fu()
    elif choice == "d":
        KitchenChoices.update_re()
    elif choice == "e":
        KitchenChoices.update_de()
    elif choice == "r":
        menu()
    elif choice == "q":
        print("Restaurant Management shutting down, goodbye!")
        sys.exit()
    else:
        print("You must only select either A, B, C, D or Q")
        print("Please try again")
        kitchen()


def manager():
    from manager_api import ManagerChoices

    print("-----The Institute Management Portal-----")

    choice = input(
        """
    A: Reports
    B: Activate Waiter
    C: Deactivate Waiter
    D: Delete Customer
    R: Return
    Q: Quit

    Please enter your choice: """
    ).lower()
    if choice == "a":
        ManagerChoices.reports()
    elif choice == "b":
        ManagerChoices.activate_w()
    elif choice == "c":
        ManagerChoices.deactivate_w()
    elif choice == "d":
        ManagerChoices.del_cu()
    elif choice == "r":
        menu()
    elif choice == "q":
        print("Restaurant Management shutting down, goodbye!")
        sys.exit()
    else:
        print("You must only select either A, B, C, D or Q")
        print("Please try again")
        manager()


def waitlist():
    from waitlist_api import WaitListChoices

    print("-----The Institute Waitlist-----")

    choice = input(
        """
    A: Show Waitlist
    B: Add to Waitlist
    C: Mark as Seated
    R: Return
    Q: Quit

    Please enter your choice: """
    ).lower()

    if choice == "a":
        WaitListChoices.show_list()
    elif choice == "b":
        WaitListChoices.insert()
    elif choice == "c":
        WaitListChoices.update()
    elif choice == "r":
        menu()
    elif choice == "q":
        print("Restaurant Management shutting down, goodbye!")
        sys.exit()
    else:
        print("You must only select either A, B, C or Q")
        print("Please try again")
        waitlist()


if __name__ == "__main__":
    main()
