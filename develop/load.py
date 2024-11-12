import pandas as pd
import json

# File paths for your local machine
file_1 = r'C:\Users\nanda\OneDrive\Desktop\Anjana\Data Engineering\MusicApp\JSON scripts\response_1731370482411.json'
file_2 = r'C:\Users\nanda\OneDrive\Desktop\Anjana\Data Engineering\MusicApp\JSON scripts\response_1731427222631.json'
file_3 = r'C:\Users\nanda\OneDrive\Desktop\Anjana\Data Engineering\MusicApp\JSON scripts\response_1731427256227.json'

def load_data():
    # Load data from the JSON files with utf-8 encoding
    with open(file_1, encoding='utf-8') as f1, open(file_2, encoding='utf-8') as f2, open(file_3, encoding='utf-8') as f3:
        data_1 = json.load(f1)
        data_2 = json.load(f2)
        data_3 = json.load(f3)

    # Combine all the data into a single DataFrame
    df = pd.DataFrame(data_1 + data_2 + data_3)
    
    # Print the first few rows of the DataFrame to check the data
    print("DataFrame loaded:")
    print(df.head())  # Shows the first 5 rows of the DataFrame
    
    # Check for missing values before filling
    print("\nMissing values before filling:")
    print(df.isnull().sum())  # Display count of missing values for each column
    
    # Fill missing values for numeric columns with the mean
    numeric_columns = df.select_dtypes(include='number').columns
    df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())
    
    # Fill missing values for non-numeric columns (e.g., using a placeholder like "Unknown")
    non_numeric_columns = df.select_dtypes(exclude='number').columns
    df[non_numeric_columns] = df[non_numeric_columns].fillna("Unknown")
    
    # Check for missing values after filling
    print("\nMissing values after filling:")
    print(df.isnull().sum())  # Display count of missing values after filling
    
    return df