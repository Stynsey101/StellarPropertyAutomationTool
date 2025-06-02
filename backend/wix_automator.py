# backend/wix_automator.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# This function will set up the Selenium driver and log into Wix
def login_to_wix(email, password):
    """
    Initializes a Selenium WebDriver, navigates to the Wix login page,
    and performs the login operation.

    Args:
        email (str): The user's Wix email address.
        password (str): The user's Wix password.

    Returns:
        webdriver.Chrome: The authenticated WebDriver instance.
        Returns None if login fails.
    """
    print("Initializing browser...")
    # Sets up the Chrome driver automatically
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.maximize_window()

    wix_login_url = "https://users.wix.com/signin"
    driver.get(wix_login_url)
    print(f"Navigated to Wix login page: {wix_login_url}")

    try:
        # --- Step 1: Enter Email ---
        # Wait up to 15 seconds for the email input field to be present and visible
        email_field = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[data-testid="email"]'))
        )
        print("Email field located. Entering email...")
        email_field.send_keys(email)

        # --- Step 2: Click Continue ---
        # Find and click the 'Continue with Email' button
        continue_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="submit"]'))
        )
        continue_button.click()
        print("Clicked 'Continue with Email'.")

        # --- Step 3: Enter Password ---
        # Now, wait for the password field to appear
        password_field = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[data-testid="password"]'))
        )
        print("Password field located. Entering password...")
        password_field.send_keys(password)

        # --- Step 4: Click Login ---
        # Find and click the final login button
        login_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="submit"]'))
        )
        login_button.click()
        print("Login submitted. Verifying success...")

        # --- Step 5: Verify Successful Login ---
        # Wait for an element that only appears on the dashboard after login.
        # Based on your screenshot, the 'CMS' sidebar link is a good candidate.
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//div[text()='CMS']"))
        )
        print("✅ Login successful! Dashboard is visible.")
        return driver # Return the authenticated driver object for further use

    except Exception as e:
        print(f"❌ An error occurred during login: {e}")
        # Take a screenshot to help with debugging
        driver.save_screenshot("login_error.png")
        print("Screenshot 'login_error.png' saved for debugging.")
        driver.quit()
        return None