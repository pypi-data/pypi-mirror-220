from testui.support.testui_driver import TestUIDriver

from .set_request_header import set_request_header


def set_user_agent(driver: TestUIDriver, value: str or None = None) -> None:
    return set_request_header(driver, "User-Agent", value)
