import zipfile
import os
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def extract_epub(epub_path, output_dir):
    logger.info(f"Extracting EPUB: {epub_path}")
    try:
        with zipfile.ZipFile(epub_path, 'r') as zip_ref:
            zip_ref.extractall(output_dir)
        logger.info(f"EPUB extracted to: {output_dir}")
        return output_dir
    except Exception as e:
        logger.error(f"Error extracting EPUB: {str(e)}")
        raise

def process_epub_content(output_dir):
    logger.info(f"Processing EPUB content in: {output_dir}")
    html_files = []
    try:
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                if file.endswith('.html') or file.endswith('.xhtml'):
                    file_path = os.path.join(root, file)
                    logger.info(f"Processing file: {file_path}")
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    soup = BeautifulSoup(content, 'html.parser')
                    body = soup.find('body')
                    if body:
                        cleaned_content = body.get_text()
                        output_file = os.path.join(output_dir, f"processed_{file}")
                        with open(output_file, 'w', encoding='utf-8') as f:
                            f.write(cleaned_content)
                        html_files.append(f"processed_{file}")
                        logger.info(f"Processed and saved: {output_file}")
        return sorted(html_files)
    except Exception as e:
        logger.error(f"Error processing EPUB content: {str(e)}")
        raise