from mcp_server.services.db import get_connection

def business_analysis(**kwargs):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # --- counts ---
        cursor.execute("SELECT COUNT(*) FROM customers")
        customers_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM products")
        products_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM orders")
        orders_count = cursor.fetchone()[0]

        # --- sample customers ---
        cursor.execute("""
            SELECT name, state, segment
            FROM customers
            LIMIT 5
        """)
        customers_sample = [
            {"name": r[0], "state": r[1], "segment": r[2]}
            for r in cursor.fetchall()
        ]

        # --- sample orders ---
        cursor.execute("""
            SELECT total, status, payment
            FROM orders
            LIMIT 5
        """)

        orders_sample = [
            {"total": float(r[0]), "status": r[1], "payment": r[2]}
            for r in cursor.fetchall()
        ]

        #---Orders Distribution by Status
        cursor.execute("""
            SELECT 
                status,
                COUNT(*) AS count,
                ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM orders), 2) AS percentage
            FROM orders
            GROUP BY status
            ORDER BY count DESC
        """)

        orders_distribution = [
            {
                "status": r[0],
                "count": r[1],
                "percentage": float(r[2]),
            }
            for r in cursor.fetchall()
        ]

        #---Customers Distribution by State
        cursor.execute("""
            SELECT 
                state,
                COUNT(*) AS count,
                ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM customers), 2) AS percentage
            FROM customers
            GROUP BY state
            ORDER BY count DESC
        """)

        customers_by_state = [
            {
                "state": r[0],
                "count": r[1],
                "percentage": float(r[2]),
            }
            for r in cursor.fetchall()
        ]

        return {
            "counts": {
                "customers": customers_count,
                "products": products_count,
                "orders": orders_count,
            },
            "customers_sample": customers_sample,
            "orders_sample": orders_sample,
            "orders_distribution": orders_distribution,
            "customers_by_state": customers_by_state
        }

    finally:
        cursor.close()
        conn.close()
