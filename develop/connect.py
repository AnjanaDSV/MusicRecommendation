import asyncpg
import os
from dotenv import load_dotenv
load_dotenv()

async def connect_to_db():
    try:
        # Ensure that environment variables are loaded correctly
        client_id = os.getenv("CLIENT_ID")
        client_secret = os.getenv("CLIENT_SECRET")
        
        if not client_id or not client_secret:
            raise ValueError("Missing CLIENT_ID or CLIENT_SECRET in the environment variables.")
        
        return {'host': client_id, 'port': client_secret}
    
    except Exception as e:
        print(f"Error retrieving credentials: {e}")
        return None