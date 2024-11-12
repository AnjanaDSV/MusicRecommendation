import pandas as pd
import json

# File paths for your local machine
file_1 = r'C:\Users\nanda\OneDrive\Desktop\Anjana\Data Engineering\MusicApp\JSON scripts\response_1731370482411.json'
file_2 = r'C:\Users\nanda\OneDrive\Desktop\Anjana\Data Engineering\MusicApp\JSON scripts\response_1731427222631.json'
file_3 = r'C:\Users\nanda\OneDrive\Desktop\Anjana\Data Engineering\MusicApp\JSON scripts\response_1731427256227.json'

# Load data from the JSON files with utf-8 encoding
with open(file_1, encoding='utf-8') as f1, open(file_2, encoding='utf-8') as f2, open(file_3, encoding='utf-8') as f3:
    data_1 = json.load(f1)
    data_2 = json.load(f2)
    data_3 = json.load(f3)

# Combine all the data into a single DataFrame
df = pd.DataFrame(data_1 + data_2 + data_3)

# Display the DataFrame
print(df)

