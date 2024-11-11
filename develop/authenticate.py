import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from connect import connect_to_db

class Spotify():
    def __init__(self):
        self.sp=None

    
    async def authentication(self):
        credentials = await connect_to_db()  
        if credentials is not None:
            client_id = credentials.get('host')
            client_secret=credentials.get('port')
        else:
            print("Error: credentials are None.")

        # Set up Spotify authentication
        client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

   

    async def get_track_info(self, track_id):
        if self.sp:
            track = self.sp.track(track_id)  # Use Spotify's track API to retrieve track info
            audio_features = self.sp.audio_features(track_id)[0]  # Get audio features
            return {
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'danceability': audio_features['danceability'],
                'energy': audio_features['energy'],
                'acousticness': audio_features['acousticness'],
                'popularity': track['popularity']
            }
        return None

    async def get_user_top_tracks(self):
        if self.sp:
            top_tracks = self.sp.current_user_top_tracks(limit=10)
            tracks_info = [(track['name'], track['artists'][0]['name']) for track in top_tracks['items']]
            return tracks_info
        return None

    async def get_user_playlists(self):
        if self.sp:
            playlists = self.sp.current_user_playlists()
            playlists_info = [(playlist['name'], playlist['trackCount']) for playlist in playlists['items']]
            return playlists_info
        return None


async def main():
    spotify = Spotify()
    await spotify.authentication()
    track_info = await spotify.get_track_info('1fzAuUVbzlhZ1lJAx9PtY6')  # Replace with a valid track ID
    
    if track_info:
        track_name = track_info['name']
        artist_name = track_info['artist']
        print(f"Track: {track_name}, Artist: {artist_name}")
        # You can print other information too
        print(f"Danceability: {track_info['danceability']}")
        print(f"Energy: {track_info['energy']}")
        print(f"Acousticness: {track_info['acousticness']}")
        print(f"Popularity: {track_info['popularity']}")
    else:
        print("Failed to retrieve track information.")

    
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())