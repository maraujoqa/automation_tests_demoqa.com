import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path 

# Name and path in the directory where the script is running.
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
FILE_NAME = "file_for_upload.txt"
FILE_PATH = os.path.join(DIRETORIO_ATUAL, FILE_NAME)

# Creates the temporary file (just an empty file)
try:
    Path(FILE_PATH).touch() 
    print(f"✅ Temporary file '{FILE_NAME}' created in: {FILE_PATH}")
except Exception as e:
    print(f"❌ Error creating temporary file: {e}")
    # Do not proceed if the file cannot be created
    exit()

browser = None 
try:
    print("🔹 Starting browser setup...")
    browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    browser.maximize_window()
    browser.implicitly_wait(10)
    browser.get("https://demoqa.com/")
    print("✅ Access to 'demoqa.com' successful.")
    
    # 1. Choose the "Forms" option on the home page
    forms_card = browser.find_element(By.XPATH, "//h5[text()='Forms']")
    forms_card.click()
    print("✅ Navigation to 'Forms' section complete.")
    
    # 2. Select the "Practice Forms" submenu
    practice_form_locator = (By.XPATH, "//li[contains(., 'Practice Form')]")
    practice_form_link = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable(practice_form_locator)
    )
    practice_form_link.click()
    print("✅ Navigation to 'Practice Forms' section complete.")
    browser.execute_script("window.scrollTo(0, 300);")
    time.sleep(1)
    
    # 3. Basic data
    browser.find_element(By.ID, "firstName").send_keys("Matheus")
    browser.find_element(By.ID, "lastName").send_keys("Araujo")
    browser.find_element(By.ID, "userEmail").send_keys("test.matheus@example.com")
    print("✅ Basic data filled successfully.")
    
    # 4. Gender
    browser.find_element(By.XPATH, "//label[text()='Male']").click() 
    print("✅ Gender selected successfully.")
    
    # 5. Mobile number
    browser.find_element(By.ID, "userNumber").send_keys("9876543210")
    print("✅ Phone number filled successfully.")

    # 6. Date of Birth
    browser.find_element(By.ID, "dateOfBirthInput").click()
    print("🔹 Calendar pop-up opened.")
    year_select_element = browser.find_element(By.CLASS_NAME, "react-datepicker__year-select")
    year_select = Select(year_select_element)
    year_select.select_by_value("1995")
    print("✅ Year '1995' selected.")
    month_select_element = browser.find_element(By.CLASS_NAME, "react-datepicker__month-select")
    month_select = Select(month_select_element)
    month_select.select_by_index(3) 
    print("✅ Month 'April' selected.")
    day_locator = (By.XPATH, "//div[contains(@class, 'react-datepicker__day') and text()='14']")
    day_14 = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable(day_locator)
    )
    day_14.click()
    print("✅ Day '14' clicked. Date filled: 14 Apr 1995.")
    
    # 7. Subjects
    subject_input = browser.find_element(By.ID, "subjectsInput")
    subject_input.send_keys("Arts")
    subject_input.send_keys(Keys.ENTER)
    print("✅ Subject filled successfully.")
    
    # 8. Hobby
    browser.find_element(By.XPATH, "//label[text()='Music']").click()
    print("✅ Hobby 'Music' selected.")

    # 9. Submit a txt. file (usando o FILE_PATH dinâmico)
    browser.find_element(By.ID, "uploadPicture").send_keys(FILE_PATH)
    print(f"✅ File uploaded successfully. Path sent: {FILE_PATH}")
 
    # 10. Current Address
    browser.find_element(By.ID, "currentAddress").send_keys("Street Automation, N° 123, Neighborhood Python, City Selenium")
    print("✅ Current address filled successfully.")

    # 11. State and City
    state_input = browser.find_element(By.ID, "react-select-3-input")
    state_input.send_keys("NCR")
    state_input.send_keys(Keys.ENTER)
    print("✅ State selected successfully.")
    
    city_input = browser.find_element(By.ID, "react-select-4-input")
    city_input.send_keys("Delhi")
    city_input.send_keys(Keys.ENTER)
    print("✅ City selected successfully.")
    
    print("✅ Form filled successfully. All fields completed.")

    # --- SUBMISSION AND VALIDATION ---
    
    # 12. Submit the form
    submit_button = browser.find_element(By.ID, "submit")
    browser.execute_script("arguments[0].click();", submit_button)
    print("🔹 Submitting form...")
    print("✅ Form submitted successfully.")

    # 13. Ensure the pop-up has been opened
    modal_locator = (By.CLASS_NAME, "modal-content")
    WebDriverWait(browser, 10).until(EC.visibility_of_element_located(modal_locator))
    print("✅ Confirmation popup detected.")

    # 14. Pause for visual confirmation
    time.sleep(5)

    # 15. Close popup
    close_button = browser.find_element(By.ID, "closeLargeModal")
    close_button.click()
    print("✅ Popup closed successfully.")
    
    print("\n🎯 TEST FINISHED SUCCESSFULLY — ALL STEPS VALIDATED ✅")

except Exception as e:
    print(f"\n❌ --- ERROR DURING TEST ---")
    print(f"❌ An error occurred: {type(e).__name__}: {e}")

finally:
    # --- TEARDOWN ---
    # 1. Browser closed
    if browser:
        browser.quit()
        print("🧹 Browser closed.")
        
    # 2. Remove the temporary file
    if os.path.exists(FILE_PATH):
        os.remove(FILE_PATH)
        print(f"🧹 Temporary file '{FILE_NAME}' removed.")