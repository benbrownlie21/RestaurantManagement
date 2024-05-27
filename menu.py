import sys


def main():
    menu()


def menu():
    print("-----Welcome to The Institute-----")

    choice = input(
        """
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
    elif choice == "q":
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
    elif choice == "q":
        sys.exit()
    else:
        print("You must only select either A, B, C, D or Q")
        print("Please try again")
        restaurant()


def kitchen():
    from kitchen_api import KitchenChoices

    print("-----The Institute Kitchen-----")

    choice = input(
        """
    A: Prepare Food
    B: Food Availability
    C: Mark as Ready
    D: Mark as Delivered
    Q: Quit

    Please enter your choice: """
    ).lower()

    if choice == "a":
        KitchenChoices.update_pf()
    elif choice == "b":
        KitchenChoices.update_fu()
    elif choice == "c":
        KitchenChoices.update_re()
    elif choice == "d":
        KitchenChoices.update_de()
    elif choice == "q":
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
    A: Number of Total Orders
    B: Number of Active Orders
    C: Number of Cancelled Orders
    D: Best Waiters
    Q: Quit

    Please enter your choice: """
    ).lower()

    if choice == "a":
        ManagerChoices.search_to()
    elif choice == "b":
        ManagerChoices.search_ao()
    elif choice == "c":
        ManagerChoices.search_co()
    elif choice == "d":
        ManagerChoices.search_bw()
    elif choice == "q":
        sys.exit()
    else:
        print("You must only select either A, B, C, D or Q")
        print("Please try again")
        manager()


if __name__ == "__main__":
    main()