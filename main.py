# A Python program that reads a PDF file aloud using text-to-speech.
# It allows the user to select a voice, set the starting page, adjust playback speed, and optionally save the audio as a WAV file.  
# Below are the imports: pyttsx3, PyPDF2, and tkinter libraries.
import pyttsx3 as pyt
import PyPDF2 as PyPDF
from tkinter.filedialog import * 
#Function to choose and set the voice for text-to-speech
def Voice(engine):
    voices = engine.getProperty('voices')
    print("Please choose a voice from the following options:")
    for i, voice in enumerate(voices):    
        print(f"{i}: {voice.name} ({voice.id})")
    try:
        choice = int(input("\nEnter the number of the voice you want to use: "))
        if 0 <= choice < len(voices):
            engine.setProperty('voice', voices[choice].id)
            print(f"Voice set to: {voices[choice].name}")
        else:
            print("Invalid choice. Default voice will be used.")
    except ValueError:
        print("Invalid input. Default voice will be used.")
#Function to save audio as WAV file    
def SaveWAV(engine, reader, startPage, endPage):  
    saveWAV = input("Do you want to save the audio as a WAV file? (yes/no): ").strip().lower()
    if saveWAV == 'yes':
        fullSaveText = ""
        outputFilename = input("Enter the output WAV file name (with .wav extension): ")
        for num in range(startPage, endPage):
            print(f"Processing page {num+1} of {endPage}...")
            page = reader.pages[num]
            text = page.extract_text()
            if text:
                fullSaveText += text + "\n "
        engine.save_to_file(fullSaveText,outputFilename)
        engine.runAndWait()
        print(f"Audio saved as {outputFilename}")  
    elif saveWAV == 'no':
        print("Procceding without saving a file")
    else:
        print("Invalid Input. Procceding without saving a file")
#Function
def Speak(engine, reader, startPage, endPage):
    fullText = ""
    for num in range(startPage, endPage):
        page = reader.pages[num]
        text = page.extract_text()
        if text:
            fullText += text + "\n"
    engine.say(fullText)
    engine.runAndWait()

def main():
    engine = pyt.init()
    Voice(engine)
    book = askopenfilename()
    reader = PyPDF.PdfReader(book)
    numberOfPages = len(reader.pages)
    print(f"Total pages: {numberOfPages}")
    startPage = int(input("Enter the starting page number: ")) - 1
    endPage = int(input("Enter the ending page number: "))
    rate = int(input("Enter playback speed (default is 200): "))
    engine.setProperty('rate', rate)
    SaveWAV(engine, reader, startPage, endPage)
    Speak(engine, reader, startPage, endPage)

main()