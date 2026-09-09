import re

class LanguageDetector:
    # Tamil Unicode block: U+0B80 to U+0BFF
    TAMIL_UNICODE_REGEX = re.compile(r'[\u0B80-\u0BFF]')
    
    # Common Tamil transliterated grievance keywords
    TAMIL_TRANSLIT_KEYWORDS = {
        "thanni", "kudineer", "kuppai", "saalai", "kuzhi", "vilakku",
        "sandhai", "theru", "nalla", "kettu", "manidhar", "kaalvai",
        "aarambam", "thondharavu", "vettaveli", "vanakkam"
    }

    @classmethod
    def detect(cls, text: str) -> str:
        if not text:
            return "en"
            
        tamil_chars = len(cls.TAMIL_UNICODE_REGEX.findall(text))
        total_chars = len(text.strip())
        
        # If > 10% characters are Tamil script, classify as Tamil
        if total_chars > 0 and (tamil_chars / total_chars) > 0.10:
            return "ta"
            
        # Check transliterated words
        words = set(re.findall(r'\b\w+\b', text.lower()))
        if len(words.intersection(cls.TAMIL_TRANSLIT_KEYWORDS)) >= 2:
            return "ta"
            
        return "en"


def detect_language(text: str) -> str:
    return LanguageDetector.detect(text)
