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
    
    # Split text into smaller chunks
    chunk_size = 1000  # characters
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    
    for i, chunk in enumerate(chunks):
        print(f"Processing chunk {i+1}/{len(chunks)}...")
        engine.save_to_file(chunk, f'temp_audio_{i}.mp3')
        engine.runAndWait()
    
    print(f"Speech conversion completed. Time taken: {time.time() - start_time:.2f} seconds")

    # Step 4: Process audio
    print("Processing audio...")
    final_audio = AudioSegment.empty()
    for i in range(len(chunks)):
        chunk_audio = AudioSegment.from_mp3(f'temp_audio_{i}.mp3')
        final_audio += chunk_audio
        os.remove(f'temp_audio_{i}.mp3')
    
    # Step 5: Export final audio
    print(f"Exporting audiobook to {output_path}...")
    final_audio.export(output_path, format="mp3")

    print(f"Audiobook successfully saved to {output_path}")
    print(f"Total time taken: {time.time() - start_time:.2f} seconds")

# Usage
# epub_to_audiobook('input.epub', 'output.mp3')
epub_to_audiobook('当尼采哭泣.epub', 'audio-book-2.mp3')
