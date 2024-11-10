import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from connect import connect_to_db

class Spotify():
    def _init_(self):
        self.connection = None
        self.sp=None

    
    async def authentication(self):
        credentials = await connect_to_db()  
        if credentials is not None:
            client_id = credentials.get('host')
            client_secret=credentials.get('port')
            print(f"Client ID: {client_id}")
        else:
            print("Error: credentials are None.")

        # Set up Spotify authentication
        client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        
    async def close_connection(self):
        if self.connection:
            await self.connection.close()

    async def get_track_info(self, track_id):
        if self.sp:
            track = self.sp.track(track_id)  # Use Spotify's track API to retrieve track info.
            return track['name'], track['artists'][0]['name']
        return None


async def main():
    spotify = Spotify()
    await spotify.authentication()
    track_name, artist_name = await spotify.get_track_info('spotify_track_id')  # Replace with a valid track ID
    print(f"Track: {track_name}, Artist: {artist_name}")
    await spotify.close_connection()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())