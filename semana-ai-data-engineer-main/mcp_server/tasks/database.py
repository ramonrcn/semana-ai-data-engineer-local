from mcp_server.services.db import get_connection
from mcp_server.logging_config import get_logger

logger = get_logger(__name__)


def business_analysis():
    logger.info("[TASK] business_analysis started")

    conn = get_connection()
    cursor = conn.cursor()

    results = {}

    try:
        # 1. Count rows
        cursor.execute("""
            SELECT
                (SELECT COUNT(*) FROM customers),
                (SELECT COUNT(*) FROM products),
                (SELECT COUNT(*) FROM orders)
        """)
        results["counts"] = cursor.fetchone()

        # 2. Sample customers
        cursor.execute("""
            SELECT name, state, segment
            FROM customers
            LIMIT 5
        """)
        results["customers_sample"] = cursor.fetchall()

        # 3. Sample orders
        cursor.execute("""
            SELECT total, status, payment
            FROM orders
            LIMIT 5
        """)
        results["orders_sample"] = cursor.fetchall()

        # 4. Orders by status
        cursor.execute("""
            SELECT status, COUNT(*) as count,
                   ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) as pct
            FROM orders
            GROUP BY status
        """)
        results["orders_distribution"] = cursor.fetchall()

        # 5. Customers by state
        cursor.execute("""
            SELECT state, COUNT(*)
            FROM customers
            GROUP BY state
        """)
        results["customers_by_state"] = cursor.fetchall()

        logger.info("[TASK] business_analysis completed")

        return results

    except Exception as e:
        logger.exception("[TASK] business_analysis failed")
        raise e

    finally:
        cursor.close()
        conn.close()