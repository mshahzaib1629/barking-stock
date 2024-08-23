from bs4 import BeautifulSoup
from lxml import etree
import requests

# Sample HTML
html_content = """
<html>
    <head>
        <title>Example Title</title>
        <script type="text/javascript">
            console.log("Sample script");
        </script>
    </head>
    <body>
        <div id="announcements-watch_wrapper">
            <div class="row">
                <div class="col-sm-12">
                    <table id="announcements-watch">
                        <tbody>
                            <tr><td>Row 1</td></tr>
                            <tr><td>Row 2</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </body>
</html>
"""

# URL of the webpage containing the table
url = "https://sarmaaya.pk/psx/announcements"

# Send a GET request to the webpage
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

table = soup.find(id='announcements-watch')

headers = [header.text.strip() for header in table.find_all('th')]
rows = table.find_all('tr')

print("TABLE: ", len(rows))

# Process and print the filtered rows
for row in rows:
    cells = [cell.text.strip() for cell in row.find_all('td')]
    print(dict(zip(headers, cells))) 


# Xpath for table rows:
# //div[@id='announcements-watch_wrapper']/div[@class='row'][2]/div[@class='col-sm-12']/table[@id='announcements-watch']/tbody/tr