# metadata.py

import os
from app.config import DEFAULT_DESCRIPTION, DEFAULT_TAGS

def generate_title(base_title, index):
    """Generate a title with an incremental index"""
    return f"{base_title} #{index}"

def get_description():
    """Return default description (could later be AI-generated)"""
    return DEFAULT_DESCRIPTION

def get_tags():
    """Return default tags (could later be AI-generated)"""
    return DEFAULT_TAGS 