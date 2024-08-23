from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Set up Chrome WebDriver using webdriver-manager
options = webdriver.ChromeOptions()
options.headless = True  # Set to True if you do not want to open a visible browser window
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# URL of the webpage you want to scrape
url = "https://dps.psx.com.pk/announcements/companies"  # Replace with your actual URL

# Open the webpage
driver.get(url)

# Apply an explicit wait to ensure the page has loaded
wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds for conditions

# Handle iframes: Find all iframes and close them by switching to the main content
try:
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    for iframe in iframes:
        # Switch to each iframe
        driver.switch_to.frame(iframe)
        print("Switched to an iframe.")

        # Optionally, perform actions within the iframe or just note it
        # Here we are simply switching back to the default content
        driver.switch_to.default_content()

    print(f"Closed {len(iframes)} iframes and returned to the main content.")
except Exception as e:
    print(f"Error while handling iframes: {e}")

# Ensure we are in the main content before processing the XPath
driver.switch_to.default_content()

# Use XPath to find the element with the desired structure with explicit wait
try:
    # Wait for the presence of the desired element with explicit wait
    elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//table[@id='announcementsTable']/tbody[@class='tbl__body']/tr")))
    
    # Check if elements were found
    if elements:
        print(f"Found {len(elements)} rows.")
        for element in elements:
            print(element.text)
    else:
        print("No elements found with the provided XPath.")

except Exception as e:
    print(f"An error occurred while waiting for elements: {e}")

# Close the browser session
driver.quit()
