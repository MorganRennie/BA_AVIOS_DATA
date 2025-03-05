#This first section of code finds the datatable from the URL, extracts the column headers from the first two rows,
#and then appends the remaining data. The new table is then saved to the parent folder.

!pip install requests beautifulsoup4 pandas
!pip install cloudscraper

import requests
from bs4 import BeautifulSoup
import pandas as pd
import cloudscraper

scraper = cloudscraper.create_scraper()

# URL of the webpage, sectioned off in case it changes.
url = 'https://www.headforpoints.com/2024/08/29/how-many-avios-do-i-need-to-fly-to-2/'

# Send a GET request to the URL
response = scraper.get(url)

# Check if the request was successful
if response.status_code == 200:
    # if the code is successful: 

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the table by ID, if the table name changes, update the id.
    table = soup.find('figure', id='aviostable').find('table')

    # if we successfully find the table: 
    if table is not None:
        
        # Extract the header rows
        header_rows = table.find_all('tr')[:2]  # Get the first two rows for headers as the table is set up split.

        # Initialize headers list
        headers = []

        # Append the first header from the first row
        first_header = header_rows[0].find_all('th')[0].text.strip()
        headers.append(first_header)

        # Extract and merge the remaining headers
        header1_cells = header_rows[0].find_all('th')[1:]  # First row headers excluding the first cell
        header2_cells = header_rows[1].find_all('th')[1:]  # Second row headers excluding the first cell

        # Merge headers into a single list
        for header1, header2 in zip(header1_cells, header2_cells):
            h1 = header1.text.strip()
            h2 = header2.text.strip()
            
            # Merge headers if both are non-empty
            if h1 and h2:
                merged_header = f"{h1} {h2}"
                headers.append(merged_header)

        # Extract table rows starting after the header rows
        rows = []
        for tr in table.find_all('tr')[2:]:  # Skip the first two header rows
            cells = [td.text.strip() for td in tr.find_all('td')]
            if cells:  # Ensure there's data in the row
                rows.append(cells)

        # Create a DataFrame with the merged headers
        df = pd.DataFrame(rows, columns=headers)
        
        # Save the DataFrame to a CSV file
        df.to_csv("aviostable.csv", index=False)
        print("Success. Saved as aviostable.csv in parent folder.")
        
    # else if the table is not found from the URL: 
    else:
        print("Table not found")
        
# else if we have failed to access the website
else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)
