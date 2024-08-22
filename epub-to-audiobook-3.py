import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import pyttsx3
from pydub import AudioSegment
import os
import time

def epub_to_audiobook(epub_path, output_path):
    print("Starting conversion process...")
    start_time = time.time()
    
    # Step 1: Extract text from epub
    print("Extracting text from epub...")
    book = epub.read_epub(epub_path)
    chapters = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            chapters.append(item.get_content())
    print(f"Extracted {len(chapters)} chapters. Time taken: {time.time() - start_time:.2f} seconds")

    # Step 2: Clean and prepare text
    print("Cleaning and preparing text...")
    text = ""
    for i, chapter in enumerate(chapters):
        soup = BeautifulSoup(chapter, 'html.parser')
        text += soup.get_text() + "\n\n"
        print(f"Processed chapter {i+1}/{len(chapters)}")
    print(f"Text preparation completed. Time taken: {time.time() - start_time:.2f} seconds")

    # Step 3: Convert text to speech
    print("Converting text to speech...")
    engine = pyttsx3.init()
    
    # Set up a callback to track progress
    def onWord(name, location, length):
        print(f"Converting word at position {location}")
    engine.connect('started-word', onWord)
    
    engine.save_to_file(text, 'temp_audio.mp3')
    engine.runAndWait()
    print(f"Speech conversion completed. Time taken: {time.time() - start_time:.2f} seconds")

    # Step 4: Process audio
    print("Processing audio...")
    audio = AudioSegment.from_mp3('temp_audio.mp3')
    
    # Step 5: Export final audio
    print(f"Exporting audiobook to {output_path}...")
    audio.export(output_path, format="mp3")

    # Clean up temporary file
    os.remove('temp_audio.mp3')

    print(f"Audiobook successfully saved to {output_path}")
    print(f"Total time taken: {time.time() - start_time:.2f} seconds")

# Usage 
epub_to_audiobook('当尼采哭泣.epub', 'audio-book-3.mp3')
