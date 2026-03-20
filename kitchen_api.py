from tabulate import tabulate
import menu
from db import Database


class KitchenChoices:
    db = Database()

    @classmethod
    def show_orders(cls):
        query = """
        SELECT 
            order_id,
            customer_id,
            waiter_id,
            STRING_AGG(CASE WHEN order_data->>'category' = 'Starters' THEN order_data->>'item_name' ELSE NULL END, ', ') AS Starters,
            STRING_AGG(CASE WHEN order_data->>'category' = 'Mains' THEN order_data->>'item_name' ELSE NULL END, ', ') AS Mains,
            STRING_AGG(CASE WHEN order_data->>'category' = 'Sides' THEN order_data->>'item_name' ELSE NULL END, ', ') AS Sides,
            STRING_AGG(CASE WHEN order_data->>'category' = 'Drinks' THEN order_data->>'item_name' ELSE NULL END, ', ') AS Drinks,
            STRING_AGG(CASE WHEN order_data->>'category' = 'Desserts' THEN order_data->>'item_name' ELSE NULL END, ', ') AS Desserts,
            CASE WHEN order_ready = TRUE THEN 'Ready for Delivery' ELSE 'Not Ready for Delivery' END AS Action
        FROM 
            orders,
            jsonb_array_elements(items::jsonb) AS order_data
        WHERE
            cancelled <> TRUE
        AND
            order_complete <> TRUE
        AND
            order_delivered <> TRUE
        GROUP BY 
            order_id, customer_id, waiter_id
        ORDER BY
            modified DESC    
        """
        cls.db.cursor.execute(query)
        results = cls.db.cursor.fetchall()
        if results:
            headers = [desc[0].upper() for desc in cls.db.cursor.description]
            print(tabulate(results, headers=headers, tablefmt="fancy_grid", stralign="center"))
        menu.kitchen()

    @classmethod
    def update_pf(cls):
        # updates the db table orders changing prepare_order from FALSE to TRUE
        order_id_input = input("Enter Order ID: ")
        query = f"""
        UPDATE Orders
        SET prepare_order = TRUE
        WHERE order_id = '{order_id_input}'
        """
        cls.db.cursor.execute(query)
        print(f"The food for Order ID '{order_id_input}' is being prepared")
        menu.kitchen()

    @classmethod
    def update_fu(cls):
        # updates the db table menu changing available from TRUE to FALSE or FALSE to TRUE
        choice_input = input("Activate or Deactivate Item: ").lower()
        if choice_input == "deactivate":
            item_id_input = input("Enter Food ID: ")
            query2 = """
            SELECT item_name
            FROM menu
            WHERE item_id = %s
            """
            cls.db.cursor.execute(query2, (item_id_input,))
            result = cls.db.cursor.fetchone()

            if result:
                item_name = result[0]

            query = """
            UPDATE menu
            SET available = FALSE
            WHERE item_id = %s
            """

            cls.db.cursor.execute(query, (item_id_input,))
            print(
                f"The food item '{item_name}' is not available and has been removed from the menu\n"
            )
            menu.restaurant()
        elif choice_input == "activate":
            item_id_input = input("Enter Food ID: ")
            query2 = """
            SELECT item_name
            FROM menu
            WHERE item_id = %s
            """
            cls.db.cursor.execute(query2, (item_id_input,))
            result = cls.db.cursor.fetchone()

            if result:
                item_name = result[0]

            query = """
            UPDATE menu
            SET available = TRUE
            WHERE item_id = %s
            """

            cls.db.cursor.execute(query, (item_id_input,))
            print(
                f"The food item '{item_name}' is now available and has been added to the menu\n"
            )
            menu.kitchen()

    @classmethod
    def update_re(cls):
        # updates the db table orders changing order_ready from FALSE to TRUE
        order_id_input = input("Enter Order ID: ")
        query = f"""
        UPDATE Orders
        SET order_ready = TRUE
        WHERE order_id = '{order_id_input}'
        """
        cls.db.cursor.execute(query)
        print(f"The food for Order ID '{order_id_input}' is ready for the customer")
        menu.kitchen()

    @classmethod
    def update_de(cls):
        # updates the db table orders changing order_delivered from FALSE to TRUE
        order_id_input = input("Enter Order ID: ")
        query = f"""
        UPDATE Orders
        SET order_delivered = TRUE
        WHERE order_id = '{order_id_input}'
        """
        cls.db.cursor.execute(query)
        print(
            f"The food for Order ID '{order_id_input}' has been delivered successfully"
        )
        menu.kitchen()

    @classmethod
    def close_connection(cls):
        cls.db.close_connection()
