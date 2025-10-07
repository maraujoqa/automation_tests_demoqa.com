from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# WebDriver Configuration (Chrome, in this example)
driver = webdriver.Chrome()
driver.maximize_window()

try:
    # 1️⃣ Access the main website
    driver.get("https://demoqa.com/")

    # 2️⃣ Click on "Interactions"
    interactions_card = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//h5[text()='Interactions']"))
    )
    interactions_card.click()

    # 3️⃣ Click on "Sortable"
    sortable_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Sortable']"))
    )
    sortable_link.click()

    # Wait for the item list to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "demo-tabpane-list"))
    )

    # 4️⃣ Capture all list items
    list_items = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#demo-tabpane-list .list-group-item"))
    )

    # Extract the text of each item (e.g., ["One", "Two", "Three", "Four", "Five", "Six"])
    item_texts = [item.text.strip() for item in list_items]

    # Define the expected correct order
    expected_ascending_order = ["One", "Two", "Three", "Four", "Five", "Six"]

    print("Current order:", item_texts)

    # 5️⃣ Check if they are already in ascending order
    if item_texts == expected_ascending_order:
        print("✅ Elements are already in ascending order. No action needed.")
    else:
        print("🔄 Reorganizing items to ascending order...")

        actions = ActionChains(driver)

        # Reorder via drag and drop
        # The logic iterates through the target order and moves the corresponding item to its correct position (i)
        for i, target_item_text in enumerate(expected_ascending_order):
            # Find the index of the item we need to move
            current_index = item_texts.index(target_item_text)

            # If the item is not already in the correct position (i)
            if current_index != i:
                # The item element to be dragged (current location)
                source_element = list_items[current_index]
                # The element to drop onto (target location)
                target_element = list_items[i]
                
                # Perform the drag-and-drop action
                actions.click_and_hold(source_element).move_to_element(target_element).pause(0.5).release().perform()
                time.sleep(0.5) # Wait for UI to update

                # Update the local list_items list after the drag/drop
                list_items = driver.find_elements(By.CSS_SELECTOR, "#demo-tabpane-list .list-group-item")
                
                # Update the local text list to reflect the new state for next iteration
                item_texts.pop(current_index)
                item_texts.insert(i, target_item_text)

        print("✅ Items successfully reorganized!")

finally:
    # Wait a few seconds to view before closing
    time.sleep(3)
    driver.quit()