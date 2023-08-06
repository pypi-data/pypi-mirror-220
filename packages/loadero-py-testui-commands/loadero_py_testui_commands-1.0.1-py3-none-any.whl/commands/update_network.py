from testui.support import logger
from testui.support.testui_driver import TestUIDriver
from testui.elements.testui_element import testui_error


def update_network(
    driver: TestUIDriver, network_mode: str, network_config: dict or None = None
) -> None:
    if not network_mode:
        testui_error(driver, "[ERROR] Loadero: No network mode provided")
        return

    if not isinstance(network_mode, str):
        testui_error(
            driver, "[ERROR] Loadero: `network_mode` must be of type str"
        )
        return

    if network_mode == "custom" and not isinstance(network_config, dict):
        testui_error(
            driver, "[ERROR] Loadero: `network_config` must be of type dict"
        )
        return


    logger.log_debug(f'Network mode changed to "{network_mode}"')
