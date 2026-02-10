"""
Multi-Query Parser for Bankoo AI
Splits compound queries into individual tasks and processes them in sequence.
"""

import re
from typing import List, Tuple

def parse_multiple_queries(text: str) -> List[str]:
    """
    Split text into multiple queries based on natural language patterns.
    
    Examples:
        "Search weather in Paris, Mumbai, and Tokyo" → 3 queries
        "Tell me about Python. What is JavaScript?" → 2 queries
        "A\\nB\\nC" → 3 queries
    """
    # Pattern 1: "Search weather in A, B, and C" - list of locations
    weather_list_pattern = r'search\s+weather\s+in\s+(.*?)(?:\?|$)'
    match = re.search(weather_list_pattern, text.lower(), re.IGNORECASE)
    
    if match:
        locations_str = match.group(1)
        # Split by commas and 'and'
        locations = re.split(r'\s*,\s*|\s+and\s+', locations_str)
        locations = [loc.strip() for loc in locations if loc.strip() and len(loc.strip()) > 1]
        
        if len(locations) > 1:
            # Found multiple weather locations
            return [f"search weather in {loc}" for loc in locations]
    
    # Pattern 2: "Search A, B, and C" - general search with list
    general_list_pattern = r'search\s+(?:for\s+)?(.*?)(?:\?|$)'
    match = re.search(general_list_pattern, text.lower(), re.IGNORECASE)
    
    if match and 'weather' not in text.lower():
        topics_str = match.group(1)
        topics = re.split(r'\s*,\s*|\s+and\s+', topics_str)
        topics = [t.strip() for t in topics if t.strip() and len(t.strip()) > 2]
        
        if len(topics) > 1:
            return [f"search {topic}" for topic in topics]
    
    # Pattern 3: Multiple sentences (periods, newlines)
    parts = re.split(r'(?<=[.!?])\s+(?=[A-Z])|[\n;]', text)
    
    queries = []
    for part in parts:
        part = part.strip()
        if len(part) > 5:  # Minimum query length
            queries.append(part)
    
    # If we found multiple parts, return them
    if len(queries) > 1:
        return queries
    
    # No splits detected, return original text as single query
    return [text]


def format_batch_response(query_index: int, total_queries: int, response: str) -> str:
    """
    Format a response with progress indicator for batch processing.
    
    Example: "[1/3] 🌤️ Weather in Paris: 15°C"
    """
    progress = f"[{query_index}/{total_queries}]"
    return f"{progress} {response}"


def detect_multi_query(text: str) -> bool:
    """
    Quick check if text likely contains multiple queries.
    """
    indicators = [
        text.count(',') >= 2,  # Multiple commas
        text.count(' and ') >= 1,  # "A and B"
        text.count('\n') >= 1,  # Line breaks
        len(re.findall(r'search', text.lower())) >= 2,  # Multiple "search" keywords
    ]
    
    return any(indicators)
