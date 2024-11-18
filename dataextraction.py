import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the webpage, sectioned off in case it changes.
url = 'https://www.headforpoints.com/2024/08/29/how-many-avios-do-i-need-to-fly-to-2/'

# Set up headers to mimic a browser request: website was set up to automatically reject access.
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Referer": "https://www.google.com",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
}

# Send a GET request to the URL with the headers
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # if the code is successful: 

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the table by ID, if the table name changes, update the id.
    table = soup.find('figure', id='aviostable').find('table')

    if table is not None:
        # if we successfully find the table: 
        # Extract the header rows
        header_rows = table.find_all('tr')[:2]  # Get the first two rows of headers

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
        df = pd.DataFrame(rows, columns=headers)  # Use the merged headers

        # Check the number of columns in the data and compare with headers
        print(f"Number of rows: {len(rows)}, Expected columns: {len(headers)}")
        
        # Save the DataFrame to a CSV file
        df.to_csv('aviostable.csv', index=False)
        print("Data has been extracted and saved to aviostable.csv.")
    # if the table is not found in the extracted html: 
    else:
        print("Table not found in the HTML.")
# if we have failed to access the website
else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)
