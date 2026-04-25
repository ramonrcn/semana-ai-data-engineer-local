from mcp_server.services.db import get_connection
from mcp_server.logging_config import get_logger
from mcp_server.utils.formatters import (format_business_executive,
    format_business_analysis )

logger = get_logger(__name__)

def business_analysis(trace_id=None, mode="exploration", **kwargs):
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

        # --- avg order value ---
        logger.info("Calculating average order value", extra={"trace_id": trace_id})
        cursor.execute("""
            SELECT ROUND(AVG(total), 2)
            FROM orders
        """)
        avg_order_value = float(cursor.fetchone()[0])

        # --- top 3 states by orders ---
        logger.info("Calculating top states by orders", extra={"trace_id": trace_id})

        cursor.execute("""
            SELECT c.state, COUNT(*) as count
            FROM orders o
            JOIN customers c ON o.customer_id = c.customer_id
            GROUP BY c.state
            ORDER BY count DESC
            LIMIT 3
        """)
        top_states = [
            {"state": r[0], "count": r[1]}
            for r in cursor.fetchall()
        ]

        # --- payment distribution ---
        logger.info("Calculating payment distribution", extra={"trace_id": trace_id})
        cursor.execute("""
            SELECT payment, COUNT(*) as count,
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM orders), 2) as percentage
            FROM orders
            GROUP BY payment
            ORDER BY count DESC
        """)
        payment_distribution = [
            {
                "payment": r[0],
                "count": r[1],
                "percentage": float(r[2])
            }
            for r in cursor.fetchall()
        ]

        # --- revenue by segment ---
        logger.info("Calculating revenue by segment", extra={"trace_id": trace_id})
        cursor.execute("""
            SELECT c.segment, ROUND(SUM(o.total), 2) as revenue
            FROM orders o
            JOIN customers c ON o.customer_id = c.customer_id
            GROUP BY c.segment
            ORDER BY revenue DESC
        """)
        revenue_by_segment = [
            {
                "segment": r[0],
                "revenue": float(r[1])
            }
            for r in cursor.fetchall()
        ]

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

        raw_data = {
            # --- core counts ---
            "counts": {
                "customers": customers_count,
                "products": products_count,
                "orders": orders_count,
            },

            # --- samples (exploration/debug) ---
            "customers_sample": customers_sample,
            "orders_sample": orders_sample,

            # --- distributions ---
            "orders_distribution": orders_distribution,
            "customers_by_state": customers_by_state,

            # --- business metrics ---
            "avg_order_value": avg_order_value,
            "top_states": top_states,
            "payment_distribution": payment_distribution,
            "revenue_by_segment": revenue_by_segment,
        }

        if mode == "executive":
            report = format_business_executive(raw_data)
        else:
            report = format_business_analysis(raw_data)

        return report

    finally:
        cursor.close()
        conn.close()
