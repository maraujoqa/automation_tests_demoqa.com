import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_nova_janela_demoqa():
    """Automated test that validates opening and switching between windows on demoqa.com."""

    # Setup Chrome WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        print("🔹 Starting browser setup...")
        driver.implicitly_wait(10)
        wait = WebDriverWait(driver, 10)

        # 1️⃣ Access site
        driver.get("https://demoqa.com/")
        driver.maximize_window()
        print("✅ Access to 'demoqa.com' successful.")

        # 2️⃣ Choose the "Alerts, Frame & Windows" option on the home page
        print("🔹 Navigating to 'Alerts, Frame & Windows'...")
        alerts_frames_windows_card = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='card mt-4 top-card'][3]"))
        )
        alerts_frames_windows_card.click()
        print("✅ Navigation to 'Alerts, Frame & Windows' successful.")

        # 3️⃣ Select the "Browser Windows" submenu
        print("🔹 Opening 'Browser Windows' submenu...")
        browser_windows_item = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Browser Windows']"))
        )
        browser_windows_item.click()
        print("✅ 'Browser Windows' page opened successfully.")

        main_window_handle = driver.current_window_handle
        print(f"ℹ️ Main window handle captured: {main_window_handle}")

        # 4️⃣ Click the 'New Window' button
        print("🔹 Clicking 'New Window' button...")
        new_window_button = wait.until(
            EC.element_to_be_clickable((By.ID, "windowButton"))
        )
        new_window_button.click()
        print("✅ 'New Window' button clicked successfully.")

        # 5️⃣ Validate new window opened
        handles = driver.window_handles
        if len(handles) > 1:
            print(f"✅ New window detected. Handles found: {handles}")
        else:
            print("❌ New window not opened. Only one handle found.")
            raise AssertionError("New window not opened.")

        new_window_handle = [h for h in handles if h != main_window_handle][0]
        driver.switch_to.window(new_window_handle)
        print(f"✅ Focus switched to new window: {new_window_handle}")

        # Validate the message "This is a sample page"
        print("🔹 Validating message in the new window...")
        sample_page_text_element = wait.until(
            EC.presence_of_element_located((By.ID, "sampleHeading"))
        )
        validated_message = sample_page_text_element.text

        if validated_message == "This is a sample page":
            print(f"✅ Message validated successfully: '{validated_message}'")
        else:
            print(f"❌ Unexpected message found: '{validated_message}'")
            raise AssertionError(f"Expected 'This is a sample page' but found '{validated_message}'")

        # 6️⃣ Close the newly opened window
        driver.close()
        print("✅ New window closed successfully.")

        # Return focus to the main window
        driver.switch_to.window(main_window_handle)
        print("✅ Focus returned to main window.")

        # Final pause for viewing
        time.sleep(3)

        print("\n🎯 TEST FINISHED SUCCESSFULLY — ALL STEPS VALIDATED ✅")

    except Exception as e:
        print("\n❌ --- ERROR DURING TEST EXECUTION ---")
        print(f"❌ Exception: {type(e).__name__}: {e}")
        raise

    finally:
        # Ensures browser closure even if an exception occurs
        if 'driver' in locals():
            try:
                driver.quit()
                print("🧹 Browser closed. Test finished.")
            except Exception as e:
                print(f"⚠️ Error closing browser: {e}")


if __name__ == "__main__":
    test_nova_janela_demoqa()
