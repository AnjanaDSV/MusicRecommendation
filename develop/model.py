import load  # Import the load.py module
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

# Load the data using load.py
df = load.load_data()  # This will call the load_data() function defined in load.py

# Extract the relevant features
features = df[['danceability', 'energy', 'acousticness', 'popularity']]

# Optionally, normalize the features
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

# Calculate the cosine similarity between tracks
similarity_matrix = cosine_similarity(features_scaled)

