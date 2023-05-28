LANGUGAGE_MAP = {
    'en': 'English', 'vi': 'Vietnamese', 'zh': 'Chinese', 'id': 'Indonesian', 
    'ms': 'Malay', 'hi': 'Hindi', 'ta': 'Tamil', 'th': 'Thai', 'my': 'Burmese', 
    'ja': 'Japanese', 'km': 'Khmer', 'lo': 'Lao', 'fil': 'Fillipino', 'ko': 'Korean', 
    'es': 'Spanish', 'tl': 'Tagalog', 'fr': 'French'
}

def is_supported_language(language_code):
    return language_code in LANGUGAGE_MAP.keys()
