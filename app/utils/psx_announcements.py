from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timezone
import os

def _find_project_root(current_path, marker_files=('.git', 'setup.py', 'requirements.txt')):
    # Keep traversing up until we find a known project file or directory
    while current_path != os.path.dirname(current_path):  # While we haven't reached the top
        if any(os.path.exists(os.path.join(current_path, marker)) for marker in marker_files):
            return current_path
        current_path = os.path.dirname(current_path)
    
    return None

def scrap_psx_company_announcement_page():
    # URL of the webpage you want to scrape
    url = "https://dps.psx.com.pk/announcements/companies"  # Replace with your actual URL
    
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Enable headless mode
    chrome_options.add_argument("--no-sandbox")  # Prevent sandboxing (necessary for some environments)
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

    # Load webdriver
    driver_file_name = os.getenv("CHROME_DRIVER_FILE_NAME")
    current_file_path = os.path.dirname(os.path.abspath(__file__))
    project_root_path = _find_project_root(current_file_path)
    chrome_driver_path = os.path.join(project_root_path, 'chrome_driver', driver_file_name)
    
    if  driver_file_name and os.path.exists(chrome_driver_path):
        # If chrome driver is placed in chrome_driver directory, we can access it from there
        print(f"loading chrome driver from {chrome_driver_path}")
        driver = webdriver.Chrome(service=ChromeService(chrome_driver_path), options=chrome_options)
    else:
        # Install and use Chrome Driver
        print("installing chrome driver")
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        # The chrome driver will be stored in following directories w.r.t os:
        # Windows
        # C:\Users\<YourUsername>\.wdm\drivers\chromedriver\<version>
        # Linux
        # /home/<YourUsername>/.wdm/drivers/chromedriver/<version>
        # macOS
        # /Users/<YourUsername>/.wdm/drivers/chromedriver/<version>
    
    # Open the webpage
    driver.get(url)
    fetch_date_time_epoch = datetime.now(timezone.utc).timestamp().__floor__()
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
                del row_data['']
                
                # converting date time to epoch
                datetime_str =  f"{row_data['DATE']} {row_data['TIME']}"
                # Define the format for parsing the datetime string
                datetime_format = "%b %d, %Y %I:%M %p"

                # Parse the datetime string into a datetime object
                datetime_obj = datetime.strptime(datetime_str, datetime_format)

                row_data['EPOCH'] = int(datetime_obj.timestamp())
                
                # extracting image and pdf links
                last_cell = cell_elements[-1]
                links = last_cell.find_elements(By.XPATH, ".//a")
                
                for link in enumerate(links):
                    link_text = link[1].text
                    # Check if pdf is available in last cell
                    if link_text == 'PDF':
                        row_data['PDF'] = link[1].get_attribute('href')
                    
                    # Check if 'View' is avaliable in last cell
                    elif link_text == 'View':
                        image_base_url = "https://dps.psx.com.pk/download/image"
                        image_id = link[1].get_attribute('data-images')
                        row_data['VIEW'] = f"{image_base_url}/{image_id}"
                

                # Append the row data to the table data list
                table_data.append(row_data)
        else:
            print("No elements found with the provided XPath.")

        return fetch_date_time_epoch, table_data

    except Exception as e:
        print(f"An error occurred while waiting for elements: {e}")

    finally:
        # Close the browser session
        driver.quit()
