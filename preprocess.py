import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import os
import json
from pydub import AudioSegment
from pydub.silence import split_on_silence
import nltk
from nltk.tokenize import sent_tokenize
from tqdm import tqdm

nltk.download('punkt', quiet=True)

def extract_epub_chapters(epub_path):
    print("Extracting chapters from EPUB...")
    book = epub.read_epub(epub_path)
    chapters = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            chapter_title = soup.find('h1') or soup.find('h2')
            title = chapter_title.text if chapter_title else f"Chapter {len(chapters) + 1}"
            content = soup.get_text()
            chapters.append({"title": title, "content": content})
    return chapters

def find_chapter_boundaries(audio, chapters):
    print("Finding chapter boundaries...")
    # 使用静音检测来分割音频
    chunks = split_on_silence(audio, min_silence_len=1000, silence_thresh=-40)
    
    boundaries = [0]
    current_pos = 0
    chunk_index = 0
    
    for i, chapter in enumerate(tqdm(chapters)):
        chapter_sentences = sent_tokenize(chapter['content'])
        sentence_count = len(chapter_sentences)
        target_chunks = max(1, int(sentence_count / len(chapters) * len(chunks)))
        
        while chunk_index < len(chunks) and len(boundaries) <= i + 1:
            current_pos += len(chunks[chunk_index])
            chunk_index += 1
            if chunk_index % target_chunks == 0 or chunk_index == len(chunks):
                boundaries.append(current_pos)
                break
    
    if len(boundaries) < len(chapters) + 1:
        boundaries.append(len(audio))
    
    return boundaries

def process_chapters(epub_path, mp3_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    chapters = extract_epub_chapters(epub_path)
    full_audio = AudioSegment.from_mp3(mp3_path)
    
    boundaries = find_chapter_boundaries(full_audio, chapters)
    
    print("Processing chapters and audio...")
    for i, chapter in enumerate(tqdm(chapters)):
        start = boundaries[i]
        end = boundaries[i+1]
        
        chapter_audio = full_audio[start:end]
        audio_file = f"chapter_{i+1}.mp3"
        chapter_audio.export(os.path.join(output_dir, audio_file), format="mp3", bitrate="128k")
        
        chapter['audio_file'] = audio_file
    
    with open(os.path.join(output_dir, 'chapters.json'), 'w', encoding='utf-8') as f:
        json.dump(chapters, f, ensure_ascii=False, indent=2)
    
    print("Preprocessing completed. Check the output directory for results.")

if __name__ == "__main__":
    epub_path = "当尼采哭泣.epub"
    mp3_path = "当尼采哭泣.mp3"
    output_dir = "processed_book"
    process_chapters(epub_path, mp3_path, output_dir)