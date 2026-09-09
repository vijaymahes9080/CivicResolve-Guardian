import re
from typing import Tuple, List, Dict

class PIIRedactionEngine:
    """
    Multilingual PII Redaction Engine supporting English and Tamil (தமிழ்).
    Performs deterministic regex-based masking and returns both the redacted
    text and an audit log of entities detected.
    """
    
    # 1. Phone number patterns: Indian 10-digit mobile, with optional +91, spaces or dashes
    PHONE_REGEX = re.compile(
        r'(?:\+91[\-\s]?)?(?:0)?[6-9]\d{4}[\-\s]?\d{5}\b|(?:\+91[\-\s]?)?[6-9]\d{9}\b'
    )
    
    # 2. Aadhaar number patterns: 12 digits (with optional spaces or dashes)
    AADHAAR_REGEX = re.compile(
        r'\b[2-9]{1}\d{3}[\s\-]?[0-9]{4}[\s\-]?[0-9]{4}\b'
    )
    
    # 3. Voter ID / PAN format
    VOTER_PAN_REGEX = re.compile(
        r'\b[A-Z]{3,5}[0-9]{4,5}[A-Z]?\b'
    )
    
    # 4. Email format
    EMAIL_REGEX = re.compile(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    )
    
    # 5. House / Door address patterns (English and Tamil)
    DOOR_ADDR_REGEX = re.compile(
        r'(?i)\b(?:door\s*no\.?|d\.?no\.?|house\s*no\.?|h\.?no\.?|flat\s*no\.?|plot\s*no\.?|கதவு\s*எண்)\s*[:\-]?\s*[\w\-\/\#]+'
    )
    
    # 6. Name declarations (English & Tamil)
    NAME_INTRO_REGEX = re.compile(
        r'(?i)\b(?:my\s+name\s+is|i\s+am|contact\s+person\s*:?|contact\s+me\s+at\s*:?|என்\s*பெயர்|தொடர்புக்கு)\s+([A-Z\u0B80-\u0BFF][a-z\u0B80-\u0BFF]+(?:\s+[A-Z\u0B80-\u0BFF][a-z\u0B80-\u0BFF]+)?)'
    )

    def redact(self, text: str) -> Tuple[str, List[Dict[str, str]]]:
        if not text:
            return "", []
            
        redacted_text = text
        audit_records: List[Dict[str, str]] = []
        
        # Redact Aadhaar first (to prevent overlap with phone numbers)
        for match in self.AADHAAR_REGEX.finditer(redacted_text):
            val = match.group(0)
            audit_records.append({"type": "AADHAAR", "original": val[-4:].rjust(len(val), "X")})
        redacted_text = self.AADHAAR_REGEX.sub("[AADHAAR_REDACTED]", redacted_text)
        
        # Redact Phone numbers
        for match in self.PHONE_REGEX.finditer(redacted_text):
            val = match.group(0)
            audit_records.append({"type": "PHONE", "original": val[-4:].rjust(len(val), "X")})
        redacted_text = self.PHONE_REGEX.sub("[PHONE_REDACTED]", redacted_text)
        
        # Redact Email addresses
        for match in self.EMAIL_REGEX.finditer(redacted_text):
            val = match.group(0)
            audit_records.append({"type": "EMAIL", "original": "masked@domain.com"})
        redacted_text = self.EMAIL_REGEX.sub("[EMAIL_REDACTED]", redacted_text)
        
        # Redact Door/House addresses
        for match in self.DOOR_ADDR_REGEX.finditer(redacted_text):
            audit_records.append({"type": "ADDRESS", "original": match.group(0)})
        redacted_text = self.DOOR_ADDR_REGEX.sub("[DOOR_ADDRESS_REDACTED]", redacted_text)
        
        # Redact Name intros
        def mask_name(match):
            intro = match.group(0).split()[0]
            name = match.group(1)
            audit_records.append({"type": "NAME", "original": name[0] + "***"})
            return match.group(0).replace(name, "[NAME_REDACTED]")
            
        redacted_text = self.NAME_INTRO_REGEX.sub(mask_name, redacted_text)
        
        return redacted_text, audit_records

pii_engine = PIIRedactionEngine()
