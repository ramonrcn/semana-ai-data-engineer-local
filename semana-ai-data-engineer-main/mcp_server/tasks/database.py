from mcp_server.services.db import get_connection
import logging

logger = logging.getLogger(__name__)


def business_analysis():
    logger.info("[TRACE] business_analysis started")

    conn = get_connection()
    cur = conn.cursor()

    results = {}

    cur.execute("SELECT AVG(total) FROM orders;")
    results["avg_order"] = cur.fetchone()[0]
    logger.debug("[SQL] avg_order computed")

    cur.execute("""
        SELECT state, COUNT(*) 
        FROM customers 
        JOIN orders USING(customer_id)
        GROUP BY state
        ORDER BY COUNT(*) DESC
    """)
    results["top_states"] = cur.fetchall()
    logger.debug("[SQL] top_states computed")

    cur.execute("""
        SELECT 
        SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END)::float 
        / COUNT(*) * 100
        FROM orders;
    """)
    results["cancel_rate"] = cur.fetchone()[0]
    logger.debug("[SQL] cancel_rate computed")

    cur.execute("""
        SELECT payment, COUNT(*) 
        FROM orders 
        GROUP BY payment;
    """)
    results["payments"] = cur.fetchall()
    logger.debug("[SQL] payments computed")

    cur.execute("""
        SELECT segment, SUM(total)
        FROM customers
        JOIN orders USING(customer_id)
        GROUP BY segment;
    """)
    results["revenue"] = cur.fetchall()
    logger.debug("[SQL] revenue computed")

    cur.close()
    conn.close()

    logger.info("[TRACE] business_analysis finished")

    return results