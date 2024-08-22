import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import pyttsx3
from pydub import AudioSegment

def epub_to_audiobook(epub_path, output_path):
    # Step 1: Extract text from epub
    book = epub.read_epub(epub_path)
    chapters = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            chapters.append(item.get_content())

    # Step 2: Clean and prepare text
    text = ""
    for chapter in chapters:
        soup = BeautifulSoup(chapter, 'html.parser')
        text += soup.get_text() + "\n\n"

    # Step 3: Convert text to speech
    engine = pyttsx3.init()
    engine.save_to_file(text, 'temp_audio.mp3')
    engine.runAndWait()

    # Step 4: Process audio
    audio = AudioSegment.from_mp3('temp_audio.mp3')
    
    # Adjust speed (optional)
    # audio = audio.speedup(playback_speed=1.2)

    # Step 5: Export final audio
    audio.export(output_path, format="mp3")

    print(f"Audiobook saved to {output_path}")

# Usage
epub_to_audiobook('当尼采哭泣.epub', 'audio-book.mp3')
