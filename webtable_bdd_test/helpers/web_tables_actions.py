import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def create_record(driver, first_name, last_name, email, age, salary, department):
    driver.find_element(By.ID, "addNewRecordButton").click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "firstName")))
    driver.find_element(By.ID, "firstName").send_keys(first_name)
    driver.find_element(By.ID, "lastName").send_keys(last_name)
    driver.find_element(By.ID, "userEmail").send_keys(email)
    driver.find_element(By.ID, "age").send_keys(str(age))
    driver.find_element(By.ID, "salary").send_keys(str(salary))
    driver.find_element(By.ID, "department").send_keys(department)
    driver.find_element(By.ID, "submit").click()
    time.sleep(0.5)

def edit_record(driver, index, new_first_name):
    driver.find_element(By.ID, f"edit-record-{index}").click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "firstName")))
    first_name_input = driver.find_element(By.ID, "firstName")
    first_name_input.clear()
    first_name_input.send_keys(new_first_name)
    driver.find_element(By.ID, "submit").click()
    time.sleep(0.5)

def delete_record(driver, index):
    driver.find_element(By.ID, f"delete-record-{index}").click()
    time.sleep(0.5)
