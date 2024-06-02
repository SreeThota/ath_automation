from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.virtual_authenticator import Credential
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


# Class supports:
#     1. All Driver level methods
#     2. All Element level methods
#     3. All Wait methods
#     4. All Actions related methods
#     5. All Select related methods
#     6. All keyboard actions

class SeleniumHelper:

    # WebDriverWait class methods
    @staticmethod
    def wait_until_page_title_is(driver: WebDriver, title: str, timeout=10) -> bool:
        return WebDriverWait(driver, timeout).until(expected_conditions.title_is(title))

    @staticmethod
    def wait_until_page_title_contains(driver: WebDriver, partial_title: str, timeout=10):
        return WebDriverWait(driver, timeout).until(expected_conditions.title_contains(partial_title))

    @staticmethod
    def wait_for_element_present_and_get(driver: WebDriver, locator_info: dict, timeout=10):
        element: WebElement = (WebDriverWait(driver, timeout)
                               .until(expected_conditions.presence_of_element_located((locator_info['type'],
                                                                                       locator_info['value']))))
        return element

    @staticmethod
    def wait_for_element_visible_and_get(driver: WebDriver, locator_info: dict, timeout=10):
        element: WebElement = (WebDriverWait(driver, timeout)
                               .until(expected_conditions.visibility_of_element_located((locator_info['type'],
                                                                                         locator_info['value']))))
        return element

    @staticmethod
    def wait_for_already_present_element_is_visible_and_get(driver: WebDriver, locator_info: dict,
                                                            timeout=10):
        element: WebElement = (WebDriverWait(driver, timeout).until(expected_conditions.visibility_of(
            SeleniumHelper.get_web_element(driver, locator_info))))
        return element

    @staticmethod
    def wait_for_presence_of_all_matching_elements_and_get(driver: WebDriver, locator_info: dict,
                                                           timeout=10):
        matching_elements_list: list[WebElement] = (WebDriverWait(driver, timeout).until(
            expected_conditions.presence_of_all_elements_located(
                (locator_info['type'],
                 locator_info['value']))))
        return matching_elements_list

    @staticmethod
    def wait_and_check_text_present_in_element(driver: WebDriver, locator_info: dict,
                                               expected_text: str, timeout=10):
        is_text_present: bool = (WebDriverWait(driver, timeout).until(
            expected_conditions.text_to_be_present_in_element((locator_info['type'],
                                                               locator_info['value']), expected_text)))
        return is_text_present

    @staticmethod
    def wait_and_check_text_present_in_element_value(driver: WebDriver, locator_info: dict,
                                                     expected_text: str, timeout=10):
        is_value_present: bool = (WebDriverWait(driver, timeout).until(
            expected_conditions.text_to_be_present_in_element_value((locator_info['type'],
                                                                     locator_info['value']), expected_text)))
        return is_value_present

    @staticmethod
    def wait_and_check_text_present_in_element_attribute(driver: WebDriver, locator_info: dict,
                                                         attribute: str,
                                                         expected_text: str, timeout=10):
        is_value_present_in_attr: bool = (WebDriverWait(driver, timeout).until(
            expected_conditions.text_to_be_present_in_element_attribute((locator_info['type'],
                                                                         locator_info['value']), attribute,
                                                                        expected_text)))
        return is_value_present_in_attr

    @staticmethod
    def wait_for_frame_to_be_available_and_switch_to_it(driver: WebDriver, frame_name_or_id_url: str,
                                                        timeout: 10):
        is_switched: bool = WebDriverWait(driver, timeout).until(
            expected_conditions.frame_to_be_available_and_switch_to_it(frame_name_or_id_url))
        return is_switched

    @staticmethod
    def wait_for_invisibility_of_element(driver: WebDriver, locator_info: dict, timeout=10):
        element: WebElement = WebDriverWait(driver, timeout).until(
            expected_conditions.invisibility_of_element(SeleniumHelper.get_web_element(driver, locator_info)))
        return element

    @staticmethod
    def wait_for_invisibility_of_element_located(driver: WebDriver, locator_info: dict, timeout=10):
        element: WebElement = WebDriverWait(driver, timeout).until(
            expected_conditions.invisibility_of_element_located((SeleniumHelper.get_web_element(driver, locator_info))))
        return element

    @staticmethod
    def wait_for_element_to_be_clickable(driver: WebDriver, locator_info: dict, timeout=10):
        element: WebElement = WebDriverWait(driver, timeout).until(
            expected_conditions.element_to_be_clickable(SeleniumHelper.get_web_element(driver, locator_info)))
        return element

    @staticmethod
    def wait_for_staleness_of_element(driver: WebDriver, locator_info: dict, timeout=10):
        is_stale: bool = WebDriverWait(driver, timeout).until(
            expected_conditions.staleness_of(SeleniumHelper.get_web_element(driver, locator_info)))
        return is_stale

    @staticmethod
    def wait_for_element_to_be_selected(driver: WebDriver, locator_info: dict, timeout=10):
        WebDriverWait(driver, timeout).until(
            expected_conditions.element_to_be_selected(SeleniumHelper.get_web_element(driver, locator_info)))

    @staticmethod
    def wait_for_element_located_to_be_selected(driver: WebDriver, locator_info: dict, timeout=10):
        WebDriverWait(driver, timeout).until(
            expected_conditions.element_located_to_be_selected((locator_info['type'], locator_info['value'])))

    @staticmethod
    def wait_for_element_selection_state_to_be(driver: WebDriver, locator_info: dict,
                                               selection_state: bool, timeout=10):
        is_selected: bool = WebDriverWait(driver, timeout).until(
            expected_conditions.element_selection_state_to_be(
                SeleniumHelper.get_web_element(driver, locator_info), selection_state))
        return is_selected

    @staticmethod
    def wait_for_element_located_selection_state_to_be(driver: WebDriver, locator_info: dict,
                                                       selection_state: bool, timeout=10):
        is_selected: bool = WebDriverWait(driver, timeout).until(
            expected_conditions.element_located_selection_state_to_be(
                (locator_info['type'], locator_info['value']), selection_state))
        return is_selected

    @staticmethod
    def wait_for_alert_is_present(driver: WebDriver, timeout=10):
        alert: Alert = WebDriverWait(driver, timeout).until(expected_conditions.alert_is_present())
        return alert

    # Alert class methods

    @staticmethod
    def accept_alert(driver: WebDriver) -> None:
        alert: Alert = SeleniumHelper.wait_for_alert_is_present(driver)
        alert.accept()

    @staticmethod
    def dismiss_alert(driver: WebDriver) -> None:
        alert: Alert = SeleniumHelper.wait_for_alert_is_present(driver)
        alert.dismiss()

    @staticmethod
    def enter_text_into_alert(driver: WebDriver, text: str) -> None:
        alert: Alert = SeleniumHelper.wait_for_alert_is_present(driver)
        alert.send_keys(text)

    @staticmethod
    def get_text_from_alert(driver: WebDriver) -> str:
        alert: Alert = SeleniumHelper.wait_for_alert_is_present(driver)
        return alert.text

    # WebDriver class methods
    @staticmethod
    def access_page_by_url(driver: WebDriver, url: str):
        driver.get(url)

    @staticmethod
    def get_web_element(driver: WebDriver, locator_info: dict) -> WebElement:
        element: WebElement = driver.find_element(locator_info['type'], locator_info['value'])
        return element

    @staticmethod
    def get_all_matching_web_elements(driver: WebDriver, locator_info: dict) -> list[WebElement]:
        elements: list[WebElement] = driver.find_elements(locator_info['type'], locator_info['value'])
        return elements

    @staticmethod
    def add_cookie_to_the_session(driver: WebDriver, cookie_dict: dict):
        driver.add_cookie(cookie_dict)

    @staticmethod
    def get_cookie_from_session(driver: WebDriver, cookie_name: str):
        return driver.get_cookie(cookie_name)

    @staticmethod
    def get_all_cookies_of_the_session(driver: WebDriver):
        return driver.get_cookies()

    @staticmethod
    def get_logs(driver: WebDriver, log_type: str):
        return driver.get_log(log_type)

    @staticmethod
    def get_credentials_of_the_session(driver: WebDriver):
        return driver.get_credentials()  # returns List[Credential]

    @staticmethod
    def get_downloadable_files(driver: WebDriver):
        return driver.get_downloadable_files()  # return dict

    @staticmethod
    def get_pinned_scripts_of_the_session(driver: WebDriver):
        return driver.get_pinned_scripts()  # returns list[str]

    @staticmethod
    def get_screenshot_as_base64(driver: WebDriver):
        return driver.get_screenshot_as_base64()

    @staticmethod
    def get_screenshot_as_file(driver: WebDriver, file_name: str) -> bool:
        return driver.get_screenshot_as_file(file_name)

    @staticmethod
    def get_screenshot_as_png(driver: WebDriver) -> bytes:
        return driver.get_screenshot_as_png()

    @staticmethod
    def get_current_window_handle(driver: WebDriver) -> str:
        return driver.current_window_handle  # returns window handle as str type of the current window

    @staticmethod
    def get_cache_of_the_accessing_application(driver: WebDriver):
        return driver.application_cache  # gets ApplicationCache type

    @staticmethod
    def get_current_caps(driver: WebDriver) -> dict:
        return driver.capabilities  # gets caps as dict

    @staticmethod
    def get_page_title(driver: WebDriver) -> str:
        return driver.title

    @staticmethod
    def switch_to_alert(driver: WebDriver, timeout=10) -> Alert:
        return SeleniumHelper.wait_for_alert_is_present(driver, timeout)

    @staticmethod
    def switch_to_frame(driver: WebDriver, frame_name_or_id_url: str, timeout: 10):
        if not SeleniumHelper.wait_for_frame_to_be_available_and_switch_to_it(
                driver, frame_name_or_id_url, timeout):
            Exception("Unable to switch to the given frame")

    @staticmethod
    def switch_to_parent_frame(driver: WebDriver):
        driver.switch_to.parent_frame()

    @staticmethod
    def switch_to_window(driver: WebDriver, window_name: str):
        driver.switch_to.window(window_name)

    @staticmethod
    def launch_and_switch_to_new_tab(driver: WebDriver):
        driver.switch_to.new_window("tab")

    @staticmethod
    def launch_and_switch_to_new_window(driver: WebDriver):
        driver.switch_to.new_window("window")

    @staticmethod
    def get_driver_name(driver: WebDriver) -> str:
        return driver.name

    @staticmethod
    def reload_the_page(driver: WebDriver) -> None:
        driver.refresh()

    @staticmethod
    def get_all_window_handles(driver: WebDriver) -> list[str]:
        return driver.window_handles  # return list[str]. All opened pages being returned here

    @staticmethod
    def delete_cookie_from_session(driver: WebDriver, cookie_to_delete: str) -> None:
        driver.delete_cookie(cookie_to_delete)

    @staticmethod
    def get_window_position_by_window_handle(driver: WebDriver, window_handle: str) -> dict:
        return driver.get_window_position(window_handle)

    @staticmethod
    def get_current_window_position(driver: WebDriver) -> dict:
        return driver.get_window_position(SeleniumHelper.get_current_window_handle(driver))

    @staticmethod
    def get_window_rect_info(driver: WebDriver) -> dict:
        return driver.get_window_rect()

    @staticmethod
    def get_window_size_by_window_handle(driver: WebDriver, window_handle: str) -> dict:
        return driver.get_window_size(window_handle)

    @staticmethod
    def get_current_window_size(driver: WebDriver) -> dict:
        return driver.get_window_size(SeleniumHelper.get_current_window_handle(driver))

    @staticmethod
    def add_session_credentials(driver: WebDriver, credential: Credential) -> None:
        driver.add_credential(credential)

    @staticmethod
    def remove_credentials_from_session(driver: WebDriver, credential_id: str | bytearray) -> None:
        driver.remove_credential(credential_id)

    @staticmethod
    def remove_all_credentials_from_session(driver: WebDriver) -> None:
        driver.remove_all_credentials()

    @staticmethod
    def go_to_previous_page(driver: WebDriver) -> None:
        driver.back()

    @staticmethod
    def go_to_next_page(driver: WebDriver) -> None:
        driver.forward()

    @staticmethod
    def delete_all_cookies_of_the_session(driver: WebDriver) -> None:
        driver.delete_all_cookies()

    @staticmethod
    def delete_a_cookie_from_session(driver: WebDriver, cookie_name: str) -> None:
        driver.delete_cookie(cookie_name)

    @staticmethod
    def execute_command(driver: WebDriver, command: str, params: dict | None = None) -> dict:
        return driver.execute(command, params)

    @staticmethod
    def execute_js_script(driver: WebDriver, script, args):
        driver.execute_script(script, args)

    @staticmethod
    def get_current_url(driver: WebDriver) -> str:
        return driver.current_url

    @staticmethod
    def save_captured_screenshot(driver: WebDriver, full_path: str) -> bool:
        return driver.save_screenshot(full_path)  # return bool type

    # WebElement class methods

    @staticmethod
    def clear_text_from_element(driver: WebDriver, locator_info: dict, attempts=3):
        cleared = False
        while attempts > 0 and not cleared:
            try:
                SeleniumHelper.get_web_element(driver, locator_info).clear()
                cleared = True
            except Exception as e:
                print(e)
            attempts = attempts - 1
        if not cleared and attempts == 0:
            RuntimeError("Unable to get clear text from element")
        return cleared

    @staticmethod
    def is_element_visible(driver: WebDriver, locator_info: dict, attempts=3) -> bool:
        visible = False
        while attempts > 0 and not visible:
            try:
                visible = SeleniumHelper.get_web_element(driver, locator_info).is_displayed()
            except Exception as e:
                print(e)
            attempts = attempts - 1
        if not visible and attempts == 0:
            RuntimeError("Unable to get element visible state with error")
        return visible

    @staticmethod
    def is_element_enabled(driver: WebDriver, locator_info: dict, attempts=3) -> bool:
        enabled = False
        while attempts > 0 and not enabled:
            try:
                enabled = SeleniumHelper.get_web_element(driver, locator_info).is_enabled()
            except Exception as e:
                print(e)
            attempts = attempts - 1
        if not enabled and attempts == 0:
            RuntimeError("Unable to get element enabled state with error")
        return enabled

    @staticmethod
    def is_element_selected(driver: WebDriver, locator_info: dict, attempts=3) -> bool:
        selected = False
        while attempts > 0 and not selected:
            try:
                selected = SeleniumHelper.get_web_element(driver, locator_info).is_selected()
            except Exception as e:
                print(e)
            attempts = attempts - 1
        if not selected and attempts == 0:
            RuntimeError("Unable to get element selection state with error")
        return selected

    @staticmethod
    def click_on_element(driver: WebDriver, locator_info: dict, attempts=3) -> None:
        is_clicked = False
        while attempts > 0 and not is_clicked:
            try:
                SeleniumHelper.get_web_element(driver, locator_info).click()
                is_clicked = True
            except Exception as e:
                print(e)
            attempts = attempts - 1
        if not is_clicked and attempts == 0:
            RuntimeError("Unable to click on element with error")

    @staticmethod
    def get_attribute_value(driver: WebDriver, locator_info: dict, attribute: str, attempts=3) -> str:
        is_retrieved = False
        value = ''
        while attempts > 0 and not is_retrieved:
            try:
                value = SeleniumHelper.get_web_element(driver, locator_info).get_attribute(attribute)
                is_retrieved = True
            except Exception as e:
                print(e)
            attempts = attempts - 1
        if not is_retrieved and attempts == 0:
            RuntimeError("Unable to retrieve attribute value from the element")
        return value

    @staticmethod
    def get_dom_attribute_value(driver: WebDriver, locator_info: dict, attribute: str, attempts=3) -> str:
        is_retrieved = False
        value = ''
        while attempts > 0 and not is_retrieved:
            try:
                value = SeleniumHelper.get_web_element(driver, locator_info).get_dom_attribute(attribute)
                is_retrieved = True
            except Exception as e:
                print(e)
            attempts = attempts - 1
        if not is_retrieved and attempts == 0:
            RuntimeError("Unable to retrieve attribute value from the element")
        return value

    @staticmethod
    def fill_element_with_input(driver: WebDriver, locator_info: dict, input_text: str, attempts=3) -> None:
        is_action_performed = False
        while not is_action_performed and attempts > 0:
            try:
                if SeleniumHelper.is_element_visible(driver, locator_info):
                    SeleniumHelper.get_web_element(driver, locator_info).send_keys(input_text)
                    is_action_performed = True
            except Exception as e:
                print(e)
            attempts = attempts - 1
        if not is_action_performed and attempts == 0:
            RuntimeError("Unable to enter input text into the element")

    @staticmethod
    def submit_on_element(driver: WebDriver, locator_info: dict, attempts=3) -> None:
        submitted = False
        while not submitted and attempts > 0:
            try:
                SeleniumHelper.get_web_element(driver, locator_info).submit()
                submitted = True
            except Exception as e:
                print(e)
            attempts = attempts - 1
        if not submitted and attempts == 0:
            RuntimeError("Unable to perform submit operation on element")

    @staticmethod
    def get_text_from_web_element(element: WebElement):
        return element.text

    @staticmethod
    def get_text_of_element_by_locator(driver: WebDriver, locator_info: dict):
        return SeleniumHelper.get_web_element(driver, locator_info).text

    @staticmethod
    def get_property(driver: WebDriver, locator_info: dict,
                     property_name: str) -> str | bool | WebElement | dict:
        return SeleniumHelper.get_web_element(driver, locator_info).get_property(property_name)

    @staticmethod
    def get_value_of_css_property(driver: WebDriver, locator_info: dict,
                                  property_name: str) -> str:
        return SeleniumHelper.get_web_element(driver, locator_info).value_of_css_property(property_name)

    @staticmethod
    def get_web_element_screenshot(driver: WebDriver, locator_info: dict, file_name: str) -> bool:
        return SeleniumHelper.get_web_element(driver, locator_info).screenshot(file_name)

    @staticmethod
    def enter_text_in_upper_case(driver: WebDriver, locator_info: dict, text: str):
        text = text.upper()
        SeleniumHelper.get_web_element(driver, locator_info).send_keys(text)

    @staticmethod
    def enter_text_in_lower_case(driver: WebDriver, locator_info: dict, text: str):
        text = text.lower()
        SeleniumHelper.get_web_element(driver, locator_info).send_keys(text)

    # Select class methods

    @staticmethod
    def deselect_all_options(driver: WebDriver, locator_info: dict) -> None:
        select: Select = Select(SeleniumHelper.get_web_element(driver, locator_info))
        select.deselect_all()

    @staticmethod
    def deselect_option_by_index(driver: WebDriver, locator_info: dict, index: int) -> None:
        select: Select = Select(SeleniumHelper.get_web_element(driver, locator_info))
        select.deselect_by_index(index)

    @staticmethod
    def select_option_by_index(driver: WebDriver, locator_info: dict, index: int) -> None:
        select: Select = Select(SeleniumHelper.get_web_element(driver, locator_info))
        select.select_by_index(index)

    @staticmethod
    def deselect_option_by_value(driver: WebDriver, locator_info: dict, value: str) -> None:
        select: Select = Select(SeleniumHelper.get_web_element(driver, locator_info))
        select.deselect_by_value(value)

    @staticmethod
    def select_option_by_value(driver: WebDriver, locator_info: dict, value: str) -> None:
        select: Select = Select(SeleniumHelper.get_web_element(driver, locator_info))
        select.select_by_value(value)

    @staticmethod
    def deselect_option_by_visible_text(driver: WebDriver, locator_info: dict, text: str) -> None:
        select: Select = Select(SeleniumHelper.get_web_element(driver, locator_info))
        select.deselect_by_visible_text(text)

    @staticmethod
    def select_option_by_visible_text(driver: WebDriver, locator_info: dict, text: str) -> None:
        select: Select = Select(SeleniumHelper.get_web_element(driver, locator_info))
        select.select_by_visible_text(text)

    @staticmethod
    def get_all_available_options_web_element(driver: WebDriver, locator_info: dict) -> list[WebElement]:
        select: Select = Select(SeleniumHelper.get_web_element(driver, locator_info))
        return select.options

    @staticmethod
    def get_all_available_options_text(driver: WebDriver, locator_info: dict) -> list[str]:
        all_options = []
        select: Select = Select(SeleniumHelper.get_web_element(driver, locator_info))
        for option in select.options:
            all_options.append(option.text)
        return all_options

    @staticmethod
    def get_all_selected_options_web_element(driver: WebDriver, locator_info: dict) -> list[WebElement]:
        select: Select = Select(SeleniumHelper.get_web_element(driver, locator_info))
        return select.all_selected_options

    @staticmethod
    def get_all_selected_options_text(driver: WebDriver, locator_info: dict) -> list[str]:
        all_options = []
        select: Select = Select(SeleniumHelper.get_web_element(driver, locator_info))
        for option in select.all_selected_options:
            all_options.append(option.text)
        return all_options

    @staticmethod
    def get_first_selected_option_web_element(driver: WebDriver, locator_info: dict) -> WebElement:
        select: Select = Select(SeleniumHelper.get_web_element(driver, locator_info))
        return select.first_selected_option

    @staticmethod
    def get_first_selected_option_text(driver: WebDriver, locator_info: dict) -> str:
        select: Select = Select(SeleniumHelper.get_web_element(driver, locator_info))
        return select.first_selected_option.text

    # Action chains related methods

    @staticmethod
    def move_to_element_and_click(driver: WebDriver, locator_info: dict):
        ActionChains(driver).move_to_element(SeleniumHelper.get_web_element(driver,
                                                                            locator_info)).click().perform()

    @staticmethod
    def move_to_web_element(driver: WebDriver, locator_info: dict):
        ActionChains(driver).move_to_element(SeleniumHelper.get_web_element(driver, locator_info)).perform()

    @staticmethod
    def enter_text_into_web_element_by_actions(driver: WebDriver, locator_info: dict, text: str):
        ActionChains(driver).click(SeleniumHelper.get_web_element(driver,
                                                                  locator_info)).send_keys(text).perform()

    @staticmethod
    def do_right_click_on_element(driver: WebDriver, locator_info: dict):
        ActionChains(driver).context_click(SeleniumHelper.get_web_element(driver, locator_info)).perform()

    @staticmethod
    def double_click_on_element(driver: WebDriver, locator_info: dict):
        ActionChains(driver).double_click(SeleniumHelper.get_web_element(driver, locator_info)).perform()

    @staticmethod
    def pause_for(driver: WebDriver, time_in_secs: int):
        ActionChains(driver).pause(time_in_secs).perform()

    @staticmethod
    def perform_command_operation(driver: WebDriver, key: str):
        ActionChains(driver).key_down(Keys.COMMAND).send_keys(key).key_up(Keys.COMMAND).perform()

    @staticmethod
    def perform_control_operation(driver: WebDriver, key: str):
        ActionChains(driver).key_down(Keys.CONTROL).send_keys(key).key_up(Keys.CONTROL).perform()

    @staticmethod
    def scroll_to_element(driver: WebDriver, locator_info: dict):
        ActionChains(driver).scroll_to_element(SeleniumHelper.get_web_element(driver, locator_info)).perform()

    @staticmethod
    def perform_drag_and_drop(driver: WebDriver, source: dict, target):
        ActionChains(driver).drag_and_drop(SeleniumHelper.get_web_element(driver, source),
                                           SeleniumHelper.get_web_element(driver, target)).perform()

    @staticmethod
    def click_and_hold_on_element(driver: WebDriver, locator_info: dict):
        ActionChains(driver).click_and_hold(SeleniumHelper.get_web_element(driver, locator_info)).perform()

    @staticmethod
    def release_click_hold_on_element(driver: WebDriver, locator_info: dict):
        ActionChains(driver).release(SeleniumHelper.get_web_element(driver, locator_info)).perform()

    @staticmethod
    def click_on_keyboard_enter_button(driver: WebDriver):
        ActionChains(driver).send_keys(Keys.ENTER).perform()

    @staticmethod
    def click_on_keyboard_home_button(driver: WebDriver):
        ActionChains(driver).send_keys(Keys.HOME).perform()

    @staticmethod
    def click_on_keyboard_end_button(driver: WebDriver):
        ActionChains(driver).send_keys(Keys.ENTER).perform()

    @staticmethod
    def click_on_keyboard_escape_button(driver: WebDriver):
        ActionChains(driver).send_keys(Keys.ESCAPE).perform()

    @staticmethod
    def click_on_keyboard_tab_button(driver: WebDriver):
        ActionChains(driver).send_keys(Keys.TAB).perform()

    @staticmethod
    def click_on_keyboard_alt_button(driver: WebDriver):
        ActionChains(driver).send_keys(Keys.ALT).perform()
