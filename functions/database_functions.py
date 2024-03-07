from dotenv import load_dotenv
import supabase
import os

load_dotenv()

# Constants for Supabase URL and API keys
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize the Supabase Client
supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)


def fetch_user_favorites(email):
    data, count = (
        supabase_client.table("User Favorites").select("*").eq("email", email).execute()
    )

    uri_list = []
    for entry in data[1]:
        uri_list.append(entry["dish_uri"])

    return uri_list
