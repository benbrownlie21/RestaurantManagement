from tabulate import tabulate
import menu
from db import Database

class WaitListChoices:
    db = Database()

    @classmethod
    def show_list(cls):
        query = """
        SELECT waitlist_id AS Waitlist_ID, CONCAT(first_name, ' ', last_name) AS Name, email AS Email, phone_number AS Number
        FROM Waitlist
        WHERE seated = false
        ORDER BY modified DESC
        """

        results = cls.db.execute_all(query)
        if results:
            headers = [desc[0].upper() for desc in cls.db.cursor.description]
            print(tabulate(results, headers=headers, tablefmt="fancy_grid"))
        menu.waitlist()

    @classmethod
    def insert(cls):
        fn_choice = input("Enter customer's first name: ")
        ln_choice = input("Enter customer's last name: ")
        em_choice = input("Enter customer's email address: ")
        pn_choice = input("Enter customer's telephone number: ")
        query = """
        INSERT INTO Waitlist (first_name, last_name, email, phone_number)
        VALUES (%s, %s, %s, %s);
        """
        cls.db.execute_update(query, (fn_choice, ln_choice, em_choice, pn_choice))
        print("You have been successfully added to the waitlist!")
        menu.waitlist()

    @classmethod
    def update(cls):
        wl_id = input("Enter the Waitlist ID: ")
        query_update = f"""
        UPDATE Waitlist
        SET seated = TRUE
        WHERE waitlist_id = %s
        """
        cls.db.cursor.execute(query_update, (wl_id,))
        print("You have now been seated")
        menu.waitlist()

        query_insert = f"""
        INSERT INTO Customers (first_name, last_name, email, phone_number)
        SELECT first_name, last_name, email, phone_number
        FROM waitlist
        WHERE waitlist_id = %s
        """
        cls.db.cursor.execute(query_insert, (wl_id,))

    def close_connection(cls):
        cls.db.close_connection()
