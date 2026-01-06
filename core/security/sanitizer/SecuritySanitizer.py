import re

class SecuritySanitizer:
    """
    Detects and sanitizes sensitive information using Regex patterns.
    """
    
    PATTERNS = [
        # 1. AWS Access Key (AKIA...)
        ("AWS_KEY", r'(AKIA[0-9A-Z]{16})', 0),
        
        # 2. Google API Key (AIza...)
        ("GOOGLE_KEY", r'(AIza[0-9A-Za-z-_]{35})', 0),
        
        # 3. Generic Secrets (api_key = "xyz", "password": "abc")
        # Captures: Variable name -> Separator -> Quote -> SECRET -> Quote
        # Ref: matches patterns like: apiKey="123", "secret": "abc", password = 'pass'
        ("SECRET", r'(?i)(api[_-]?key|secret|token|password|auth|credential|passwd)["\']?\s*(:|:?=|:)\s*(["\'])([^"\']+)(["\'])', 4),
        
        # 4. Bearer Token
        ("AUTH_TOKEN", r'(Bearer\s+)([a-zA-Z0-9\-\._~\+\/]+)', 2),
        
        # 5. Email Addresses
        ("EMAIL", r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', 0),
        
        # 6. IPv4 Addresses (Excluding localhost 127.0.0.1 and local 192.168.x.x to reduce noise)
        ("IP_ADDR", r'\b(?!(?:127\.|10\.|192\.168\.|172\.(?:1[6-9]|2[0-9]|3[0-1])\.))\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', 0),
    ]

    @staticmethod
    def sanitize(text: str) -> str:
        """
        Runs all regex patterns and replaces found secrets with [REDACTED].
        """
        redacted_text = text
        
        for label, pattern, group_idx in SecuritySanitizer.PATTERNS:
            def replacer(match):
                if group_idx == 0:
                    # Replace the entire match
                    return f"[{label}_REDACTED]"
                else:
                    # Replace only the specific capture group (the secret value)
                    # We reconstruct the string by replacing the secret part within the full match
                    full_match = match.group(0)
                    secret_part = match.group(group_idx)
                    return full_match.replace(secret_part, f"[{label}_REDACTED]")

            redacted_text = re.sub(pattern, replacer, redacted_text)
            
        return redacted_text