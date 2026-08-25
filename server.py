from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from livekit import api
import os

app = FastAPI()

LIVEKIT_URL = os.getenv("LIVEKIT_URL", "wss://my-classroom-tvclvnpa.livekit.cloud")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY", "APIuJX9SpuEnTUv")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET", "הסוד_שלך_כאן")

@app.get("/", response_class=HTMLResponse)
def get_index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/api/token")
def get_token(room: str, username: str, role: str):
    try:
        # אם זה מורה - מותר לו לשדר (publish). אם זה תלמיד - צפייה והאזנה בלבד.
        is_teacher = (role == "teacher")
        
        lk_api = api.AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET) \
            .with_identity(username) \
            .with_name(username) \
            .with_grants(api.VideoGrants(
                room_join=True,
                room=room,
                can_publish=is_teacher,
                can_subscribe=True,
                room_admin=is_teacher
            ))
        return {"token": lk_api.to_jwt(), "url": LIVEKIT_URL}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))