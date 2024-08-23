from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Enable headless mode
chrome_options.add_argument("--no-sandbox")  # Prevent sandboxing (necessary for some environments)
chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

# Set up Chrome WebDriver with options
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

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
    header_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//table[@id='announcementsTable']/thead/tr/th")))
    headers = [header.text.strip() for header in header_elements]

    # Extract table rows
    row_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//table[@id='announcementsTable']/tbody[@class='tbl__body']/tr")))

    # Initialize a list to hold row data
    table_data = []

    if row_elements:
        print(f"Found {len(row_elements)} rows.")

        for row_element in row_elements:
            # Extract all the cells (td) within a row
            cell_elements = row_element.find_elements(By.TAG_NAME, "td")
            
            # Create a dictionary for each row with headers as keys and cell text as values
            row_data = {headers[i]: cell.text.strip() for i, cell in enumerate(cell_elements)}
            
            last_cell = cell_elements[-1]

            # TODO: Check if 'View' is avaliable in last cell
                # If yes, extract the 'data-images' attribute (it contains document id, which can be merged with sarmaya site)
            # TODO: Check if pdf is available in last cell
                # If yes, extract the link (it's a relative link, it can be combined with dps.psx.com.pk)
            # TODO: Combine Date & Time to make a datetime attribute

            # Append the row data to the table data list
            table_data.append(row_data)
    else:
        print("No elements found with the provided XPath.")

    print("Table Data: \n", table_data)
except Exception as e:
    print(f"An error occurred while waiting for elements: {e}")

# Close the browser session
driver.quit()
