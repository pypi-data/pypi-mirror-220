import time
import signal
import re
from typing import Callable

from testui.support import logger


def time_execution(
    name: str, command: Callable, timeout: int or None = None
) -> None:
    block_name = name

    if not isinstance(block_name, str) or block_name == "":
        if command.__name__ == "" or command.__name__ == "<lambda>":
            block_name = "anonymous"
        else:
            block_name = command.__name__

    if re.match(r"^[\w-]{1,150}$", block_name) is None:
        raise ValueError(
            "Invalid name provided, "
            "name should not exceed 150 characters in length and can only "
            "contain alphanumeric characters, underscores and hyphens"
        )

    if timeout is not None:
        if not isinstance(timeout, int):
            raise TypeError("invalid timeout argument type")
        if timeout <= 0:
            raise ValueError("timeout value must be positive")

        def timeout_handler(*_):
            raise TimeoutError(
                f"Timeout {round(timeout*1000)}ms reached while "
                f"timing the execution of '{block_name}'"
            )

        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(int(timeout + 1))

    start = round(time.time() * 1000)
    command()
    end = round(time.time() * 1000)

    if timeout is not None:
        signal.alarm(0)

    duration = end - start

    logger.log_debug(
        f"[LOADERO] Execution time for '{block_name}': {duration}ms "
        f"(start: {start}; end: {end})."
    )
