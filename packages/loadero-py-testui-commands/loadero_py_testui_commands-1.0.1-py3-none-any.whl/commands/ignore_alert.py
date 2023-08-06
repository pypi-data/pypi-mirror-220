from testui.support.testui_driver import TestUIDriver
from selenium.common.exceptions import NoAlertPresentException


def ignore_alert(driver: TestUIDriver) -> None:
    try:
        driver.get_driver().switch_to.alert.accept()
    except NoAlertPresentException:
        pass
