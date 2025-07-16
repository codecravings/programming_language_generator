"""
SUPER Language Creator - Modular Version
A powerful tool for creating custom programming languages with ease.
"""

__version__ = "2.0.0"
__author__ = "SUPER Language Creator Team"
__description__ = "Create custom programming languages with an intuitive interface"

# Import main application
from .main_application import EnhancedSuperLanguageCreator, main

# Import core systems for external use
from .core_systems import (
    EnhancedThemeEngine,
    EnhancedKeywordGenerator,
    AccessibilityManager,
    EnhancedAchievementSystem,
    EnhancedSyntaxHighlighter
)

# Import language processing components
from .language_processing import (
    LanguageValidator,
    InterpreterGenerator,
    CodeExecutor,
    TemplateProcessor
)

# Import file operations
from .file_operations import (
    FileOperations,
    AutoSaveManager,
    TemplateManager
)

# Import application features
from .application_features import (
    PlaygroundManager,
    DocumentationGenerator,
    StatisticsManager,
    ExamplesGallery,
    TutorialSystem,
    HelpSystem
)

# Export main classes for external use
__all__ = [
    'EnhancedSuperLanguageCreator',
    'main',
    'EnhancedThemeEngine',
    'EnhancedKeywordGenerator',
    'LanguageValidator',
    'InterpreterGenerator',
    'FileOperations',
    'PlaygroundManager',
    'DocumentationGenerator'
]