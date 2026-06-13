import re
from .patterns import EMAIL_PATTERN


def extract_emails(text: str):
    results = []

    for match in re.finditer(EMAIL_PATTERN, text, re.VERBOSE):
        email = match.group()

        results.append({
            "text": email,
            "value": email.lower(),
            "start": match.start(),
            "end": match.end(),
            "type": "EMAIL"
        })

    return results