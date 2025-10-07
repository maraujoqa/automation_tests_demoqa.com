import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def setup_driver():
    """Setup Chrome WebDriver."""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    return driver


def create_record(driver, first_name, last_name, email, age, salary, department):
    """Create a new record in Web Tables."""
    print(f"Creating new record: {first_name} {last_name}")
    driver.find_element(By.ID, "addNewRecordButton").click()

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "firstName")))

    driver.find_element(By.ID, "firstName").send_keys(first_name)
    driver.find_element(By.ID, "lastName").send_keys(last_name)
    driver.find_element(By.ID, "userEmail").send_keys(email)
    driver.find_element(By.ID, "age").send_keys(str(age))
    driver.find_element(By.ID, "salary").send_keys(str(salary))
    driver.find_element(By.ID, "department").send_keys(department)

    driver.find_element(By.ID, "submit").click()
    print(f"Record {first_name} created successfully.\n")
    time.sleep(1)


def edit_record(driver, index, new_first_name):
    """Edit a record based on its index."""
    print(f"Editing the first name record to {new_first_name}")
    edit_button = driver.find_element(By.ID, f"edit-record-{index}")
    edit_button.click()

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "firstName")))

    first_name_input = driver.find_element(By.ID, "firstName")
    first_name_input.clear()
    first_name_input.send_keys(new_first_name)

    driver.find_element(By.ID, "submit").click()
    print(f"Record edited successfully.\n")
    time.sleep(1)


def delete_record(driver, index):
    """Delete a record based on its index."""
    print(f"Deleting record ")
    delete_button = driver.find_element(By.ID, f"delete-record-{index}")
    delete_button.click()
    print(f"Record deleted successfully.\n")
    time.sleep(1)


def main():
    driver = setup_driver()

    try:
        # Step 1: Access the site
        driver.get("https://demoqa.com/")
        print("Accessing https://demoqa.com/")

        # Step 2: Click on 'Elements'
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//h5[text()='Elements']"))).click()
        print("Clicked on 'Elements'")

        # Step 3: Click on 'Web Tables' submenu
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Web Tables']"))).click()
        print("Accessed 'Web Tables' page.\n")

        # Step 4: Create a new record
        create_record(driver, "Matheus", "Araújo", "matheus.araujo@example.com", 30, 50000, "Engineering")

        # Step 5: Edit the new record (index 4 – as the 3 first ones are default)
        edit_record(driver, 4, "Felipe")

        # Step 6: Delete the record
        delete_record(driver, 4)

    except Exception as e:
        print(f"❌ Test failed: {e}")

    finally:
        time.sleep(3)
        driver.quit()


if __name__ == "__main__":
    main()
