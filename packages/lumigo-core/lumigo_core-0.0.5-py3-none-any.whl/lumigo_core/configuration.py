import os

from lumigo_core.logger import get_logger


def get_config_int(key: str, default: int) -> int:
    try:
        return int(os.environ.get(key, default))
    except ValueError:
        get_logger().error(f"Invalid value for config {key}, using default")
        return default


class CoreConfiguration:
    chained_services_max_depth: int = get_config_int(
        "LUMIGO_CHAINED_SERVICES_MAX_DEPTH", 3
    )
    chained_services_max_width: int = get_config_int(
        "LUMIGO_CHAINED_SERVICES_MAX_WIDTH", 5
    )
