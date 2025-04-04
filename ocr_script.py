import pytesseract
import os
from PIL import Image
import re
import string
from collections import Counter

# Set the Tesseract binary path inside your project
# (Update this path if needed. Here we're using a local binary copy.)
pytesseract.pytesseract.tesseract_cmd = os.path.join(os.getcwd(), "tesseract-bin", "tesseract")

def extract_text(image_path):
    """
    Extract text from an image using Tesseract OCR.
    """
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"Error opening image: {e}")
        return ""
    text = pytesseract.image_to_string(image)
    return text

def analyze_text(text):
    """
    Analyze the extracted text to compute various metrics.
    """
    analysis = {}
    
    # Total number of characters (including and excluding spaces)
    analysis['total_characters'] = len(text)
    analysis['total_characters_no_spaces'] = len(text.replace(" ", ""))
    
    # Count digits and vowels
    analysis['digits_count'] = sum(c.isdigit() for c in text)
    vowels = set("aeiouAEIOU")
    analysis['vowels_count'] = sum(c in vowels for c in text)
    
    # Count uppercase and lowercase letters
    analysis['uppercase_count'] = sum(c.isupper() for c in text)
    analysis['lowercase_count'] = sum(c.islower() for c in text)
    
    # Number of words and sentences
    words = re.findall(r'\b\w+\b', text)
    analysis['word_count'] = len(words)
    sentences = re.split(r'[.!?]+', text)
    analysis['sentence_count'] = len([s for s in sentences if s.strip() != ""])
    
    # Average word length (handle division by zero)
    analysis['average_word_length'] = round(sum(len(word) for word in words) / len(words), 2) if words else 0
    
    # Consonant count: count alphabetic letters that are not vowels
    all_letters = [c for c in text if c.isalpha()]
    analysis['consonants_count'] = sum(1 for c in all_letters if c not in vowels)
    
    # Count punctuation characters
    punctuation_chars = set(string.punctuation)
    analysis['punctuation_count'] = sum(c in punctuation_chars for c in text)
    
    # Frequency of each character (ignoring case and spaces)
    filtered_text = re.sub(r'\s+', '', text).lower()
    analysis['char_frequency'] = dict(Counter(filtered_text))
    
    # Count numeric words (words that are entirely digits)
    analysis['numeric_word_count'] = sum(1 for word in words if word.isdigit())
    
    # Top 5 most frequent words (ignoring case)
    word_list = [word.lower() for word in words]
    word_freq = Counter(word_list)
    analysis['top_words'] = word_freq.most_common(5)
    
    return analysis

def print_analysis(analysis):
    """
    Print the text analysis results in a formatted manner.
    """
    print("\n--- OCR Text Analysis Report ---\n")
    print(f"Total Characters (including spaces): {analysis['total_characters']}")
    print(f"Total Characters (excluding spaces): {analysis['total_characters_no_spaces']}")
    print(f"Number of Digits: {analysis['digits_count']}")
    print(f"Number of Vowels: {analysis['vowels_count']}")
    print(f"Uppercase Letters: {analysis['uppercase_count']}")
    print(f"Lowercase Letters: {analysis['lowercase_count']}")
    print(f"Consonants Count: {analysis['consonants_count']}")
    print(f"Word Count: {analysis['word_count']}")
    print(f"Sentence Count: {analysis['sentence_count']}")
    print(f"Average Word Length: {analysis['average_word_length']}")
    print(f"Punctuation Count: {analysis['punctuation_count']}")
    print(f"Numeric Word Count: {analysis['numeric_word_count']}")
    
    print("\nTop 5 Most Frequent Words:")
    for word, freq in analysis['top_words']:
        print(f"  '{word}': {freq}")
    
    print("\nCharacter Frequency (all characters in lowercase, excluding spaces):")
    for char, freq in sorted(analysis['char_frequency'].items()):
        print(f"  '{char}': {freq}")
    print("\n--------------------------------\n")

def main():
    # Path to your image file - update the filename/path as needed
    image_path = "6.jpg"  # or "path/to/your_image.png"
    
    # Extract text from the image
    extracted_text = extract_text(image_path)
    
    # Print the raw extracted text
    print("Extracted Text:\n", extracted_text)
    
    # Perform analysis on the extracted text
    analysis = analyze_text(extracted_text)
    
    # Print the analysis results
    print_analysis(analysis)

if __name__ == "__main__":
    main()
