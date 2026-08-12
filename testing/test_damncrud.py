import os

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = os.getenv(
    "BASE_URL",
    "http://localhost/DamnCRUD/"
)

USERNAME = os.getenv("TEST_USERNAME", "admin")
PASSWORD = os.getenv("TEST_PASSWORD", "admin")


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 15)

    # Login sebagai precondition
    driver.get(BASE_URL + "login.php")

    wait.until(
        EC.presence_of_element_located(
            (By.NAME, "username")
        )
    ).send_keys(USERNAME)

    driver.find_element(
        By.NAME, "password"
    ).send_keys(PASSWORD)

    driver.find_element(
        By.CSS_SELECTOR,
        "button[type='submit']"
    ).click()

    try:
        wait.until(EC.url_contains("index.php"))
    except Exception:
        print("LOGIN FAILED")
        print("Current URL:", driver.current_url)
        print(
            driver.find_element(
                By.TAG_NAME,
                "body"
            ).text
        )
        driver.quit()
        raise

    yield driver

    driver.quit()


# =========================================================
# TC-CRT-01
# Create Contact
# =========================================================

def test_TC_CRT_01_create_contact(driver):

    wait = WebDriverWait(driver, 10)

    driver.get(BASE_URL + "create.php")

    wait.until(
        EC.presence_of_element_located(
            (By.ID, "name")
        )
    ).send_keys("Selenium Test")

    driver.find_element(
        By.ID, "email"
    ).send_keys("selenium@test.com")

    driver.find_element(
        By.ID, "phone"
    ).send_keys("081234567890")

    driver.find_element(
        By.ID, "title"
    ).send_keys("Software Tester")

    driver.find_element(
        By.CSS_SELECTOR,
        "input[type='submit'][value='Save']"
    ).click()

    wait.until(EC.url_contains("index.php"))

    search_box = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[type='search']")
        )
    )

    search_box.send_keys("Selenium Test")

    page_text = driver.find_element(
        By.TAG_NAME,
        "body"
    ).text

    assert "Selenium Test" in page_text
    assert "selenium@test.com" in page_text


# =========================================================
# TC-UPD-02
# Update Contact
# =========================================================

def test_TC_UPD_02_update_contact(driver):

    wait = WebDriverWait(driver, 10)

    driver.get(BASE_URL + "index.php")

    edit_link = wait.until(
        EC.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                "table#employee a[href*='update.php?id=']"
            )
        )
    )

    edit_link.click()

    wait.until(
        EC.presence_of_element_located(
            (By.ID, "name")
        )
    )

    name = driver.find_element(By.ID, "name")
    email = driver.find_element(By.ID, "email")
    phone = driver.find_element(By.ID, "phone")
    title = driver.find_element(By.ID, "title")

    name.clear()
    email.clear()
    phone.clear()
    title.clear()

    name.send_keys("Selenium Updated")
    email.send_keys("updated@test.com")
    phone.send_keys("089876543210")
    title.send_keys("QA Engineer")

    driver.find_element(
        By.CSS_SELECTOR,
        "input[type='submit'][value='Update']"
    ).click()

    wait.until(EC.url_contains("index.php"))

    page_text = driver.find_element(
        By.TAG_NAME,
        "body"
    ).text

    assert "Selenium Updated" in page_text
    assert "updated@test.com" in page_text


# =========================================================
# TC-DEL-02
# Cancel Delete
# =========================================================

def test_TC_DEL_02_cancel_delete(driver):

    wait = WebDriverWait(driver, 10)

    driver.get(BASE_URL + "index.php")

    first_row = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#employee tbody tr")
        )
    )

    original_row_text = first_row.text

    delete_link = first_row.find_element(
        By.CSS_SELECTOR,
        "a[href*='delete.php?id=']"
    )

    delete_link.click()

    alert = wait.until(
        EC.alert_is_present()
    )

    assert "Are you sure" in alert.text

    alert.dismiss()

    wait.until(EC.url_contains("index.php"))

    page_text = driver.find_element(
        By.TAG_NAME,
        "body"
    ).text

    first_name_in_row = original_row_text.split()[1]

    assert first_name_in_row in page_text


# =========================================================
# TC-PRF-02
# Upload JPG
# =========================================================

def test_TC_PRF_02_upload_jpg(driver):

    wait = WebDriverWait(driver, 10)

    driver.get(BASE_URL + "profil.php")

    file_input = wait.until(
        EC.presence_of_element_located(
            (
                By.CSS_SELECTOR,
                "input[type='file']"
            )
        )
    )

    file_path = os.path.join(
        os.path.dirname(__file__),
        "foto_test.jpg"
    )

    assert os.path.exists(
        file_path
    ), "File foto_test.jpg tidak ditemukan."

    file_input.send_keys(file_path)

    driver.find_element(
        By.CSS_SELECTOR,
        "button[type='submit']"
    ).click()

    wait.until(
        EC.url_contains("profil.php")
    )

    heading = wait.until(
        EC.presence_of_element_located(
            (By.TAG_NAME, "h2")
        )
    )

    assert heading.text == "Profil"


# =========================================================
# TC-VPG-01
# Input Thing Parameter
# =========================================================

def test_TC_VPG_01_input_thing(driver):

    wait = WebDriverWait(driver, 10)

    driver.get(BASE_URL + "vpage.php")

    thing_input = wait.until(
        EC.presence_of_element_located(
            (By.NAME, "thing")
        )
    )

    thing_input.send_keys(
        "Selenium Testing"
    )

    driver.find_element(
        By.CSS_SELECTOR,
        "input[type='submit'][value='Submit']"
    ).click()

    wait.until(
        EC.url_contains("thing=Selenium")
    )

    page_text = driver.find_element(
        By.TAG_NAME,
        "body"
    ).text

    assert "Your thing is Selenium Testing" in page_text