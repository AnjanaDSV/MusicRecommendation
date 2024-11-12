import os
from fastapi import FastAPI
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer

# Load environment variables
load_dotenv()

# Spotify API setup
client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")

# FastAPI instance
app = FastAPI()

# Spotify authentication
sp_oauth = SpotifyOAuth(client_id=client_id,
                         client_secret=client_secret,
                         redirect_uri=redirect_uri,
                         scope=["user-library-read", "playlist-read-private", "user-top-read"])

# Global variable for storing the Spotify client
sp = None

@app.get("/")
async def root():
    return {"message": "Welcome to the Spotify Metadata Retriever"}

@app.get("/login")
async def login():
    """
    Redirect the user to the Spotify login page for authentication.
    """
    auth_url = sp_oauth.get_authorize_url()
    return {"url": auth_url}

@app.get("/callback")
async def callback(code: str):
    """
    Spotify will call this route with a code parameter in the query string. The code will
    be used to fetch the access token.
    """
    global sp
    token_info = sp_oauth.get_access_token(code)
    sp = Spotify(auth=token_info['access_token'])  # Store the Spotify client with the access token
    return {"message": "Authentication successful. You can now search for tracks."}

@app.get("/search/")
async def search_track(query: str):
    """
    Search for tracks on Spotify by name and return metadata and audio features for multiple tracks.
    """
    if sp is None:
        raise HTTPException(status_code=401, detail="Not authenticated. Please log in first.")
    
    # Search for up to 10 tracks
    results = sp.search(q=query, limit=10, type='track')
    
    if results['tracks']['items']:
        tracks_info = []
        
        # Iterate over the search results and get data for each track
        for track in results['tracks']['items']:
            track_id = track['id']  # Get the track ID for fetching audio features
            audio_features = sp.audio_features(track_id)[0]  # Fetch audio features
            
            track_data = {
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'album': track['album']['name'],
                'preview_url': track['preview_url'],
                'uri': track['uri'],
                'danceability': audio_features['danceability'],
                'energy': audio_features['energy'],
                'acousticness': audio_features['acousticness'],
                'popularity': track['popularity']
            }
            tracks_info.append(track_data)
        
        return JSONResponse(content=tracks_info)
    else:
        return {"error": "No tracks found for the query"}


