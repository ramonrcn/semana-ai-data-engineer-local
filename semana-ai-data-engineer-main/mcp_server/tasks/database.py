from mcp_server.services.db import get_connection


def business_analysis():
    conn = get_connection()
    cur = conn.cursor()

    results = {}

    cur.execute("SELECT AVG(total) FROM orders;")
    results["avg_order"] = cur.fetchone()[0]

    cur.execute("""
        SELECT state, COUNT(*) 
        FROM customers 
        JOIN orders USING(customer_id)
        GROUP BY state
        ORDER BY COUNT(*) DESC
    """)
    results["top_states"] = cur.fetchall()

    cur.execute("""
        SELECT 
        SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END)::float 
        / COUNT(*) * 100
        FROM orders;
    """)
    results["cancel_rate"] = cur.fetchone()[0]

    cur.execute("""
        SELECT payment, COUNT(*) 
        FROM orders 
        GROUP BY payment;
    """)
    results["payments"] = cur.fetchall()

    cur.execute("""
        SELECT segment, SUM(total)
        FROM customers
        JOIN orders USING(customer_id)
        GROUP BY segment;
    """)
    results["revenue"] = cur.fetchall()

    cur.close()
    conn.close()

    return results