#!/usr/bin/env python
"""
    Created on 2024-12-07
    
    Author: lingjie
    Name:   __init__
    Description: Package initialization for python-shell-utilities.
    This module ensures proper initialization when the package is imported.
"""

# Initialize locale settings immediately when package is imported
try:
    from .locale_init import ensure_utf8_environment, get_encoding_info
except ImportError:
    # Fallback for direct execution
    from locale_init import ensure_utf8_environment, get_encoding_info

# Ensure UTF-8 environment
ensure_utf8_environment()

# Export key functions for external use
__all__ = ['ensure_utf8_environment', 'get_encoding_info']

# Package metadata
__version__ = "0.1.0"
__author__ = "Ling Jie"
__email__ = "jie.owl2008@gmail.com"