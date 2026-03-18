import pyttsx3
import PyPDF2
import io
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from database import init_db, save_voices, save_page_range

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

async def pdf_info(file: UploadFile = File(...)):
    contents = await file.read()
    reader = PyPDF2.PdfFileReader(io.BytesIO(contents))
    total = len(reader.pages)
    save_page_range(file.filename, total, 1, total)
    return {"filename": file.filename, "total_pages": total}

