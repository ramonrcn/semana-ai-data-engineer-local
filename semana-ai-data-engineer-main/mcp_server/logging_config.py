import logging


class CustomFormatter(logging.Formatter):
    """
    Custom formatter that appends contextual fields if available.
    """

    def format(self, record):
        base = super().format(record)

        extras = []
        for key in [
            "task_name",
            "step",
            "user_id",
            "route_type",
            "route_value",
            "duration",
            "error",
            "expected",
            "got",
        ]:
            if hasattr(record, key):
                extras.append(f"{key}={getattr(record, key)}")

        if extras:
            return f"{base} | {' '.join(extras)}"

        return base


def setup_logging():
    """
    Configure global logging once (entrypoint only).
    """

    handler = logging.StreamHandler()
    handler.setFormatter(
        CustomFormatter(
            "%(asctime)s | %(levelname)s | %(name)s:%(lineno)d | %(message)s"
        )
    )

    logging.basicConfig(level=logging.INFO, handlers=[handler])