import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('aviostable.csv')

# Update name of first column to destination
df.rename(columns={'One-way Avios prices': 'Destination'}, inplace=True)

# List of headers you want to process
columns_to_split = [
    'Economy Off-peak', 'Economy Peak', 'PremiumEconomy Off-peak',
    'PremiumEconomy Peak', 'Business Off-peak', 'Business Peak'
]

# Loop through each column in the list
for header_to_split in columns_to_split:
    # Create new column names
    points_col_name = f"{header_to_split} points"
    pounds_col_name = f"{header_to_split} pounds"
    
    # Check if the column exists in the DataFrame
    if header_to_split in df.columns:
        # Split the data in the specified header into points and pounds
        split_data = df[header_to_split].str.extract(r'(\d{1,3}(?:,\d{3})*) \+£([\d.]+)')
        
        # Handle NaN values before converting
        split_data[0] = split_data[0].fillna('0').str.replace(',', '').astype(int)  # Points column (replace NaN with '0')
        split_data[1] = split_data[1].fillna('0').astype(float)  # Pounds column (replace NaN with '0')
        
        # Assign the split data to the new columns
        df[points_col_name] = split_data[0]
        df[pounds_col_name] = split_data[1]
        
        # Optionally, drop the original column if no longer needed
        df.drop(columns=[header_to_split], inplace=True)

columns_to_pivot = df.columns[df.columns != 'Destination']

# Create an empty list to store the reshaped rows
reshaped_rows = []

# Iterate over the destinations in the DataFrame
for destination in df['Destination']:
    # Extract points and pounds for each of the columns
    for col in columns_to_pivot:
        # Extract class, peak/off-peak, and points/pounds information from the column name
        class_type, peak_or_off_peak, points_or_pounds = col.split(' ', 2)
        
        # Get the value for points or pounds for this destination and column
        points_or_pounds_value = df.loc[df['Destination'] == destination, col].values[0]
        
        # We want to keep both Points and Pounds in the same row
        if points_or_pounds == 'points':
            points = points_or_pounds_value
            pounds = None
        else:
            points = None
            pounds = points_or_pounds_value

        # Add the row data to reshaped_rows
        reshaped_rows.append({
            "Destination": destination,
            "Class": class_type,
            "Peak or Off-peak": peak_or_off_peak,
            "Points": points,
            "Pounds": pounds
        })

# Create a DataFrame from the reshaped data
reshaped_df = pd.DataFrame(reshaped_rows)

# Fill missing points or pounds with the last valid observation
reshaped_df = reshaped_df.groupby(['Destination', 'Class', 'Peak or Off-peak'], group_keys=False).apply(
    lambda group: group.ffill().bfill()
).reset_index(drop=True)

# Show the reshaped DataFrame
print(reshaped_df)

# Save the updated DataFrame back to CSV
df.to_csv('updated_aviostable.csv', index=False)
print("Updated DataFrame saved to 'updated_aviostable.csv'.")