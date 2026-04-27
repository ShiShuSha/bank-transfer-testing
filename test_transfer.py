import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = 'http://127.0.0.1:8000/?balance=30000&reserved=20001'


def open_transfer(driver):
    driver.get(BASE_URL)

    account = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Рубли') or contains(text(),'Рубли')]"))
    )

    account.click()


def test_commission_rounding(driver):
    open_transfer(driver)

    inputs = driver.find_elements(By.TAG_NAME, 'input')

    inputs[0].send_keys('1111222233334444')
    time.sleep(1)

    inputs = driver.find_elements(By.TAG_NAME, 'input')
    inputs[1].send_keys('99')

    body = driver.page_source

    assert '9' in body


def test_card_length_limit(driver):
    open_transfer(driver)

    card_input = driver.find_elements(By.TAG_NAME, 'input')[0]

    card_input.send_keys('11112222333344445')

    value = card_input.get_attribute('value')

    assert value == '1111222233334444'


def test_negative_amount(driver):
    open_transfer(driver)

    inputs = driver.find_elements(By.TAG_NAME, 'input')

    inputs[0].send_keys('1111222233334444')
    time.sleep(1)

    inputs = driver.find_elements(By.TAG_NAME, 'input')
    inputs[1].send_keys('-100')

    value = inputs[1].get_attribute('value')

    assert value == ''