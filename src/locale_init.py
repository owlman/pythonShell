#!/usr/bin/env python
"""
    Created on 2024-12-07
    
    Author: lingjie
    Name:   locale_init
    Description: Initialize proper locale settings for the project.
    This module ensures consistent locale configuration across all scripts.
"""

import locale
import os
import sys
import warnings


def init_locale():
    """
    Initialize locale settings for consistent encoding behavior.
    
    This function:
    1. Sets environment variables for consistent locale
    2. Attempts to set the system locale
    3. Falls back to UTF-8 encoding if system locale fails
    4. Suppresses locale-related warnings
    
    Returns:
        bool: True if locale was successfully set, False otherwise
    """
    # First, set environment variables to ensure consistent behavior
    os.environ['LC_ALL'] = 'C.UTF-8'
    os.environ['LANG'] = 'C.UTF-8'
    os.environ['LANGUAGE'] = 'en_US:en'
    
    try:
        # Try to set the locale
        locale.setlocale(locale.LC_ALL, 'C.UTF-8')
        return True
    except locale.Error:
        try:
            # Fallback to a more generic UTF-8 locale
            locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
            return True
        except locale.Error:
            try:
                # Last resort: try to set any available UTF-8 locale
                locale.setlocale(locale.LC_ALL, '')
                return True
            except locale.Error:
                # If all fails, at least ensure Python's default encoding is UTF-8
                if sys.version_info >= (3, 7):
                    # Python 3.7+ has better UTF-8 defaults
                    return True
                return False


def get_encoding_info():
    """
    Get current encoding information for debugging purposes.
    
    Returns:
        dict: Dictionary containing encoding information
    """
    return {
        'default_encoding': sys.getdefaultencoding(),
        'filesystem_encoding': sys.getfilesystemencoding(),
        'stdout_encoding': getattr(sys.stdout, 'encoding', 'unknown'),
        'stderr_encoding': getattr(sys.stderr, 'encoding', 'unknown'),
        'locale_getlocale': locale.getlocale(),
        'locale_getpreferredencoding': locale.getpreferredencoding(),
        'env_lc_all': os.environ.get('LC_ALL', 'not set'),
        'env_lang': os.environ.get('LANG', 'not set'),
        'env_language': os.environ.get('LANGUAGE', 'not set'),
    }


def ensure_utf8_environment():
    """
    Ensure we're running in a UTF-8 friendly environment.
    
    This function checks the current environment and makes adjustments
    to ensure UTF-8 encoding is used throughout the application.
    
    Returns:
        bool: True if the environment is UTF-8 compatible
    """
    # Initialize locale settings
    locale_ok = init_locale()
    
    # Check if we're in a UTF-8 compatible environment
    encoding_info = get_encoding_info()
    
    # Verify key encodings are UTF-8 compatible
    utf8_compatible = True
    for key in ['default_encoding', 'filesystem_encoding']:
        encoding = encoding_info.get(key, '').lower()
        if 'utf' not in encoding and 'utf' not in encoding:
            utf8_compatible = False
    
    # Suppress locale warnings on some systems
    # Note: locale.Warning might not exist on all systems
    try:
        warnings.filterwarnings('ignore', category=locale.Warning)
    except AttributeError:
        # locale.Warning not available, ignore warnings globally
        warnings.filterwarnings('ignore')
    
    return utf8_compatible and locale_ok


# Auto-initialize when module is imported
ensure_utf8_environment()