#!/usr/bin/env python3
"""
SUPER Language Creator - Modular Version
Main entry point for the modular application

This is the new modular version of LangGen that splits functionality into organized modules:
- core_systems.py: Theme engine, accessibility, achievements, syntax highlighting
- language_processing.py: Language validation, interpreter generation, code execution
- ui_components.py: Menu bars, toolbars, tabs, dialogs, and UI elements
- file_operations.py: Save/load, import/export, templates, autosave
- application_features.py: Playground, documentation, statistics, tutorials
- main_application.py: Main application controller

Usage:
    python LangGen_Modular.py

Features:
- All original LangGen functionality preserved
- Better code organization and maintainability
- Modular structure for easier development and testing
- Improved error handling and separation of concerns
"""

import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main entry point for the modular SUPER Language Creator"""
    try:
        # Import and run the main application
        from main_application import main as run_app
        run_app()
        
    except ImportError as e:
        print(f"Error: Missing required modules. {e}")
        print("Make sure all module files are present:")
        print("- core_systems.py")
        print("- language_processing.py") 
        print("- ui_components.py")
        print("- file_operations.py")
        print("- application_features.py")
        print("- main_application.py")
        sys.exit(1)
        
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

