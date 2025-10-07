from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
import time

def js_click(driver, element):
    """Scrolls into view and executes click via JS (reliable fallback against overlays)."""
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
    driver.execute_script("arguments[0].click();", element)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
wait = WebDriverWait(driver, 15)

try:
    driver.get("https://demoqa.com/")

    # --- Remove fixed banner that often interferes with clicks ---
    driver.execute_script("""
        const el = document.getElementById('fixedban');
        if (el) { el.remove(); }
        const iframe = document.querySelector('iframe[title="Advertisement"]');
        if (iframe) iframe.remove();
    """)
    time.sleep(0.5)

    # 1) Click on "Widgets"
    widgets_card = wait.until(EC.presence_of_element_located((By.XPATH, "//h5[text()='Widgets']")))
    try:
        widgets_card.click()
    except ElementClickInterceptedException:
        js_click(driver, widgets_card)

    # 2) Click on "Progress Bar" in the side menu
    progress_link = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Progress Bar']")))
    try:
        progress_link.click()
    except ElementClickInterceptedException:
        js_click(driver, progress_link)

    # 3) Get Start button and the progress bar element
    start_btn = wait.until(EC.element_to_be_clickable((By.ID, "startStopButton")))
    progress_bar = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.progress-bar")))

    # 4) Start the progress bar
    try:
        start_btn.click()
    except ElementClickInterceptedException:
        js_click(driver, start_btn)

    # 5) Monitor and stop before 25%
    current_progress_value = 0
    # loop with a short interval to try and capture before 25%
    while True:
        value_str = progress_bar.get_attribute("aria-valuenow")
        try:
            current_progress_value = int(value_str)
        except (TypeError, ValueError):
            current_progress_value = 0
        # as soon as it reaches >=25, trigger the click to stop
        if current_progress_value >= 25:
            try:
                start_btn.click()  # clicks the same button to stop
            except ElementClickInterceptedException:
                js_click(driver, start_btn)
            break
        time.sleep(0.05)  # fine-tuning for quick reaction

    # 6) Validate <= 25%
    if current_progress_value <= 25:
        print(f"✅ Bar stopped at {current_progress_value}%, OK (<= 25%)")
    else:
        raise AssertionError(f"❌ Bar stopped at {current_progress_value}%, greater than 25%")

    # 7) Start again until 100%
    try:
        start_btn.click()
    except ElementClickInterceptedException:
        js_click(driver, start_btn)

    # wait until it reaches 100% (generous timeout)
    try:
        wait.until(lambda d: int(progress_bar.get_attribute("aria-valuenow")) >= 100)
    except TimeoutException:
        raise RuntimeError("Timeout exceeded waiting for the progress bar to reach 100%")

    print("✅ Bar reached 100%")

    # 8) Reset
    reset_btn = wait.until(EC.element_to_be_clickable((By.ID, "resetButton")))
    try:
        reset_btn.click()
    except ElementClickInterceptedException:
        js_click(driver, reset_btn)

    print("✅ Reset executed successfully")

finally:
    time.sleep(1)
    driver.quit()