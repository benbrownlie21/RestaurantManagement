from tabulate import tabulate
import json
import menu
from db import Database


class RestaurantChoices:
    db = Database()

    @classmethod
    def view(cls):
        query = """
        SELECT item_name AS Name, category AS Category, concat('$', price) AS Price 
        FROM Menu 
        WHERE available = TRUE
        ORDER BY category DESC
        """

        results = cls.db.execute_all(query)
        if results:
            headers = [desc[0].upper() for desc in cls.db.cursor.description]
            print(tabulate(results, headers=headers, tablefmt="fancy_grid"))
        menu.restaurant()

    @classmethod
    def insert(cls):
        cu_choice = input("Enter Customer ID: ")
        wa_choice = input("Enter Waiter ID: ")
        while True:
            fo_choice = input(
                "What would you like to order today? (separate by commas): "
            )

            # Split the food choice input into individual item names
            item_names = [item.strip() for item in fo_choice.split(",")]

            # Prepare the items JSON array
            items = []
            for item_name in item_names:
                query = """
                SELECT item_id, category, price FROM Menu WHERE item_name = %s AND available = TRUE
                """
                cls.db.cursor.execute(query, (item_name,))
                details = cls.db.cursor.fetchone()
                if details:
                    item_id, category, price = details
                    items.append(
                        {
                            "item_id": item_id,
                            "category": category,
                            "price": price,
                            "item_name": item_name,
                        }
                    )
                else:
                    print(f"{item_name} was not found in the menu")
                    break

            if not items:
                continue

            # Convert the items list to JSON
            items_json = json.dumps(items)

            # Prepare the INSERT query
            query = """
            INSERT INTO orders (customer_id, waiter_id, items)
            VALUES (%s, %s, %s)
            """
            cls.db.cursor.execute(query, (cu_choice, wa_choice, items_json))
            item_names_str = ", ".join(f"'{item}'" for item in item_names)
            print(f"Order of {item_names_str} has been created successfully!")
            break
        menu.restaurant()

    @classmethod
    def update(cls):
        # updates a food in db table orders
        order_id_input = input("Enter Order ID: ")

        inspect_query = f"""
        SELECT items
        FROM orders
        WHERE order_id = '{order_id_input}'
        """
        cls.db.cursor.execute(inspect_query)
        order_data = cls.db.cursor.fetchone()

        if not order_data:
            print("Order not found")
            return

        items_list = order_data[0]

        item_names = [item["item_name"] for item in items_list if "item_name" in item]
        item_names_str = ", ".join(item_names)

        print(f"Currently your order is: {item_names_str}")
        change_item = input("Which item would you like to change? ")
        new_item = input("Which item would you like in its place? ")

        new_item_query = f"""
        SELECT item_id, item_name, category, price
        FROM menu
        WHERE item_name = '{new_item}'
        """
        cls.db.cursor.execute(new_item_query)
        new_item_details = cls.db.cursor.fetchone()

        if not new_item_details:
            print("New item not found in the menu")
            return

        item_id, item_name, category, price = new_item_details

        change_item_index = item_names.index(change_item)

        # Update the order with new item details
        query2 = f"""
        UPDATE orders
        SET items = jsonb_set(
            items::jsonb,
            '{{{change_item_index}}}',
            '{{"item_id": "{item_id}", "item_name": "{item_name}", "category": "{category}", "price": "{price}"}}',
            true
        )
        WHERE order_id = '{order_id_input}'
        """
        cls.db.cursor.execute(query2)
        print(f"We have changed {change_item} to {new_item}")
        menu.restaurant()

    @classmethod
    def cancelled(cls):
        order_id_input = input("Enter Order ID: ")
        query_o = """
        SELECT order_delivered
        FROM orders
        WHERE order_id = %s
        """
        cls.db.cursor.execute(query_o, (order_id_input,))
        result = cls.db.cursor.fetchone()

        if not result:
            print(f"Order ID '{order_id_input}' not found.")
            menu.restaurant()
            return

        order_delivered = bool(result[0])

        if order_delivered:
            print(
                f"Order number '{order_id_input}' has been delivered and cannot be cancelled"
            )
            menu.restaurant()
            return

        query = """
        UPDATE Orders
        SET cancelled = TRUE
        WHERE order_id = %s
        """
        cls.db.cursor.execute(query, (order_id_input,))
        print(f"The food for Order ID '{order_id_input}' has been cancelled")
        menu.restaurant()

    @classmethod
    def complete(cls):
        order_id_input = input("Enter Order ID: ")
        query3 = """
        SELECT order_complete
        FROM orders
        WHERE order_id = %s
        """
        cls.db.cursor.execute(query3, (order_id_input,))
        result = cls.db.cursor.fetchone()

        if result:
            order_complete = bool(result[0])
            if order_complete:
                print(f"Order number '{order_id_input}' has already been paid for")
                menu.restaurant()
                return
        query_c = """
        SELECT cancelled
        FROM orders
        WHERE order_id = %s
        """
        cls.db.cursor.execute(query_c, (order_id_input,))
        result = cls.db.cursor.fetchone()

        if result:
            cancelled = bool(result[0])
            if cancelled:
                print(
                    f"Order number '{order_id_input}' has been cancelled and cannot be paid for"
                )
                menu.restaurant()
                return

        query2 = """
        SELECT total_price
        FROM orders
        WHERE order_id = %s
        """
        cls.db.cursor.execute(query2, (order_id_input,))
        result = cls.db.cursor.fetchone()

        if result:
            total_price = float(result[0])
            print(f"Your total is: £{total_price}")

        pm_input = None
        while True:
            pm_input = input(
                "Enter Payment Method (1: Cash, 2: Amex, 3: Visa, 4: Mastercard): "
            )
            if pm_input.isdigit() and 1 <= int(pm_input) <= 4:
                pm_input = int(pm_input)
                break
            else:
                print("Please enter a number between 1 and 4")

        amount_paid = 0.0
        while amount_paid < total_price:
            am_input = float(input("How much would you like to pay?: "))
            amount_paid += am_input

            if amount_paid >= total_price:
                query_p = """
                UPDATE Orders
                SET payment_method_id = %s
                WHERE order_id = %s
                """
                cls.db.cursor.execute(query_p, (pm_input, order_id_input))

                query_a = """
                UPDATE Orders
                SET amount_paid = %s
                WHERE order_id = %s
                """
                cls.db.cursor.execute(query_a, (amount_paid, order_id_input))

                query = """
                UPDATE Orders
                SET order_complete = TRUE
                WHERE order_id = %s
                """
                cls.db.cursor.execute(query, (order_id_input,))
                print(
                    f"Order Total was £{total_price}. You have paid £{amount_paid} successfully. The order is now closed, thank you!"
                )
            else:
                print(
                    f"Order Total: £{total_price}. You still owe £{total_price - amount_paid:.2f}"
                )

        menu.restaurant()

    def close_connection(cls):
        cls.db.close_connection()
