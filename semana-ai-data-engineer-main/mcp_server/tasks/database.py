from mcp_server.services.db import get_connection
from mcp_server.logging_config import get_logger

logger = get_logger(__name__)

def business_analysis(trace_id=None, **kwargs):
    logger.info("Connecting to DB", extra={"trace_id": trace_id})
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # --- counts ---
        logger.info("Running counts queries", extra={"trace_id": trace_id})
        cursor.execute("SELECT COUNT(*) FROM customers")
        customers_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM products")
        products_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM orders")
        orders_count = cursor.fetchone()[0]

        # --- sample customers ---
        logger.info("Fetching sample customer data", extra={"trace_id": trace_id})
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
        logger.info("Fetching sample orders data", extra={"trace_id": trace_id})
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
        logger.info("Calculating orders distribution by status", extra={"trace_id": trace_id})
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
        logger.info("Calculating customers distribution by state", extra={"trace_id": trace_id})
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
