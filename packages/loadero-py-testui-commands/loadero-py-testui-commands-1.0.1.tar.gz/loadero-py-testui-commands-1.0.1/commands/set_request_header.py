from testui.support import logger
from testui.support.testui_driver import TestUIDriver
from testui.elements.testui_element import testui_error


def set_request_header(
    driver: TestUIDriver, header: str, value: str or None = None
) -> None:
    if not header:
        testui_error(driver, "[ERROR] Loadero: No request header provided")
        return

    logger.log_debug(f'Updated request header "{header}" to "{value}"')
