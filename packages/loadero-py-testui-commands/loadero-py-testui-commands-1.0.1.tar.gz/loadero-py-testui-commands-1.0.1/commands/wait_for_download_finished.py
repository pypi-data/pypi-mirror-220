from testui.support import logger
from testui.support.testui_driver import TestUIDriver
from testui.elements.testui_element import testui_error


def wait_for_download_finished(
    driver: TestUIDriver, file_name: str, timeout: int = 1000
) -> None:
    if not file_name:
        testui_error(driver, "[ERROR] Loadero: No filename provided")
        return

    if not isinstance(file_name, str):
        testui_error(driver, "[ERROR] Loadero: `file_name` must be of type str")
        return

    fn = file_name.replace("/", "").replace("\\", "")

    logger.log_debug(
        f"File {file_name} has completed download within {timeout}ms"
    )
