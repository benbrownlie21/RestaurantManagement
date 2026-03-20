import menu
import time
from db import Database


class ManagerChoices:
    db = Database()

    @classmethod
    def reports(cls):
        print("\n-----The Institue Reports-----\n")
        query_search_to = """
        SELECT COUNT(order_id), SUM(total_price) FROM Orders
        """
        cls.db.cursor.execute(query_search_to)
        results = cls.db.cursor.fetchall()
        for row in results:
            print(f"Total number of orders: \n{row[0]} with a total of £{row[1]}\n")

        query_search_ao = """
        SELECT COUNT(order_id), SUM(total_price) FROM Orders WHERE order_delivered = FALSE
        """
        cls.db.cursor.execute(query_search_ao)
        results = cls.db.cursor.fetchall()
        for row in results:
            print(
                f"Total number of active orders:\n{row[0]} with a total of £{row[1]}\n"
            )

        query_search_co = """
        SELECT COUNT(order_id), SUM(total_price) FROM Orders WHERE cancelled = TRUE
        """
        cls.db.cursor.execute(query_search_co)
        results = cls.db.cursor.fetchall()
        for row in results:
            print(
                f"The total number of cancelled orders is:\n{row[0]} with a total lost value of £{row[1]}\n"
            )

        query_search_bw = """
        SELECT CONCAT(wa.first_name, ' ', wa.last_name) AS full_name, COUNT(ord.waiter_id) AS total_orders
        FROM Orders AS ord 
        JOIN Waiters AS wa ON ord.waiter_id = wa.waiter_id
        GROUP BY full_name
        ORDER BY total_orders DESC
        LIMIT 1
        """
        cls.db.cursor.execute(query_search_bw)
        result = cls.db.cursor.fetchone()
        if result:
            full_name, total_orders = result
            print(
                f"The waiter with the highest number of sales is:\n{full_name} with {total_orders} orders\n"
            )

        query_search_bw = """
        SELECT CONCAT(cu.first_name, ' ', cu.last_name) AS full_name, COUNT(ord.customer_id) AS total_orders
        FROM Orders AS ord 
        JOIN Customers AS cu ON ord.customer_id = cu.customer_id
        GROUP BY full_name
        ORDER BY total_orders DESC
        LIMIT 1
        """
        cls.db.cursor.execute(query_search_bw)
        result = cls.db.cursor.fetchone()
        if result:
            full_name, total_orders = result
            print(
                f"The customer with the highest number of orders is:\n{full_name} with {total_orders} orders\n"
            )

        query_pm = """
        SELECT AVG(amount_paid) AS avg_paid, COUNT(order_id) AS num_orders
        FROM Orders
        WHERE order_complete = FALSE
        """
        cls.db.cursor.execute(query_pm)
        result = cls.db.cursor.fetchone()
        if result:
            avg_paid, num_orders = result
        print(
            f"Potential Money:\nThe Institute currently has a potential to make £{round(avg_paid*num_orders, 2)} from the current seated customers\n"
        )
        time.sleep(0.5)
        menu.manager()

    @classmethod
    def activate_w(cls):
        wa_input = input("Enter Waiter ID: ")
        query = f"""
        UPDATE Waiters
        SET active = TRUE
        WHERE waiter_id = '{wa_input}'
        """
        cls.db.cursor.execute(query)
        print(f"Waiter '{wa_input}' has been activated")
        menu.manager()

    @classmethod
    def deactivate_w(cls):
        wa_input = input("Enter Waiter ID: ")
        query = f"""
        UPDATE Waiters
        SET active = FALSE
        WHERE waiter_id = '{wa_input}'
        """
        cls.db.cursor.execute(query)
        print(f"Waiter {wa_input} has been deactivated")
        menu.manager()

    @classmethod
    def del_cu(cls):
        cu_input = input("Enter Customer ID: ")
        query = f"""
        UPDATE Customers
        SET deleted = CURRENT_TIMESTAMP
        WHERE customer_id = '{cu_input}'
        """
        cls.db.cursor.execute(query)
        print(f"Customer {cu_input} has been deleted")
        menu.manager()

    def close_connection(cls):
        cls.db.close_connection()
