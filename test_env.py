from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

print("URL:", url)
print("KEY starts with:", key[:10] if key else None)

supabase = create_client(url, key)
res = supabase.table("announcements").select("*").limit(1).execute()
print("data=", res.data, "count=", res.count)
