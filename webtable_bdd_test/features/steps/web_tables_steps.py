from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from helpers.web_tables_actions import create_record, edit_record, delete_record

@given("I am on the Web Tables page")
def step_open_webtables_page(context):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    context.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    context.driver.get("https://demoqa.com/")
    # Click on Elements
    WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//h5[text()='Elements']"))
    ).click()
    # Click on Web Tables
    WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Web Tables']"))
    ).click()

@when("I create 12 dynamic records")
def step_create_12_records(context):
    for i in range(1, 13):
        create_record(
            context.driver,
            f"User{i}",
            f"Test{i}",
            f"user{i}@mail.com",
            25 + i,
            30000 + (i * 1000),
            "QA"
        )

@then("I delete all dynamic records")
def step_delete_all_records(context):
    for i in range(4, 16):
        try:
            delete_record(context.driver, i)
        except Exception:
            pass
    context.driver.quit()
