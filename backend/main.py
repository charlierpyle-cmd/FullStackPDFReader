import pyttsx3
import PyPDF2
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from database import init_db, save_voices

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

def list_voices():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    voice_list = [{"id": v.id, "name": v.name} for v in voices]
    engine.stop()
    save_voices(voice_list)
    return voice_list