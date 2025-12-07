#!/usr/bin/env python3
"""
    Created on 2024-12-07
    
    Author: lingjie
    Name:   bootstrap
    Description: Bootstrap script for python-shell-utilities.
    This module ensures all scripts start with proper locale settings.
"""

import os
import sys

def bootstrap_locale():
    """
    Bootstrap locale settings for the entire application.
    
    This function should be called at the very beginning of any script
    to ensure proper locale initialization.
    """
    # Set environment variables for consistent locale
    os.environ['LC_ALL'] = 'C.UTF-8'
    os.environ['LANG'] = 'C.UTF-8'
    os.environ['LANGUAGE'] = 'en_US:en'
    
    # Add src directory to Python path if not already present
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src_path = os.path.join(project_root, 'src')
    
    if src_path not in sys.path:
        sys.path.insert(0, src_path)

def get_project_info():
    """
    Get project information for debugging and reporting.
    
    Returns:
        dict: Project information including paths and environment
    """
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    return {
        'project_root': project_root,
        'src_path': os.path.join(project_root, 'src'),
        'python_version': sys.version,
        'python_path': sys.executable,
        'sys_path': sys.path[:3],  # First few entries for brevity
        'environment': {
            'LC_ALL': os.environ.get('LC_ALL'),
            'LANG': os.environ.get('LANG'),
            'LANGUAGE': os.environ.get('LANGUAGE'),
        }
    }

# Auto-bootstrap when module is imported
bootstrap_locale()