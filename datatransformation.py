import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('aviostable.csv')

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

# Print the updated DataFrame
print(df.head())  # Display the first few rows to verify changes

# Save the updated DataFrame back to CSV
df.to_csv('updated_aviostable.csv', index=False)
print("Updated DataFrame saved to 'updated_aviostable.csv'.")
