import re
from typing import List

class TextProcessor:
    def __init__(self):
        """
        Initialize the TextProcessor with basic text processing capabilities.
        """
        pass

    def translate_to_english(self, text: str, source_lang: str) -> str:
        """
        Translate the input text to English. Currently a placeholder that returns the original text
        with a translation note if not already in English.
        
        Args:
            text (str): The text to translate.
            source_lang (str): The source language code (e.g., 'hi', 'ta', 'en').
        
        Returns:
            str: Translated text (or original text with a note).
        """
        if source_lang == "en":
            return text
        return f"{text} [Translated from {source_lang}]"

    def create_summary(self, text: str) -> str:
        """
        Create a summary by taking the first two sentences or the first 100 characters.
        
        Args:
            text (str): The text to summarize.
        
        Returns:
            str: A summary of the text.
        """
        if len(text.strip()) < 50:
            return text
        sentences = text.split('.')
        if len(sentences) >= 2:
            return '.'.join(sentences[:2]) + '.'
        else:
            return text[:100] + "..." if len(text) > 100 else text

    def extract_keywords(self, text: str, num_keywords: int = 5) -> List[str]:
        """
        Extract keywords from the text based on word frequency, filtering out stop words.
        
        Args:
            text (str): The text to extract keywords from.
            num_keywords (int): The number of keywords to return. Default is 5.
        
        Returns:
            List[str]: A list of extracted keywords.
        """
        # Clean text and convert to lowercase
        clean_text = re.sub(r'[^\w\s]', '', text.lower())
        words = clean_text.split()
        
        # Common stop words to filter out
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'was', 'are', 'were', 'be', 'been', 'have',
            'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
            'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we',
            'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'her',
            'its', 'our', 'their', 'from', 'up', 'about', 'into', 'over', 'after'
        }
        
        # Filter out stop words and short words
        filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Count word frequency
        word_count = {}
        for word in filtered_words:
            word_count[word] = word_count.get(word, 0) + 1
        
        # Sort by frequency and return top keywords
        sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
        keywords = [word for word, count in sorted_words[:num_keywords]]
        
        return keywords if keywords else ['story', 'myth', 'tale']

if __name__ == "__main__":
    # Example usage for testing
    tp = TextProcessor()
    sample_text = "This is a sample myth about a hero. He fought bravely. The village celebrated."
    print("Translated:", tp.translate_to_english(sample_text, "hi"))
    print("Summary:", tp.create_summary(sample_text))
    print("Keywords:", tp.extract_keywords(sample_text))