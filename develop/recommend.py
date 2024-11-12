from fastapi import FastAPI
from pydantic import BaseModel
import model  


# Initialize FastAPI
app = FastAPI()

# Define a request model for the track name (if you need to input a track name)
class TrackRequest(BaseModel):
    track_name: str

# Define a response model for the recommendations
class TrackRecommendation(BaseModel):
    name: str
    artist: str
    album: str
    danceability: float
    energy: float
    acousticness: float
    popularity: float

# Route for getting recommendations for a specific track
@app.post("/recommend/")
async def recommend_track(request: TrackRequest):
    track_name = request.track_name
    recommendations = recommend_similar_tracks(track_name, model.df, model.similarity_matrix)
    return recommendations

# Function for generating recommendations based on a track name
def recommend_similar_tracks(track_name, df, similarity_matrix):
    # Find the index of the track
    track_index = df[df['name'] == track_name].index[0]

    # Get similarity scores for the selected track
    similarity_scores = similarity_matrix[track_index]

    # Sort the tracks by similarity score (descending order)
    similar_tracks_indices = similarity_scores.argsort()[::-1]  # Sort in descending order
    similar_tracks_indices = [i for i in similar_tracks_indices if i != track_index]  # Exclude the track itself

    # Get the top 3 similar tracks
    recommendations = df.iloc[similar_tracks_indices[:3]]

    # Convert recommendations to the response model
    return [TrackRecommendation(
        name=row['name'],
        artist=row['artist'],
        album=row['album'],
        danceability=row['danceability'],
        energy=row['energy'],
        acousticness=row['acousticness'],
        popularity=row['popularity']
    ) for _, row in recommendations.iterrows()]

# Route for getting recommendations for all tracks (Optional)
@app.get("/recommend_all/")
async def recommend_all_tracks():
    recommendations = recommend_similar_tracks_for_all(model.df, model.similarity_matrix)
    return recommendations

# Function to recommend similar tracks for all songs in the dataset
def recommend_similar_tracks_for_all(df, similarity_matrix):
    recommendations = []  # List to store recommendations for all tracks

    # Loop through all tracks in the DataFrame
    for track_index in range(len(df)):
        # Get similarity scores for the current track
        similarity_scores = similarity_matrix[track_index]

        # Sort the tracks by similarity score (descending order)
        similar_tracks_indices = similarity_scores.argsort()[::-1]  # Sort in descending order
        similar_tracks_indices = [i for i in similar_tracks_indices if i != track_index]  # Exclude the track itself

        # Get the top 3 similar tracks
        top_similar_tracks = df.iloc[similar_tracks_indices[:3]]

        # Add the recommendations for the current track to the list
        recommendations.append({
            'track_name': df.iloc[track_index]['name'],
            'recommendations': top_similar_tracks[['name', 'artist', 'album', 'danceability', 'energy', 'acousticness', 'popularity']].to_dict(orient='records')
        })

    return recommendations
