import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import pyttsx3
import os
import time
import re

def clean_text(text):
    # Remove extra whitespace and newlines
    text = re.sub(r'\s+', ' ', text).strip()
    # Remove any non-printable characters
    text = ''.join(char for char in text if char.isprintable() or char.isspace())
    return text

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
    full_text = ""
    for i, chapter in enumerate(chapters):
        soup = BeautifulSoup(chapter, 'html.parser')
        chapter_text = clean_text(soup.get_text())
        full_text += chapter_text + "\n\n"
        print(f"Processed chapter {i+1}/{len(chapters)} - Length: {len(chapter_text)} characters")
    
    print(f"Total text length: {len(full_text)} characters")
    print(f"Text preparation completed. Time taken: {time.time() - start_time:.2f} seconds")

    if len(full_text) == 0:
        print("Error: No text extracted from the epub file.")
        return

    # Step 3: Convert text to speech using pyttsx3
    print("Converting text to speech...")
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)  # Speed of speech
        
        # Split text into smaller chunks
        max_chunk_size = 5000  # characters
        text_chunks = [full_text[i:i+max_chunk_size] for i in range(0, len(full_text), max_chunk_size)]
        
        for i, chunk in enumerate(text_chunks):
            print(f"Processing chunk {i+1}/{len(text_chunks)}...")
            engine.save_to_file(chunk, f'temp_audio_{i}.mp3')
            engine.runAndWait()
        
        print(f"Speech conversion completed. Time taken: {time.time() - start_time:.2f} seconds")
        
        # Combine audio files
        print("Combining audio chunks...")
        with open(output_path, 'wb') as outfile:
            for i in range(len(text_chunks)):
                with open(f'temp_audio_{i}.mp3', 'rb') as infile:
                    outfile.write(infile.read())
                os.remove(f'temp_audio_{i}.mp3')
        
        print(f"Audio combination completed. Time taken: {time.time() - start_time:.2f} seconds")
    except Exception as e:
        print(f"Error during TTS conversion or export: {str(e)}")
        return

    # Step 4: Verify audio file
    if os.path.exists(output_path):
        file_size = os.path.getsize(output_path)
        print(f"Generated audio file size: {file_size} bytes")
        if file_size < 1000:  # Arbitrary small size to check
            print("Warning: Generated audio file is suspiciously small.")
    else:
        print("Error: Audio file was not generated.")
        return

    print(f"Audiobook successfully saved to {output_path}")
    print(f"Total time taken: {time.time() - start_time:.2f} seconds")

# Usage
epub_to_audiobook('当尼采哭泣.epub', 'audio-book-5.mp3')
