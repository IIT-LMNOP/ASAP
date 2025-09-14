import re
from urllib.parse import urlparse
from typing import List, Dict, Any

def normalize_skills(skills: List[str]) -> List[str]:
    return list(set([s.strip().title() for s in skills if s.strip()]))

def validate_url(url: str) -> bool:
    if not url:
        return False
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def clean_social_media(social: Dict[str, str]) -> Dict[str, str]:
    cleaned = {}
    for key, value in social.items():
        cleaned[key] = value if validate_url(value) else None
    return cleaned

def extract_json_from_response(response: str) -> Dict[str, Any]:
    """Extract JSON block from LLM output (handles fluff)"""
    start = response.find('{')
    end = response.rfind('}') + 1
    if start == -1 or end == 0:
        raise ValueError("No JSON found in response")
    json_str = response[start:end]
    import json
    return json.loads(json_str)