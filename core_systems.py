"""
Core Systems Module for LangGen
Contains: Theme Engine, Accessibility Manager, Achievement System, and Syntax Highlighter
"""

import tkinter as tk
from tkinter import ttk
import json
import os
import random
import re
from dataclasses import dataclass
from typing import Dict, List, Any, Optional

# Try to import additional libraries for enhanced features
try:
    from PIL import Image, ImageTk, ImageDraw
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

# ============================================================================
# ENHANCED THEME ENGINE WITH MODERN COLORS
# ============================================================================

class EnhancedThemeEngine:
    """Advanced theme system with modern color schemes and accessibility"""
    
    themes = {
        'modern_light': {
            'name': 'Modern Light',
            'bg': '#ffffff',
            'fg': '#1a202c',
            'primary': '#667eea',
            'secondary': '#764ba2',
            'accent': '#f093fb',
            'danger': '#ff6b6b',
            'success': '#51cf66',
            'warning': '#ffd43b',
            'info': '#74c0fc',
            'card': '#f8f9fa',
            'border': '#e9ecef',
            'shadow': '#00000010',
            'sidebar': '#f1f3f4',
            'toolbar': '#ffffff',
            'gradient_start': '#667eea',
            'gradient_end': '#764ba2'
        },
        'dark_pro': {
            'name': 'Dark Professional',
            'bg': '#0f0f23',
            'fg': '#ffffff',
            'primary': '#bb86fc',
            'secondary': '#3700b3',
            'accent': '#03dac6',
            'danger': '#cf6679',
            'success': '#4caf50',
            'warning': '#ff9800',
            'info': '#2196f3',
            'card': '#1e1e2e',
            'border': '#2d2d44',
            'shadow': '#00000040',
            'sidebar': '#181825',
            'toolbar': '#1e1e2e',
            'gradient_start': '#bb86fc',
            'gradient_end': '#3700b3'
        },
        'ocean_breeze': {
            'name': 'Ocean Breeze',
            'bg': '#e3f2fd',
            'fg': '#0d47a1',
            'primary': '#1976d2',
            'secondary': '#0288d1',
            'accent': '#00acc1',
            'danger': '#d32f2f',
            'success': '#388e3c',
            'warning': '#f57c00',
            'info': '#1976d2',
            'card': '#ffffff',
            'border': '#bbdefb',
            'shadow': '#0d47a120',
            'sidebar': '#e1f5fe',
            'toolbar': '#ffffff',
            'gradient_start': '#1976d2',
            'gradient_end': '#00acc1'
        },
        'sunset_glow': {
            'name': 'Sunset Glow',
            'bg': '#fff5f5',
            'fg': '#742a2a',
            'primary': '#ed8936',
            'secondary': '#dd6b20',
            'accent': '#f56565',
            'danger': '#e53e3e',
            'success': '#38a169',
            'warning': '#d69e2e',
            'info': '#3182ce',
            'card': '#ffffff',
            'border': '#fed7d7',
            'shadow': '#74222220',
            'sidebar': '#fef5e7',
            'toolbar': '#ffffff',
            'gradient_start': '#ed8936',
            'gradient_end': '#f56565'
        },
        'forest_zen': {
            'name': 'Forest Zen',
            'bg': '#f0fff4',
            'fg': '#1a202c',
            'primary': '#38a169',
            'secondary': '#2f855a',
            'accent': '#68d391',
            'danger': '#e53e3e',
            'success': '#38a169',
            'warning': '#d69e2e',
            'info': '#3182ce',
            'card': '#ffffff',
            'border': '#c6f6d5',
            'shadow': '#22543d20',
            'sidebar': '#f0fff4',
            'toolbar': '#ffffff',
            'gradient_start': '#38a169',
            'gradient_end': '#68d391'
        },
        'high_contrast': {
            'name': 'High Contrast (Accessible)',
            'bg': '#ffffff',
            'fg': '#000000',
            'primary': '#0066cc',
            'secondary': '#004499',
            'accent': '#ff6600',
            'danger': '#cc0000',
            'success': '#006600',
            'warning': '#cc6600',
            'info': '#0066cc',
            'card': '#ffffff',
            'border': '#000000',
            'shadow': '#00000030',
            'sidebar': '#f0f0f0',
            'toolbar': '#ffffff',
            'gradient_start': '#0066cc',
            'gradient_end': '#004499'
        }
    }

    @staticmethod
    def create_gradient_bg(canvas, width, height, start_color, end_color):
        """Create a gradient background on canvas"""
        # Convert hex to RGB
        def hex_to_rgb(hex_color):
            return tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))
        
        start_rgb = hex_to_rgb(start_color)
        end_rgb = hex_to_rgb(end_color)
        
        # Create gradient
        for i in range(height):
            ratio = i / height
            r = int(start_rgb[0] * (1 - ratio) + end_rgb[0] * ratio)
            g = int(start_rgb[1] * (1 - ratio) + end_rgb[1] * ratio)
            b = int(start_rgb[2] * (1 - ratio) + end_rgb[2] * ratio)
            color = f'#{r:02x}{g:02x}{b:02x}'
            canvas.create_line(0, i, width, i, fill=color)

# ============================================================================
# ENHANCED RANDOM KEYWORDS GENERATOR
# ============================================================================

class EnhancedKeywordGenerator:
    """Enhanced random keyword generator with more themes and context"""
    
    themes = {
        'space_odyssey': {
            'name': 'Space Odyssey',
            'icon': '🚀',
            'keywords': {
                'function': ['orbit', 'launch', 'mission', 'voyage', 'explore', 'journey'],
                'variable': ['cargo', 'fuel', 'data', 'signal', 'beacon', 'pod'],
                'if': ['scan', 'detect', 'check', 'probe', 'analyze'],
                'else': ['otherwise', 'alternate', 'backup', 'fallback'],
                'loop': ['cycle', 'orbit', 'rotate', 'revolve', 'spin'],
                'return': ['land', 'dock', 'arrive', 'report', 'transmit'],
                'true': ['confirmed', 'positive', 'affirmative', 'yes'],
                'false': ['negative', 'denied', 'abort', 'no'],
                'null': ['void', 'empty', 'vacuum', 'space']
            },
            'functions': {
                'print': ['broadcast', 'transmit', 'announce', 'signal', 'display'],
                'input': ['receive', 'scan', 'capture', 'detect', 'read'],
                'length': ['measure', 'distance', 'size', 'span'],
                'random': ['cosmic', 'stellar', 'nebula', 'quantum']
            }
        },
        'magical_realm': {
            'name': 'Magical Realm',
            'icon': '🧙‍♀️',
            'keywords': {
                'function': ['spell', 'enchant', 'cast', 'conjure', 'invoke', 'ritual'],
                'variable': ['essence', 'charm', 'rune', 'crystal', 'potion', 'scroll'],
                'if': ['divine', 'foresee', 'prophecy', 'vision', 'oracle'],
                'else': ['otherwise', 'alternative', 'destiny'],
                'loop': ['chant', 'ritual', 'circle', 'spiral'],
                'return': ['manifest', 'summon', 'appear', 'reveal'],
                'true': ['blessed', 'sacred', 'divine', 'pure'],
                'false': ['cursed', 'dark', 'forbidden', 'void'],
                'null': ['empty', 'void', 'shadow', 'nothing']
            },
            'functions': {
                'print': ['reveal', 'manifest', 'show', 'display', 'illuminate'],
                'input': ['commune', 'channel', 'receive', 'divine'],
                'length': ['measure', 'count', 'weigh'],
                'random': ['fate', 'chance', 'luck', 'destiny']
            }
        },
        'nature_harmony': {
            'name': 'Nature Harmony',
            'icon': '🌿',
            'keywords': {
                'function': ['grow', 'bloom', 'flourish', 'nurture', 'cultivate'],
                'variable': ['seed', 'root', 'branch', 'leaf', 'flower', 'fruit'],
                'if': ['sense', 'feel', 'observe', 'notice'],
                'else': ['otherwise', 'naturally', 'alternatively'],
                'loop': ['cycle', 'season', 'flow', 'pattern'],
                'return': ['yield', 'harvest', 'produce', 'bear'],
                'true': ['alive', 'thriving', 'healthy', 'vibrant'],
                'false': ['wilted', 'dormant', 'dry'],
                'null': ['empty', 'barren', 'void']
            },
            'functions': {
                'print': ['show', 'display', 'reveal', 'express'],
                'input': ['absorb', 'gather', 'collect', 'receive'],
                'length': ['measure', 'span', 'reach'],
                'random': ['wild', 'natural', 'organic', 'free']
            }
        },
        'cyber_future': {
            'name': 'Cyber Future',
            'icon': '🤖',
            'keywords': {
                'function': ['execute', 'process', 'compute', 'run', 'operate'],
                'variable': ['data', 'cache', 'buffer', 'memory', 'register'],
                'if': ['scan', 'analyze', 'check', 'verify', 'test'],
                'else': ['fallback', 'alternative', 'backup'],
                'loop': ['iterate', 'cycle', 'repeat', 'process'],
                'return': ['output', 'result', 'response', 'yield'],
                'true': ['active', 'online', 'connected', 'ready'],
                'false': ['offline', 'error', 'failed', 'inactive'],
                'null': ['empty', 'null', 'void', 'undefined']
            },
            'functions': {
                'print': ['output', 'display', 'log', 'echo'],
                'input': ['read', 'scan', 'capture', 'input'],
                'length': ['size', 'count', 'bytes'],
                'random': ['generate', 'random', 'chaos']
            }
        },
        'pirate_adventure': {
            'name': 'Pirate Adventure',
            'icon': '🏴‍☠️',
            'keywords': {
                'function': ['sail', 'voyage', 'quest', 'adventure', 'explore'],
                'variable': ['treasure', 'gold', 'chest', 'map', 'compass'],
                'if': ['scout', 'lookout', 'spy', 'search'],
                'else': ['otherwise', 'alternatively', 'abandon'],
                'loop': ['patrol', 'cruise', 'circle', 'navigate'],
                'return': ['dock', 'anchor', 'harbor', 'port'],
                'true': ['aye', 'agreed', 'confirmed'],
                'false': ['nay', 'denied', 'refused'],
                'null': ['empty', 'void', 'lost']
            },
            'functions': {
                'print': ['shout', 'announce', 'declare', 'proclaim'],
                'input': ['hear', 'listen', 'receive'],
                'length': ['measure', 'count', 'tally'],
                'random': ['fortune', 'fate', 'chance']
            }
        },
        'food_kitchen': {
            'name': 'Food & Kitchen',
            'icon': '👨‍🍳',
            'keywords': {
                'function': ['cook', 'bake', 'prepare', 'recipe', 'make'],
                'variable': ['ingredient', 'spice', 'dish', 'meal', 'flavor'],
                'if': ['taste', 'check', 'season', 'sample'],
                'else': ['otherwise', 'alternatively', 'substitute'],
                'loop': ['stir', 'mix', 'blend', 'whisk'],
                'return': ['serve', 'present', 'dish', 'plate'],
                'true': ['delicious', 'tasty', 'perfect', 'done'],
                'false': ['bland', 'raw', 'burnt'],
                'null': ['empty', 'plain', 'nothing']
            },
            'functions': {
                'print': ['serve', 'present', 'display', 'show'],
                'input': ['gather', 'collect', 'get'],
                'length': ['measure', 'count', 'portion'],
                'random': ['surprise', 'special', 'daily']
            }
        }
    }
    
    @classmethod
    def get_random_theme(cls):
        """Get a random theme"""
        return random.choice(list(cls.themes.keys()))
    
    @classmethod
    def generate_keywords(cls, theme_name=None):
        """Generate random keywords from a theme"""
        if theme_name is None:
            theme_name = cls.get_random_theme()
        
        if theme_name not in cls.themes:
            theme_name = cls.get_random_theme()
        
        theme = cls.themes[theme_name]
        result = {}
        
        for keyword, options in theme['keywords'].items():
            result[keyword] = random.choice(options)
        
        return result, theme['name'], theme['icon']
    
    @classmethod
    def generate_functions(cls, theme_name=None):
        """Generate random function names from a theme"""
        if theme_name is None:
            theme_name = cls.get_random_theme()
        
        if theme_name not in cls.themes:
            theme_name = cls.get_random_theme()
        
        theme = cls.themes[theme_name]
        result = {}
        
        for func, options in theme['functions'].items():
            result[func] = random.choice(options)
        
        return result

# ============================================================================
# ACCESSIBILITY MANAGER
# ============================================================================

class AccessibilityManager:
    """Manage accessibility features"""
    
    def __init__(self, root):
        self.root = root
        self.font_size = 12
        self.high_contrast = False
        self.screen_reader_mode = False
        
    def increase_font_size(self):
        """Increase font size for better readability"""
        self.font_size = min(self.font_size + 2, 24)
        self.apply_font_changes()
    
    def decrease_font_size(self):
        """Decrease font size"""
        self.font_size = max(self.font_size - 2, 8)
        self.apply_font_changes()
    
    def apply_font_changes(self):
        """Apply font size changes to all widgets"""
        self._update_fonts_recursive(self.root)
    
    def _update_fonts_recursive(self, widget):
        """Recursively update fonts"""
        try:
            current_font = widget.cget('font')
            if current_font:
                if isinstance(current_font, tuple):
                    family, size, *style = current_font
                    widget.configure(font=(family, self.font_size, *style))
                else:
                    widget.configure(font=('Arial', self.font_size))
        except:
            pass
        
        for child in widget.winfo_children():
            self._update_fonts_recursive(child)
    
    def toggle_high_contrast(self):
        """Toggle high contrast mode"""
        self.high_contrast = not self.high_contrast
        return 'high_contrast' if self.high_contrast else None
    
    def setup_keyboard_navigation(self, widget):
        """Setup keyboard navigation for widget"""
        widget.bind('<Tab>', self._handle_tab)
        widget.bind('<Shift-Tab>', self._handle_shift_tab)
        widget.bind('<Return>', self._handle_enter)
        widget.bind('<space>', self._handle_space)
    
    def _handle_tab(self, event):
        """Handle tab navigation"""
        event.widget.tk_focusNext().focus()
        return "break"
    
    def _handle_shift_tab(self, event):
        """Handle shift+tab navigation"""
        event.widget.tk_focusPrev().focus()
        return "break"
    
    def _handle_enter(self, event):
        """Handle enter key"""
        if hasattr(event.widget, 'invoke'):
            event.widget.invoke()
        return "break"
    
    def _handle_space(self, event):
        """Handle space key"""
        if hasattr(event.widget, 'invoke'):
            event.widget.invoke()
        return "break"

# ============================================================================
# ENHANCED ACHIEVEMENT SYSTEM
# ============================================================================

@dataclass
class Achievement:
    id: str
    name: str
    description: str
    icon: str
    points: int
    unlocked: bool = False
    category: str = "general"

class EnhancedAchievementSystem:
    """Enhanced gamification system with categories and better rewards"""
    
    def __init__(self):
        self.achievements = [
            # Beginner achievements
            Achievement("first_lang", "First Steps", "Create your first language", "🎯", 10, category="beginner"),
            Achievement("name_master", "Name Master", "Give your language a creative name", "📝", 15, category="beginner"),
            Achievement("keyword_explorer", "Keyword Explorer", "Define your first keyword", "🔤", 20, category="beginner"),
            
            # Progress achievements
            Achievement("keyword_master", "Keyword Master", "Define all basic keywords", "🔥", 30, category="progress"),
            Achievement("function_guru", "Function Guru", "Define all essential functions", "🛠️", 35, category="progress"),
            Achievement("error_friend", "Error Friend", "Create friendly error messages", "🤗", 25, category="progress"),
            
            # Creativity achievements
            Achievement("emoji_lover", "Emoji Lover", "Use emojis in your language", "😄", 30, category="creativity"),
            Achievement("theme_explorer", "Theme Explorer", "Try different themes", "🎨", 25, category="creativity"),
            Achievement("random_master", "Random Master", "Use random keyword generator", "🎲", 20, category="creativity"),
            
            # Advanced achievements
            Achievement("test_pilot", "Test Pilot", "Test your language multiple times", "🧪", 40, category="advanced"),
            Achievement("code_writer", "Code Writer", "Write substantial example code", "✍️", 45, category="advanced"),
            Achievement("share_joy", "Share the Joy", "Export your language", "📤", 50, category="advanced"),
            
            # Master achievements
            Achievement("language_family", "Language Family", "Create multiple languages", "👨‍👩‍👧‍👦", 75, category="master"),
            Achievement("perfectionist", "Perfectionist", "Complete all language fields", "💎", 100, category="master"),
            Achievement("speed_demon", "Speed Demon", "Create a language in under 5 minutes", "⚡", 60, category="master"),
        ]
        
        self.total_points = 0
        self.streaks = {}
        self.load_progress()
    
    def unlock(self, achievement_id: str):
        """Unlock an achievement"""
        for ach in self.achievements:
            if ach.id == achievement_id and not ach.unlocked:
                ach.unlocked = True
                self.total_points += ach.points
                self.save_progress()
                return ach
        return None
    
    def get_progress(self):
        """Get achievement progress"""
        unlocked = sum(1 for a in self.achievements if a.unlocked)
        total = len(self.achievements)
        return unlocked, total, self.total_points
    
    def get_achievements_by_category(self):
        """Get achievements grouped by category"""
        categories = {}
        for ach in self.achievements:
            if ach.category not in categories:
                categories[ach.category] = []
            categories[ach.category].append(ach)
        return categories
    
    def save_progress(self):
        """Save achievement progress"""
        data = {
            'achievements': {a.id: a.unlocked for a in self.achievements},
            'total_points': self.total_points,
            'streaks': self.streaks
        }
        try:
            with open('.achievements.json', 'w') as f:
                json.dump(data, f)
        except:
            pass
    
    def load_progress(self):
        """Load achievement progress"""
        try:
            with open('.achievements.json', 'r') as f:
                data = json.load(f)
                for ach in self.achievements:
                    if ach.id in data['achievements']:
                        ach.unlocked = data['achievements'][ach.id]
                self.total_points = data.get('total_points', 0)
                self.streaks = data.get('streaks', {})
        except:
            pass

# ============================================================================
# ENHANCED SYNTAX HIGHLIGHTER
# ============================================================================

class EnhancedSyntaxHighlighter:
    """Enhanced syntax highlighting with better colors and more features"""
    
    def __init__(self, text_widget, language_data, theme='light'):
        self.text = text_widget
        self.language = language_data
        self.theme = theme
        self.setup_tags()
    
    def setup_tags(self):
        """Setup enhanced color tags for syntax highlighting"""
        if self.theme == 'dark':
            colors = {
                'keyword': '#ff79c6',
                'string': '#f1fa8c',
                'number': '#bd93f9',
                'comment': '#6272a4',
                'function': '#50fa7b',
                'operator': '#ff5555',
                'identifier': '#f8f8f2',
                'boolean': '#ffb86c'
            }
        else:
            colors = {
                'keyword': '#d73a49',
                'string': '#032f62',
                'number': '#005cc5',
                'comment': '#6a737d',
                'function': '#6f42c1',
                'operator': '#d73a49',
                'identifier': '#24292e',
                'boolean': '#005cc5'
            }
        
        # Configure tags with enhanced styling
        for tag, color in colors.items():
            font_style = ('Consolas' if os.name == 'nt' else 'Monaco', 11)
            if tag == 'keyword':
                font_style = font_style + ('bold',)
            elif tag == 'comment':
                font_style = font_style + ('italic',)
            elif tag == 'function':
                font_style = font_style + ('bold',)
            
            self.text.tag_config(tag, foreground=color, font=font_style)
    
    def highlight(self):
        """Apply enhanced syntax highlighting"""
        # Clear existing tags
        for tag in ['keyword', 'string', 'number', 'comment', 'function', 'operator', 'identifier', 'boolean']:
            self.text.tag_remove(tag, '1.0', 'end')
        
        content = self.text.get('1.0', 'end-1c')
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            self._highlight_line(line, line_num)
    
    def _highlight_line(self, line, line_num):
        """Highlight a single line"""
        start_pos = f"{line_num}.0"
        
        # Keywords
        for keyword in self.language.get('keywords', {}).values():
            if keyword:
                self._highlight_pattern(line, line_num, rf'\b{re.escape(keyword)}\b', 'keyword')
        
        # Built-in functions
        for func in self.language.get('builtins', {}).values():
            if func:
                self._highlight_pattern(line, line_num, rf'\b{re.escape(func)}\b(?=\s*\()', 'function')
        
        # Strings
        self._highlight_pattern(line, line_num, r'"[^"]*"', 'string')
        self._highlight_pattern(line, line_num, r"'[^']*'", 'string')
        
        # Numbers
        self._highlight_pattern(line, line_num, r'\b\d+(\.\d+)?\b', 'number')
        
        # Comments
        self._highlight_pattern(line, line_num, r'#.*$', 'comment')
        
        # Booleans
        true_val = self.language.get('keywords', {}).get('true', 'true')
        false_val = self.language.get('keywords', {}).get('false', 'false')
        if true_val:
            self._highlight_pattern(line, line_num, rf'\b{re.escape(true_val)}\b', 'boolean')
        if false_val:
            self._highlight_pattern(line, line_num, rf'\b{re.escape(false_val)}\b', 'boolean')
        
        # Operators
        operators = ['+', '-', '*', '/', '=', '==', '!=', '<', '>', '<=', '>=']
        for op in operators:
            self._highlight_pattern(line, line_num, re.escape(op), 'operator')
    
    def _highlight_pattern(self, line, line_num, pattern, tag):
        """Highlight pattern in line"""
        for match in re.finditer(pattern, line):
            start = f"{line_num}.{match.start()}"
            end = f"{line_num}.{match.end()}"
            self.text.tag_add(tag, start, end)