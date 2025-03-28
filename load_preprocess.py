import requests
import os
import re
import nltk
nltk.download('punkt')

def download_gutenberg_text(url):
    """
    Download and clean a text file from Project Gutenberg
    """
    try:
        response = requests.get(url)
        text = response.text
        
        # Remove Project Gutenberg header and footer
        start_marker = text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
        end_marker = text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
        
        if start_marker != -1 and end_marker != -1:
            text = text[start_marker:end_marker]
        
        # Basic text cleaning
        text = re.sub(r'\n+', ' ', text)  # Replace multiple newlines
        text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
        
        return text.strip()
    except Exception as e:
        print(f"Error downloading text: {e}")
        return None

def prepare_dataset(urls, output_file='gutenberg_dataset.txt', max_segments=10000):
    """
    Collect texts from multiple Gutenberg URLs and prepare dataset
    """
    all_segments = []
    
    for url in urls:
        text = download_gutenberg_text(url)
        if text:
            # Tokenize into sentences
            sentences = nltk.sent_tokenize(text)
            all_segments.extend(sentences)
            
            # Stop if we reach max segments
            if len(all_segments) >= max_segments:
                break
    
    # Trim to desired range (5000-10000 segments)
    all_segments = all_segments[:max_segments]
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        for segment in all_segments:
            f.write(segment + '\n')
    
    print(f"Dataset created with {len(all_segments)} segments")
    return all_segments

# Example Gutenberg URLs (classic literature)
gutenberg_urls = [
    'https://www.gutenberg.org/files/1342/1342-0.txt',  # Pride and Prejudice
    'https://www.gutenberg.org/files/11/11-0.txt',      # Alice in Wonderland
    'https://www.gutenberg.org/files/84/84-0.txt',      # Frankenstein
    'https://www.gutenberg.org/files/1661/1661-0.txt'   # The Adventures of Sherlock Holmes
]

# Collect and prepare dataset
dataset = prepare_dataset(gutenberg_urls)