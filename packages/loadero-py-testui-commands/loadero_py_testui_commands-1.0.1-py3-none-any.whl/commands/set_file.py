from testui.support.testui_driver import TestUIDriver
from testui.elements.testui_element import Elements, testui_error


def set_file(driver: TestUIDriver, element: Elements, file_name: str) -> None:
    if element is None:
        testui_error(driver, "[ERROR] Loadero: No input field element provided")
        return

    if not file_name:
        testui_error(driver, "[ERROR] Loadero: No filename provided")
        return

    element.send_keys(file_name)
