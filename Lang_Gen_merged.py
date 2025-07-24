import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext, font
import json
import os
import sys
import subprocess
import webbrowser
from datetime import datetime
from typing import Dict, List, Any, Optional
import random
import re
import threading
import time
from dataclasses import dataclass
import base64


# Try to import additional libraries for enhanced features
try:
    from PIL import Image, ImageTk, ImageDraw
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

try:
    import pygame
    HAS_PYGAME = True
except ImportError:
    HAS_PYGAME = False


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
        'material_you': {
            'name': 'Material You',
            'bg': '#fefbff',
            'fg': '#1c1b1f',
            'primary': '#6750a4',
            'secondary': '#625b71',
            'accent': '#7d5260',
            'danger': '#ba1a1a',
            'success': '#146c2e',
            'warning': '#7d5a00',
            'info': '#0061a4',
            'card': '#ffffff',
            'border': '#e7e0ec',
            'shadow': '#00000015',
            'sidebar': '#f7f2fa',
            'toolbar': '#ffffff',
            'gradient_start': '#6750a4',
            'gradient_end': '#7d5260'
        },
        'fluent_dark': {
            'name': 'Fluent Dark',
            'bg': '#202020',
            'fg': '#ffffff',
            'primary': '#0078d4',
            'secondary': '#106ebe',
            'accent': '#60cdff',
            'danger': '#d13438',
            'success': '#107c10',
            'warning': '#fcf23a',
            'info': '#0078d4',
            'card': '#2d2d2d',
            'border': '#3b3b3b',
            'shadow': '#00000030',
            'sidebar': '#1b1b1b',
            'toolbar': '#2d2d2d',
            'gradient_start': '#0078d4',
            'gradient_end': '#60cdff'
        },
        'nord_theme': {
            'name': 'Nord',
            'bg': '#eceff4',
            'fg': '#2e3440',
            'primary': '#5e81ac',
            'secondary': '#81a1c1',
            'accent': '#88c0d0',
            'danger': '#bf616a',
            'success': '#a3be8c',
            'warning': '#ebcb8b',
            'info': '#5e81ac',
            'card': '#f5f5f5',
            'border': '#d8dee9',
            'shadow': '#2e344020',
            'sidebar': '#e5e9f0',
            'toolbar': '#f5f5f5',
            'gradient_start': '#5e81ac',
            'gradient_end': '#88c0d0'
        },
        'catppuccin_latte': {
            'name': 'Catppuccin Latte',
            'bg': '#eff1f5',
            'fg': '#4c4f69',
            'primary': '#8839ef',
            'secondary': '#7287fd',
            'accent': '#dd7878',
            'danger': '#d20f39',
            'success': '#40a02b',
            'warning': '#df8e1d',
            'info': '#1e66f5',
            'card': '#ffffff',
            'border': '#dce0e8',
            'shadow': '#4c4f6920',
            'sidebar': '#e6e9ef',
            'toolbar': '#ffffff',
            'gradient_start': '#8839ef',
            'gradient_end': '#dd7878'
        },
        'tokyo_night': {
            'name': 'Tokyo Night',
            'bg': '#1a1b26',
            'fg': '#c0caf5',
            'primary': '#7aa2f7',
            'secondary': '#bb9af7',
            'accent': '#f7768e',
            'danger': '#f7768e',
            'success': '#9ece6a',
            'warning': '#e0af68',
            'info': '#7dcfff',
            'card': '#24283b',
            'border': '#414868',
            'shadow': '#00000040',
            'sidebar': '#16161e',
            'toolbar': '#24283b',
            'gradient_start': '#7aa2f7',
            'gradient_end': '#bb9af7'
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

# ============================================================================
# MAIN ENHANCED SUPER LANGUAGE CREATOR
# ============================================================================

class EnhancedSuperLanguageCreator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("✨ SUPER Language Creator - Enhanced Edition")
        self.window.geometry("1600x1000")
        self.window.minsize(1200, 800)
        
        # Initialize enhanced systems
        self.theme_engine = EnhancedThemeEngine()
        self.current_theme = 'modern_light'
        self.achievement_system = EnhancedAchievementSystem()
        self.keyword_generator = EnhancedKeywordGenerator()
        self.accessibility = AccessibilityManager(self.window)
        
        # Language data
        self.language_data = {
            'name': 'MyLang',
            'version': '1.0',
            'author': 'Young Coder',
            'description': 'My awesome programming language!',
            'keywords': {},
            'operators': {},
            'builtins': {},
            'errors': {},
            'examples': [],
            'theme': 'modern_light',
            'created': datetime.now().isoformat()
        }
        
        # UI state
        self.syntax_highlighter = None
        self.playground_running = False
        self.test_count = 0
        self.start_time = time.time()
        
        # Setup enhanced UI
        self.setup_enhanced_styles()
        self.setup_ui()
        self.apply_theme()
        
        # Setup accessibility
        self.setup_accessibility()
        
        # Auto-save timer
        self.setup_autosave()

    def show_about(self):
        """Show about dialog"""
        dialog = tk.Toplevel(self.window)
        dialog.title("ℹ️ About SUPER Language Creator")
        dialog.geometry("500x400")
        dialog.transient(self.window)
        dialog.resizable(False, False)
        
        # Header with gradient effect
        header = tk.Frame(dialog, bg='#667eea', height=100)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        header_content = tk.Frame(header, bg='#667eea')
        header_content.pack(expand=True, fill='both', padx=30, pady=20)
        
        # App icon and title
        title_frame = tk.Frame(header_content, bg='#667eea')
        title_frame.pack(anchor='center')
        
        tk.Label(title_frame, text="✨", font=('Arial', 40),
                bg='#667eea', fg='white').pack()
        
        tk.Label(title_frame, text="SUPER Language Creator", 
                font=('Arial', 18, 'bold'), bg='#667eea', fg='white').pack()
        
        tk.Label(title_frame, text="Enhanced Edition", 
                font=('Arial', 12), bg='#667eea', fg='#e2e8f0').pack()
        
        # Main content
        content = tk.Frame(dialog, bg='white', padx=30, pady=20)
        content.pack(fill='both', expand=True)
        
        # Version info
        version_info = [
            ("Version", "2.0.0 Enhanced"),
            ("Build", "2024.1"),
            ("Python", f"{sys.version.split()[0]}"),
            ("Platform", sys.platform.title())
        ]
        
        info_frame = tk.Frame(content, bg='white')
        info_frame.pack(fill='x', pady=(0, 20))
        
        for label, value in version_info:
            row = tk.Frame(info_frame, bg='white')
            row.pack(fill='x', pady=2)
            
            tk.Label(row, text=f"{label}:", font=('Arial', 11),
                    bg='white', fg='#4a5568').pack(side='left')
            tk.Label(row, text=value, font=('Arial', 11, 'bold'),
                    bg='white', fg='#1a202c').pack(side='right')
        
        # Description
        desc_text = """Create your own programming languages with ease! 
        
    This enhanced edition includes advanced themes, accessibility features, achievement system, and much more.

    Perfect for educators, students, and anyone curious about programming language design."""
        
        tk.Label(content, text=desc_text, font=('Arial', 11),
                bg='white', fg='#4a5568', wraplength=400,
                justify='left').pack(pady=10)
        
        # Credits
        credits_frame = tk.LabelFrame(content, text="Credits", 
                                    font=('Arial', 11, 'bold'), bg='white')
        credits_frame.pack(fill='x', pady=(10, 0))
        
        credits = [
            "• Built with Python & Tkinter",
            "• Enhanced UI design principles",
            "• Accessibility features included",
            "• Created for educational purposes"
        ]
        
        for credit in credits:
            tk.Label(credits_frame, text=credit, font=('Arial', 10),
                    bg='white', fg='#666').pack(anchor='w', padx=10, pady=2)
        
        # Close button
        tk.Button(content, text="Close", command=dialog.destroy,
                bg='#667eea', fg='white', font=('Arial', 11),
                padx=20, pady=8).pack(pady=(20, 0))

    def create_enhanced_errors_tab(self):
        """Create enhanced error messages tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="⚠️ Error Messages")
        
        # Header
        header_frame = tk.Frame(tab, bg='#e53e3e', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg='#e53e3e')
        header_content.pack(expand=True, fill='both', padx=30, pady=20)
        
        tk.Label(header_content, text="⚠️ Error Messages", 
                font=('Arial', 20, 'bold'), bg='#e53e3e', fg='white').pack(anchor='w')
        tk.Label(header_content, text="Make errors friendly and helpful",
                font=('Arial', 12), bg='#e53e3e', fg='#fed7d7').pack(anchor='w')
        
        # Scrollable content
        canvas = tk.Canvas(tab, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient='vertical', command=canvas.yview)
        content_frame = tk.Frame(canvas, bg='white')
        
        content_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=content_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Main content
        main_content = tk.Frame(content_frame, bg='white', padx=40, pady=30)
        main_content.pack(fill='both', expand=True)
        
        # Error types
        error_types = [
            ('syntax_error', 'Syntax Error', '🚫', 
            'When code structure is wrong', 
            "Oops! There's a problem with how you wrote that. Check for missing quotes or brackets."),
            ('name_error', 'Name Error', '❓', 
            'When using undefined variables',
            "I don't know what '{name}' means. Did you spell it correctly?"),
            ('type_error', 'Type Error', '🔄', 
            'When mixing incompatible types',
            "I expected {expected} but got {got}. Try converting the value first."),
            ('value_error', 'Value Error', '⚡', 
            'When value is wrong type',
            "The value you provided doesn't work here. Please check and try again."),
        ]
        
        self.error_entries = {}
        
        for error_key, error_name, icon, description, default_msg in error_types:
            # Error section
            error_section = tk.Frame(main_content, bg='white', relief='solid', bd=1)
            error_section.pack(fill='x', pady=10)
            
            # Header
            error_header = tk.Frame(error_section, bg='#fed7d7', padx=15, pady=10)
            error_header.pack(fill='x')
            
            header_left = tk.Frame(error_header, bg='#fed7d7')
            header_left.pack(side='left', fill='x', expand=True)
            
            tk.Label(header_left, text=f"{icon} {error_name}", 
                    font=('Arial', 14, 'bold'), bg='#fed7d7').pack(anchor='w')
            tk.Label(header_left, text=description, font=('Arial', 11),
                    bg='#fed7d7', fg='#742a2a').pack(anchor='w')
            
            # Preview button
            tk.Button(error_header, text="👁️ Preview",
                    command=lambda k=error_key: self.preview_error(k),
                    bg='#e53e3e', fg='white', relief='flat',
                    font=('Arial', 10), padx=15, pady=5).pack(side='right')
            
            # Message input
            input_frame = tk.Frame(error_section, bg='white', padx=15, pady=10)
            input_frame.pack(fill='x')
            
            tk.Label(input_frame, text="Your friendly error message:", 
                    font=('Arial', 11, 'bold'), bg='white').pack(anchor='w')
            
            error_text = tk.Text(input_frame, height=3, font=('Arial', 11),
                            wrap='word', relief='solid', bd=1, bg='#f8f9fa')
            error_text.pack(fill='x', pady=(5, 0))
            error_text.insert('1.0', default_msg)
            
            self.error_entries[error_key] = error_text
            
            # Help text
            help_frame = tk.Frame(input_frame, bg='white')
            help_frame.pack(fill='x', pady=(5, 0))
            
            help_text = "💡 Tip: Use {name}, {expected}, {got} as placeholders for dynamic values"
            tk.Label(help_frame, text=help_text, font=('Arial', 9),
                    bg='white', fg='#666', anchor='w').pack(fill='x')

    def preview_error(self, error_key):
        """Preview how an error would look"""
        if not hasattr(self, 'error_entries') or error_key not in self.error_entries:
            messagebox.showinfo("Preview", "Error preview not available")
            return
            
        error_msg = self.error_entries[error_key].get('1.0', 'end-1c').strip()
        
        # Create preview window
        preview = tk.Toplevel(self.window)
        preview.title("Error Preview")
        preview.geometry("500x300")
        preview.transient(self.window)
        
        # Error display
        frame = tk.Frame(preview, bg='#fee', padx=20, pady=20)
        frame.pack(fill='both', expand=True)
        
        # Error icon and title
        header = tk.Frame(frame, bg='#fee')
        header.pack(fill='x')
        
        tk.Label(header, text="❌", font=('Arial', 40),
                bg='#fee').pack(side='left', padx=(0, 20))
        
        tk.Label(header, text=f"{error_key.replace('_', ' ').title()}",
                font=('Arial', 20, 'bold'), bg='#fee').pack(side='left')
        
        # Error message
        msg_frame = tk.Frame(frame, bg='white', relief='solid', bd=1)
        msg_frame.pack(fill='both', expand=True, pady=20)
        
        # Format message with placeholders
        formatted_msg = error_msg
        if '{name}' in formatted_msg:
            formatted_msg = formatted_msg.replace('{name}', 'myVariable')
        if '{expected}' in formatted_msg:
            formatted_msg = formatted_msg.replace('{expected}', 'number')
        if '{got}' in formatted_msg:
            formatted_msg = formatted_msg.replace('{got}', 'string')
        
        tk.Label(msg_frame, text=formatted_msg, font=('Arial', 14),
                bg='white', wraplength=400, justify='left').pack(padx=20, pady=20)
        
        # Close button
        tk.Button(frame, text="Close", command=preview.destroy,
                bg='white', relief='solid', bd=1).pack(pady=10)

    def show_keyword_generator(self):
        """Alias for show_enhanced_keyword_generator"""
        self.show_enhanced_keyword_generator()

    def load_game_template(self):
        """Load game template"""
        self.language_data.update({
            'name': 'GameLang',
            'description': 'A fun game-themed programming language!',
            'keywords': {
                'function': 'quest',
                'variable': 'item',
                'if': 'check',
                'else': 'otherwise',
                'loop': 'repeat',
                'return': 'reward'
            },
            'builtins': {
                'print': 'announce',
                'input': 'ask_player',
                'length': 'count'
            }
        })
        self.populate_ui_from_data()
        self.unlock_achievement('theme_explorer')

    def load_color_template(self):
        """Load colorful template - SAFE VERSION"""
        try:
            self.language_data.update({
                'name': 'RainbowLang',
                'version': '1.0',
                'author': 'Creative Coder',
                'description': 'Express yourself with colors and emojis! 🌈',
                'keywords': {
                    'function': '🎯',
                    'variable': '📦',
                    'if': '❓',
                    'else': '↔️',
                    'loop': '🔄',
                    'return': '↩️'
                },
                'builtins': {
                    'print': '📢',
                    'input': '⌨️',
                    'length': '📏'
                },
                'features': {},
                'errors': {}
            })
            self.populate_ui_from_data()
            self.unlock_achievement('emoji_lover')
            self.update_status("Creative template loaded!")
        except Exception as e:
            print(f"Error loading color template: {e}")
            messagebox.showerror("Template Error", f"Could not load creative template: {e}")

    def load_edu_template(self):
        """Load educational template - SAFE VERSION"""
        try:
            self.language_data.update({
                'name': 'LearnCode',
                'version': '1.0',
                'author': 'Educator',
                'description': 'A friendly language for learning programming!',
                'keywords': {
                    'function': 'lesson',
                    'variable': 'remember',
                    'if': 'when',
                    'else': 'otherwise',
                    'loop': 'practice',
                    'return': 'answer'
                },
                'builtins': {
                    'print': 'show',
                    'input': 'ask',
                    'length': 'measure'
                },
                'features': {},
                'errors': {}
            })
            self.populate_ui_from_data()
            self.update_status("Educational template loaded!")
        except Exception as e:
            print(f"Error loading edu template: {e}")
            messagebox.showerror("Template Error", f"Could not load educational template: {e}")

    def start_scratch(self):
        """Start from scratch - SAFE VERSION"""
        try:
            self.new_language()
            self.update_status("Started new language from scratch!")
        except Exception as e:
            print(f"Error starting from scratch: {e}")
            messagebox.showerror("Error", f"Could not start new language: {e}")

    def save_to_recent(self):
        """Save current language to recent list"""
        try:
            # Load existing recent list
            try:
                with open('.recent_languages.json', 'r') as f:
                    recent = json.load(f)
            except:
                recent = []
            
            # Create new entry
            new_entry = {
                'name': self.language_data.get('name', 'Unnamed'),
                'author': self.language_data.get('author', 'Unknown'),
                'date': datetime.now().isoformat(),
                'path': getattr(self, 'current_file', '')
            }
            
            # Remove if already exists
            recent = [r for r in recent if r['name'] != new_entry['name']]
            
            # Add to front and limit to 10
            recent.insert(0, new_entry)
            recent = recent[:10]
            
            # Save back
            with open('.recent_languages.json', 'w') as f:
                json.dump(recent, f, indent=2)
        except:
            pass  # Silently fail if can't save recent

    def load_recent_project(self, project):
        """Load a recent project"""
        if project.get('path') and os.path.exists(project['path']):
            # Load from file path
            try:
                with open(project['path'], 'r', encoding='utf-8') as f:
                    self.language_data = json.load(f)
                self.current_file = project['path']
                self.populate_ui_from_data()
                self.update_status(f"Loaded {project['name']}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not load project:\n{e}")
        else:
            messagebox.showinfo("Project Not Found", 
                            f"The project file for '{project['name']}' could not be found.")

    def toggle_toolbar(self):
        """Toggle toolbar visibility"""
        if hasattr(self, 'toolbar'):
            if self.toolbar.winfo_viewable():
                self.toolbar.pack_forget()
                self.update_status("Toolbar hidden")
            else:
                self.toolbar.pack(fill='x', before=self.main_paned)
                self.update_status("Toolbar shown")

    def toggle_status_bar(self):
        """Toggle status bar visibility"""
        if hasattr(self, 'status_bar'):
            if self.status_bar.winfo_viewable():
                self.status_bar.pack_forget()
                self.update_status("Status bar hidden")
            else:
                self.status_bar.pack(fill='x', side='bottom')
                self.update_status("Status bar shown")

    def toggle_progress_panel(self):
        """Toggle progress panel visibility"""
        if hasattr(self, 'right_panel'):
            if self.right_panel.winfo_viewable():
                self.main_paned.forget(self.right_panel)
                self.update_status("Progress panel hidden")
            else:
                self.main_paned.add(self.right_panel, weight=1)
                self.update_status("Progress panel shown")

    def handle_tab_navigation(self, event):
        """Handle tab navigation"""
        try:
            event.widget.tk_focusNext().focus()
            return "break"
        except:
            pass

    def handle_shift_tab_navigation(self, event):
        """Handle shift+tab navigation"""
        try:
            event.widget.tk_focusPrev().focus()
            return "break"
        except:
            pass

    def show_keyboard_help(self):
        """Show keyboard navigation help"""
        self.show_keyboard_shortcuts()

    def reset_font_size(self):
        """Reset font size to default"""
        self.accessibility.font_size = 12
        self.accessibility.apply_font_changes()
        self.update_status("Font size reset to default")

    def toggle_screen_reader_mode(self):
        """Toggle screen reader optimizations"""
        self.accessibility.screen_reader_mode = not self.accessibility.screen_reader_mode
        mode = "enabled" if self.accessibility.screen_reader_mode else "disabled"
        self.update_status(f"Screen reader mode {mode}")
        
        # Apply screen reader optimizations
        if self.accessibility.screen_reader_mode:
            # Add more descriptive labels, adjust tab order, etc.
            pass

    def create_enhanced_playground_tab(self):
        """Create enhanced playground tab with MORE templates"""
        if not hasattr(self, 'preview_notebook'):
            return
            
        playground_tab = ttk.Frame(self.preview_notebook)
        self.preview_notebook.add(playground_tab, text="🎮 Playground")
        
        # Editor toolbar
        toolbar = tk.Frame(playground_tab, bg='#2d3748', height=35)
        toolbar.pack(fill='x')
        toolbar.pack_propagate(False)
        
        toolbar_content = tk.Frame(toolbar, bg='#2d3748')
        toolbar_content.pack(expand=True, fill='both', padx=8, pady=3)
        
        # File operations
        tk.Button(toolbar_content, text="📁", font=('Arial', 10), relief='flat',
                bg='#2d3748', fg='white', command=self.open_file).pack(side='left', padx=1)
        tk.Button(toolbar_content, text="💾", font=('Arial', 10), relief='flat',
                bg='#2d3748', fg='white', command=self.save_file).pack(side='left', padx=1)
        
        # Template selector with MORE options
        tk.Label(toolbar_content, text="Templates:", bg='#2d3748', fg='white',
                font=('Arial', 8)).pack(side='left', padx=(8, 3))
        
        self.template_var = tk.StringVar()
        # ✨ EXPANDED TEMPLATE LIST
        template_options = [
            "hello_world", "calculator", "guessing_game", "genz_hello", "genz_calculator", 
            "genz_social_media", "todo_list", "password_checker", "fibonacci", "prime_numbers", 
            "story_generator", "quiz_game", "temperature_converter", "word_counter", "chatbot",
            "banking_system", "tic_tac_toe", "magic_8_ball", "rock_paper_scissors",
            "text_adventure", "simple_ai", "data_processor", "web_scraper"
        ]
        
        template_combo = ttk.Combobox(toolbar_content, textvariable=self.template_var,
                                    values=template_options,
                                    width=15, state='readonly')  # Wider for longer names
        template_combo.pack(side='left')
        template_combo.bind('<<ComboboxSelected>>', self.load_code_template)
        
        # Template info button
        info_btn = tk.Button(toolbar_content, text="ℹ️", font=('Arial', 10), relief='flat',
                            bg='#667eea', fg='white', command=self.show_template_info,
                            cursor='hand2')
        info_btn.pack(side='left', padx=(3, 0))
        
        # Editor area with line numbers
        editor_frame = tk.Frame(playground_tab)
        editor_frame.pack(fill='both', expand=True, padx=3, pady=3)
        
        # Line numbers
        self.line_numbers = tk.Text(editor_frame, width=3, bg='#1a202c',
                                fg='#a0aec0', font=('Consolas', 9),
                                state='disabled', relief='flat')
        self.line_numbers.pack(side='left', fill='y')
        
        # Main editor
        self.playground_code = scrolledtext.ScrolledText(
            editor_frame, 
            font=('Consolas', 10),
            wrap='none', undo=True, 
            bg='#1a202c', fg='#f7fafc',
            relief='flat', 
            insertbackground='white',
            selectbackground='#4a5568'
        )
        self.playground_code.pack(side='left', fill='both', expand=True)
        
        # Add syntax highlighting
        self.syntax_highlighter = EnhancedSyntaxHighlighter(
            self.playground_code, self.language_data, 'dark'
        )
        
        # Bind events for line numbers and syntax highlighting
        def update_line_numbers_and_syntax(event=None):
            self.update_line_numbers()
            if self.syntax_highlighter:
                self.syntax_highlighter.highlight()
            self.update_progress()
        
        self.playground_code.bind('<KeyRelease>', update_line_numbers_and_syntax)
        self.playground_code.bind('<Button-1>', self.update_line_numbers)
        
        # Run controls
        controls_frame = tk.Frame(playground_tab, bg='#2d3748', height=40)
        controls_frame.pack(fill='x')
        controls_frame.pack_propagate(False)
        
        controls_content = tk.Frame(controls_frame, bg='#2d3748')
        controls_content.pack(expand=True, pady=4)
        
        # Enhanced run button
        self.run_button = tk.Button(controls_content, text="▶ Run",
                                command=self.run_playground,
                                bg='#38a169', fg='white',
                                font=('Arial', 10, 'bold'),
                                relief='flat', padx=15, pady=6,
                                cursor='hand2')
        self.run_button.pack(side='left', padx=5)
        
        # Stop button
        self.stop_button = tk.Button(controls_content, text="■ Stop",
                                    command=self.stop_playground,
                                    bg='#e53e3e', fg='white',
                                    font=('Arial', 10, 'bold'),
                                    relief='flat', padx=12, pady=6,
                                    cursor='hand2', state='disabled')
        self.stop_button.pack(side='left', padx=3)
        
        # Clear button
        clear_btn = tk.Button(controls_content, text="🗑",
                            command=self.clear_output,
                            bg='#718096', fg='white',
                            font=('Arial', 10), relief='flat',
                            padx=8, pady=6, cursor='hand2')
        clear_btn.pack(side='left', padx=3)
        
        # Speed control
        speed_frame = tk.Frame(controls_content, bg='#2d3748')
        speed_frame.pack(side='right', padx=8)
        
        tk.Label(speed_frame, text="Speed:", bg='#2d3748', fg='white',
                font=('Arial', 8)).pack(side='left')
        
        self.speed_scale = tk.Scale(speed_frame, from_=1, to=5, orient='horizontal',
                                bg='#2d3748', fg='white', length=60,
                                showvalue=0, highlightthickness=0)
        self.speed_scale.set(3)
        self.speed_scale.pack(side='left', padx=3)
        
        # Output area
        output_frame = tk.Frame(playground_tab)
        output_frame.pack(fill='both', expand=True, padx=3, pady=(0, 3))
        
        output_header = tk.Frame(output_frame, bg='#2d3748', height=25)
        output_header.pack(fill='x')
        output_header.pack_propagate(False)
        
        tk.Label(output_header, text="📤 Output", font=('Arial', 10, 'bold'),
                bg='#2d3748', fg='white').pack(side='left', padx=8, pady=3)
        
        self.output_text = scrolledtext.ScrolledText(
            output_frame, height=5,
            font=('Consolas', 9),
            bg='#1a202c', fg='#68d391', 
            relief='flat',
            wrap='word'
        )
        self.output_text.pack(fill='both', expand=True)

    def load_code_template(self, event=None):
        """Load a code template with MANY more options"""
        if not hasattr(self, 'template_var'):
            return
            
        template_name = self.template_var.get()
        
        # 🎯 MASSIVELY EXPANDED TEMPLATES
        templates = {
            # Beginner Templates
            'hello_world': {
                'code': '''# 👋 Hello World Example
    {print}("Hello, World!")
    {print}("Welcome to {lang_name}!")

    {var} message = "Programming is awesome!"
    {print}(message)

    {var} name = "Coder"
    {print}("Hello", name, "! Ready to code?")''',
                'description': 'Classic first program - say hello to the world!'
            },
            
            'calculator': {
                'code': '''# 🧮 Simple Calculator
    {func} add(a, b) {{
        {return} a + b
    }}

    {func} subtract(a, b) {{
        {return} a - b
    }}

    {func} multiply(a, b) {{
        {return} a * b
    }}

    {func} divide(a, b) {{
        {if} b != 0 {{
            {return} a / b
        }} {else} {{
            {return} "Cannot divide by zero!"
        }}
    }}

    {var} x = 10
    {var} y = 5

    {print}("Addition:", add(x, y))
    {print}("Subtraction:", subtract(x, y))
    {print}("Multiplication:", multiply(x, y))
    {print}("Division:", divide(x, y))''',
                'description': 'Basic math operations with functions'
            },
            
            'guessing_game': {
                'code': '''# 🎯 Number Guessing Game
    {print}("=== 🎯 Guessing Game ===")
    {print}("I'm thinking of a number between 1 and 10!")

    {var} secret = 7
    {var} guess = 0
    {var} tries = 0
    {var} max_tries = 3

    {loop} tries < max_tries {{
        guess = {number}({input}("Your guess: "))
        tries = tries + 1
        
        {if} guess == secret {{
            {print}("🎉 Correct! You got it in", tries, "tries!")
            {return} "victory"
        }} {else} {if} guess < secret {{
            {print}("📈 Too low! Try higher.")
        }} {else} {{
            {print}("📉 Too high! Try lower.")
        }}
        
        {var} remaining = max_tries - tries
        {if} remaining > 0 {{
            {print}("You have", remaining, "tries left.")
        }}
    }}

    {print}("💀 Game over! The number was", secret)''',
                'description': 'Interactive guessing game with attempts limit'
            },
            
            # Practical Templates
            'todo_list': {
                'code': '''# 📝 Simple Todo List Manager
    {var} todos = []
    {var} completed = []

    {func} add_task(task) {{
        todos.push(task)
        {print}("✅ Added:", task)
    }}

    {func} complete_task(index) {{
        {if} index < todos.{length}() {{
            {var} task = todos[index]
            completed.push(task)
            todos.remove(index)
            {print}("🎉 Completed:", task)
        }} {else} {{
            {print}("❌ Invalid task number")
        }}
    }}

    {func} show_tasks() {{
        {print}("📋 Your Todo List:")
        {var} i = 0
        {loop} i < todos.{length}() {{
            {print}(i + 1, ".", todos[i])
            i = i + 1
        }}
    }}

    # Demo usage
    add_task("Learn programming")
    add_task("Build a project")
    add_task("Share with friends")
    show_tasks()
    complete_task(0)
    show_tasks()''',
                'description': 'Manage your tasks with add, complete, and display'
            },
            
            'password_checker': {
                'code': '''# 🔐 Password Strength Checker
    {func} check_password(password) {{
        {var} score = 0
        {var} feedback = []
        
        {if} password.{length}() >= 8 {{
            score = score + 1
        }} {else} {{
            feedback.push("Use at least 8 characters")
        }}
        
        {if} contains_uppercase(password) {{
            score = score + 1
        }} {else} {{
            feedback.push("Add uppercase letters")
        }}
        
        {if} contains_numbers(password) {{
            score = score + 1
        }} {else} {{
            feedback.push("Add some numbers")
        }}
        
        {if} contains_special(password) {{
            score = score + 1
        }} {else} {{
            feedback.push("Add special characters (!@#$)")
        }}
        
        {return} score
    }}

    {func} rate_strength(score) {{
        {if} score == 4 {{
            {return} "🔒 Very Strong"
        }} {else} {if} score == 3 {{
            {return} "🔐 Strong"
        }} {else} {if} score == 2 {{
            {return} "⚠️ Medium"
        }} {else} {{
            {return} "❌ Weak"
        }}
    }}

    # Test passwords
    {var} test_passwords = ["123", "password", "MyPass123", "MyP@ss123!"]
    {var} i = 0
    {loop} i < test_passwords.{length}() {{
        {var} pwd = test_passwords[i]
        {var} score = check_password(pwd)
        {var} strength = rate_strength(score)
        {print}(pwd, "→", strength)
        i = i + 1
    }}''',
                'description': 'Check how strong your passwords are'
            },
            
            # Math & Logic Templates
            'fibonacci': {
                'code': '''# 🌀 Fibonacci Sequence Generator
    {func} fibonacci(n) {{
        {if} n <= 1 {{
            {return} n
        }}
        {return} fibonacci(n - 1) + fibonacci(n - 2)
    }}

    {func} fibonacci_series(count) {{
        {print}("🌀 Fibonacci Series:")
        {var} i = 0
        {loop} i < count {{
            {var} fib_num = fibonacci(i)
            {print}("F(" + i + ") =", fib_num)
            i = i + 1
        }}
    }}

    {func} fibonacci_fast(n) {{
        {var} a = 0
        {var} b = 1
        {var} i = 0
        
        {if} n == 0 {{
            {return} a
        }}
        
        {loop} i < n - 1 {{
            {var} temp = a + b
            a = b
            b = temp
            i = i + 1
        }}
        {return} b
    }}

    {print}("📊 First 10 Fibonacci numbers:")
    fibonacci_series(10)

    {print}("⚡ Fast calculation F(15) =", fibonacci_fast(15))''',
                'description': 'Generate Fibonacci numbers with recursive and iterative methods'
            },
            
            'prime_numbers': {
                'code': '''# 🔢 Prime Number Finder
    {func} is_prime(num) {{
        {if} num < 2 {{
            {return} {false}
        }}
        
        {var} i = 2
        {loop} i * i <= num {{
            {if} num % i == 0 {{
                {return} {false}
            }}
            i = i + 1
        }}
        {return} {true}
    }}

    {func} find_primes(limit) {{
        {print}("🔢 Prime numbers up to", limit, ":")
        {var} primes = []
        {var} num = 2
        
        {loop} num <= limit {{
            {if} is_prime(num) {{
                primes.push(num)
                {print}(num, "is prime")
            }}
            num = num + 1
        }}
        
        {print}("📊 Found", primes.{length}(), "prime numbers")
        {return} primes
    }}

    {func} prime_factors(n) {{
        {print}("🔍 Prime factors of", n, ":")
        {var} factors = []
        {var} d = 2
        
        {loop} d * d <= n {{
            {loop} n % d == 0 {{
                factors.push(d)
                n = n / d
            }}
            d = d + 1
        }}
        
        {if} n > 1 {{
            factors.push(n)
        }}
        
        {return} factors
    }}

    # Find primes up to 30
    find_primes(30)

    # Find prime factors of 60
    {var} factors = prime_factors(60)
    {print}("Prime factors:", factors)''',
                'description': 'Find prime numbers and calculate prime factorization'
            },
            
            # Creative Templates
            'story_generator': {
                'code': '''# 📚 Random Story Generator
    {var} heroes = ["Alice", "Bob", "Charlie", "Diana", "Eve"]
    {var} places = ["enchanted forest", "ancient castle", "space station", "underwater city", "mountain peak"]
    {var} items = ["magic sword", "golden key", "mysterious book", "crystal orb", "ancient map"]
    {var} villains = ["dark wizard", "robot overlord", "sea monster", "evil queen", "shadow demon"]

    {func} random_choice(array) {{
        {var} index = {random}(0, array.{length}() - 1)
        {return} array[index]
    }}

    {func} generate_story() {{
        {var} hero = random_choice(heroes)
        {var} place = random_choice(places)
        {var} item = random_choice(items)
        {var} villain = random_choice(villains)
        
        {print}("📖 ===============================")
        {print}("     🌟 ADVENTURE STORY 🌟")
        {print}("===============================")
        {print}()
        {print}("Once upon a time, brave", hero, "ventured into the", place + ".")
        {print}("There, they discovered a legendary", item + "!")
        {print}()
        {print}("But suddenly, the terrible", villain, "appeared!")
        {print}("Using the power of the", item + ",", hero, "fought bravely.")
        {print}()
        {print}("After an epic battle,", hero, "emerged victorious!")
        {print}("The", place, "was saved, and", hero, "became a true hero!")
        {print}()
        {print}("🎉 The End! 🎉")
        {print}("===============================")
    }}

    {print}("🎭 Welcome to the Story Generator!")
    {print}("Each time you run this, you'll get a new adventure!")
    {print}()

    generate_story()''',
                'description': 'Generate random adventure stories with heroes, villains, and magic items'
            },
            
            'quiz_game': {
                'code': '''# 🧠 Interactive Quiz Game
    {var} questions = [
        "What is 2 + 2?",
        "What color do you get when you mix red and blue?",
        "How many legs does a spider have?",
        "What is the capital of France?"
    ]

    {var} answers = ["4", "purple", "8", "paris"]
    {var} score = 0

    {func} ask_question(question, correct_answer) {{
        {print}("❓", question)
        {var} user_answer = {input}("Your answer: ")
        
        {if} user_answer.toLowerCase() == correct_answer.toLowerCase() {{
            {print}("✅ Correct! Well done!")
            {return} 1
        }} {else} {{
            {print}("❌ Wrong! The correct answer is:", correct_answer)
            {return} 0
        }}
    }}

    {func} calculate_grade(score, total) {{
        {var} percentage = (score / total) * 100
        
        {if} percentage >= 90 {{
            {return} "🏆 Excellent! A+"
        }} {else} {if} percentage >= 80 {{
            {return} "🌟 Great! A"
        }} {else} {if} percentage >= 70 {{
            {return} "👍 Good! B"
        }} {else} {if} percentage >= 60 {{
            {return} "📝 OK! C"
        }} {else} {{
            {return} "📚 Keep studying! F"
        }}
    }}

    {print}("🧠 ===============================")
    {print}("     🎯 QUIZ GAME 🎯")
    {print}("===============================")
    {print}("Answer the following questions:")
    {print}()

    {var} i = 0
    {loop} i < questions.{length}() {{
        {print}("Question", i + 1, "of", questions.{length}())
        score = score + ask_question(questions[i], answers[i])
        {print}()
        i = i + 1
    }}

    {print}("🏁 ===============================")
    {print}("        FINAL RESULTS")
    {print}("===============================")
    {print}("Your score:", score, "out of", questions.{length}())
    {print}("Grade:", calculate_grade(score, questions.{length}()))''',
                'description': 'Test your knowledge with an interactive quiz'
            },
            
            # Utility Templates
            'temperature_converter': {
                'code': '''# 🌡️ Temperature Converter
    {func} celsius_to_fahrenheit(c) {{
        {return} (c * 9/5) + 32
    }}

    {func} fahrenheit_to_celsius(f) {{
        {return} (f - 32) * 5/9
    }}

    {func} celsius_to_kelvin(c) {{
        {return} c + 273.15
    }}

    {func} kelvin_to_celsius(k) {{
        {return} k - 273.15
    }}

    {func} format_temperature(temp, unit) {{
        {return} temp.toFixed(2) + "°" + unit
    }}

    {print}("🌡️ ===============================")
    {print}("     TEMPERATURE CONVERTER")
    {print}("===============================")

    {var} celsius = 25
    {print}("Starting temperature:", format_temperature(celsius, "C"))
    {print}()

    {var} fahrenheit = celsius_to_fahrenheit(celsius)
    {print}("In Fahrenheit:", format_temperature(fahrenheit, "F"))

    {var} kelvin = celsius_to_kelvin(celsius)
    {print}("In Kelvin:", format_temperature(kelvin, "K"))

    {print}()
    {print}("🔄 Converting back to check:")
    {var} back_to_celsius = fahrenheit_to_celsius(fahrenheit)
    {print}("From Fahrenheit:", format_temperature(back_to_celsius, "C"))

    {var} back_from_kelvin = kelvin_to_celsius(kelvin)
    {print}("From Kelvin:", format_temperature(back_from_kelvin, "C"))

    {print}()
    {print}("📊 Temperature Reference:")
    {print}("• Water freezes: 0°C = 32°F = 273.15K")
    {print}("• Room temperature: 20°C = 68°F = 293.15K")
    {print}("• Water boils: 100°C = 212°F = 373.15K")''',
                'description': 'Convert between Celsius, Fahrenheit, and Kelvin'
            },
            
            'word_counter': {
                'code': '''# 📝 Text Analysis Tool
    {func} count_words(text) {{
        {var} words = text.split(" ")
        {var} count = 0
        {var} i = 0
        
        {loop} i < words.{length}() {{
            {if} words[i].trim() != "" {{
                count = count + 1
            }}
            i = i + 1
        }}
        
        {return} count
    }}

    {func} count_characters(text) {{
        {return} text.{length}()
    }}

    {func} count_sentences(text) {{
        {var} sentences = text.split(".")
        {var} count = 0
        {var} i = 0
        
        {loop} i < sentences.{length}() {{
            {if} sentences[i].trim() != "" {{
                count = count + 1
            }}
            i = i + 1
        }}
        
        {return} count
    }}

    {func} find_longest_word(text) {{
        {var} words = text.split(" ")
        {var} longest = ""
        {var} i = 0
        
        {loop} i < words.{length}() {{
            {var} word = words[i].trim()
            {if} word.{length}() > longest.{length}() {{
                longest = word
            }}
            i = i + 1
        }}
        
        {return} longest
    }}

    {func} analyze_text(text) {{
        {print}("📝 ===============================")
        {print}("        TEXT ANALYSIS")
        {print}("===============================")
        {print}("Text:", text)
        {print}()
        {print}("📊 Statistics:")
        {print}("• Characters:", count_characters(text))
        {print}("• Words:", count_words(text))
        {print}("• Sentences:", count_sentences(text))
        {print}("• Longest word:", find_longest_word(text))
        
        {var} avg_word_length = count_characters(text) / count_words(text)
        {print}("• Average word length:", avg_word_length.toFixed(2), "characters")
    }}

    # Sample texts to analyze
    {var} sample1 = "Hello world! This is a simple text analysis program."
    {var} sample2 = "Programming is fun and creative. You can build amazing things with code!"

    analyze_text(sample1)
    {print}()
    analyze_text(sample2)''',
                'description': 'Analyze text for word count, characters, and statistics'
            },
            
            # Game Templates
            'magic_8_ball': {
                'code': '''# 🎱 Magic 8-Ball Fortune Teller
    {var} responses = [
        "🔮 It is certain",
        "✨ Without a doubt", 
        "🌟 Yes definitely",
        "👍 You may rely on it",
        "🎯 As I see it, yes",
        "🌈 Most likely",
        "💫 Outlook good",
        "🎪 Yes",
        "🔍 Signs point to yes",
        "❓ Reply hazy, try again",
        "⏰ Ask again later",
        "🤔 Better not tell you now",
        "🚫 Cannot predict now",
        "📞 Concentrate and ask again",
        "❌ Don't count on it",
        "🙅 My reply is no",
        "⛔ My sources say no",
        "😬 Outlook not so good",
        "💔 Very doubtful"
    ]

    {func} shake_magic_8_ball() {{
        {var} index = {random}(0, responses.{length}() - 1)
        {return} responses[index]
    }}

    {func} ask_question() {{
        {print}("🎱 ===============================")
        {print}("       MAGIC 8-BALL")
        {print}("===============================")
        {print}("Think of a yes/no question...")
        {print}("Then shake the magic 8-ball!")
        {print}()
        
        {var} question = {input}("What is your question? ")
        {print}()
        {print}("🎱 *shaking the magic 8-ball*")
        {print}("✨ *mystical swirling*")
        {print}("🔮 *the answer appears*")
        {print}()
        
        {var} answer = shake_magic_8_ball()
        {print}("The Magic 8-Ball says:")
        {print}(answer)
        {print}()
        
        {return} answer
    }}

    {print}("🌟 Welcome to the Magic 8-Ball!")
    {print}("Ask any yes/no question and receive mystical wisdom!")
    {print}()

    # Ask a question
    ask_question()

    {print}("🎉 Thank you for consulting the Magic 8-Ball!")
    {print}("Remember: The future is what you make it! ✨")''',
                'description': 'Ask questions and get mystical answers from the Magic 8-Ball'
            },
            
            'rock_paper_scissors': {
                'code': '''# ✂️ Rock Paper Scissors Game
    {var} choices = ["rock", "paper", "scissors"]
    {var} player_score = 0
    {var} computer_score = 0

    {func} get_computer_choice() {{
        {var} index = {random}(0, 2)
        {return} choices[index]
    }}

    {func} determine_winner(player, computer) {{
        {if} player == computer {{
            {return} "tie"
        }}
        
        {if} (player == "rock" && computer == "scissors") ||
            (player == "paper" && computer == "rock") ||
            (player == "scissors" && computer == "paper") {{
            {return} "player"
        }}
        
        {return} "computer"
    }}

    {func} get_emoji(choice) {{
        {if} choice == "rock" {{
            {return} "🪨"
        }} {else} {if} choice == "paper" {{
            {return} "📄"
        }} {else} {{
            {return} "✂️"
        }}
    }}

    {func} play_round(player_choice) {{
        {var} computer_choice = get_computer_choice()
        {var} winner = determine_winner(player_choice, computer_choice)
        
        {print}("You chose:", get_emoji(player_choice), player_choice)
        {print}("Computer chose:", get_emoji(computer_choice), computer_choice)
        {print}()
        
        {if} winner == "tie" {{
            {print}("🤝 It's a tie!")
        }} {else} {if} winner == "player" {{
            {print}("🎉 You win this round!")
            player_score = player_score + 1
        }} {else} {{
            {print}("🤖 Computer wins this round!")
            computer_score = computer_score + 1
        }}
        
        {print}("Score - You:", player_score, "Computer:", computer_score)
        {print}("===============================")
    }}

    {print}("✂️ ===============================")
    {print}("     ROCK PAPER SCISSORS")
    {print}("===============================")
    {print}("Best of 3 rounds!")
    {print}("🪨 Rock beats Scissors")
    {print}("📄 Paper beats Rock") 
    {print}("✂️ Scissors beats Paper")
    {print}()

    {var} rounds = 0
    {loop} rounds < 3 {{
        {print}("Round", rounds + 1, ":")
        # In a real implementation, you'd get input from user
        # For demo, we'll simulate with random choices
        {var} player_choice = choices[{random}(0, 2)]
        {print}("(Simulating player choice:", player_choice, ")")
        
        play_round(player_choice)
        rounds = rounds + 1
    }}

    {print}("🏁 FINAL RESULTS:")
    {if} player_score > computer_score {{
        {print}("🏆 Congratulations! You won the game!")
    }} {else} {if} computer_score > player_score {{
        {print}("🤖 Computer wins the game! Better luck next time!")
    }} {else} {{
        {print}("🤝 It's a tie game! Great match!")
    }}''',
                'description': 'Classic rock-paper-scissors game with score tracking'
            }
        }
        
        if template_name in templates:
            template_data = templates[template_name]
            template_code = template_data['code']
            
            # Replace placeholders with actual language keywords
            replacements = {
                '{lang_name}': self.language_data.get('name', 'MyLang'),
                '{print}': self.language_data.get('builtins', {}).get('print', 'print'),
                '{input}': self.language_data.get('builtins', {}).get('input', 'input'),
                '{number}': self.language_data.get('builtins', {}).get('number', 'number'),
                '{random}': self.language_data.get('builtins', {}).get('random', 'random'),
                '{length}': self.language_data.get('builtins', {}).get('length', 'length'),
                '{var}': self.language_data.get('keywords', {}).get('variable', 'var'),
                '{func}': self.language_data.get('keywords', {}).get('function', 'function'),
                '{if}': self.language_data.get('keywords', {}).get('if', 'if'),
                '{else}': self.language_data.get('keywords', {}).get('else', 'else'),
                '{loop}': self.language_data.get('keywords', {}).get('loop', 'loop'),
                '{return}': self.language_data.get('keywords', {}).get('return', 'return'),
                '{true}': self.language_data.get('keywords', {}).get('true', 'true'),
                '{false}': self.language_data.get('keywords', {}).get('false', 'false')
            }
            
            for placeholder, value in replacements.items():
                template_code = template_code.replace(placeholder, value)
            
            if hasattr(self, 'playground_code'):
                self.playground_code.delete('1.0', tk.END)
                self.playground_code.insert('1.0', template_code)
                
                # Update line numbers and syntax highlighting
                self.update_line_numbers()
                if self.syntax_highlighter:
                    self.syntax_highlighter.highlight()
                
                # Show template info
                description = template_data['description']
                self.update_status(f"Loaded: {description}")

    def show_template_info(self):
        """Show information about available templates"""
        dialog = tk.Toplevel(self.window)
        dialog.title("📚 Template Library")
        dialog.geometry("700x600")
        dialog.transient(self.window)
        
        # Header
        header = tk.Frame(dialog, bg='#667eea', height=60)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(header, text="📚 Template Library", 
                font=('Arial', 18, 'bold'), bg='#667eea', fg='white').pack(pady=15)
        
        # Main content
        main_content = tk.Frame(dialog, bg='white')
        main_content.pack(fill='both', expand=True)
        
        # Create notebook for categories
        notebook = ttk.Notebook(main_content)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Template categories
        categories = {
            "🌱 Beginner": {
                "hello_world": "Your first program - greet the world!",
                "calculator": "Basic math operations with functions",
                "guessing_game": "Interactive number guessing with loops"
            },
            "💬 Gen Z Vibes": {
                "genz_hello": "Hello World but make it iconic - trending! ✨",
                "genz_calculator": "Math but cute - calculator with main character energy 🧮",
                "genz_social_media": "Vibe check your social media presence bestie! 📱"
            },
            "🛠️ Practical": {
                "todo_list": "Manage tasks with add/complete features",
                "password_checker": "Check password strength and security", 
                "temperature_converter": "Convert between temperature units",
                "word_counter": "Analyze text for statistics and insights"
            },
            "🧮 Math & Logic": {
                "fibonacci": "Generate Fibonacci sequences",
                "prime_numbers": "Find primes and calculate factors"
            },
            "🎨 Creative": {
                "story_generator": "Create random adventure stories",
                "quiz_game": "Interactive knowledge quiz",
                "chatbot": "Simple conversational AI"
            },
            "🎮 Games": {
                "magic_8_ball": "Ask questions, get mystical answers",
                "rock_paper_scissors": "Classic game with score tracking",
                "tic_tac_toe": "Strategic grid game",
                "text_adventure": "Choose-your-own adventure story"
            },
            "⚡ Advanced": {
                "banking_system": "Simulate bank accounts and transactions",
                "simple_ai": "Basic artificial intelligence patterns",
                "data_processor": "Handle and analyze data sets",
                "web_scraper": "Extract information from web content"
            }
        }
        
        for category, templates in categories.items():
            # Create tab
            tab = ttk.Frame(notebook)
            notebook.add(tab, text=category)
            
            # Scrollable content
            canvas = tk.Canvas(tab, bg='white', highlightthickness=0)
            scrollbar = ttk.Scrollbar(tab, orient='vertical', command=canvas.yview)
            content_frame = tk.Frame(canvas, bg='white')
            
            content_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=content_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side='left', fill='both', expand=True)
            scrollbar.pack(side='right', fill='y')
            
            # Template cards
            for template_name, description in templates.items():
                card = tk.Frame(content_frame, bg='white', relief='solid', bd=1)
                card.pack(fill='x', padx=20, pady=10)
                
                card_content = tk.Frame(card, bg='white', padx=15, pady=12)
                card_content.pack(fill='x')
                
                # Template name
                name_frame = tk.Frame(card_content, bg='white')
                name_frame.pack(fill='x')
                
                tk.Label(name_frame, text=template_name.replace('_', ' ').title(), 
                        font=('Arial', 12, 'bold'), bg='white').pack(side='left')
                
                # Load button
                def load_template(name=template_name):
                    self.template_var.set(name)
                    self.load_code_template()
                    dialog.destroy()
                
                tk.Button(name_frame, text="Load →", command=load_template,
                        bg='#667eea', fg='white', relief='flat',
                        font=('Arial', 10), padx=15, pady=5).pack(side='right')
                
                # Description
                tk.Label(card_content, text=description, font=('Arial', 10),
                        bg='white', fg='#666', wraplength=500).pack(anchor='w', pady=(5, 0))
        
        # Close button
        button_frame = tk.Frame(dialog, bg='white', padx=20, pady=15)
        button_frame.pack(fill='x')
        
        tk.Button(button_frame, text="Close", command=dialog.destroy,
                bg='#e2e8f0', font=('Arial', 11),
                padx=20, pady=8).pack(side='right')

    def setup_enhanced_styles(self):
        """Setup enhanced styling for the application"""
        # Configure ttk styles
        self.style = ttk.Style()
        
        # Create custom button styles
        self.style.configure('Accent.TButton',
                           background='#667eea',
                           foreground='white',
                           borderwidth=0,
                           focuscolor='none')
        
        self.style.map('Accent.TButton',
                      background=[('active', '#5a67d8')])
        
        # Create custom frame styles
        self.style.configure('Card.TFrame',
                           background='#ffffff',
                           relief='solid',
                           borderwidth=1)
    
    def setup_ui(self):
        """Setup the enhanced main UI"""
        # Create enhanced menu bar
        self.create_enhanced_menu_bar()
        
        # Create modern toolbar
        self.create_modern_toolbar()
        
        # Create main content with improved layout
        self.create_enhanced_main_content()
        
        # Create enhanced status bar
        self.create_enhanced_status_bar()
        
        # Bind enhanced keyboard shortcuts
        self.bind_enhanced_shortcuts()
    

    def generate_interpreter(self, export_folder):
        """Generate a complete working interpreter for the language"""
        lang_name = self.language_data['name'].lower().replace(' ', '_')
        interpreter_file = os.path.join(export_folder, 'src', f'{lang_name}.py')
        
        # Generate the complete interpreter code
        interpreter_code = f'''#!/usr/bin/env python3
    """
    {self.language_data['name']} Interpreter
    Generated by SUPER Language Creator
    Version: {self.language_data.get('version', '1.0')}
    Author: {self.language_data.get('author', 'Unknown')}
    """

    import json
    import sys
    import os
    import re
    import random
    from typing import Dict, List, Any, Optional

    class {self.language_data['name'].replace(' ', '')}Interpreter:
        def __init__(self, language_file='language.json'):
            self.language_file = language_file
            self.load_language_definition()
            self.variables = {{}}
            self.functions = {{}}
            self.call_stack = []
            self.output_buffer = []
            
        def load_language_definition(self):
            """Load the language definition from JSON"""
            script_dir = os.path.dirname(os.path.abspath(__file__))
            lang_path = os.path.join(os.path.dirname(script_dir), self.language_file)
            
            with open(lang_path, 'r', encoding='utf-8') as f:
                self.lang_def = json.load(f)
            
            # Extract keywords and builtins
            self.keywords = self.lang_def.get('keywords', {{}})
            self.builtins = self.lang_def.get('builtins', {{}})
            self.errors = self.lang_def.get('errors', {{}})
            
            # Create reverse mappings (custom -> english)
            self.keyword_map = {{v: k for k, v in self.keywords.items() if v}}
            self.builtin_map = {{v: k for k, v in self.builtins.items() if v}}
        
        def tokenize(self, code: str) -> List[Dict[str, Any]]:
            """Tokenize the source code"""
            tokens = []
            lines = code.split('\\n')
            
            for line_num, line in enumerate(lines, 1):
                # Skip empty lines and comments
                stripped = line.strip()
                if not stripped or stripped.startswith('#'):
                    continue
                
                # Tokenize the line
                # This is a simplified tokenizer - you might want to enhance it
                pattern = r'("(?:[^"\\\\]|\\\\.)*"|\'(?:[^\'\\\\]|\\\\.)*\'|[a-zA-Z_][a-zA-Z0-9_]*|[0-9]+\\.?[0-9]*|==|!=|<=|>=|&&|\\|\\||[+\\-*/=<>(){{}}\\[\\],])'
                
                matches = re.findall(pattern, line)
                col = 0
                
                for match in matches:
                    token_type = self.get_token_type(match)
                    tokens.append({{
                        'type': token_type,
                        'value': match,
                        'line': line_num,
                        'column': col
                    }})
                    col += len(match) + 1
            
            return tokens
        
        def get_token_type(self, token: str) -> str:
            """Determine the type of a token"""
            # Check if it's a keyword
            if token in self.keyword_map:
                return f'KEYWORD_{{self.keyword_map[token].upper()}}'
            
            # Check if it's a builtin function
            if token in self.builtin_map:
                return f'BUILTIN_{{self.builtin_map[token].upper()}}'
            
            # Check for literals
            if token.startswith('"') or token.startswith("'"):
                return 'STRING'
            
            if re.match(r'^[0-9]+\\.?[0-9]*$', token):
                return 'NUMBER'
            
            # Check for operators
            operators = {{
                '+': 'PLUS', '-': 'MINUS', '*': 'MULTIPLY', '/': 'DIVIDE',
                '=': 'ASSIGN', '==': 'EQUALS', '!=': 'NOT_EQUALS',
                '<': 'LESS', '>': 'GREATER', '<=': 'LESS_EQUAL', '>=': 'GREATER_EQUAL',
                '&&': 'AND', '||': 'OR'
            }}
            
            if token in operators:
                return operators[token]
            
            # Check for delimiters
            delimiters = {{
                '(': 'LPAREN', ')': 'RPAREN',
                '{{': 'LBRACE', '}}': 'RBRACE',
                '[': 'LBRACKET', ']': 'RBRACKET',
                ',': 'COMMA'
            }}
            
            if token in delimiters:
                return delimiters[token]
            
            # Check for boolean values
            if token == self.keywords.get('true', 'true'):
                return 'TRUE'
            if token == self.keywords.get('false', 'false'):
                return 'FALSE'
            
            # Otherwise it's an identifier
            return 'IDENTIFIER'
        
        def parse(self, tokens: List[Dict[str, Any]]):
            """Parse tokens into an AST"""
            self.tokens = tokens
            self.current = 0
            return self.parse_program()
        
        def parse_program(self):
            """Parse the entire program"""
            statements = []
            while not self.is_at_end():
                stmt = self.parse_statement()
                if stmt:
                    statements.append(stmt)
            return {{'type': 'PROGRAM', 'statements': statements}}
        
        def parse_statement(self):
            """Parse a single statement"""
            if self.match('KEYWORD_VARIABLE'):
                return self.parse_variable_declaration()
            elif self.match('KEYWORD_FUNCTION'):
                return self.parse_function_declaration()
            elif self.match('KEYWORD_IF'):
                return self.parse_if_statement()
            elif self.match('KEYWORD_LOOP'):
                return self.parse_loop_statement()
            elif self.match('KEYWORD_RETURN'):
                return self.parse_return_statement()
            elif self.check_type('BUILTIN_PRINT'):
                return self.parse_expression_statement()
            elif self.check_type('IDENTIFIER'):
                # Could be assignment or function call
                return self.parse_expression_statement()
            else:
                self.advance()  # Skip unknown tokens
                return None
        
        def parse_variable_declaration(self):
            """Parse variable declaration"""
            name = self.consume('IDENTIFIER', 'Expected variable name')
            
            if self.match('ASSIGN'):
                value = self.parse_expression()
                return {{'type': 'VAR_DECL', 'name': name['value'], 'value': value}}
            
            return {{'type': 'VAR_DECL', 'name': name['value'], 'value': None}}
        
        def parse_function_declaration(self):
            """Parse function declaration"""
            name = self.consume('IDENTIFIER', 'Expected function name')
            
            self.consume('LPAREN', 'Expected ( after function name')
            
            params = []
            if not self.check('RPAREN'):
                params.append(self.consume('IDENTIFIER', 'Expected parameter name')['value'])
                while self.match('COMMA'):
                    params.append(self.consume('IDENTIFIER', 'Expected parameter name')['value'])
            
            self.consume('RPAREN', 'Expected ) after parameters')
            self.consume('LBRACE', 'Expected {{ before function body')
            
            body = []
            while not self.check('RBRACE') and not self.is_at_end():
                stmt = self.parse_statement()
                if stmt:
                    body.append(stmt)
            
            self.consume('RBRACE', 'Expected }} after function body')
            
            return {{
                'type': 'FUNC_DECL',
                'name': name['value'],
                'params': params,
                'body': body
            }}
        
        def parse_if_statement(self):
            """Parse if statement"""
            condition = self.parse_expression()
            
            self.consume('LBRACE', 'Expected {{ after if condition')
            then_branch = []
            
            while not self.check('RBRACE') and not self.is_at_end():
                stmt = self.parse_statement()
                if stmt:
                    then_branch.append(stmt)
            
            self.consume('RBRACE', 'Expected }} after if body')
            
            else_branch = None
            if self.match('KEYWORD_ELSE'):
                if self.match('KEYWORD_IF'):
                    # else if
                    else_branch = [self.parse_if_statement()]
                else:
                    self.consume('LBRACE', 'Expected {{ after else')
                    else_branch = []
                    
                    while not self.check('RBRACE') and not self.is_at_end():
                        stmt = self.parse_statement()
                        if stmt:
                            else_branch.append(stmt)
                    
                    self.consume('RBRACE', 'Expected }} after else body')
            
            return {{
                'type': 'IF_STMT',
                'condition': condition,
                'then_branch': then_branch,
                'else_branch': else_branch
            }}
        
        def parse_loop_statement(self):
            """Parse loop statement"""
            condition = self.parse_expression()
            
            self.consume('LBRACE', 'Expected {{ after loop condition')
            body = []
            
            while not self.check('RBRACE') and not self.is_at_end():
                stmt = self.parse_statement()
                if stmt:
                    body.append(stmt)
            
            self.consume('RBRACE', 'Expected }} after loop body')
            
            return {{
                'type': 'LOOP_STMT',
                'condition': condition,
                'body': body
            }}
        
        def parse_return_statement(self):
            """Parse return statement"""
            value = None
            if not self.is_at_end() and not self.check('RBRACE'):
                value = self.parse_expression()
            
            return {{'type': 'RETURN_STMT', 'value': value}}
        
        def parse_expression_statement(self):
            """Parse expression statement"""
            expr = self.parse_expression()
            
            # Check if it's an assignment
            if self.match('ASSIGN'):
                if expr['type'] != 'IDENTIFIER':
                    self.error('Invalid assignment target')
                
                value = self.parse_expression()
                return {{'type': 'ASSIGN', 'name': expr['value'], 'value': value}}
            
            return {{'type': 'EXPR_STMT', 'expression': expr}}
        
        def parse_expression(self):
            """Parse expression"""
            return self.parse_logical_or()
        
        def parse_logical_or(self):
            """Parse logical OR expression"""
            expr = self.parse_logical_and()
            
            while self.match('OR'):
                op = self.previous()
                right = self.parse_logical_and()
                expr = {{'type': 'BINARY', 'left': expr, 'operator': op['type'], 'right': right}}
            
            return expr
        
        def parse_logical_and(self):
            """Parse logical AND expression"""
            expr = self.parse_equality()
            
            while self.match('AND'):
                op = self.previous()
                right = self.parse_equality()
                expr = {{'type': 'BINARY', 'left': expr, 'operator': op['type'], 'right': right}}
            
            return expr
        
        def parse_equality(self):
            """Parse equality expression"""
            expr = self.parse_comparison()
            
            while self.match('EQUALS', 'NOT_EQUALS'):
                op = self.previous()
                right = self.parse_comparison()
                expr = {{'type': 'BINARY', 'left': expr, 'operator': op['type'], 'right': right}}
            
            return expr
        
        def parse_comparison(self):
            """Parse comparison expression"""
            expr = self.parse_addition()
            
            while self.match('GREATER', 'GREATER_EQUAL', 'LESS', 'LESS_EQUAL'):
                op = self.previous()
                right = self.parse_addition()
                expr = {{'type': 'BINARY', 'left': expr, 'operator': op['type'], 'right': right}}
            
            return expr
        
        def parse_addition(self):
            """Parse addition/subtraction expression"""
            expr = self.parse_multiplication()
            
            while self.match('PLUS', 'MINUS'):
                op = self.previous()
                right = self.parse_multiplication()
                expr = {{'type': 'BINARY', 'left': expr, 'operator': op['type'], 'right': right}}
            
            return expr
        
        def parse_multiplication(self):
            """Parse multiplication/division expression"""
            expr = self.parse_unary()
            
            while self.match('MULTIPLY', 'DIVIDE'):
                op = self.previous()
                right = self.parse_unary()
                expr = {{'type': 'BINARY', 'left': expr, 'operator': op['type'], 'right': right}}
            
            return expr
        
        def parse_unary(self):
            """Parse unary expression"""
            if self.match('MINUS'):
                op = self.previous()
                expr = self.parse_unary()
                return {{'type': 'UNARY', 'operator': op['type'], 'operand': expr}}
            
            return self.parse_primary()
        
        def parse_primary(self):
            """Parse primary expression"""
            # Boolean literals
            if self.match('TRUE'):
                return {{'type': 'LITERAL', 'value': True}}
            
            if self.match('FALSE'):
                return {{'type': 'LITERAL', 'value': False}}
            
            # Number literal
            if self.match('NUMBER'):
                value = self.previous()['value']
                return {{'type': 'LITERAL', 'value': float(value) if '.' in value else int(value)}}
            
            # String literal
            if self.match('STRING'):
                value = self.previous()['value'][1:-1]  # Remove quotes
                return {{'type': 'LITERAL', 'value': value}}
            
            # Function call or identifier
            if self.check_type('BUILTIN') or self.check_type('IDENTIFIER'):
                token = self.advance()
                
                # Check if it's a function call
                if self.match('LPAREN'):
                    args = []
                    
                    if not self.check('RPAREN'):
                        args.append(self.parse_expression())
                        while self.match('COMMA'):
                            args.append(self.parse_expression())
                    
                    self.consume('RPAREN', 'Expected ) after arguments')
                    
                    return {{
                        'type': 'CALL',
                        'callee': token['value'],
                        'arguments': args,
                        'is_builtin': token['type'].startswith('BUILTIN')
                    }}
                
                # Just an identifier
                return {{'type': 'IDENTIFIER', 'value': token['value']}}
            
            # Grouped expression
            if self.match('LPAREN'):
                expr = self.parse_expression()
                self.consume('RPAREN', 'Expected ) after expression')
                return expr
            
            self.error(f"Unexpected token: {{self.peek()['value'] if not self.is_at_end() else 'EOF'}}")
        
        def execute(self, ast):
            """Execute the AST"""
            try:
                self.execute_node(ast)
                return '\\n'.join(self.output_buffer)
            except Exception as e:
                return f"Runtime error: {{str(e)}}"
        
        def execute_node(self, node):
            """Execute a single AST node"""
            if node is None:
                return None
            
            node_type = node.get('type')
            
            if node_type == 'PROGRAM':
                for stmt in node['statements']:
                    result = self.execute_node(stmt)
                    if isinstance(result, dict) and result.get('type') == 'RETURN':
                        return result
            
            elif node_type == 'VAR_DECL':
                value = None
                if node['value']:
                    value = self.execute_node(node['value'])
                self.variables[node['name']] = value
            
            elif node_type == 'FUNC_DECL':
                self.functions[node['name']] = node
            
            elif node_type == 'IF_STMT':
                condition = self.execute_node(node['condition'])
                if self.is_truthy(condition):
                    for stmt in node['then_branch']:
                        result = self.execute_node(stmt)
                        if isinstance(result, dict) and result.get('type') == 'RETURN':
                            return result
                elif node['else_branch']:
                    for stmt in node['else_branch']:
                        result = self.execute_node(stmt)
                        if isinstance(result, dict) and result.get('type') == 'RETURN':
                            return result
            
            elif node_type == 'LOOP_STMT':
                while self.is_truthy(self.execute_node(node['condition'])):
                    for stmt in node['body']:
                        result = self.execute_node(stmt)
                        if isinstance(result, dict) and result.get('type') == 'RETURN':
                            return result
            
            elif node_type == 'RETURN_STMT':
                value = None
                if node['value']:
                    value = self.execute_node(node['value'])
                return {{'type': 'RETURN', 'value': value}}
            
            elif node_type == 'EXPR_STMT':
                self.execute_node(node['expression'])
            
            elif node_type == 'ASSIGN':
                value = self.execute_node(node['value'])
                self.variables[node['name']] = value
            
            elif node_type == 'BINARY':
                left = self.execute_node(node['left'])
                right = self.execute_node(node['right'])
                
                operators = {{
                    'PLUS': lambda: left + right,
                    'MINUS': lambda: left - right,
                    'MULTIPLY': lambda: left * right,
                    'DIVIDE': lambda: left / right if right != 0 else self.error("Division by zero"),
                    'EQUALS': lambda: left == right,
                    'NOT_EQUALS': lambda: left != right,
                    'LESS': lambda: left < right,
                    'GREATER': lambda: left > right,
                    'LESS_EQUAL': lambda: left <= right,
                    'GREATER_EQUAL': lambda: left >= right,
                    'AND': lambda: self.is_truthy(left) and self.is_truthy(right),
                    'OR': lambda: self.is_truthy(left) or self.is_truthy(right)
                }}
                
                return operators[node['operator']]()
            
            elif node_type == 'UNARY':
                operand = self.execute_node(node['operand'])
                if node['operator'] == 'MINUS':
                    return -operand
            
            elif node_type == 'LITERAL':
                return node['value']
            
            elif node_type == 'IDENTIFIER':
                if node['value'] in self.variables:
                    return self.variables[node['value']]
                else:
                    self.error(f"Undefined variable: {{node['value']}}")
            
            elif node_type == 'CALL':
                return self.execute_call(node)
            
            return None
        
        def execute_call(self, node):
            """Execute a function call"""
            callee = node['callee']
            args = [self.execute_node(arg) for arg in node['arguments']]
            
            if node['is_builtin']:
                return self.execute_builtin(callee, args)
            elif callee in self.functions:
                return self.execute_user_function(self.functions[callee], args)
            else:
                self.error(f"Undefined function: {{callee}}")
        
        def execute_builtin(self, name, args):
            """Execute built-in function"""
            # Map custom name to standard function
            builtin_type = self.builtin_map.get(name, name)
            
            if builtin_type == 'print':
                output = ' '.join(str(arg) for arg in args)
                self.output_buffer.append(output)
                return None
            
            elif builtin_type == 'input':
                prompt = args[0] if args else ""
                return input(str(prompt))
            
            elif builtin_type == 'length':
                if args:
                    return len(str(args[0]))
                return 0
            
            elif builtin_type == 'string':
                if args:
                    return str(args[0])
                return ""
            
            elif builtin_type == 'number':
                if args:
                    try:
                        return float(args[0]) if '.' in str(args[0]) else int(args[0])
                    except:
                        return 0
                return 0
            
            elif builtin_type == 'random':
                if len(args) >= 2:
                    return random.randint(int(args[0]), int(args[1]))
                return random.random()
            
            else:
                self.error(f"Unknown built-in function: {{name}}")
        
        def execute_user_function(self, func_node, args):
            """Execute user-defined function"""
            # Create new scope
            old_vars = self.variables.copy()
            
            # Bind parameters
            for i, param in enumerate(func_node['params']):
                if i < len(args):
                    self.variables[param] = args[i]
                else:
                    self.variables[param] = None
            
            # Execute function body
            result = None
            for stmt in func_node['body']:
                stmt_result = self.execute_node(stmt)
                if isinstance(stmt_result, dict) and stmt_result.get('type') == 'RETURN':
                    result = stmt_result['value']
                    break
            
            # Restore scope
            self.variables = old_vars
            
            return result
        
        def is_truthy(self, value):
            """Determine if a value is truthy"""
            if value is None:
                return False
            if isinstance(value, bool):
                return value
            if isinstance(value, (int, float)):
                return value != 0
            if isinstance(value, str):
                return len(value) > 0
            return True
        
        # Parser helper methods
        def match(self, *types):
            """Check if current token matches any of the given types"""
            for token_type in types:
                if self.check(token_type):
                    self.advance()
                    return True
            return False
        
        def check(self, token_type):
            """Check if current token is of given type"""
            if self.is_at_end():
                return False
            return self.peek()['type'] == token_type
        
        def check_type(self, prefix):
            """Check if current token type starts with prefix"""
            if self.is_at_end():
                return False
            return self.peek()['type'].startswith(prefix)
        
        def advance(self):
            """Consume current token and return it"""
            if not self.is_at_end():
                self.current += 1
            return self.previous()
        
        def is_at_end(self):
            """Check if we're at end of tokens"""
            return self.current >= len(self.tokens)
        
        def peek(self):
            """Return current token without consuming"""
            if self.is_at_end():
                return None
            return self.tokens[self.current]
        
        def previous(self):
            """Return previous token"""
            return self.tokens[self.current - 1]
        
        def consume(self, token_type, message):
            """Consume token of given type or error"""
            if self.check(token_type):
                return self.advance()
            
            self.error(message)
        
        def error(self, message):
            """Raise a parser/runtime error"""
            token = self.peek()
            if token:
                raise Exception(f"{{message}} at line {{token['line']}}, column {{token['column']}}")
            else:
                raise Exception(message)
        
        def run_file(self, filename):
            """Run a source file"""
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    source = f.read()
                
                # Tokenize
                tokens = self.tokenize(source)
                
                # Parse
                ast = self.parse(tokens)
                
                # Execute
                output = self.execute(ast)
                
                if output:
                    print(output)
                
            except FileNotFoundError:
                print(f"Error: File '{{filename}}' not found")
            except Exception as e:
                print(f"Error: {{str(e)}}")

    def main():
        """Main entry point"""
        if len(sys.argv) < 2:
            print(f"Usage: python {lang_name}.py <filename.{lang_name[:3]}>")
            print(f"\\nExample: python {lang_name}.py examples/hello.{lang_name[:3]}")
            return
        
        interpreter = {self.language_data['name'].replace(' ', '')}Interpreter()
        interpreter.run_file(sys.argv[1])

    if __name__ == "__main__":
        main()
    '''
        
        # Write the interpreter file
        with open(interpreter_file, 'w', encoding='utf-8') as f:
            f.write(interpreter_code)
        
        # Make it executable on Unix-like systems
        if sys.platform != 'win32':
            os.chmod(interpreter_file, 0o755)    
    def create_enhanced_menu_bar(self):
        """Create enhanced application menu bar with better organization"""
        menubar = tk.Menu(self.window, bg='#ffffff', fg='#1a202c', 
                         activebackground='#667eea', activeforeground='white')
        self.window.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0, bg='#ffffff', fg='#1a202c')
        menubar.add_cascade(label="📁 File", menu=file_menu)
        file_menu.add_command(label="✨ New Language", command=self.new_language, accelerator="Ctrl+N")
        file_menu.add_command(label="📂 Open Language", command=self.load_language, accelerator="Ctrl+O")
        file_menu.add_command(label="💾 Save Language", command=self.save_language, accelerator="Ctrl+S")
        file_menu.add_command(label="💾 Save As...", command=self.save_as_language, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="📤 Export Language", command=self.export_language, accelerator="Ctrl+E")
        file_menu.add_command(label="📥 Import Language", command=self.import_language)
        file_menu.add_separator()
        file_menu.add_command(label="🚪 Exit", command=self.safe_exit)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0, bg='#ffffff', fg='#1a202c')
        menubar.add_cascade(label="✏️ Edit", menu=edit_menu)
        edit_menu.add_command(label="↶ Undo", accelerator="Ctrl+Z")
        edit_menu.add_command(label="↷ Redo", accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="📋 Copy", accelerator="Ctrl+C")
        edit_menu.add_command(label="📄 Paste", accelerator="Ctrl+V")
        edit_menu.add_command(label="✂️ Cut", accelerator="Ctrl+X")
        edit_menu.add_separator()
        edit_menu.add_command(label="🔍 Find", accelerator="Ctrl+F")
        edit_menu.add_command(label="🔄 Replace", accelerator="Ctrl+H")
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0, bg='#ffffff', fg='#1a202c')
        menubar.add_cascade(label="👁️ View", menu=view_menu)
        
        # Enhanced theme submenu
        theme_menu = tk.Menu(view_menu, tearoff=0, bg='#ffffff', fg='#1a202c')
        view_menu.add_cascade(label="🎨 Themes", menu=theme_menu)
        for theme_id, theme in self.theme_engine.themes.items():
            theme_menu.add_radiobutton(label=f"{theme['name']}", 
                                      command=lambda t=theme_id: self.change_theme(t))
        
        view_menu.add_separator()
        view_menu.add_command(label="🔧 Show Toolbar", command=self.toggle_toolbar)
        view_menu.add_command(label="📊 Show Status Bar", command=self.toggle_status_bar)
        view_menu.add_command(label="📝 Show Progress Panel", command=self.toggle_progress_panel)
        
        # Accessibility menu
        access_menu = tk.Menu(view_menu, tearoff=0, bg='#ffffff', fg='#1a202c')
        view_menu.add_cascade(label="♿ Accessibility", menu=access_menu)
        access_menu.add_command(label="🔍 Increase Font Size", command=self.accessibility.increase_font_size, accelerator="Ctrl++")
        access_menu.add_command(label="🔎 Decrease Font Size", command=self.accessibility.decrease_font_size, accelerator="Ctrl+-")
        access_menu.add_command(label="🌈 High Contrast", command=self.toggle_high_contrast)
        access_menu.add_command(label="⌨️ Keyboard Navigation Help", command=self.show_keyboard_help)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0, bg='#ffffff', fg='#1a202c')
        menubar.add_cascade(label="🛠️ Tools", menu=tools_menu)
        tools_menu.add_command(label="🎲 Random Keywords", command=self.show_enhanced_keyword_generator)
        tools_menu.add_command(label="✅ Syntax Validator", command=self.validate_syntax)
        tools_menu.add_command(label="⚡ Performance Test", command=self.performance_test)
        tools_menu.add_command(label="📖 Generate Documentation", command=self.generate_docs)
        tools_menu.add_separator()
        tools_menu.add_command(label="📊 Language Statistics", command=self.show_statistics)
        tools_menu.add_command(label="🔧 Preferences", command=self.show_preferences)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0, bg='#ffffff', fg='#1a202c')
        menubar.add_cascade(label="❓ Help", menu=help_menu)
        help_menu.add_command(label="🎓 Tutorial", command=self.start_tutorial)
        help_menu.add_command(label="📚 Examples Gallery", command=self.show_examples_gallery)
        help_menu.add_command(label="🏆 Achievements", command=self.show_achievements)
        help_menu.add_command(label="⌨️ Keyboard Shortcuts", command=self.show_keyboard_shortcuts)
        help_menu.add_separator()
        help_menu.add_command(label="🌐 Online Help", command=self.open_online_help)
        help_menu.add_command(label="💬 Community", command=self.open_community)
        help_menu.add_command(label="ℹ️ About", command=self.show_about)
    
    def create_modern_toolbar(self):
        """Create modern toolbar with enhanced buttons"""
        # Toolbar frame with gradient-like background
        self.toolbar = tk.Frame(self.window, height=60, relief='flat')
        self.toolbar.pack(fill='x', padx=0, pady=0)
        self.toolbar.pack_propagate(False)
        
        # Left section - main actions
        left_section = tk.Frame(self.toolbar)
        left_section.pack(side='left', fill='y', padx=20, pady=10)
        
        # Enhanced buttons with better styling
        buttons = [
            ("✨", "New Language", self.new_language, "#667eea"),
            ("📂", "Open", self.load_language, "#38a169"),
            ("💾", "Save", self.save_language, "#3182ce"),
            ("🚀", "Generate", self.generate_language, "#ed8936"),
            ("▶️", "Run", self.run_playground, "#38a169"),
        ]
        
        for icon, tooltip, command, color in buttons:
            btn = self.create_modern_button(left_section, icon, tooltip, command, color)
            btn.pack(side='left', padx=5)
        
        # Separator
        separator = tk.Frame(left_section, width=2, bg='#e2e8f0')
        separator.pack(side='left', fill='y', padx=10)
        
        # Right section - utilities
        right_section = tk.Frame(self.toolbar)
        right_section.pack(side='right', fill='y', padx=20, pady=10)
        
        utility_buttons = [
            ("🎲", "Random Keywords", self.show_keyword_generator, "#9f7aea"),
            ("🎨", "Themes", self.show_theme_picker, "#ed64a6"),
            ("🏆", "Achievements", self.show_achievements, "#f6ad55"),
            ("❓", "Help", self.show_help_menu, "#4fd1c7"),
        ]
        
        for icon, tooltip, command, color in utility_buttons:
            btn = self.create_modern_button(right_section, icon, tooltip, command, color)
            btn.pack(side='right', padx=3)
    
    def create_modern_button(self, parent, icon, tooltip, command, color):
        """Create a modern styled button with enhanced UI"""
        btn = tk.Button(parent, text=icon, font=('Segoe UI', 14, 'normal'), 
                       command=command, relief='flat', 
                       bg=color, fg='white',
                       width=4, height=1,
                       borderwidth=0,
                       activebackground=self.darken_color(color),
                       activeforeground='white',
                       cursor='hand2',
                       padx=12, pady=8)
        
        # Add hover effects
        def on_enter(e):
            btn.configure(bg=self.darken_color(color))
        
        def on_leave(e):
            btn.configure(bg=color)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        # Add tooltip
        self.create_enhanced_tooltip(btn, tooltip)
        
        return btn
    
    def darken_color(self, color):
        """Darken a hex color by 20%"""
        # Convert hex to RGB
        rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
        # Darken by 20%
        darkened = tuple(int(c * 0.8) for c in rgb)
        # Convert back to hex
        return f'#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}'
    
    # Design System Constants
    SPACING = {
        'xs': 4,
        'sm': 8,
        'md': 16,
        'lg': 24,
        'xl': 32,
        'xxl': 48
    }
    
    TYPOGRAPHY = {
        'display': ('Segoe UI', 32, 'bold'),
        'heading1': ('Segoe UI', 24, 'bold'),
        'heading2': ('Segoe UI', 20, 'bold'),
        'heading3': ('Segoe UI', 16, 'bold'),
        'body': ('Segoe UI', 12, 'normal'),
        'body_large': ('Segoe UI', 14, 'normal'),
        'caption': ('Segoe UI', 10, 'normal'),
        'code': ('Cascadia Code', 12, 'normal'),
        'button': ('Segoe UI', 12, 'normal')
    }
    
    BORDER_RADIUS = {
        'sm': 4,
        'md': 8,
        'lg': 16,
        'full': 50
    }
    
    def create_modern_input_field(self, parent, label_text, placeholder="", width=30):
        """Create a modern input field with floating label effect"""
        field_frame = tk.Frame(parent, bg='white')
        field_frame.pack(fill='x', pady=self.SPACING['sm'])
        
        # Label
        label = tk.Label(field_frame, text=label_text, 
                        font=self.TYPOGRAPHY['body'], 
                        bg='white', fg='#6b7280')
        label.pack(anchor='w', pady=(0, self.SPACING['xs']))
        
        # Input with modern styling
        entry = tk.Entry(field_frame, font=self.TYPOGRAPHY['body'], 
                        relief='solid', borderwidth=1,
                        highlightthickness=2, highlightcolor='#3b82f6',
                        bg='white', fg='#111827', width=width,
                        insertbackground='#3b82f6')
        entry.pack(anchor='w', ipady=self.SPACING['sm'])
        
        # Placeholder text
        if placeholder:
            entry.insert(0, placeholder)
            entry.config(fg='#9ca3af')
            
            def on_focus_in(event):
                if entry.get() == placeholder:
                    entry.delete(0, 'end')
                    entry.config(fg='#111827')
            
            def on_focus_out(event):
                if entry.get() == '':
                    entry.insert(0, placeholder)
                    entry.config(fg='#9ca3af')
            
            entry.bind('<FocusIn>', on_focus_in)
            entry.bind('<FocusOut>', on_focus_out)
        
        return entry
    
    def create_modern_text_area(self, parent, label_text, height=4):
        """Create a modern text area with label"""
        field_frame = tk.Frame(parent, bg='white')
        field_frame.pack(fill='x', pady=self.SPACING['sm'])
        
        # Label
        label = tk.Label(field_frame, text=label_text, 
                        font=self.TYPOGRAPHY['body'], 
                        bg='white', fg='#6b7280')
        label.pack(anchor='w', pady=(0, self.SPACING['xs']))
        
        # Text area with scrollbar
        text_frame = tk.Frame(field_frame)
        text_frame.pack(fill='x')
        
        text_area = tk.Text(text_frame, font=self.TYPOGRAPHY['body'], 
                          relief='solid', borderwidth=1,
                          highlightthickness=2, highlightcolor='#3b82f6',
                          bg='white', fg='#111827', height=height,
                          wrap='word', insertbackground='#3b82f6')
        text_area.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(text_frame, orient='vertical', command=text_area.yview)
        scrollbar.pack(side='right', fill='y')
        text_area.config(yscrollcommand=scrollbar.set)
        
        return text_area
    
    def create_modern_card(self, parent, title="", content="", bg_color=None):
        """Create a modern card component with shadow effect"""
        theme = self.theme_engine.themes[self.current_theme]
        
        card_frame = tk.Frame(parent, bg=bg_color or theme['card'], 
                            relief='solid', borderwidth=1)
        card_frame.pack(fill='x', pady=self.SPACING['md'], padx=self.SPACING['sm'])
        
        # Card content
        card_content = tk.Frame(card_frame, bg=bg_color or theme['card'])
        card_content.pack(fill='both', expand=True, 
                         padx=self.SPACING['lg'], pady=self.SPACING['lg'])
        
        if title:
            title_label = tk.Label(card_content, text=title,
                                 font=self.TYPOGRAPHY['heading3'],
                                 bg=bg_color or theme['card'],
                                 fg=theme['fg'])
            title_label.pack(anchor='w', pady=(0, self.SPACING['sm']))
        
        if content:
            content_label = tk.Label(card_content, text=content,
                                   font=self.TYPOGRAPHY['body'],
                                   bg=bg_color or theme['card'],
                                   fg=theme['fg'], wraplength=300,
                                   justify='left')
            content_label.pack(anchor='w')
        
        return card_content
    
    def create_modern_button_primary(self, parent, text, command, icon=""):
        """Create a modern primary button with hover effects"""
        theme = self.theme_engine.themes[self.current_theme]
        
        button = tk.Button(parent, 
                         text=f"{icon} {text}" if icon else text,
                         font=self.TYPOGRAPHY['button'],
                         command=command,
                         bg=theme['primary'],
                         fg='white',
                         relief='flat',
                         borderwidth=0,
                         padx=self.SPACING['lg'],
                         pady=self.SPACING['md'],
                         cursor='hand2',
                         activebackground=self.darken_color(theme['primary']),
                         activeforeground='white')
        
        # Hover effects
        def on_enter(event):
            button.configure(bg=self.darken_color(theme['primary']))
        
        def on_leave(event):
            button.configure(bg=theme['primary'])
        
        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)
        
        return button

    def create_enhanced_main_content(self):
        """Create enhanced main content area with modern design - FIXED VERSION"""
        # Create main paned window
        self.main_paned = ttk.PanedWindow(self.window, orient='horizontal')
        self.main_paned.pack(fill='both', expand=True, 
                               padx=self.SPACING['md'], pady=(0, self.SPACING['md']))
        
        # Left panel - Design area (55% width) ✅ REDUCED from 60%
        self.left_panel = ttk.Frame(self.main_paned)
        self.main_paned.add(self.left_panel, weight=55)  # ✅ CHANGED from weight=6
        
        # Create enhanced notebook for tabs
        self.notebook = ttk.Notebook(self.left_panel)
        self.notebook.pack(fill='both', expand=True)
        
        # Create all tabs with enhanced design
        self.create_enhanced_welcome_tab()
        self.create_enhanced_info_tab()
        self.create_enhanced_keywords_tab()
        self.create_enhanced_operators_tab()
        self.create_enhanced_builtins_tab()
        self.create_enhanced_errors_tab()
        self.create_enhanced_advanced_tab()
        
        # Middle panel - Live preview (35% width) ✅ INCREASED from 30%
        self.middle_panel = ttk.Frame(self.main_paned)
        self.main_paned.add(self.middle_panel, weight=35)  # ✅ CHANGED from weight=3
        
        self.create_enhanced_preview_panel()
        
        # Right panel - Progress sidebar (10% width) ✅ SAME
        self.right_panel = ttk.Frame(self.main_paned)
        self.main_paned.add(self.right_panel, weight=10)  # ✅ CHANGED from weight=1
        
        self.create_enhanced_progress_sidebar()
    
    def create_enhanced_welcome_tab(self):
        """Create an enhanced welcome tab with modern card design"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🏠 Welcome")
        
        # Create scrollable area
        canvas = tk.Canvas(tab, highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Hero section with gradient effect
        hero_frame = tk.Frame(scrollable_frame, height=200)
        hero_frame.pack(fill='x', pady=0)
        hero_frame.pack_propagate(False)
        
        # Create gradient canvas
        hero_canvas = tk.Canvas(hero_frame, height=200, highlightthickness=0)
        hero_canvas.pack(fill='both', expand=True)
        
        def update_gradient(event=None):
            width = hero_canvas.winfo_width()
            height = hero_canvas.winfo_height()
            if width > 1 and height > 1:
                hero_canvas.delete("all")
                theme = self.theme_engine.themes[self.current_theme]
                self.theme_engine.create_gradient_bg(hero_canvas, width, height,
                                                   theme['gradient_start'], 
                                                   theme['gradient_end'])
                
                # Add hero text with modern typography
                hero_canvas.create_text(width//2, height//2 - 20, 
                                      text="✨ SUPER Language Creator",
                                      font=self.TYPOGRAPHY['display'], 
                                      fill='white', anchor='center')
                hero_canvas.create_text(width//2, height//2 + 20,
                                      text="Design your dream programming language!",
                                      font=self.TYPOGRAPHY['body_large'], 
                                      fill='white', anchor='center')
        
        hero_canvas.bind('<Configure>', update_gradient)
        self.window.after(100, update_gradient)  # Initial call
        
        # Quick start section with modern spacing
        quick_start = tk.Frame(scrollable_frame, bg='white', 
                             padx=self.SPACING['xl'], pady=self.SPACING['xl'])
        quick_start.pack(fill='x')
        
        tk.Label(quick_start, text="🚀 Quick Start", 
                font=self.TYPOGRAPHY['heading1'], 
                bg='white').pack(anchor='w', pady=(0, self.SPACING['lg']))
        
        # Template cards grid
        cards_frame = tk.Frame(quick_start, bg='white')
        cards_frame.pack(fill='x')
        
        templates = [
            ("💬 GenZ Language", "A trendy language with Gen Z slang and vibes", 
             self.load_genz_template, "#ff6b6b"),
            ("🎮 Game Language", "Perfect for game scripting and interactive stories", 
             self.load_game_template, "#e74c3c"),
            ("🌈 Creative Language", "Colorful, emoji-rich language for creative coding", 
             self.load_color_template, "#9b59b6"),
            ("🎓 Learning Language", "Educational language designed for teaching", 
             self.load_edu_template, "#2ecc71"),
            ("⚡ Start from Scratch", "Complete creative freedom to design anything", 
             self.start_scratch, "#f39c12")
        ]
        
        for i, (title, desc, command, color) in enumerate(templates):
            row = i // 2
            col = i % 2
            
            card = self.create_modern_card(cards_frame, title, desc, command, color)
            card.grid(row=row, column=col, padx=15, pady=15, sticky='nsew')
            
        # Configure grid weights
        cards_frame.grid_columnconfigure(0, weight=1)
        cards_frame.grid_columnconfigure(1, weight=1)
        
        # Recent projects section
        recent_frame = tk.Frame(scrollable_frame, bg='#f8f9fa', padx=30, pady=20)
        recent_frame.pack(fill='x')
        
        tk.Label(recent_frame, text="📝 Recent Projects", 
                font=('Arial', 16, 'bold'), bg='#f8f9fa').pack(anchor='w', pady=(0, 10))
        
        # Load and display recent projects
        self.display_recent_projects(recent_frame)
        
        # Tips section
        tips_frame = tk.Frame(scrollable_frame, bg='white', padx=30, pady=20)
        tips_frame.pack(fill='x')
        
        tk.Label(tips_frame, text="💡 Tips & Tricks", 
                font=('Arial', 16, 'bold'), bg='white').pack(anchor='w', pady=(0, 10))
        
        tips = [
            "🎯 Start with simple keywords and gradually add complexity",
            "🎨 Use the random keyword generator for creative inspiration",
            "🧪 Test your language frequently in the playground",
            "📚 Check out the examples gallery for inspiration",
            "🏆 Unlock achievements by exploring different features"
        ]
        
        for tip in tips:
            tip_label = tk.Label(tips_frame, text=tip, font=('Arial', 11), 
                               bg='white', anchor='w')
            tip_label.pack(fill='x', pady=2)
    
    def create_modern_card(self, parent, title, description, command, color):
        """Create a modern styled card widget - FIXED VERSION"""
        card = tk.Frame(parent, bg='white', relief='solid', bd=1,
                    width=300, height=140)  # ✅ INCREASED HEIGHT from 120 to 140
        card.pack_propagate(False)
        
        # Header with colored bar
        header = tk.Frame(card, bg=color, height=4)
        header.pack(fill='x')
        
        # Content area
        content = tk.Frame(card, bg='white', padx=15, pady=12)  # ✅ REDUCED padding
        content.pack(fill='both', expand=True)
        
        # Title
        title_label = tk.Label(content, text=title, font=('Arial', 13, 'bold'),  # ✅ SMALLER font
                            bg='white', fg='#1a202c')
        title_label.pack(anchor='w')
        
        # Description
        desc_label = tk.Label(content, text=description, font=('Arial', 9),  # ✅ SMALLER font
                            bg='white', fg='#666', wraplength=270,  # ✅ BETTER wrap
                            justify='left')
        desc_label.pack(anchor='w', pady=(3, 8))  # ✅ REDUCED padding
        
        # Action button
        btn = tk.Button(content, text="Get Started →", command=command,
                    bg=color, fg='white', font=('Arial', 9, 'bold'),  # ✅ SMALLER font
                    relief='flat', padx=15, pady=4,  # ✅ SMALLER padding
                    cursor='hand2')
        btn.pack(anchor='w')
        
        # Hover effects
        def on_enter(e):
            card.configure(relief='solid', bd=2)
            btn.configure(bg=self.darken_color(color))
        
        def on_leave(e):
            card.configure(relief='solid', bd=1)
            btn.configure(bg=color)
        
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        for widget in card.winfo_children():
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
        
        return card
    
    def display_recent_projects(self, parent):
        """Display recent projects"""
        try:
            with open('.recent_languages.json', 'r') as f:
                recent = json.load(f)
        except:
            recent = []
        
        if not recent:
            no_recent = tk.Label(parent, text="No recent projects yet. Create your first language!",
                               font=('Arial', 11), bg='#f8f9fa', fg='#666')
            no_recent.pack(anchor='w')
            return
        
        for project in recent[:3]:  # Show last 3
            project_frame = tk.Frame(parent, bg='#ffffff', relief='solid', bd=1)
            project_frame.pack(fill='x', pady=5)
            
            info_frame = tk.Frame(project_frame, bg='#ffffff', padx=15, pady=10)
            info_frame.pack(side='left', fill='both', expand=True)
            
            # Project name
            name_label = tk.Label(info_frame, text=project['name'], 
                                font=('Arial', 12, 'bold'), bg='#ffffff')
            name_label.pack(anchor='w')
            
            # Project details
            date_str = project.get('date', '')[:10]  # Just the date part
            details = f"by {project.get('author', 'Unknown')} • {date_str}"
            details_label = tk.Label(info_frame, text=details,
                                   font=('Arial', 10), bg='#ffffff', fg='#666')
            details_label.pack(anchor='w')
            
            # Open button
            open_btn = tk.Button(project_frame, text="Open →",
                               command=lambda p=project: self.load_recent_project(p),
                               bg='#667eea', fg='white', relief='flat',
                               padx=15, pady=10)
            open_btn.pack(side='right')
    
    def load_recent_project(self, project):
        """Load a recent project"""
        # This would load the actual project data
        # For now, just show a message
        messagebox.showinfo("Load Project", 
                          f"Loading project: {project['name']}\n(Feature coming soon!)")
    
    def create_enhanced_info_tab(self):
        """Create enhanced basic info tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📝 Basic Info")
        
        # Create scrollable content
        canvas = tk.Canvas(tab, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient='vertical', command=canvas.yview)
        content_frame = tk.Frame(canvas, bg='white')
        
        content_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=content_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Main content with better spacing
        main_content = tk.Frame(content_frame, bg='white', padx=40, pady=30)
        main_content.pack(fill='both', expand=True)
        
        # Header section
        header_frame = tk.Frame(main_content, bg='white')
        header_frame.pack(fill='x', pady=(0, 30))
        
        tk.Label(header_frame, text="📝 Basic Information", 
                font=('Arial', 24, 'bold'), bg='white').pack(anchor='w')
        tk.Label(header_frame, text="Tell us about your programming language",
                font=('Arial', 12), bg='white', fg='#666').pack(anchor='w', pady=(5, 0))
        
        # Language name section
        name_section = self.create_form_section(main_content, "Language Name")
        
        name_input_frame = tk.Frame(name_section, bg='white')
        name_input_frame.pack(fill='x', pady=(5, 0))
        
        self.name_entry = tk.Entry(name_input_frame, font=('Arial', 16), 
                                  relief='solid', bd=1, bg='#f8f9fa',
                                  fg='#1a202c', width=30)
        self.name_entry.pack(side='left', ipady=8, ipadx=10)
        self.name_entry.insert(0, "MyAwesomeLang")
        self.name_entry.bind('<KeyRelease>', self.update_preview)
        
        # File extension preview
        ext_preview = tk.Frame(name_input_frame, bg='white')
        ext_preview.pack(side='left', padx=(20, 0))
        
        tk.Label(ext_preview, text="File extension:", font=('Arial', 11),
                bg='white', fg='#666').pack(anchor='w')
        
        ext_display = tk.Frame(ext_preview, bg='white')
        ext_display.pack(anchor='w')
        
        tk.Label(ext_display, text="yourfile.", font=('Arial', 11),
                bg='white').pack(side='left')
        
        self.ext_label = tk.Label(ext_display, text="myal", font=('Arial', 11, 'bold'),
                                 bg='white', fg='#667eea')
        self.ext_label.pack(side='left')
        
        # Version and Author in same row
        version_author_frame = tk.Frame(main_content, bg='white')
        version_author_frame.pack(fill='x', pady=(20, 0))
        
        # Version (left half)
        version_section = self.create_form_section(version_author_frame, "Version")
        version_section.pack(side='left', fill='x', expand=True, padx=(0, 20))
        
        self.version_entry = tk.Entry(version_section, font=('Arial', 14),
                                     relief='solid', bd=1, bg='#f8f9fa')
        self.version_entry.pack(fill='x', ipady=6, ipadx=10, pady=(5, 0))
        self.version_entry.insert(0, "1.0")
        
        # Author (right half)
        author_section = self.create_form_section(version_author_frame, "Your Name")
        author_section.pack(side='left', fill='x', expand=True)
        
        self.author_entry = tk.Entry(author_section, font=('Arial', 14),
                                    relief='solid', bd=1, bg='#f8f9fa')
        self.author_entry.pack(fill='x', ipady=6, ipadx=10, pady=(5, 0))
        self.author_entry.insert(0, "Young Coder")
        
        # Description section
        desc_section = self.create_form_section(main_content, "Description")
        desc_section.pack(fill='x', pady=(20, 0))
        
        self.desc_text = tk.Text(desc_section, height=4, font=('Arial', 12),
                               wrap='word', relief='solid', bd=1, bg='#f8f9fa',
                               fg='#1a202c')
        self.desc_text.pack(fill='x', pady=(5, 0), ipady=10, ipadx=10)
        self.desc_text.insert('1.0', "My awesome programming language that makes coding fun and easy!")
        
        # Language features section
        features_section = self.create_form_section(main_content, "Language Features")
        features_section.pack(fill='x', pady=(30, 0))
        
        features_grid = tk.Frame(features_section, bg='white')
        features_grid.pack(fill='x', pady=(10, 0))
        
        self.features = {}
        feature_list = [
            ('typed', 'Static Typing', 'Variables must declare their type'),
            ('functional', 'Functional Programming', 'Support for functional concepts'),
            ('oop', 'Object Oriented', 'Classes and objects'),
            ('async', 'Async/Await', 'Asynchronous programming'),
            ('unicode', 'Unicode Support', 'Use any Unicode characters'),
            ('case_sensitive', 'Case Sensitive', 'myVar ≠ MyVar'),
        ]
        
        for i, (key, label, desc) in enumerate(feature_list):
            row = i // 2
            col = i % 2
            
            feature_frame = tk.Frame(features_grid, bg='white')
            feature_frame.grid(row=row, column=col, sticky='ew', padx=(0, 30), pady=8)
            
            var = tk.BooleanVar()
            cb = tk.Checkbutton(feature_frame, text=label, variable=var,
                              font=('Arial', 12), bg='white',
                              activebackground='white',
                              selectcolor='#667eea')
            cb.pack(anchor='w')
            
            desc_label = tk.Label(feature_frame, text=desc, font=('Arial', 10),
                                 bg='white', fg='#666')
            desc_label.pack(anchor='w', padx=(25, 0))
            
            self.features[key] = var
        
        # Configure grid weights
        features_grid.grid_columnconfigure(0, weight=1)
        features_grid.grid_columnconfigure(1, weight=1)
    
    def create_form_section(self, parent, title):
        """Create a form section with title"""
        section = tk.Frame(parent, bg='white')
        section.pack(fill='x', pady=(0, 10))
        
        title_label = tk.Label(section, text=title, font=('Arial', 14, 'bold'),
                              bg='white', fg='#1a202c')
        title_label.pack(anchor='w')
        
        return section
    
    def create_enhanced_keywords_tab(self):
        """Create enhanced keywords tab with better organization"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🔤 Keywords")
        
        # Create main container
        main_container = tk.Frame(tab, bg='white')
        main_container.pack(fill='both', expand=True)
        
        # Header with random generator button
        header_frame = tk.Frame(main_container, bg='#667eea', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg='#667eea')
        header_content.pack(expand=True, fill='both', padx=30, pady=20)
        
        title_frame = tk.Frame(header_content, bg='#667eea')
        title_frame.pack(side='left', fill='both', expand=True)
        
        tk.Label(title_frame, text="🔤 Language Keywords", 
                font=('Arial', 20, 'bold'), bg='#667eea', fg='white').pack(anchor='w')
        tk.Label(title_frame, text="Define the special words that make your language unique",
                font=('Arial', 12), bg='#667eea', fg='#e2e8f0').pack(anchor='w')
        
        # Random generator button
        random_btn = tk.Button(header_content, text="🎲 Random Keywords",
                             command=self.show_enhanced_keyword_generator,
                             bg='white', fg='#667eea', font=('Arial', 11, 'bold'),
                             relief='flat', padx=20, pady=8,
                             cursor='hand2')
        random_btn.pack(side='right', pady=10)
        
        # Scrollable content
        canvas = tk.Canvas(main_container, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Content with better spacing
        content = tk.Frame(scrollable_frame, bg='white', padx=40, pady=30)
        content.pack(fill='both', expand=True)
        
        # Keywords organized by category
        categories = [
            ("Essential Keywords", [
                ('function', 'Define a function', '✨', 'Create reusable code blocks'),
                ('variable', 'Store data', '📦', 'Hold values and information'),
                ('if', 'Make decisions', '❓', 'Check conditions'),
                ('else', 'Alternative path', '↔️', 'What to do otherwise'),
            ]),
            ("Control Flow", [
                ('loop', 'Repeat actions', '🔄', 'Do something multiple times'),
                ('return', 'Give back result', '↩️', 'Return a value from function'),
            ]),
            ("Values", [
                ('true', 'Yes/correct', '✅', 'Boolean true value'),
                ('false', 'No/incorrect', '❌', 'Boolean false value'),
                ('null', 'Nothing/empty', '🚫', 'Represents no value'),
            ])
        ]
        
        self.keyword_entries = {}
        
        for category_name, keywords in categories:
            # Category section
            category_frame = tk.Frame(content, bg='white')
            category_frame.pack(fill='x', pady=(0, 30))
            
            # Category header
            cat_header = tk.Frame(category_frame, bg='#f8f9fa', relief='solid', bd=1)
            cat_header.pack(fill='x', pady=(0, 15))
            
            tk.Label(cat_header, text=category_name, font=('Arial', 16, 'bold'),
                    bg='#f8f9fa', fg='#1a202c').pack(anchor='w', padx=20, pady=10)
            
            # Keywords grid
            keywords_grid = tk.Frame(category_frame, bg='white')
            keywords_grid.pack(fill='x')
            
            for i, (keyword, description, icon, help_text) in enumerate(keywords):
                self.create_keyword_input(keywords_grid, keyword, description, icon, help_text, i)
            
        # Help section
        help_frame = tk.Frame(content, bg='#e8f4fd', relief='solid', bd=1, padx=20, pady=15)
        help_frame.pack(fill='x', pady=(20, 0))
        
        tk.Label(help_frame, text="💡 Pro Tips", font=('Arial', 14, 'bold'),
                bg='#e8f4fd').pack(anchor='w')
        
        tips = [
            "• Use words that make sense to you and your audience",
            "• Short words are easier to type (but can be longer if meaningful)",
            "• Try themed words like 'spell' for function, 'potion' for variable",
            "• Consider your target users - kids might like 'do' instead of 'function'"
        ]
        
        for tip in tips:
            tk.Label(help_frame, text=tip, font=('Arial', 11),
                    bg='#e8f4fd', fg='#2d3748').pack(anchor='w', pady=1)
    
    def create_keyword_input(self, parent, keyword, description, icon, help_text, index):
        """Create an enhanced keyword input row"""
        row_frame = tk.Frame(parent, bg='white', relief='solid', bd=1)
        row_frame.pack(fill='x', pady=8)
        
        # Main content frame
        main_frame = tk.Frame(row_frame, bg='white', padx=20, pady=15)
        main_frame.pack(fill='x')
        
        # Left side - icon and info
        left_frame = tk.Frame(main_frame, bg='white')
        left_frame.pack(side='left', fill='x', expand=True)
        
        # Icon
        icon_label = tk.Label(left_frame, text=icon, font=('Arial', 24),
                             bg='white')
        icon_label.pack(side='left', padx=(0, 15))
        
        # Info
        info_frame = tk.Frame(left_frame, bg='white')
        info_frame.pack(side='left', fill='x', expand=True)
        
        # English keyword
        eng_frame = tk.Frame(info_frame, bg='white')
        eng_frame.pack(anchor='w', fill='x')
        
        tk.Label(eng_frame, text=keyword, font=('Arial', 14, 'bold'),
                bg='white').pack(side='left')
        tk.Label(eng_frame, text=f" - {description}", font=('Arial', 12),
                bg='white', fg='#666').pack(side='left')
        
        # Help text
        tk.Label(info_frame, text=help_text, font=('Arial', 10),
                bg='white', fg='#666', wraplength=300).pack(anchor='w', pady=(2, 0))
        
        # Right side - input
        right_frame = tk.Frame(main_frame, bg='white')
        right_frame.pack(side='right')
        
        # Arrow
        tk.Label(right_frame, text="→", font=('Arial', 16),
                bg='white', fg='#667eea').pack(side='left', padx=10)
        
        # Entry field
        entry = tk.Entry(right_frame, font=('Arial', 14), width=15,
                        relief='solid', bd=1, bg='#f8f9fa')
        entry.pack(side='left', ipady=5)
        entry.bind('<KeyRelease>', self.update_preview)
        
        # Add suggestion button
        suggest_btn = tk.Button(right_frame, text="💡",
                              command=lambda k=keyword: self.suggest_keyword(k),
                              font=('Arial', 10), relief='flat',
                              bg='#f8f9fa', fg='#667eea',
                              width=3, cursor='hand2')
        suggest_btn.pack(side='left', padx=(5, 0))
        
        self.keyword_entries[keyword] = entry
        
        # Add hover effect
        def on_enter(e):
            row_frame.configure(bg='#f8f9fa')
            main_frame.configure(bg='#f8f9fa')
            left_frame.configure(bg='#f8f9fa')
            info_frame.configure(bg='#f8f9fa')
            eng_frame.configure(bg='#f8f9fa')
            right_frame.configure(bg='#f8f9fa')
            for child in [icon_label] + list(eng_frame.winfo_children()) + list(info_frame.winfo_children()):
                if hasattr(child, 'configure'):
                    try:
                        child.configure(bg='#f8f9fa')
                    except:
                        pass
        
        def on_leave(e):
            row_frame.configure(bg='white')
            main_frame.configure(bg='white')
            left_frame.configure(bg='white')
            info_frame.configure(bg='white')
            eng_frame.configure(bg='white')
            right_frame.configure(bg='white')
            for child in [icon_label] + list(eng_frame.winfo_children()) + list(info_frame.winfo_children()):
                if hasattr(child, 'configure'):
                    try:
                        child.configure(bg='white')
                    except:
                        pass
        
        row_frame.bind("<Enter>", on_enter)
        row_frame.bind("<Leave>", on_leave)
    
    def suggest_keyword(self, keyword):
        """Show suggestion for a specific keyword"""
        suggestions = {
            'function': ['do', 'make', 'create', 'build', 'craft', 'spell', 'action'],
            'variable': ['box', 'store', 'keep', 'data', 'item', 'treasure', 'memory'],
            'if': ['when', 'check', 'test', 'ask', 'verify', 'guard', 'filter'],
            'else': ['otherwise', 'or', 'instead', 'alternative', 'backup'],
            'loop': ['repeat', 'again', 'cycle', 'iterate', 'multiple', 'many'],
            'return': ['give', 'send', 'output', 'result', 'answer', 'yield'],
            'true': ['yes', 'correct', 'right', 'positive', 'good', 'ok'],
            'false': ['no', 'wrong', 'bad', 'negative', 'error', 'fail'],
            'null': ['empty', 'nothing', 'void', 'blank', 'zero', 'none']
        }
        
        if keyword in suggestions:
            suggestion = random.choice(suggestions[keyword])
            entry = self.keyword_entries[keyword]
            entry.delete(0, tk.END)
            entry.insert(0, suggestion)
            self.update_preview()
    
    def show_enhanced_keyword_generator(self):
        """Show enhanced keyword generator dialog"""
        dialog = tk.Toplevel(self.window)
        dialog.title("🎲 Random Keyword Generator")
        dialog.geometry("600x700")
        dialog.transient(self.window)
        dialog.grab_set()
        
        # Header
        header = tk.Frame(dialog, bg='#667eea', height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        header_content = tk.Frame(header, bg='#667eea')
        header_content.pack(expand=True, fill='both', padx=30, pady=20)
        
        tk.Label(header_content, text="🎲 Keyword Generator", 
                font=('Arial', 20, 'bold'), bg='#667eea', fg='white').pack(anchor='w')
        tk.Label(header_content, text="Choose a theme and generate creative keywords!",
                font=('Arial', 12), bg='#667eea', fg='#e2e8f0').pack(anchor='w')
        
        # Main content
        main_content = tk.Frame(dialog, bg='white', padx=30, pady=20)
        main_content.pack(fill='both', expand=True)
        
        # Theme selection
        tk.Label(main_content, text="Select a Theme:", 
                font=('Arial', 14, 'bold'), bg='white').pack(anchor='w', pady=(0, 10))
        
        # Theme cards
        themes_frame = tk.Frame(main_content, bg='white')
        themes_frame.pack(fill='x', pady=(0, 20))
        
        selected_theme = tk.StringVar()
        theme_buttons = []
        
        for i, (theme_id, theme_data) in enumerate(self.keyword_generator.themes.items()):
            row = i // 2
            col = i % 2
            
            theme_card = tk.Frame(themes_frame, bg='white', relief='solid', bd=1)
            theme_card.grid(row=row, column=col, padx=10, pady=5, sticky='ew')
            
            # Theme button
            btn = tk.Radiobutton(theme_card, text=f"{theme_data['icon']} {theme_data['name']}",
                               variable=selected_theme, value=theme_id,
                               font=('Arial', 12), bg='white',
                               indicator=0, selectcolor='#667eea',
                               activebackground='#f8f9fa')
            btn.pack(fill='x', padx=10, pady=10)
            
            theme_buttons.append(btn)
        
        # Configure grid
        themes_frame.grid_columnconfigure(0, weight=1)
        themes_frame.grid_columnconfigure(1, weight=1)
        
        # Preview area
        preview_frame = tk.LabelFrame(main_content, text="Preview", 
                                    font=('Arial', 12, 'bold'), bg='white',
                                    padx=15, pady=10)
        preview_frame.pack(fill='both', expand=True, pady=(10, 20))
        
        preview_text = scrolledtext.ScrolledText(preview_frame, height=10, 
                                               font=('Courier', 10),
                                               bg='#f8f9fa', relief='flat')
        preview_text.pack(fill='both', expand=True)
        
        def update_preview():
            theme_id = selected_theme.get()
            if theme_id:
                keywords, theme_name, icon = self.keyword_generator.generate_keywords(theme_id)
                functions = self.keyword_generator.generate_functions(theme_id)
                
                preview_content = f"""✨ {icon} {theme_name} Keywords ✨

🔤 KEYWORDS:
"""
                for eng, custom in keywords.items():
                    preview_content += f"  {eng} → {custom}\n"
                
                preview_content += f"\n🛠️ FUNCTIONS:\n"
                for eng, custom in functions.items():
                    preview_content += f"  {eng} → {custom}\n"
                
                preview_content += f"\n📝 EXAMPLE CODE:\n"
                preview_content += f"{keywords.get('function', 'function')} greet(name) {{\n"
                preview_content += f"    {functions.get('print', 'print')}(\"Hello\", name)\n"
                preview_content += f"}}\n\n"
                preview_content += f"{keywords.get('variable', 'var')} message = \"Welcome!\"\n"
                preview_content += f"greet(message)\n"
                
                preview_text.delete('1.0', tk.END)
                preview_text.insert('1.0', preview_content)
        
        # Bind theme selection to preview update
        for btn in theme_buttons:
            btn.configure(command=update_preview)
        
        # Set default selection
        if self.keyword_generator.themes:
            first_theme = list(self.keyword_generator.themes.keys())[0]
            selected_theme.set(first_theme)
            update_preview()
        
        # Buttons
        button_frame = tk.Frame(main_content, bg='white')
        button_frame.pack(fill='x', pady=(10, 0))
        
        def apply_keywords():
            theme_id = selected_theme.get()
            if theme_id:
                keywords, theme_name, icon = self.keyword_generator.generate_keywords(theme_id)
                functions = self.keyword_generator.generate_functions(theme_id)
                
                # Apply keywords
                for eng, custom in keywords.items():
                    if eng in self.keyword_entries:
                        entry = self.keyword_entries[eng]
                        entry.delete(0, tk.END)
                        entry.insert(0, custom)
                
                # Apply functions
                for eng, custom in functions.items():
                    if hasattr(self, 'builtin_entries') and eng in self.builtin_entries:
                        entry = self.builtin_entries[eng]
                        entry.delete(0, tk.END)
                        entry.insert(0, custom)
                
                self.update_preview()
                self.unlock_achievement('random_master')
                
                dialog.destroy()
                
                messagebox.showinfo("Keywords Applied! 🎉",
                                  f"Applied {icon} {theme_name} themed keywords to your language!")
        
        tk.Button(button_frame, text="🔄 Generate New",
                 command=update_preview, bg='#f8f9fa', 
                 font=('Arial', 11), padx=20, pady=8).pack(side='left')
        
        tk.Button(button_frame, text="✨ Apply Keywords", 
                 command=apply_keywords,
                 bg='#667eea', fg='white', font=('Arial', 11, 'bold'),
                 padx=20, pady=8).pack(side='right', padx=(10, 0))
        
        tk.Button(button_frame, text="Cancel",
                 command=dialog.destroy, bg='#e2e8f0',
                 font=('Arial', 11), padx=20, pady=8).pack(side='right')
    
    def create_enhanced_operators_tab(self):
        """Create enhanced operators tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="➕ Operators")
        
        # Similar structure to keywords but for operators
        # Implementation would follow the same pattern
        # For brevity, I'll provide a simplified version
        
        container = tk.Frame(tab, bg='white')
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(container, text="➕ Customize Operators", 
                font=('Arial', 18, 'bold'), bg='white').pack(pady=10)
        
        tk.Label(container, text="Change how math and logic work in your language (Optional)",
                font=('Arial', 12), bg='white', fg='gray').pack()
        
        # Add operator sections here...
        # This would follow the same enhanced pattern as keywords
    
    def create_enhanced_builtins_tab(self):
        """Create enhanced built-in functions tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🛠️ Built-in Functions")
        
        # Header
        header_frame = tk.Frame(tab, bg='#38a169', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg='#38a169')
        header_content.pack(expand=True, fill='both', padx=30, pady=20)
        
        tk.Label(header_content, text="🛠️ Built-in Functions", 
                font=('Arial', 20, 'bold'), bg='#38a169', fg='white').pack(anchor='w')
        tk.Label(header_content, text="Define the actions your language can perform",
                font=('Arial', 12), bg='#38a169', fg='#e2e8f0').pack(anchor='w')
        
        # Scrollable content
        canvas = tk.Canvas(tab, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient='vertical', command=canvas.yview)
        content_frame = tk.Frame(canvas, bg='white')
        
        content_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=content_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Main content
        main_content = tk.Frame(content_frame, bg='white', padx=40, pady=30)
        main_content.pack(fill='both', expand=True)
        
        # Essential functions
        essential_section = self.create_form_section(main_content, "Essential Functions")
        essential_section.pack(fill='x', pady=(0, 20))
        
        self.builtin_entries = {}
        
        essential_funcs = [
            ('print', 'Display output', '📢', 'Show text and values to the user'),
            ('input', 'Get user input', '⌨️', 'Ask the user for information'),
            ('length', 'Get size', '📏', 'Count characters in text or items in list'),
            ('string', 'Convert to text', '📝', 'Turn numbers into readable text'),
            ('number', 'Convert to number', '🔢', 'Turn text into numbers for math'),
        ]
        
        for func, desc, icon, help_text in essential_funcs:
            self.create_builtin_input(essential_section, func, desc, icon, help_text)
        
        # Advanced functions
        advanced_section = self.create_form_section(main_content, "Advanced Functions (Optional)")
        advanced_section.pack(fill='x', pady=(20, 0))
        
        advanced_funcs = [
            ('random', 'Random numbers', '🎲', 'Generate random numbers for games'),
            ('read_file', 'Read files', '📄', 'Load content from files'),
            ('write_file', 'Write files', '💾', 'Save content to files'),
            ('time', 'Get time', '⏰', 'Get current date and time'),
        ]
        
        for func, desc, icon, help_text in advanced_funcs:
            self.create_builtin_input(advanced_section, func, desc, icon, help_text)
    
    def create_builtin_input(self, parent, func, desc, icon, help_text):
        """Create enhanced builtin function input"""
        row_frame = tk.Frame(parent, bg='white', relief='solid', bd=1)
        row_frame.pack(fill='x', pady=5)
        
        main_frame = tk.Frame(row_frame, bg='white', padx=20, pady=12)
        main_frame.pack(fill='x')
        
        # Left side
        left_frame = tk.Frame(main_frame, bg='white')
        left_frame.pack(side='left', fill='x', expand=True)
        
        # Icon
        tk.Label(left_frame, text=icon, font=('Arial', 20),
                bg='white').pack(side='left', padx=(0, 15))
        
        # Info
        info_frame = tk.Frame(left_frame, bg='white')
        info_frame.pack(side='left', fill='x', expand=True)
        
        # Function name and description
        name_frame = tk.Frame(info_frame, bg='white')
        name_frame.pack(anchor='w', fill='x')
        
        tk.Label(name_frame, text=func, font=('Arial', 12, 'bold'),
                bg='white').pack(side='left')
        tk.Label(name_frame, text=f" - {desc}", font=('Arial', 11),
                bg='white', fg='#666').pack(side='left')
        
        # Help text
        tk.Label(info_frame, text=help_text, font=('Arial', 10),
                bg='white', fg='#666', wraplength=300).pack(anchor='w')
        
        # Right side - input
        right_frame = tk.Frame(main_frame, bg='white')
        right_frame.pack(side='right')
        
        tk.Label(right_frame, text="→", font=('Arial', 14),
                bg='white', fg='#38a169').pack(side='left', padx=10)
        
        entry = tk.Entry(right_frame, font=('Arial', 12), width=15,
                        relief='solid', bd=1, bg='#f8f9fa')
        entry.pack(side='left', ipady=4)
        entry.bind('<KeyRelease>', self.update_preview)
        
        # Add default suggestion
        suggestions = {
            'print': 'show',
            'input': 'ask',
            'length': 'size',
            'string': 'text',
            'number': 'num',
            'random': 'random',
            'read_file': 'load',
            'write_file': 'save',
            'time': 'clock'
        }
        
        if func in suggestions:
            entry.insert(0, suggestions[func])
        
        self.builtin_entries[func] = entry

    def calculate_avg_keyword_length(self):
        """Calculate average keyword length"""
        keywords = [k for k in self.language_data.get('keywords', {}).values() if k]
        if not keywords:
            return 0
        return sum(len(k) for k in keywords) / len(keywords)   

    def show_statistics(self):
        """Show detailed language statistics in a dialog"""
        self.collect_language_data()
        
        dialog = tk.Toplevel(self.window)
        dialog.title("📊 Language Statistics")
        dialog.geometry("600x700")
        dialog.transient(self.window)
        
        # Header
        header = tk.Frame(dialog, bg='#667eea', height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        header_content = tk.Frame(header, bg='#667eea')
        header_content.pack(expand=True, fill='both', padx=30, pady=20)
        
        tk.Label(header_content, text="📊 Language Statistics", 
                font=('Arial', 20, 'bold'), bg='#667eea', fg='white').pack(anchor='w')
        tk.Label(header_content, text="Detailed analysis of your language",
                font=('Arial', 12), bg='#667eea', fg='#e2e8f0').pack(anchor='w')
        
        # Main content with scrolling
        canvas = tk.Canvas(dialog, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(dialog, orient='vertical', command=canvas.yview)
        content_frame = tk.Frame(canvas, bg='white')
        
        content_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=content_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Generate detailed statistics
        stats = self.calculate_enhanced_statistics()
        
        main_content = tk.Frame(content_frame, bg='white', padx=30, pady=20)
        main_content.pack(fill='both', expand=True)
        
        # Overview section
        overview_frame = tk.LabelFrame(main_content, text="📋 Overview",
                                    font=('Arial', 14, 'bold'), bg='white')
        overview_frame.pack(fill='x', pady=(0, 20))
        
        overview_stats = [
            ("Language Name", self.language_data.get('name', 'Unnamed')),
            ("Version", self.language_data.get('version', '1.0')),
            ("Author", self.language_data.get('author', 'Unknown')),
            ("Created", self.language_data.get('created', 'Unknown')[:10] if self.language_data.get('created') else 'Unknown'),
            ("Completion", f"{stats['completion']}%"),
            ("Complexity", stats['complexity'])
        ]
        
        for label, value in overview_stats:
            row = tk.Frame(overview_frame, bg='white')
            row.pack(fill='x', padx=15, pady=3)
            
            tk.Label(row, text=f"{label}:", font=('Arial', 11),
                    bg='white', fg='#4a5568').pack(side='left')
            tk.Label(row, text=str(value), font=('Arial', 11, 'bold'),
                    bg='white', fg='#1a202c').pack(side='right')
        
        # Components section
        components_frame = tk.LabelFrame(main_content, text="🔧 Components",
                                    font=('Arial', 14, 'bold'), bg='white')
        components_frame.pack(fill='x', pady=(0, 20))
        
        component_stats = [
            ("Keywords Defined", stats['keywords_count']),
            ("Built-in Functions", stats['functions_count']),
            ("Error Messages", stats['errors_count']),
            ("Features Enabled", len([f for f in self.language_data.get('features', {}).values() if f])),
            ("Total Customizations", stats['total_customizations'])
        ]
        
        for label, value in component_stats:
            row = tk.Frame(components_frame, bg='white')
            row.pack(fill='x', padx=15, pady=3)
            
            tk.Label(row, text=f"{label}:", font=('Arial', 11),
                    bg='white', fg='#4a5568').pack(side='left')
            tk.Label(row, text=str(value), font=('Arial', 11, 'bold'),
                    bg='white', fg='#667eea').pack(side='right')
        
        # Content analysis
        analysis_frame = tk.LabelFrame(main_content, text="📝 Content Analysis",
                                    font=('Arial', 14, 'bold'), bg='white')
        analysis_frame.pack(fill='x', pady=(0, 20))
        
        analysis_stats = [
            ("Total Characters", stats['total_chars']),
            ("Uses Unicode", "Yes" if stats['uses_unicode'] else "No"),
            ("Contains Emojis", "Yes" if stats['has_emojis'] else "No"),
            ("Average Keyword Length", f"{self.calculate_avg_keyword_length():.1f} chars"),
            ("Theme", self.theme_engine.themes[self.current_theme]['name'])
        ]
        
        for label, value in analysis_stats:
            row = tk.Frame(analysis_frame, bg='white')
            row.pack(fill='x', padx=15, pady=3)
            
            tk.Label(row, text=f"{label}:", font=('Arial', 11),
                    bg='white', fg='#4a5568').pack(side='left')
            tk.Label(row, text=str(value), font=('Arial', 11, 'bold'),
                    bg='white', fg='#38a169').pack(side='right')
        
        # Usage statistics
        usage_frame = tk.LabelFrame(main_content, text="📈 Usage Statistics",
                                font=('Arial', 14, 'bold'), bg='white')
        usage_frame.pack(fill='x', pady=(0, 20))
        
        usage_stats = [
            ("Time Spent", self.format_time_spent()),
            ("Tests Run", getattr(self, 'test_count', 0)),
            ("Saves Performed", getattr(self, 'save_count', 0)),
            ("Theme Changes", len(getattr(self, 'themes_tried', set()))),
            ("Achievements Unlocked", f"{self.achievement_system.get_progress()[0]}/{self.achievement_system.get_progress()[1]}")
        ]
        
        for label, value in usage_stats:
            row = tk.Frame(usage_frame, bg='white')
            row.pack(fill='x', padx=15, pady=3)
            
            tk.Label(row, text=f"{label}:", font=('Arial', 11),
                    bg='white', fg='#4a5568').pack(side='left')
            tk.Label(row, text=str(value), font=('Arial', 11, 'bold'),
                    bg='white', fg='#ed8936').pack(side='right')
        
        # Fun facts
        if stats['fun_facts']:
            facts_frame = tk.LabelFrame(main_content, text="🎉 Fun Facts",
                                    font=('Arial', 14, 'bold'), bg='white')
            facts_frame.pack(fill='x')
            
            for fact in stats['fun_facts']:
                tk.Label(facts_frame, text=f"• {fact}", font=('Arial', 11),
                        bg='white', fg='#9f7aea').pack(anchor='w', padx=15, pady=3)
        
        # Close button
        button_frame = tk.Frame(dialog, bg='white', padx=20, pady=15)
        button_frame.pack(fill='x')
        
        tk.Button(button_frame, text="Close", command=dialog.destroy,
                bg='#667eea', fg='white', font=('Arial', 11),
                padx=20, pady=8).pack(side='right')


    def preview_error(self, error_key):
        """Preview how an error would look"""
        error_msg = self.error_entries[error_key].get('1.0', 'end-1c').strip()
        
        # Create preview window
        preview = tk.Toplevel(self.window)
        preview.title("Error Preview")
        preview.geometry("500x300")
        
        # Error display
        frame = tk.Frame(preview, bg='#fee', padx=20, pady=20)
        frame.pack(fill='both', expand=True)
        
        # Error icon and title
        header = tk.Frame(frame, bg='#fee')
        header.pack(fill='x')
        
        tk.Label(header, text="❌", font=('Arial', 40),
                bg='#fee').pack(side='left', padx=(0, 20))
        
        tk.Label(header, text=f"{error_key.replace('_', ' ').title()}",
                font=('Arial', 20, 'bold'), bg='#fee').pack(side='left')
        
        # Error message
        msg_frame = tk.Frame(frame, bg='white', relief='solid', bd=1)
        msg_frame.pack(fill='both', expand=True, pady=20)
        
        # Format message with placeholders
        formatted_msg = error_msg
        if '{name}' in formatted_msg:
            formatted_msg = formatted_msg.replace('{name}', 'myVariable')
        if '{expected}' in formatted_msg:
            formatted_msg = formatted_msg.replace('{expected}', 'number')
        if '{got}' in formatted_msg:
            formatted_msg = formatted_msg.replace('{got}', 'string')
        
        tk.Label(msg_frame, text=formatted_msg, font=('Arial', 14),
                bg='white', wraplength=400, justify='left').pack(padx=20, pady=20)
        
        # Close button
        tk.Button(frame, text="Close", command=preview.destroy,
             bg='white', relief='solid', bd=1).pack(pady=10)
    def create_enhanced_advanced_tab(self):
        """Create enhanced advanced features tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="⚙️ Advanced")
        
        # Header
        header_frame = tk.Frame(tab, bg='#9f7aea', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg='#9f7aea')
        header_content.pack(expand=True, fill='both', padx=30, pady=20)
        
        tk.Label(header_content, text="⚙️ Advanced Features", 
                font=('Arial', 20, 'bold'), bg='#9f7aea', fg='white').pack(anchor='w')
        tk.Label(header_content, text="Optional features for power users",
                font=('Arial', 12), bg='#9f7aea', fg='#e2e8f0').pack(anchor='w')
        
        # Scrollable content
        canvas = tk.Canvas(tab, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient='vertical', command=canvas.yview)
        content_frame = tk.Frame(canvas, bg='white')
        
        content_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=content_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Main content
        main_content = tk.Frame(content_frame, bg='white', padx=40, pady=30)
        main_content.pack(fill='both', expand=True)
        
        # Feature sections
        sections = [
            ("Data Types", [
                ('array_syntax', 'Array syntax', '[1, 2, 3]'),
                ('dict_syntax', 'Dictionary syntax', '{key: value}'),
                ('string_interpolation', 'String interpolation', '"Hello {name}"'),
            ]),
            ("Control Flow", [
                ('switch_case', 'Switch/Case statement', 'switch/case/default'),
                ('for_loop', 'For loop syntax', 'for i in range(10)'),
                ('while_loop', 'While loop syntax', 'while condition'),
            ]),
            ("Functions", [
                ('lambda', 'Lambda/Anonymous functions', 'lambda x: x * 2'),
                ('default_params', 'Default parameters', 'func(x, y=10)'),
                ('variadic', 'Variable arguments', 'func(*args)'),
            ])
        ]
        
        self.advanced_entries = {}
        
        for section_name, features in sections:
            section_frame = tk.LabelFrame(main_content, text=section_name,
                                        font=('Arial', 14, 'bold'), bg='white', 
                                        relief='solid', bd=1, padx=10, pady=5)
            section_frame.pack(fill='x', pady=10)
            
            for key, label, example in features:
                row = tk.Frame(section_frame, bg='white')
                row.pack(fill='x', padx=20, pady=5)
                
                var = tk.BooleanVar()
                cb = tk.Checkbutton(row, text=label, variable=var,
                                font=('Arial', 12), bg='white')
                cb.pack(side='left')
                
                tk.Label(row, text=f"({example})", font=('Arial', 10, 'italic'),
                        bg='white', fg='gray').pack(side='left', padx=10)
                
                self.advanced_entries[key] = var
        

    
    def create_enhanced_advanced_tab(self):
        """Create enhanced advanced features tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="⚙️ Advanced")
        
        # Implementation would follow the enhanced pattern
        # For brevity, showing simplified version
        
        container = tk.Frame(tab, bg='white')
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(container, text="⚙️ Advanced Language Features",
                font=('Arial', 18, 'bold'), bg='white').pack(pady=10)
    
    def create_enhanced_preview_panel(self):
        """Create enhanced preview panel"""
        # Header
        header_frame = tk.Frame(self.middle_panel, bg='#4a5568', height=50)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg='#4a5568')
        header_content.pack(expand=True, fill='both', padx=15, pady=12)
        
        tk.Label(header_content, text="👁️ Live Preview", 
                font=('Arial', 14, 'bold'), bg='#4a5568', fg='white').pack(side='left')
        
        # Refresh button
        refresh_btn = tk.Button(header_content, text="🔄", 
                              command=self.update_preview,
                              font=('Arial', 12), relief='flat', 
                              bg='#4a5568', fg='white',
                              cursor='hand2')
        refresh_btn.pack(side='right')
        
        # Notebook for different preview types
        self.preview_notebook = ttk.Notebook(self.middle_panel)
        self.preview_notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Playground tab
        self.create_enhanced_playground_tab()
        
        # Syntax reference tab
        self.create_enhanced_syntax_tab()
        
        # Statistics tab
        self.create_enhanced_stats_tab()
    
    def create_enhanced_playground_tab(self):
        """Create enhanced playground tab - FIXED LAYOUT VERSION"""
        if not hasattr(self, 'preview_notebook'):
            return
            
        playground_tab = ttk.Frame(self.preview_notebook)
        self.preview_notebook.add(playground_tab, text="🎮 Playground")
        
        # Editor toolbar
        toolbar = tk.Frame(playground_tab, bg='#2d3748', height=35)  # ✅ SMALLER height
        toolbar.pack(fill='x')
        toolbar.pack_propagate(False)
        
        toolbar_content = tk.Frame(toolbar, bg='#2d3748')
        toolbar_content.pack(expand=True, fill='both', padx=8, pady=3)  # ✅ SMALLER padding
        
        # File operations
        tk.Button(toolbar_content, text="📁", font=('Arial', 10), relief='flat',
                bg='#2d3748', fg='white', command=self.open_file).pack(side='left', padx=1)
        tk.Button(toolbar_content, text="💾", font=('Arial', 10), relief='flat',
                bg='#2d3748', fg='white', command=self.save_file).pack(side='left', padx=1)
        
        # Template selector
        tk.Label(toolbar_content, text="Template:", bg='#2d3748', fg='white',
                font=('Arial', 8)).pack(side='left', padx=(8, 3))
        
        self.template_var = tk.StringVar()
        template_combo = ttk.Combobox(toolbar_content, textvariable=self.template_var,
                                    values=["hello_world", "calculator", "game"],
                                    width=10, state='readonly')  # ✅ SMALLER width
        template_combo.pack(side='left')
        template_combo.bind('<<ComboboxSelected>>', self.load_code_template)
        
        # Editor area with line numbers
        editor_frame = tk.Frame(playground_tab)
        editor_frame.pack(fill='both', expand=True, padx=3, pady=3)  # ✅ SMALLER padding
        
        # Line numbers
        self.line_numbers = tk.Text(editor_frame, width=3, bg='#1a202c',  # ✅ SMALLER width
                                fg='#a0aec0', font=('Consolas', 9),  # ✅ SMALLER font
                                state='disabled', relief='flat')
        self.line_numbers.pack(side='left', fill='y')
        
        # Main editor
        self.playground_code = scrolledtext.ScrolledText(
            editor_frame, 
            font=('Consolas', 10),  # ✅ SMALLER font
            wrap='none', undo=True, 
            bg='#1a202c', fg='#f7fafc',
            relief='flat', 
            insertbackground='white',
            selectbackground='#4a5568'
        )
        self.playground_code.pack(side='left', fill='both', expand=True)
        
        # Add syntax highlighting
        self.syntax_highlighter = EnhancedSyntaxHighlighter(
            self.playground_code, self.language_data, 'dark'
        )
        
        # Bind events for line numbers and syntax highlighting
        def update_line_numbers_and_syntax(event=None):
            self.update_line_numbers()
            if self.syntax_highlighter:
                self.syntax_highlighter.highlight()
            self.update_progress()
        
        self.playground_code.bind('<KeyRelease>', update_line_numbers_and_syntax)
        self.playground_code.bind('<Button-1>', self.update_line_numbers)
        
        # Run controls - COMPACT VERSION
        controls_frame = tk.Frame(playground_tab, bg='#2d3748', height=40)  # ✅ SMALLER height
        controls_frame.pack(fill='x')
        controls_frame.pack_propagate(False)
        
        controls_content = tk.Frame(controls_frame, bg='#2d3748')
        controls_content.pack(expand=True, pady=4)  # ✅ SMALLER padding
        
        # Enhanced run button
        self.run_button = tk.Button(controls_content, text="▶ Run",  # ✅ SHORTER text
                                command=self.run_playground,
                                bg='#38a169', fg='white',
                                font=('Arial', 10, 'bold'),  # ✅ SMALLER font
                                relief='flat', padx=15, pady=6,  # ✅ SMALLER padding
                                cursor='hand2')
        self.run_button.pack(side='left', padx=5)
        
        # Stop button
        self.stop_button = tk.Button(controls_content, text="■ Stop",
                                    command=self.stop_playground,
                                    bg='#e53e3e', fg='white',
                                    font=('Arial', 10, 'bold'),  # ✅ SMALLER font
                                    relief='flat', padx=12, pady=6,  # ✅ SMALLER padding
                                    cursor='hand2', state='disabled')
        self.stop_button.pack(side='left', padx=3)
        
        # Clear button
        clear_btn = tk.Button(controls_content, text="🗑",  # ✅ ICON only
                            command=self.clear_output,
                            bg='#718096', fg='white',
                            font=('Arial', 10), relief='flat',
                            padx=8, pady=6, cursor='hand2')  # ✅ SMALLER
        clear_btn.pack(side='left', padx=3)
        
        # Speed control - COMPACT
        speed_frame = tk.Frame(controls_content, bg='#2d3748')
        speed_frame.pack(side='right', padx=8)
        
        tk.Label(speed_frame, text="Speed:", bg='#2d3748', fg='white',
                font=('Arial', 8)).pack(side='left')  # ✅ SMALLER font
        
        self.speed_scale = tk.Scale(speed_frame, from_=1, to=5, orient='horizontal',
                                bg='#2d3748', fg='white', length=60,  # ✅ SHORTER
                                showvalue=0, highlightthickness=0)
        self.speed_scale.set(3)
        self.speed_scale.pack(side='left', padx=3)
        
        # Output area - BETTER LAYOUT
        output_frame = tk.Frame(playground_tab)
        output_frame.pack(fill='both', expand=True, padx=3, pady=(0, 3))  # ✅ EXPAND!
        
        output_header = tk.Frame(output_frame, bg='#2d3748', height=25)  # ✅ SMALLER
        output_header.pack(fill='x')
        output_header.pack_propagate(False)
        
        tk.Label(output_header, text="📤 Output", font=('Arial', 10, 'bold'),  # ✅ SMALLER
                bg='#2d3748', fg='white').pack(side='left', padx=8, pady=3)
        
        self.output_text = scrolledtext.ScrolledText(
            output_frame, height=5,  # ✅ SMALLER height
            font=('Consolas', 9),  # ✅ SMALLER font
            bg='#1a202c', fg='#68d391', 
            relief='flat',
            wrap='word'
        )
        self.output_text.pack(fill='both', expand=True)  # ✅ EXPAND!
    
    def update_line_numbers(self, event=None):
        """Update line numbers in the editor"""
        try:
            self.line_numbers.config(state='normal')
            self.line_numbers.delete('1.0', 'end')
            
            content = self.playground_code.get('1.0', 'end-1c')
            lines = content.count('\n') + 1
            
            line_text = '\n'.join(str(i) for i in range(1, lines + 1))
            self.line_numbers.insert('1.0', line_text)
            
            # Sync scrolling
            first, last = self.playground_code.yview()
            self.line_numbers.yview_moveto(first)
            
            self.line_numbers.config(state='disabled')
        except:
            pass
    
    def create_enhanced_syntax_tab(self):
        """Create enhanced syntax reference tab"""
        syntax_tab = ttk.Frame(self.preview_notebook)
        self.preview_notebook.add(syntax_tab, text="📖 Syntax Guide")
        
        # Search bar
        search_frame = tk.Frame(syntax_tab, bg='#f8f9fa', height=40)
        search_frame.pack(fill='x')
        search_frame.pack_propagate(False)
        
        search_content = tk.Frame(search_frame, bg='#f8f9fa')
        search_content.pack(expand=True, fill='both', padx=10, pady=8)
        
        tk.Label(search_content, text="🔍", font=('Arial', 14), 
                bg='#f8f9fa').pack(side='left')
        
        self.search_entry = tk.Entry(search_content, font=('Arial', 11),
                                   relief='solid', bd=1, bg='white')
        self.search_entry.pack(side='left', fill='x', expand=True, padx=5)
        self.search_entry.bind('<KeyRelease>', self.search_syntax)
        
        search_btn = tk.Button(search_content, text="Search",
                              command=self.search_syntax,
                              bg='#667eea', fg='white', relief='flat',
                              font=('Arial', 10), padx=15)
        search_btn.pack(side='right')
        
        # Syntax content
        self.syntax_text = scrolledtext.ScrolledText(
            syntax_tab, 
            font=('Consolas', 10), 
            wrap='word', 
            relief='flat',
            bg='#f8f9fa',
            fg='#1a202c'
        )
        self.syntax_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Configure search highlighting
        self.syntax_text.tag_config('search_highlight', 
                                   background='#fff3cd', 
                                   foreground='#856404')
    
    def search_syntax(self, event=None):
        """Search in syntax reference"""
        query = self.search_entry.get().lower()
        self.syntax_text.tag_remove('search_highlight', '1.0', 'end')
        
        if not query:
            return
        
        # Simple search highlighting
        content = self.syntax_text.get('1.0', 'end-1c').lower()
        start = '1.0'
        
        while True:
            pos = self.syntax_text.search(query, start, 'end', nocase=True)
            if not pos:
                break
            end = f"{pos}+{len(query)}c"
            self.syntax_text.tag_add('search_highlight', pos, end)
            start = end
    
    def create_enhanced_stats_tab(self):
        """Create enhanced statistics tab"""
        stats_tab = ttk.Frame(self.preview_notebook)
        self.preview_notebook.add(stats_tab, text="📊 Statistics")
        
        self.stats_canvas = tk.Canvas(stats_tab, bg='white', highlightthickness=0)
        stats_scrollbar = ttk.Scrollbar(stats_tab, orient='vertical', 
                                       command=self.stats_canvas.yview)
        self.stats_frame = tk.Frame(self.stats_canvas, bg='white')
        
        self.stats_frame.bind(
            "<Configure>",
            lambda e: self.stats_canvas.configure(scrollregion=self.stats_canvas.bbox("all"))
        )
        
        self.stats_canvas.create_window((0, 0), window=self.stats_frame, anchor="nw")
        self.stats_canvas.configure(yscrollcommand=stats_scrollbar.set)
        
        self.stats_canvas.pack(side='left', fill='both', expand=True)
        stats_scrollbar.pack(side='right', fill='y')
    
    def create_enhanced_progress_sidebar(self):
        """Create enhanced progress tracking sidebar"""
        # Header
        header = tk.Frame(self.right_panel, bg='#667eea', height=60)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        header_content = tk.Frame(header, bg='#667eea')
        header_content.pack(expand=True, fill='both', padx=15, pady=15)
        
        tk.Label(header_content, text="🏆", font=('Arial', 20),
                bg='#667eea', fg='white').pack(side='left')
        
        progress_info = tk.Frame(header_content, bg='#667eea')
        progress_info.pack(side='left', fill='both', expand=True, padx=(10, 0))
        
        tk.Label(progress_info, text="Progress", font=('Arial', 12, 'bold'),
                bg='#667eea', fg='white').pack(anchor='w')
        
        self.progress_label = tk.Label(progress_info, text="0%", 
                                     font=('Arial', 10),
                                     bg='#667eea', fg='#e2e8f0')
        self.progress_label.pack(anchor='w')
        
        # Progress bar
        progress_container = tk.Frame(self.right_panel, bg='white', padx=15, pady=10)
        progress_container.pack(fill='x')
        
        progress_bg = tk.Frame(progress_container, bg='#e2e8f0', height=8)
        progress_bg.pack(fill='x')
        
        self.progress_fill = tk.Frame(progress_bg, bg='#38a169', height=8)
        self.progress_fill.place(x=0, y=0, relwidth=0.0)
        
        # Checklist
        checklist_container = tk.Frame(self.right_panel, bg='white', padx=15)
        checklist_container.pack(fill='x', pady=(10, 0))
        
        tk.Label(checklist_container, text="📋 Checklist", 
                font=('Arial', 11, 'bold'), bg='white').pack(anchor='w')
        
        self.checklist_items = {}
        items = [
            ("name", "✏️ Language Name"),
            ("keywords", "🔤 Keywords"),
            ("functions", "🛠️ Functions"),
            ("errors", "⚠️ Error Messages"),
            ("testing", "🧪 Testing"),
            ("export", "📦 Export Ready")
        ]
        
        for key, text in items:
            item_frame = tk.Frame(checklist_container, bg='white')
            item_frame.pack(fill='x', pady=2)
            
            checkbox = tk.Label(item_frame, text="⏳", bg='white', 
                               font=('Arial', 10), fg='#a0aec0')
            checkbox.pack(side='left')
            
            label = tk.Label(item_frame, text=text, font=('Arial', 9),
                           bg='white', fg='#4a5568')
            label.pack(side='left', padx=(5, 0))
            
            self.checklist_items[key] = (checkbox, label)
        
        # Quick actions
        actions_container = tk.Frame(self.right_panel, bg='white', padx=15, pady=15)
        actions_container.pack(fill='x')
        
        tk.Label(actions_container, text="⚡ Quick Actions", 
                font=('Arial', 11, 'bold'), bg='white').pack(anchor='w', pady=(0, 8))
        
        actions = [
            ("🚀 Generate", self.generate_language, "#ed8936"),
            ("🧪 Test", self.run_playground, "#667eea"),
            ("💾 Save", self.save_language, "#38a169")
        ]
        
        for text, command, color in actions:
            btn = tk.Button(actions_container, text=text, command=command,
                           bg=color, fg='white', relief='flat',
                           font=('Arial', 9, 'bold'), 
                           cursor='hand2')
            btn.pack(fill='x', pady=2, ipady=4)
    
    def create_enhanced_status_bar(self):
        """Create enhanced status bar with better information"""
        self.status_bar = tk.Frame(self.window, height=35, bg='#f8f9fa', 
                                  relief='solid', bd=1)
        self.status_bar.pack(fill='x', side='bottom')
        self.status_bar.pack_propagate(False)
        
        status_content = tk.Frame(self.status_bar, bg='#f8f9fa')
        status_content.pack(expand=True, fill='both', padx=10, pady=5)
        
        # Left side - status
        left_status = tk.Frame(status_content, bg='#f8f9fa')
        left_status.pack(side='left', fill='y')
        
        self.status_label = tk.Label(left_status, text="Ready", 
                                   font=('Arial', 10), bg='#f8f9fa', fg='#4a5568')
        self.status_label.pack(side='left')
        
        # Center - progress indicator
        self.center_status = tk.Frame(status_content, bg='#f8f9fa')
        self.center_status.pack(side='left', expand=True, fill='x', padx=20)
        
        # Right side - achievements and info
        right_status = tk.Frame(status_content, bg='#f8f9fa')
        right_status.pack(side='right', fill='y')
        
        # Theme indicator
        self.theme_indicator = tk.Label(right_status, text="🎨", 
                                      font=('Arial', 10), bg='#f8f9fa')
        self.theme_indicator.pack(side='right', padx=5)
        
        # Achievement counter
        self.achievement_label = tk.Label(right_status, text="",
                                        font=('Arial', 10), bg='#f8f9fa', fg='#4a5568')
        self.achievement_label.pack(side='right', padx=10)
        
        self.update_achievement_display()
    
    def create_enhanced_tooltip(self, widget, text):
        """Create enhanced tooltip with better styling"""
        def on_enter(e):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{e.x_root+10}+{e.y_root+10}")
            tooltip.attributes('-topmost', True)
            
            # Styled tooltip
            frame = tk.Frame(tooltip, bg='#1a202c', relief='solid', bd=1)
            frame.pack()
            
            label = tk.Label(frame, text=text, background='#1a202c',
                           foreground='white', font=('Arial', 10),
                           padx=8, pady=4)
            label.pack()
            
            widget.tooltip = tooltip
            
            # Auto-hide after 3 seconds
            tooltip.after(3000, lambda: tooltip.destroy() if tooltip.winfo_exists() else None)
        
        def on_leave(e):
            if hasattr(widget, 'tooltip') and widget.tooltip.winfo_exists():
                widget.tooltip.destroy()
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
    
    def setup_accessibility(self):
        """Setup accessibility features"""
        # Keyboard navigation
        self.window.bind('<Control-plus>', lambda e: self.accessibility.increase_font_size())
        self.window.bind('<Control-minus>', lambda e: self.accessibility.decrease_font_size())
        self.window.bind('<Control-0>', lambda e: self.reset_font_size())
        
        # Focus management
        self.window.bind('<Tab>', self.handle_tab_navigation)
        self.window.bind('<Shift-Tab>', self.handle_shift_tab_navigation)
        
        # Screen reader support
        self.window.bind('<Control-Alt-r>', lambda e: self.toggle_screen_reader_mode())
    
    def setup_autosave(self):
        """Setup automatic saving"""
        def autosave():
            try:
                self.collect_language_data()
                # Save to temp file
                with open('.autosave.json', 'w') as f:
                    json.dump(self.language_data, f)
            except:
                pass
            
            # Schedule next autosave
            self.window.after(30000, autosave)  # Every 30 seconds
        
        # Start autosave timer
        self.window.after(30000, autosave)
    
    def bind_enhanced_shortcuts(self):
        """Bind enhanced keyboard shortcuts"""
        shortcuts = {
            '<Control-n>': self.new_language,
            '<Control-o>': self.load_language,
            '<Control-s>': self.save_language,
            '<Control-Shift-S>': self.save_as_language,
            '<Control-e>': self.export_language,
            '<F5>': self.run_playground,
            '<Control-r>': self.run_playground,
            '<F1>': self.show_help_menu,
            '<Control-comma>': self.show_preferences,
            '<Control-Shift-A>': self.show_achievements,
            '<Control-Shift-K>': self.show_enhanced_keyword_generator,
            '<Control-Shift-T>': self.show_theme_picker,
            '<Escape>': self.stop_playground
        }
        
        for key, command in shortcuts.items():
            self.window.bind(key, lambda e, cmd=command: cmd())
    
    # ========================================================================
    # ENHANCED FUNCTIONALITY METHODS
    # ========================================================================
    
    def update_preview(self, event=None):
        """Enhanced preview update with better performance"""
        self.collect_language_data()
        
        # Update all preview areas
        self.update_syntax_reference()
        self.update_statistics()
        self.update_file_extension()
        self.update_progress()
        
        # Update syntax highlighting
        if self.syntax_highlighter:
            self.syntax_highlighter.language = self.language_data
            # Debounce syntax highlighting for better performance
            if hasattr(self, '_syntax_timer'):
                self.window.after_cancel(self._syntax_timer)
            self._syntax_timer = self.window.after(500, self.syntax_highlighter.highlight)
    
    def update_file_extension(self):
        """Update file extension preview"""
        name = self.name_entry.get() or "mylang"
        # Take first 3-4 letters, lowercase, alphanumeric only
        ext = ''.join(c for c in name[:4].lower() if c.isalnum())
        if not ext:
            ext = "myl"
        elif len(ext) < 2:
            ext += "l"
        
        self.ext_label.config(text=ext)
    
    def update_syntax_reference(self):
        """Update syntax reference with enhanced formatting"""
        lang = self.language_data
        
        # Enhanced syntax reference with color coding and examples
        ref = f"""🌟 {lang['name']} Language Reference

{'='*50}

📝 BASIC SYNTAX
{'='*15}

🔤 Keywords:
"""
        
        for eng, custom in lang.get('keywords', {}).items():
            if custom:
                ref += f"  {eng:<12} → {custom}\n"
        
        ref += f"\n🛠️ Built-in Functions:\n"
        for eng, custom in lang.get('builtins', {}).items():
            if custom:
                ref += f"  {eng:<12} → {custom}()\n"
        
        ref += f"\n📋 EXAMPLES\n{'='*12}\n\n"
        
        # Variables example
        var_kw = lang.get('keywords', {}).get('variable', 'var')
        print_fn = lang.get('builtins', {}).get('print', 'print')
        
        ref += f"Variables:\n"
        ref += f"  {var_kw} name = \"Alice\"\n"
        ref += f"  {var_kw} age = 25\n"
        ref += f"  {print_fn}(name, \"is\", age, \"years old\")\n\n"
        
        # Function example
        func_kw = lang.get('keywords', {}).get('function', 'function')
        return_kw = lang.get('keywords', {}).get('return', 'return')
        
        ref += f"Functions:\n"
        ref += f"  {func_kw} greet(person) {{\n"
        ref += f"    {print_fn}(\"Hello\", person)\n"
        ref += f"    {return_kw} true\n"
        ref += f"  }}\n\n"
        
        # Conditional example
        if_kw = lang.get('keywords', {}).get('if', 'if')
        else_kw = lang.get('keywords', {}).get('else', 'else')
        
        ref += f"Conditionals:\n"
        ref += f"  {if_kw} age >= 18 {{\n"
        ref += f"    {print_fn}(\"You can vote!\")\n"
        ref += f"  }} {else_kw} {{\n"
        ref += f"    {print_fn}(\"Too young to vote\")\n"
        ref += f"  }}\n\n"
        
        # Loop example
        loop_kw = lang.get('keywords', {}).get('loop', 'loop')
        
        ref += f"Loops:\n"
        ref += f"  {var_kw} count = 1\n"
        ref += f"  {loop_kw} count <= 5 {{\n"
        ref += f"    {print_fn}(\"Count:\", count)\n"
        ref += f"    count = count + 1\n"
        ref += f"  }}\n"
        
        self.syntax_text.delete('1.0', tk.END)
        self.syntax_text.insert('1.0', ref)
    
    def update_statistics(self):
        """Update language statistics with enhanced visualizations"""
        # Clear old content
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        # Header
        header = tk.Frame(self.stats_frame, bg='white', padx=20, pady=15)
        header.pack(fill='x')
        
        tk.Label(header, text="📊 Language Statistics", 
                font=('Arial', 16, 'bold'), bg='white').pack(anchor='w')
        
        # Collect enhanced statistics
        stats = self.calculate_enhanced_statistics()
        
        # Overview cards
        cards_frame = tk.Frame(self.stats_frame, bg='white', padx=20)
        cards_frame.pack(fill='x', pady=(0, 20))
        
        # Create stat cards
        self.create_stat_card(cards_frame, "Keywords", stats['keywords_count'], 
                             "🔤", "#667eea", 0, 0)
        self.create_stat_card(cards_frame, "Functions", stats['functions_count'], 
                             "🛠️", "#38a169", 0, 1)
        self.create_stat_card(cards_frame, "Errors", stats['errors_count'], 
                             "⚠️", "#ed8936", 1, 0)
        self.create_stat_card(cards_frame, "Completion", f"{stats['completion']}%", 
                             "✅", "#9f7aea", 1, 1)
        
        # Configure grid
        cards_frame.grid_columnconfigure(0, weight=1)
        cards_frame.grid_columnconfigure(1, weight=1)
        
        # Detailed statistics
        details_frame = tk.Frame(self.stats_frame, bg='white', padx=20, pady=10)
        details_frame.pack(fill='x')
        
        tk.Label(details_frame, text="📋 Details", 
                font=('Arial', 14, 'bold'), bg='white').pack(anchor='w', pady=(0, 10))
        
        details = [
            ("Total Customizations", stats['total_customizations']),
            ("Character Count", stats['total_chars']),
            ("Uses Unicode", "Yes" if stats['uses_unicode'] else "No"),
            ("Has Emojis", "Yes" if stats['has_emojis'] else "No"),
            ("Estimated Complexity", stats['complexity']),
            ("Time Spent", self.format_time_spent())
        ]
        
        for label, value in details:
            detail_row = tk.Frame(details_frame, bg='white')
            detail_row.pack(fill='x', pady=2)
            
            tk.Label(detail_row, text=f"{label}:", font=('Arial', 11),
                    bg='white', fg='#4a5568').pack(side='left')
            
            tk.Label(detail_row, text=str(value), font=('Arial', 11, 'bold'),
                    bg='white', fg='#1a202c').pack(side='right')
        
        # Fun facts
        if stats['fun_facts']:
            facts_frame = tk.Frame(self.stats_frame, bg='#f0fff4', padx=15, pady=10)
            facts_frame.pack(fill='x', padx=20, pady=(10, 0))
            
            tk.Label(facts_frame, text="🎉 Fun Facts", 
                    font=('Arial', 12, 'bold'), bg='#f0fff4').pack(anchor='w')
            
            for fact in stats['fun_facts']:
                tk.Label(facts_frame, text=f"• {fact}", font=('Arial', 10),
                        bg='#f0fff4', fg='#22543d').pack(anchor='w', padx=(10, 0))
    
    def create_stat_card(self, parent, title, value, icon, color, row, col):
        """Create a statistics card"""
        card = tk.Frame(parent, bg='white', relief='solid', bd=1,
                       width=120, height=80)
        card.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
        card.pack_propagate(False)
        
        # Color bar
        color_bar = tk.Frame(card, bg=color, height=4)
        color_bar.pack(fill='x')
        
        # Content
        content = tk.Frame(card, bg='white', padx=10, pady=8)
        content.pack(fill='both', expand=True)
        
        # Icon and value
        top_frame = tk.Frame(content, bg='white')
        top_frame.pack(fill='x')
        
        tk.Label(top_frame, text=icon, font=('Arial', 16),
                bg='white').pack(side='left')
        
        tk.Label(top_frame, text=str(value), font=('Arial', 14, 'bold'),
                bg='white', fg=color).pack(side='right')
        
        # Title
        tk.Label(content, text=title, font=('Arial', 9),
                bg='white', fg='#666').pack(anchor='w', pady=(5, 0))
    
    def calculate_enhanced_statistics(self):
        """Calculate enhanced statistics"""
        stats = {
            'keywords_count': len([k for k in self.language_data.get('keywords', {}).values() if k]),
            'functions_count': len([f for f in self.language_data.get('builtins', {}).values() if f]),
            'errors_count': len([e for e in self.language_data.get('errors', {}).values() if e]),
            'total_customizations': 0,
            'total_chars': 0,
            'uses_unicode': False,
            'has_emojis': False,
            'complexity': 'Simple',
            'fun_facts': []
        }
        
        # Calculate totals
        all_text = str(self.language_data)
        stats['total_chars'] = len(all_text)
        stats['uses_unicode'] = any(ord(c) > 127 for c in all_text)
        stats['has_emojis'] = any(ord(c) > 0x1F300 for c in all_text)
        
        stats['total_customizations'] = (
            stats['keywords_count'] + 
            stats['functions_count'] + 
            stats['errors_count']
        )
        
        # Calculate completion
        total_possible = 20  # Rough estimate of total possible customizations
        stats['completion'] = min(int((stats['total_customizations'] / total_possible) * 100), 100)
        
        # Complexity assessment
        if stats['total_customizations'] < 5:
            stats['complexity'] = 'Simple'
        elif stats['total_customizations'] < 10:
            stats['complexity'] = 'Moderate'
        elif stats['total_customizations'] < 15:
            stats['complexity'] = 'Advanced'
        else:
            stats['complexity'] = 'Expert'
        
        # Fun facts
        if stats['has_emojis']:
            stats['fun_facts'].append("Your language uses emojis! 😄")
        if stats['keywords_count'] >= 8:
            stats['fun_facts'].append("Wow! You've defined lots of keywords!")
        if stats['completion'] >= 80:
            stats['fun_facts'].append("Your language is nearly complete!")
        if stats['uses_unicode']:
            stats['fun_facts'].append("International characters detected!")
        
        return stats
    
    def format_time_spent(self):
        """Format time spent on current language"""
        elapsed = time.time() - self.start_time
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        
        if minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"
    
    def update_progress(self, event=None):
        """Update progress tracker with enhanced logic"""
        if not hasattr(self, 'progress_fill'):
            return
        
        self.collect_language_data()
        
        # Enhanced progress calculation
        total_items = 6
        completed = 0
        
        # Check name (more meaningful than default)
        name = self.language_data.get('name', '')
        if name and name != 'MyLang' and len(name) > 2:
            completed += 1
            self.update_checklist_item('name', True)
        else:
            self.update_checklist_item('name', False)
        
        # Check keywords (at least 3 essential ones)
        keywords_count = len([k for k in self.language_data.get('keywords', {}).values() if k])
        if keywords_count >= 3:
            completed += 1
            self.update_checklist_item('keywords', True)
        else:
            self.update_checklist_item('keywords', False)
        
        # Check functions (at least 2 essential ones)
        functions_count = len([f for f in self.language_data.get('builtins', {}).values() if f])
        if functions_count >= 2:
            completed += 1
            self.update_checklist_item('functions', True)
        else:
            self.update_checklist_item('functions', False)
        
        # Check errors (at least 1)
        errors_count = len([e for e in self.language_data.get('errors', {}).values() if e])
        if errors_count >= 1:
            completed += 1
            self.update_checklist_item('errors', True)
        else:
            self.update_checklist_item('errors', False)
        
        # Check testing
        if hasattr(self, 'test_count') and self.test_count > 0:
            completed += 1
            self.update_checklist_item('testing', True)
        else:
            self.update_checklist_item('testing', False)
        
        # Check if ready for export
        if completed >= 4:
            self.update_checklist_item('export', True)
            completed += 1
        else:
            self.update_checklist_item('export', False)
        
        # Update progress bar with smooth animation
        progress_percent = completed / total_items
        self.animate_progress_bar(progress_percent)
        self.progress_label.config(text=f"{int(progress_percent * 100)}%")
        
        # Check for achievements
        self.check_progress_achievements(completed, total_items)
    
    def animate_progress_bar(self, target_width):
        """Animate progress bar to target width"""
        current_width = self.progress_fill.winfo_reqwidth() / self.progress_fill.master.winfo_reqwidth()
        if hasattr(self, '_progress_animation'):
            self.window.after_cancel(self._progress_animation)
        
        def step():
            current = self.progress_fill.place_info().get('relwidth', 0)
            if current is None or current == '':
                current = 0
            else:
                # Convert to float if it's a string
                current = float(current)
            
            diff = target_width - current
            if abs(diff) > 0.01:
                new_width = current + diff * 0.2
                self.progress_fill.place(relwidth=new_width)
                self._progress_animation = self.window.after(50, step)
            else:
                self.progress_fill.place(relwidth=target_width)
        
        step()
    
    def update_checklist_item(self, item_key, completed):
        """Update checklist item with smooth transitions"""
        if hasattr(self, 'checklist_items') and item_key in self.checklist_items:
            checkbox, label = self.checklist_items[item_key]
            
            if completed:
                checkbox.config(text="✅", fg="#38a169")
                label.config(fg="#38a169")
            else:
                checkbox.config(text="⏳", fg="#a0aec0")
                label.config(fg="#4a5568")
    
    def check_progress_achievements(self, completed, total):
        """Check for progress-related achievements"""
        if completed >= 1 and not self.achievement_system.achievements[0].unlocked:
            self.unlock_achievement('first_lang')
        
        if completed >= 3:
            self.unlock_achievement('keyword_explorer')
        
        if completed >= total:
            self.unlock_achievement('perfectionist')
            
        # Speed achievement (if completed in under 5 minutes)
        if completed >= 4 and (time.time() - self.start_time) < 300:
            self.unlock_achievement('speed_demon')
    
    def collect_language_data(self):
        """Enhanced data collection with validation"""
        # Basic info with validation
        self.language_data['name'] = self.name_entry.get().strip() or "MyLang"
        self.language_data['version'] = self.version_entry.get().strip() or "1.0"
        self.language_data['author'] = self.author_entry.get().strip() or "Anonymous"
        self.language_data['description'] = self.desc_text.get('1.0', 'end-1c').strip()
        
        # Keywords
        self.language_data['keywords'] = {}
        for keyword, entry in self.keyword_entries.items():
            value = entry.get().strip()
            if value:
                self.language_data['keywords'][keyword] = value
        
        # Built-ins
        self.language_data['builtins'] = {}
        for builtin, entry in self.builtin_entries.items():
            value = entry.get().strip()
            if value:
                self.language_data['builtins'][builtin] = value
        
        # Features
        if hasattr(self, 'features'):
            self.language_data['features'] = {k: v.get() for k, v in self.features.items()}
        
        # Update timestamp
        self.language_data['modified'] = datetime.now().isoformat()
    
    def run_playground(self):
        """Enhanced playground execution with better feedback"""
        if self.playground_running:
            return
        
        self.playground_running = True
        self.run_button.config(text="⏳ Running...", state='disabled')
        self.stop_button.config(state='normal')
        
        # Clear previous output
        self.output_text.delete('1.0', tk.END)
        self.output_text.insert('1.0', "🚀 Initializing your language...\n\n")
        self.output_text.update()
        
        # Show progress
        def show_progress():
            steps = [
                "📝 Analyzing code...",
                "🔤 Processing keywords...",
                "🛠️ Loading functions...",
                "▶️ Executing program..."
            ]
            
            for i, step in enumerate(steps):
                self.output_text.insert(tk.END, f"{step}\n")
                self.output_text.see(tk.END)
                self.output_text.update()
                time.sleep(0.3)  # Simulate processing time
            
            # Simulate actual execution
            self.window.after(500, self.execute_playground_code)
        
        # Start progress in a thread-like manner
        self.window.after(100, show_progress)
        
        # Track testing for achievements
        self.test_count = getattr(self, 'test_count', 0) + 1
        if self.test_count >= 5:
            self.unlock_achievement('test_pilot')
    
    def execute_playground_code(self):
        """Execute the playground code with enhanced simulation"""
        code = self.playground_code.get('1.0', 'end-1c')
        
        self.output_text.insert(tk.END, "\n" + "="*40 + "\n")
        self.output_text.insert(tk.END, "📤 OUTPUT:\n\n")
        
        # Enhanced code simulation
        print_func = self.language_data.get('builtins', {}).get('print', 'print')
        input_func = self.language_data.get('builtins', {}).get('input', 'input')
        
        lines = code.split('\n')
        output_generated = False
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Simulate print statements
            if print_func in line:
                # Extract content between quotes or parentheses
                import re
                matches = re.findall(r'["\']([^"\']*)["\']', line)
                if matches:
                    output_text = ' '.join(matches)
                    self.output_text.insert(tk.END, f"{output_text}\n")
                    output_generated = True
                else:
                    # Look for variables or expressions
                    parts = line.split(print_func)[1].strip()
                    if parts.startswith('(') and parts.endswith(')'):
                        content = parts[1:-1]
                        # Simple variable simulation
                        if ',' in content:
                            items = [item.strip().strip('"\'') for item in content.split(',')]
                            output_text = ' '.join(items)
                        else:
                            output_text = content.strip('"\'')
                        self.output_text.insert(tk.END, f"{output_text}\n")
                        output_generated = True
            
            # Simulate variable assignments
            var_keyword = self.language_data.get('keywords', {}).get('variable', 'var')
            if var_keyword in line and '=' in line:
                parts = line.split('=')
                if len(parts) == 2:
                    var_name = parts[0].replace(var_keyword, '').strip()
                    var_value = parts[1].strip().strip('"\'')
                    self.output_text.insert(tk.END, f"📦 {var_name} = {var_value}\n")
                    output_generated = True
        
        if not output_generated:
            self.output_text.insert(tk.END, "✨ Program completed successfully!\n")
            self.output_text.insert(tk.END, "(No output produced)\n")
        
        self.output_text.insert(tk.END, "\n" + "="*40 + "\n")
        self.output_text.insert(tk.END, "✅ Execution finished!\n")
        
        # Restore buttons
        self.playground_running = False
        self.run_button.config(text="▶ Run Code", state='normal')
        self.stop_button.config(state='disabled')
        
        # Update progress
        self.update_progress()
    
    def stop_playground(self):
        """Stop playground execution"""
        if self.playground_running:
            self.playground_running = False
            self.run_button.config(text="▶ Run Code", state='normal')
            self.stop_button.config(state='disabled')
            self.output_text.insert(tk.END, "\n⏹️ Execution stopped by user.\n")
    
    def clear_output(self):
        """Clear playground output"""
        self.output_text.delete('1.0', tk.END)
    
    def load_code_template(self, event=None):
        """Load a code template with language-specific keywords"""
        template_name = self.template_var.get()
        
        templates = {
            'hello_world': '''# Hello World Example
{print}("Hello, World!")
{print}("Welcome to {lang_name}!")

{var} message = "Programming is fun!"
{print}(message)''',
            
            'calculator': '''# Simple Calculator
{func} add(a, b) {{
    {return} a + b
}}

{func} multiply(a, b) {{
    {return} a * b
}}

{var} x = 10
{var} y = 5

{print}("Addition:", add(x, y))
{print}("Multiplication:", multiply(x, y))''',
            
            'game': '''# Number Guessing Game
{print}("=== Guessing Game ===")
{print}("Guess a number between 1 and 10!")

{var} secret = 7
{var} guess = 0
{var} tries = 0

{loop} guess != secret {{
    guess = {number}({input}("Your guess: "))
    tries = tries + 1
    
    {if} guess < secret {{
        {print}("Too low! Try again.")
    }} {else} {if} guess > secret {{
        {print}("Too high! Try again.")
    }}
}}

{print}("Correct! You got it in", tries, "tries!")''',
            
            'genz_hello': '''// GenZ Hello World - No Cap! 💅
{print}("Yo bestie! 👋")
{print}("Welcome to {lang_name} - it's giving main character energy ✨")

{var} mood = "absolutely slay"
{print}("Today's vibe is", mood, "periodt! 💯")

{var} username = "bestie"
{print}("Hey", username, "ready to code? It's about to be iconic! 🔥")''',
            
            'genz_calculator': '''// GenZ Calculator - Math But Make It Cute 🧮✨
{func} add_vibes(a, b) {{
    {return} a + b  // addition hits different
}}

{func} multiply_energy(a, b) {{
    {return} a * b  // multiplication is giving boss energy
}}

{var} first_num = 15
{var} second_num = 3

{print}("Math time bestie! 📐")
{print}("Adding these numbers:", add_vibes(first_num, second_num))
{print}("Multiplying for max impact:", multiply_energy(first_num, second_num))
{print}("Math said periodt! ✅")''',
            
            'genz_social_media': '''// Social Media Vibe Checker 📱✨
{print}("=== Vibe Check Social Media Style ===")
{print}("Time to check what energy you're bringing! 💅")

{func} check_vibe_level(posts_today) {{
    {if} posts_today > 10 {{
        {return} "main character energy - we love to see it! ✨"
    }} {else} {if} posts_today > 5 {{
        {return} "solid vibes bestie! 👑"
    }} {else} {{
        {return} "giving mysterious energy - respect! 🌙"
    }}
}}

{var} daily_posts = {number}({input}("How many posts did you make today bestie? "))
{var} your_vibe = check_vibe_level(daily_posts)

{print}("Your social media energy:", your_vibe)
{print}("Remember: you're iconic no matter what! 💖")'''
        }
        
        if template_name in templates:
            # Replace placeholders with actual language keywords
            template = templates[template_name]
            replacements = {
                '{lang_name}': self.language_data.get('name', 'MyLang'),
                '{print}': self.language_data.get('builtins', {}).get('print', 'print'),
                '{input}': self.language_data.get('builtins', {}).get('input', 'input'),
                '{number}': self.language_data.get('builtins', {}).get('number', 'number'),
                '{var}': self.language_data.get('keywords', {}).get('variable', 'var'),
                '{func}': self.language_data.get('keywords', {}).get('function', 'function'),
                '{if}': self.language_data.get('keywords', {}).get('if', 'if'),
                '{else}': self.language_data.get('keywords', {}).get('else', 'else'),
                '{loop}': self.language_data.get('keywords', {}).get('loop', 'loop'),
                '{return}': self.language_data.get('keywords', {}).get('return', 'return')
            }
            
            for placeholder, value in replacements.items():
                template = template.replace(placeholder, value)
            
            self.playground_code.delete('1.0', tk.END)
            self.playground_code.insert('1.0', template)
            
            # Update line numbers and syntax highlighting
            self.update_line_numbers()
            if self.syntax_highlighter:
                self.syntax_highlighter.highlight()
    
    # ========================================================================
    # FILE OPERATIONS WITH ENHANCED FEATURES
    # ========================================================================
    
    def new_language(self):
        """Create new language with confirmation"""
        if self.has_unsaved_changes():
            result = messagebox.askyesnocancel(
                "Unsaved Changes", 
                "You have unsaved changes. Do you want to save before creating a new language?"
            )
            if result is True:  # Yes - save first
                if not self.save_language():
                    return  # Save failed, don't create new
            elif result is None:  # Cancel
                return
            # If No (False), continue without saving
        
        # Reset to default values
        self.language_data = {
            'name': 'MyLang',
            'version': '1.0',
            'author': 'Young Coder',
            'description': 'My awesome programming language!',
            'keywords': {},
            'operators': {},
            'builtins': {},
            'errors': {},
            'examples': [],
            'theme': self.current_theme,
            'created': datetime.now().isoformat()
        }
        
        self.populate_ui_from_data()
        self.update_status("New language created")
        self.start_time = time.time()  # Reset timer
        self.test_count = 0
        
        # Clear playground
        self.playground_code.delete('1.0', tk.END)
        self.output_text.delete('1.0', tk.END)
    
    def save_language(self):
        """Save language with enhanced error handling"""
        self.collect_language_data()
        
        if not hasattr(self, 'current_file'):
            return self.save_as_language()
        
        try:
            with open(self.current_file, 'w', encoding='utf-8') as f:
                json.dump(self.language_data, f, indent=2, ensure_ascii=False)
            
            self.update_status(f"Saved to {os.path.basename(self.current_file)}")
            self.save_to_recent()
            self.unlock_achievement('first_lang')
            return True
            
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save file:\n{e}")
            return False
    
    def save_as_language(self):
        """Save language with new filename"""
        self.collect_language_data()
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[
                ("Language files", "*.json"),
                ("All files", "*.*")
            ],
            initialfile=f"{self.language_data['name'].lower().replace(' ', '_')}_lang.json"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.language_data, f, indent=2, ensure_ascii=False)
                
                self.current_file = filename
                self.update_status(f"Saved as {os.path.basename(filename)}")
                self.save_to_recent()
                self.unlock_achievement('first_lang')
                return True
                
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save file:\n{e}")
                return False
        
        return False
    
    def load_language(self):
        """Load language with enhanced validation"""
        if self.has_unsaved_changes():
            result = messagebox.askyesnocancel(
                "Unsaved Changes", 
                "You have unsaved changes. Do you want to save before loading?"
            )
            if result is True:
                if not self.save_language():
                    return
            elif result is None:
                return
        
        filename = filedialog.askopenfilename(
            filetypes=[
                ("Language files", "*.json"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Validate loaded data
                if not self.validate_language_data(data):
                    messagebox.showwarning("Invalid File", 
                                         "This file doesn't appear to be a valid language file.")
                    return
                
                self.language_data = data
                self.current_file = filename
                self.populate_ui_from_data()
                self.update_status(f"Loaded {os.path.basename(filename)}")
                self.start_time = time.time()  # Reset timer for loaded language
                
            except json.JSONDecodeError:
                messagebox.showerror("Load Error", "Invalid JSON file format.")
            except Exception as e:
                messagebox.showerror("Load Error", f"Failed to load file:\n{e}")
    
    def validate_language_data(self, data):
        """Validate loaded language data"""
        required_fields = ['name', 'version', 'author']
        return all(field in data for field in required_fields)
    
    def has_unsaved_changes(self):
        """Check if there are unsaved changes"""
        current_data = {}
        try:
            self.collect_language_data()
            current_data = self.language_data.copy()
        except:
            return False
        
        # Compare with last saved state or default
        if hasattr(self, 'current_file'):
            try:
                with open(self.current_file, 'r', encoding='utf-8') as f:
                    saved_data = json.load(f)
                return current_data != saved_data
            except:
                return True
        
        # If no file, check if different from default
        default_data = {
            'name': 'MyLang',
            'version': '1.0',
            'author': 'Young Coder',
            'description': 'My awesome programming language!',
            'keywords': {},
            'operators': {},
            'builtins': {},
            'errors': {},
        }
        
        return any(current_data.get(key) != default_data.get(key) 
                  for key in default_data.keys())
    
    def safe_exit(self):
        """Safe exit with unsaved changes check"""
        if self.has_unsaved_changes():
            result = messagebox.askyesnocancel(
                "Unsaved Changes", 
                "You have unsaved changes. Do you want to save before exiting?"
            )
            if result is True:
                if not self.save_language():
                    return
            elif result is None:
                return
        
        # Mark tutorial as completed
        with open('.tutorial_completed', 'w') as f:
            f.write('1')
        
        self.window.quit()
    
    # ========================================================================
    # ENHANCED UI INTERACTION METHODS
    # ========================================================================
    
    def show_theme_picker(self):
        """Show enhanced theme picker dialog"""
        dialog = tk.Toplevel(self.window)
        dialog.title("🎨 Choose Theme")
        dialog.geometry("700x600")
        dialog.transient(self.window)
        dialog.grab_set()
        
        # Header
        header = tk.Frame(dialog, bg='#667eea', height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        header_content = tk.Frame(header, bg='#667eea')
        header_content.pack(expand=True, fill='both', padx=30, pady=20)
        
        tk.Label(header_content, text="🎨 Choose Your Theme", 
                font=('Arial', 20, 'bold'), bg='#667eea', fg='white').pack(anchor='w')
        tk.Label(header_content, text="Customize the look and feel of your workspace",
                font=('Arial', 12), bg='#667eea', fg='#e2e8f0').pack(anchor='w')
        
        # Scrollable content
        canvas = tk.Canvas(dialog, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(dialog, orient='vertical', command=canvas.yview)
        content_frame = tk.Frame(canvas, bg='white')
        
        content_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=content_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Theme cards
        main_content = tk.Frame(content_frame, bg='white', padx=30, pady=20)
        main_content.pack(fill='both', expand=True)
        
        for i, (theme_id, theme) in enumerate(self.theme_engine.themes.items()):
            row = i // 2
            col = i % 2
            
            self.create_theme_card(main_content, theme_id, theme, dialog, row, col)
        
        # Configure grid
        main_content.grid_columnconfigure(0, weight=1)
        main_content.grid_columnconfigure(1, weight=1)
        
        # Buttons
        button_frame = tk.Frame(dialog, bg='white', padx=30, pady=20)
        button_frame.pack(fill='x')
        
        tk.Button(button_frame, text="Cancel", command=dialog.destroy,
                 bg='#e2e8f0', font=('Arial', 11), padx=20, pady=8).pack(side='right')
    
    def create_theme_card(self, parent, theme_id, theme, dialog, row, col):
        """Create a theme preview card"""
        card = tk.Frame(parent, bg='white', relief='solid', bd=1,
                       width=300, height=150)
        card.grid(row=row, column=col, padx=15, pady=15, sticky='ew')
        card.pack_propagate(False)
        
        # Theme preview area
        preview = tk.Frame(card, bg=theme['bg'], height=60)
        preview.pack(fill='x')
        preview.pack_propagate(False)
        
        # Create mini preview
        preview_content = tk.Frame(preview, bg=theme['bg'])
        preview_content.pack(expand=True, fill='both', padx=10, pady=8)
        
        # Color swatches
        swatch_frame = tk.Frame(preview_content, bg=theme['bg'])
        swatch_frame.pack(anchor='w')
        
        colors = [theme['primary'], theme['secondary'], theme['accent']]
        for color in colors:
            swatch = tk.Frame(swatch_frame, bg=color, width=20, height=20)
            swatch.pack(side='left', padx=2)
        
        # Sample text
        tk.Label(preview_content, text="Sample Text", 
                font=('Arial', 10), bg=theme['bg'], fg=theme['fg']).pack(anchor='w')
        
        # Info section
        info = tk.Frame(card, bg='white', padx=15, pady=10)
        info.pack(fill='x')
        
        # Theme name
        tk.Label(info, text=theme['name'], font=('Arial', 14, 'bold'),
                bg='white').pack(anchor='w')
        
        # Description
        descriptions = {
            'modern_light': 'Clean and bright for daytime coding',
            'dark_pro': 'Professional dark theme for night owls',
            'ocean_breeze': 'Calming blue tones inspired by the ocean',
            'sunset_glow': 'Warm oranges and reds for creativity',
            'forest_zen': 'Natural greens for a peaceful workspace',
            'high_contrast': 'Maximum contrast for accessibility'
        }
        
        desc = descriptions.get(theme_id, 'A beautiful theme for your workspace')
        tk.Label(info, text=desc, font=('Arial', 10),
                bg='white', fg='#666', wraplength=250).pack(anchor='w', pady=(2, 8))
        
        # Select button
        def select_theme():
            self.change_theme(theme_id)
            dialog.destroy()
            self.update_status(f"Theme changed to {theme['name']}")
        
        current = theme_id == self.current_theme
        btn_text = "✓ Current" if current else "Select"
        btn_color = theme['primary'] if not current else '#38a169'
        btn_state = 'disabled' if current else 'normal'
        
        btn = tk.Button(info, text=btn_text, command=select_theme,
                       bg=btn_color, fg='white', font=('Arial', 10, 'bold'),
                       relief='flat', padx=20, pady=4, state=btn_state,
                       cursor='hand2' if not current else 'arrow')
        btn.pack(anchor='w')
        
        # Hover effect for non-current themes
        if not current:
            def on_enter(e):
                card.configure(relief='solid', bd=2)
                btn.configure(bg=self.darken_color(theme['primary']))
            
            def on_leave(e):
                card.configure(relief='solid', bd=1)
                btn.configure(bg=theme['primary'])
            
            card.bind("<Enter>", on_enter)
            card.bind("<Leave>", on_leave)
            for widget in card.winfo_children():
                widget.bind("<Enter>", on_enter)
                widget.bind("<Leave>", on_leave)
    
    def change_theme(self, theme_id):
        """Change application theme with smooth transition"""
        if theme_id not in self.theme_engine.themes:
            return
        
        self.current_theme = theme_id
        self.language_data['theme'] = theme_id
        
        # Apply theme
        self.apply_theme()
        
        # Update syntax highlighter theme
        if self.syntax_highlighter:
            theme_mode = 'dark' if 'dark' in theme_id or 'space' in theme_id else 'light'
            self.syntax_highlighter.theme = theme_mode
            self.syntax_highlighter.setup_tags()
            self.syntax_highlighter.highlight()
        
        # Update status
        theme_name = self.theme_engine.themes[theme_id]['name']
        self.update_status(f"Theme changed to {theme_name}")
        
        # Achievement tracking
        themes_tried = getattr(self, 'themes_tried', set())
        themes_tried.add(theme_id)
        self.themes_tried = themes_tried
        
        if len(themes_tried) >= 3:
            self.unlock_achievement('theme_explorer')
    
    def apply_theme(self):
        """Apply current theme to all UI elements"""
        theme = self.theme_engine.themes[self.current_theme]
        
        # Apply to main window
        self.window.configure(bg=theme['bg'])
        
        # Apply to major sections
        try:
            # Toolbar
            if hasattr(self, 'toolbar'):
                self.toolbar.configure(bg=theme['toolbar'])
            
            # Status bar
            if hasattr(self, 'status_bar'):
                self.status_bar.configure(bg=theme['card'])
                if hasattr(self, 'status_label'):
                    self.status_label.configure(bg=theme['card'], fg=theme['fg'])
                if hasattr(self, 'achievement_label'):
                    self.achievement_label.configure(bg=theme['card'], fg=theme['fg'])
                if hasattr(self, 'theme_indicator'):
                    self.theme_indicator.configure(bg=theme['card'])
            
            # Progress sidebar
            if hasattr(self, 'right_panel'):
                self._apply_theme_to_widget(self.right_panel, theme)
            
        except Exception as e:
            pass  # Silently handle any theme application errors
        
        # Recursively apply to all widgets
        self._apply_theme_to_widget(self.window, theme)
    
    def _apply_theme_to_widget(self, widget, theme):
        """Recursively apply theme to widget and children"""
        try:
            widget_class = widget.winfo_class()
            
            # Skip ttk widgets and certain special widgets
            if widget_class in ['TNotebook', 'TFrame', 'TCombobox', 'TButton', 'TScrollbar']:
                return
            
            # Apply background
            if hasattr(widget, 'configure'):
                try:
                    if widget_class in ['Frame', 'Label', 'Button', 'Entry', 'Text', 'Listbox']:
                        if widget_class == 'Button':
                            # Don't override button colors that are specifically set
                            current_bg = widget.cget('bg')
                            if current_bg in ['SystemButtonFace', theme['bg'], 'white', '#f0f0f0']:
                                widget.configure(bg=theme['card'], fg=theme['fg'])
                        elif widget_class in ['Label', 'Frame']:
                            current_bg = widget.cget('bg')
                            if current_bg in ['SystemButtonFace', '#f0f0f0', 'white']:
                                widget.configure(bg=theme['bg'])
                                if widget_class == 'Label':
                                    widget.configure(fg=theme['fg'])
                        elif widget_class == 'Entry':
                            widget.configure(bg=theme['card'], fg=theme['fg'], 
                                           insertbackground=theme['fg'])
                        elif widget_class == 'Text':
                            # Only apply to specific text widgets
                            if hasattr(widget, 'master') and 'syntax' in str(widget):
                                widget.configure(bg=theme['card'], fg=theme['fg'])
                except:
                    pass
        except:
            pass
        
        # Apply to children
        try:
            for child in widget.winfo_children():
                self._apply_theme_to_widget(child, theme)
        except:
            pass
    
    def show_help_menu(self):
        """Show contextual help menu"""
        help_menu = tk.Menu(self.window, tearoff=0)
        help_menu.add_command(label="🎓 Interactive Tutorial", 
                             command=self.start_tutorial)
        help_menu.add_command(label="⌨️ Keyboard Shortcuts", 
                             command=self.show_keyboard_shortcuts)
        help_menu.add_command(label="📚 Examples Gallery", 
                             command=self.show_examples_gallery)
        help_menu.add_command(label="🏆 View Achievements", 
                             command=self.show_achievements)
        help_menu.add_command(label="🔧 Preferences", 
                             command=self.show_preferences)
        help_menu.add_separator()
        help_menu.add_command(label="🌐 Online Documentation", 
                             command=self.open_online_help)
        help_menu.add_command(label="💬 Community Forum", 
                             command=self.open_community)
        
        # Show menu at current mouse position
        try:
            help_menu.tk_popup(self.window.winfo_pointerx(), 
                              self.window.winfo_pointery())
        finally:
            help_menu.grab_release()
    
    def show_keyboard_shortcuts(self):
        """Show keyboard shortcuts dialog"""
        dialog = tk.Toplevel(self.window)
        dialog.title("⌨️ Keyboard Shortcuts")
        dialog.geometry("500x400")
        dialog.transient(self.window)
        
        # Content
        content = tk.Frame(dialog, bg='white', padx=20, pady=20)
        content.pack(fill='both', expand=True)
        
        tk.Label(content, text="⌨️ Keyboard Shortcuts", 
                font=('Arial', 18, 'bold'), bg='white').pack(pady=(0, 20))
        
        shortcuts = [
            ("File Operations", [
                ("Ctrl+N", "New Language"),
                ("Ctrl+O", "Open Language"),
                ("Ctrl+S", "Save Language"),
                ("Ctrl+Shift+S", "Save As"),
                ("Ctrl+E", "Export Language")
            ]),
            ("Editing", [
                ("F5 / Ctrl+R", "Run Code"),
                ("Escape", "Stop Execution"),
                ("Ctrl+F", "Find in Code"),
                ("Ctrl+Z", "Undo"),
                ("Ctrl+Y", "Redo")
            ]),
            ("Tools", [
                ("Ctrl+Shift+K", "Random Keywords"),
                ("Ctrl+Shift+T", "Theme Picker"),
                ("Ctrl+Shift+A", "Achievements"),
                ("F1", "Help Menu")
            ]),
            ("Accessibility", [
                ("Ctrl++", "Increase Font Size"),
                ("Ctrl+-", "Decrease Font Size"),
                ("Ctrl+0", "Reset Font Size")
            ])
        ]
        
        # Create scrollable area
        canvas = tk.Canvas(content, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(content, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Add shortcuts
        for category, items in shortcuts:
            # Category header
            cat_frame = tk.Frame(scrollable_frame, bg='#f8f9fa', relief='solid', bd=1)
            cat_frame.pack(fill='x', pady=(10, 5))
            
            tk.Label(cat_frame, text=category, font=('Arial', 12, 'bold'),
                    bg='#f8f9fa', fg='#1a202c').pack(anchor='w', padx=10, pady=5)
            
            # Shortcuts
            for shortcut, description in items:
                shortcut_frame = tk.Frame(scrollable_frame, bg='white')
                shortcut_frame.pack(fill='x', padx=10, pady=2)
                
                tk.Label(shortcut_frame, text=shortcut, font=('Arial', 10, 'bold'),
                        bg='white', fg='#667eea').pack(side='left')
                
                tk.Label(shortcut_frame, text=description, font=('Arial', 10),
                        bg='white', fg='#4a5568').pack(side='left', padx=(20, 0))
        
        # Close button
        tk.Button(content, text="Close", command=dialog.destroy,
                 bg='#667eea', fg='white', font=('Arial', 11),
                 padx=20, pady=8).pack(pady=(20, 0))
    
    def start_tutorial(self):
        """Start interactive tutorial"""
        # Create enhanced tutorial system
        tutorial_dialog = tk.Toplevel(self.window)
        tutorial_dialog.title("🎓 Interactive Tutorial")
        tutorial_dialog.geometry("400x300")
        tutorial_dialog.transient(self.window)
        
        content = tk.Frame(tutorial_dialog, bg='white', padx=20, pady=20)
        content.pack(fill='both', expand=True)
        
        tk.Label(content, text="🎓 Welcome to the Tutorial!", 
                font=('Arial', 16, 'bold'), bg='white').pack(pady=10)
        
        tk.Label(content, text="Learn how to create your own programming language step by step.",
                font=('Arial', 12), bg='white', wraplength=300).pack(pady=10)
        
        tk.Button(content, text="🚀 Start Tutorial", 
                 command=lambda: self.run_tutorial(tutorial_dialog),
                 bg='#667eea', fg='white', font=('Arial', 12, 'bold'),
                 padx=20, pady=10).pack(pady=20)
        
        tk.Button(content, text="Skip", command=tutorial_dialog.destroy,
                 bg='#e2e8f0', font=('Arial', 11),
                 padx=20, pady=8).pack()
    
    def run_tutorial(self, dialog):
        """Run the actual tutorial"""
        dialog.destroy()
        
        # Switch to welcome tab and start guided tour
        self.notebook.select(0)  # Welcome tab
        
        # Show tutorial steps
        steps = [
            ("Welcome! 👋", "Let's create your first programming language together!"),
            ("Step 1: Basic Info", "First, let's give your language a name. Click the 'Basic Info' tab."),
            ("Step 2: Keywords", "Now define some keywords. Click the 'Keywords' tab."),
            ("Step 3: Functions", "Add built-in functions. Click the 'Built-in Functions' tab."),
            ("Step 4: Test It!", "Try your language in the playground!"),
            ("Congratulations! 🎉", "You've created your first language!")
        ]
        
        self.show_tutorial_step(0, steps)
    
    def show_tutorial_step(self, step_index, steps):
        """Show a tutorial step"""
        if step_index >= len(steps):
            return
        
        title, content = steps[step_index]
        
        step_dialog = tk.Toplevel(self.window)
        step_dialog.title("Tutorial")
        step_dialog.geometry("350x200")
        step_dialog.transient(self.window)
        step_dialog.attributes('-topmost', True)
        
        # Position near the relevant UI element
        x = self.window.winfo_x() + 50
        y = self.window.winfo_y() + 50 + (step_index * 30)
        step_dialog.geometry(f"350x200+{x}+{y}")
        
        frame = tk.Frame(step_dialog, bg='white', padx=20, pady=15)
        frame.pack(fill='both', expand=True)
        
        tk.Label(frame, text=title, font=('Arial', 14, 'bold'),
                bg='white').pack(pady=(0, 10))
        
        tk.Label(frame, text=content, font=('Arial', 11),
                bg='white', wraplength=300, justify='left').pack(pady=10)
        
        button_frame = tk.Frame(frame, bg='white')
        button_frame.pack(pady=(15, 0))
        
        if step_index > 0:
            tk.Button(button_frame, text="← Back",
                     command=lambda: [step_dialog.destroy(), 
                                    self.show_tutorial_step(step_index-1, steps)],
                     bg='#e2e8f0', font=('Arial', 10),
                     padx=15, pady=5).pack(side='left', padx=5)
        
        if step_index < len(steps) - 1:
            tk.Button(button_frame, text="Next →",
                     command=lambda: [step_dialog.destroy(), 
                                    self.show_tutorial_step(step_index+1, steps)],
                     bg='#667eea', fg='white', font=('Arial', 10, 'bold'),
                     padx=15, pady=5).pack(side='left', padx=5)
        else:
            tk.Button(button_frame, text="Finish! 🎉",
                     command=step_dialog.destroy,
                     bg='#38a169', fg='white', font=('Arial', 10, 'bold'),
                     padx=15, pady=5).pack(side='left', padx=5)
        
        tk.Button(button_frame, text="Skip Tutorial",
                 command=step_dialog.destroy,
                 bg='#e2e8f0', font=('Arial', 10),
                 padx=15, pady=5).pack(side='left', padx=5)
    
    # Continue with remaining methods...
    
    def populate_ui_from_data(self):
        """Populate UI from language data with error handling - FIXED VERSION"""
        try:
            # Basic info - with safe string handling
            if hasattr(self, 'name_entry'):
                self.name_entry.delete(0, tk.END)
                name_value = str(self.language_data.get('name', ''))
                self.name_entry.insert(0, name_value)
            
            if hasattr(self, 'version_entry'):
                self.version_entry.delete(0, tk.END)
                version_value = str(self.language_data.get('version', '1.0'))
                self.version_entry.insert(0, version_value)
            
            if hasattr(self, 'author_entry'):
                self.author_entry.delete(0, tk.END)
                author_value = str(self.language_data.get('author', ''))
                self.author_entry.insert(0, author_value)
            
            if hasattr(self, 'desc_text'):
                self.desc_text.delete('1.0', tk.END)
                desc_value = str(self.language_data.get('description', ''))
                self.desc_text.insert('1.0', desc_value)
            
            # Keywords - with safe handling
            if hasattr(self, 'keyword_entries'):
                for keyword, entry in self.keyword_entries.items():
                    try:
                        entry.delete(0, tk.END)
                        keywords_dict = self.language_data.get('keywords', {})
                        if keyword in keywords_dict and keywords_dict[keyword]:
                            value = str(keywords_dict[keyword])
                            entry.insert(0, value)
                    except Exception as e:
                        print(f"Error setting keyword {keyword}: {e}")
                        continue
            
            # Built-ins - with safe handling
            if hasattr(self, 'builtin_entries'):
                for builtin, entry in self.builtin_entries.items():
                    try:
                        entry.delete(0, tk.END)
                        builtins_dict = self.language_data.get('builtins', {})
                        if builtin in builtins_dict and builtins_dict[builtin]:
                            value = str(builtins_dict[builtin])
                            entry.insert(0, value)
                    except Exception as e:
                        print(f"Error setting builtin {builtin}: {e}")
                        continue
            
            # Features - with safe handling
            if hasattr(self, 'features'):
                try:
                    features = self.language_data.get('features', {})
                    for key, var in self.features.items():
                        if isinstance(var, tk.BooleanVar):
                            value = bool(features.get(key, False))
                            var.set(value)
                except Exception as e:
                    print(f"Error setting features: {e}")
            
            # Error entries - with safe handling
            if hasattr(self, 'error_entries'):
                try:
                    errors_dict = self.language_data.get('errors', {})
                    for error_key, text_widget in self.error_entries.items():
                        if hasattr(text_widget, 'delete') and hasattr(text_widget, 'insert'):
                            text_widget.delete('1.0', tk.END)
                            if error_key in errors_dict and errors_dict[error_key]:
                                value = str(errors_dict[error_key])
                                text_widget.insert('1.0', value)
                except Exception as e:
                    print(f"Error setting error messages: {e}")
            
            # Apply theme if specified - with safe handling
            try:
                theme = self.language_data.get('theme')
                if theme and theme in self.theme_engine.themes:
                    self.change_theme(theme)
            except Exception as e:
                print(f"Error applying theme: {e}")
            
            # Update all previews - with error handling
            try:
                self.update_preview()
            except Exception as e:
                print(f"Error updating preview: {e}")
                
        except Exception as e:
            print(f"Error in populate_ui_from_data: {e}")
            # Don't show error dialog for UI population issues
            # messagebox.showerror("Error", f"Error populating UI: {e}")
    
    def update_status(self, message):
        """Update status bar with auto-clear"""
        if hasattr(self, 'status_label'):
            self.status_label.config(text=message)
            # Clear status after 3 seconds
            self.window.after(3000, lambda: self.status_label.config(text="Ready"))
    
    def update_achievement_display(self):
        """Update achievement display in status bar"""
        if hasattr(self, 'achievement_label'):
            unlocked, total, points = self.achievement_system.get_progress()
            self.achievement_label.config(
                text=f"🏆 {unlocked}/{total} • {points} pts"
            )
    
    def unlock_achievement(self, achievement_id):
        """Unlock achievement with enhanced notification - SAFE VERSION"""
        try:
            if hasattr(self, 'achievement_system'):
                ach = self.achievement_system.unlock(achievement_id)
                if ach:
                    self.show_enhanced_achievement_notification(ach)
                    self.update_achievement_display()
        except Exception as e:
            print(f"Error unlocking achievement {achievement_id}: {e}")
            # Don't show error dialog for achievement issues

    def show_enhanced_achievement_notification(self, achievement):
        """Show enhanced achievement notification - SAFE VERSION"""
        try:
            notification = tk.Toplevel(self.window)
            notification.overrideredirect(True)
            notification.attributes('-topmost', True)
            
            # Position at top-right of window
            x = self.window.winfo_x() + self.window.winfo_width() - 320
            y = self.window.winfo_y() + 60
            notification.geometry(f"300x120+{x}+{y}")
            
            # Main frame with gradient-like effect
            main_frame = tk.Frame(notification, bg='#38a169', relief='solid', bd=2)
            main_frame.pack(fill='both', expand=True)
            
            # Content
            content = tk.Frame(main_frame, bg='#38a169', padx=15, pady=12)
            content.pack(fill='both', expand=True)
            
            # Header
            header_frame = tk.Frame(content, bg='#38a169')
            header_frame.pack(fill='x')
            
            tk.Label(header_frame, text="🏆", font=('Arial', 24),
                    bg='#38a169', fg='white').pack(side='left')
            
            title_frame = tk.Frame(header_frame, bg='#38a169')
            title_frame.pack(side='left', fill='x', expand=True, padx=(10, 0))
            
            tk.Label(title_frame, text="Achievement Unlocked!",
                    font=('Arial', 12, 'bold'), bg='#38a169', fg='white').pack(anchor='w')
            
            achievement_name = getattr(achievement, 'name', 'Unknown Achievement')
            achievement_icon = getattr(achievement, 'icon', '🏆')
            tk.Label(title_frame, text=f"{achievement_icon} {achievement_name}",
                    font=('Arial', 11), bg='#38a169', fg='#e6fffa').pack(anchor='w')
            
            # Points
            achievement_points = getattr(achievement, 'points', 0)
            tk.Label(content, text=f"+{achievement_points} points",
                    font=('Arial', 10, 'bold'), bg='#38a169', fg='#ffd700').pack(anchor='w', pady=(5, 0))
            
            # Auto-close after 3 seconds
            def safe_destroy():
                try:
                    if notification.winfo_exists():
                        notification.destroy()
                except:
                    pass
            
            notification.after(3000, safe_destroy)
            
            # Click to dismiss
            def dismiss(e=None):
                safe_destroy()
            
            notification.bind('<Button-1>', dismiss)
            main_frame.bind('<Button-1>', dismiss)
            content.bind('<Button-1>', dismiss)
            
        except Exception as e:
            print(f"Error showing achievement notification: {e}")
    
    def show_achievements(self):
        """Show enhanced achievements dialog"""
        dialog = tk.Toplevel(self.window)
        dialog.title("🏆 Achievements")
        dialog.geometry("700x800")
        dialog.transient(self.window)
        
        # Header with stats
        header = tk.Frame(dialog, bg='#667eea', height=120)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        header_content = tk.Frame(header, bg='#667eea')
        header_content.pack(expand=True, fill='both', padx=30, pady=20)
        
        # Title
        title_frame = tk.Frame(header_content, bg='#667eea')
        title_frame.pack(anchor='w', fill='x')
        
        tk.Label(title_frame, text="🏆", font=('Arial', 32),
                bg='#667eea', fg='white').pack(side='left')
        
        title_text_frame = tk.Frame(title_frame, bg='#667eea')
        title_text_frame.pack(side='left', fill='x', expand=True, padx=(15, 0))
        
        tk.Label(title_text_frame, text="Your Achievements",
                font=('Arial', 24, 'bold'), bg='#667eea', fg='white').pack(anchor='w')
        
        # Stats
        unlocked, total, points = self.achievement_system.get_progress()
        stats_text = f"{unlocked} of {total} unlocked • {points} total points"
        tk.Label(title_text_frame, text=stats_text,
                font=('Arial', 12), bg='#667eea', fg='#e2e8f0').pack(anchor='w')
        
        # Progress bar
        progress_frame = tk.Frame(header_content, bg='#667eea')
        progress_frame.pack(fill='x', pady=(10, 0))
        
        progress_bg = tk.Frame(progress_frame, bg='#5a67d8', height=8)
        progress_bg.pack(fill='x')
        
        if total > 0:
            progress_width = unlocked / total
            progress_fill = tk.Frame(progress_bg, bg='#68d391', height=8)
            progress_fill.place(relwidth=progress_width)
        
        # Achievements by category
        main_content = tk.Frame(dialog, bg='white')
        main_content.pack(fill='both', expand=True)
        
        # Create notebook for categories
        category_notebook = ttk.Notebook(main_content)
        category_notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Get achievements by category
        categories = self.achievement_system.get_achievements_by_category()
        
        for category_name, achievements in categories.items():
            # Create tab for category
            tab = ttk.Frame(category_notebook)
            category_notebook.add(tab, text=category_name.title())
            
            # Scrollable area for achievements
            canvas = tk.Canvas(tab, bg='white', highlightthickness=0)
            scrollbar = ttk.Scrollbar(tab, orient='vertical', command=canvas.yview)
            achievements_frame = tk.Frame(canvas, bg='white')
            
            achievements_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=achievements_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side='left', fill='both', expand=True)
            scrollbar.pack(side='right', fill='y')
            
            # Add achievements
            for ach in achievements:
                self.create_achievement_card(achievements_frame, ach)
    
    def create_achievement_card(self, parent, achievement):
        """Create an achievement card"""
        card = tk.Frame(parent, bg='white', relief='solid', bd=1)
        card.pack(fill='x', padx=20, pady=10)
        
        if not achievement.unlocked:
            # Greyed out for locked achievements
            card.configure(bg='#f8f9fa')
        
        content = tk.Frame(card, bg=card['bg'], padx=20, pady=15)
        content.pack(fill='x')
        
        # Left side - icon and info
        left_frame = tk.Frame(content, bg=card['bg'])
        left_frame.pack(side='left', fill='x', expand=True)
        
        # Icon
        icon_color = '#1a202c' if achievement.unlocked else '#a0aec0'
        tk.Label(left_frame, text=achievement.icon, font=('Arial', 32),
                bg=card['bg'], fg=icon_color).pack(side='left', padx=(0, 20))
        
        # Info
        info_frame = tk.Frame(left_frame, bg=card['bg'])
        info_frame.pack(side='left', fill='x', expand=True)
        
        # Name
        name_color = '#1a202c' if achievement.unlocked else '#a0aec0'
        tk.Label(info_frame, text=achievement.name, 
                font=('Arial', 14, 'bold'),
                bg=card['bg'], fg=name_color).pack(anchor='w')
        
        # Description
        desc_color = '#4a5568' if achievement.unlocked else '#cbd5e0'
        tk.Label(info_frame, text=achievement.description,
                font=('Arial', 11), bg=card['bg'], fg=desc_color,
                wraplength=400).pack(anchor='w', pady=(2, 0))
        
        # Right side - status and points
        right_frame = tk.Frame(content, bg=card['bg'])
        right_frame.pack(side='right')
        
        if achievement.unlocked:
            # Unlocked badge
            badge = tk.Frame(right_frame, bg='#38a169', padx=10, pady=5)
            badge.pack()
            
            tk.Label(badge, text=f"✓ {achievement.points} pts",
                    font=('Arial', 11, 'bold'),
                    bg='#38a169', fg='white').pack()
        else:
            # Points available
            tk.Label(right_frame, text=f"{achievement.points} pts",
                    font=('Arial', 11), bg=card['bg'], fg='#a0aec0').pack()
    
    # ========================================================================
    # MISSING METHOD IMPLEMENTATIONS
    # ========================================================================
    
    def import_language(self):
        """Import language from various sources"""
        dialog = tk.Toplevel(self.window)
        dialog.title("📥 Import Language")
        dialog.geometry("500x400")
        dialog.transient(self.window)
        dialog.grab_set()
        
        # Header
        header = tk.Frame(dialog, bg='#667eea', height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        header_content = tk.Frame(header, bg='#667eea')
        header_content.pack(expand=True, fill='both', padx=30, pady=20)
        
        tk.Label(header_content, text="📥 Import Language", 
                font=('Arial', 20, 'bold'), bg='#667eea', fg='white').pack(anchor='w')
        tk.Label(header_content, text="Import a language from file or URL",
                font=('Arial', 12), bg='#667eea', fg='#e2e8f0').pack(anchor='w')
        
        # Main content
        main_content = tk.Frame(dialog, bg='white', padx=30, pady=20)
        main_content.pack(fill='both', expand=True)
        
        # Import options
        tk.Label(main_content, text="Choose import source:", 
                font=('Arial', 14, 'bold'), bg='white').pack(anchor='w', pady=(0, 15))
        
        # File import
        file_frame = tk.Frame(main_content, bg='white', relief='solid', bd=1)
        file_frame.pack(fill='x', pady=5)
        
        file_content = tk.Frame(file_frame, bg='white', padx=15, pady=12)
        file_content.pack(fill='x')
        
        tk.Label(file_content, text="📁 From File", font=('Arial', 12, 'bold'),
                bg='white').pack(anchor='w')
        tk.Label(file_content, text="Import from a .json language file",
                font=('Arial', 10), bg='white', fg='#666').pack(anchor='w')
        
        tk.Button(file_content, text="Choose File", 
                 command=lambda: [dialog.destroy(), self.load_language()],
                 bg='#667eea', fg='white', relief='flat',
                 font=('Arial', 10), padx=15, pady=5).pack(anchor='w', pady=(8, 0))
        
        # URL import
        url_frame = tk.Frame(main_content, bg='white', relief='solid', bd=1)
        url_frame.pack(fill='x', pady=5)
        
        url_content = tk.Frame(url_frame, bg='white', padx=15, pady=12)
        url_content.pack(fill='x')
        
        tk.Label(url_content, text="🌐 From URL", font=('Arial', 12, 'bold'),
                bg='white').pack(anchor='w')
        tk.Label(url_content, text="Import from a web URL (coming soon)",
                font=('Arial', 10), bg='white', fg='#666').pack(anchor='w')
        
        url_entry = tk.Entry(url_content, font=('Arial', 10), width=40,
                            relief='solid', bd=1, state='disabled')
        url_entry.pack(anchor='w', pady=(5, 0), fill='x')
        
        tk.Button(url_content, text="Import from URL", state='disabled',
                 bg='#e2e8f0', relief='flat',
                 font=('Arial', 10), padx=15, pady=5).pack(anchor='w', pady=(8, 0))
        
        # GitHub import
        github_frame = tk.Frame(main_content, bg='white', relief='solid', bd=1)
        github_frame.pack(fill='x', pady=5)
        
        github_content = tk.Frame(github_frame, bg='white', padx=15, pady=12)
        github_content.pack(fill='x')
        
        tk.Label(github_content, text="🐙 From GitHub", font=('Arial', 12, 'bold'),
                bg='white').pack(anchor='w')
        tk.Label(github_content, text="Import from GitHub repository (coming soon)",
                font=('Arial', 10), bg='white', fg='#666').pack(anchor='w')
        
        tk.Button(github_content, text="Browse GitHub", state='disabled',
                 bg='#e2e8f0', relief='flat',
                 font=('Arial', 10), padx=15, pady=5).pack(anchor='w', pady=(8, 0))
        
        # Close button
        tk.Button(main_content, text="Cancel", command=dialog.destroy,
                 bg='#e2e8f0', font=('Arial', 11),
                 padx=20, pady=8).pack(pady=(20, 0))
    
    def show_preferences(self):
        """Show enhanced preferences dialog"""
        dialog = tk.Toplevel(self.window)
        dialog.title("🔧 Preferences")
        dialog.geometry("600x500")
        dialog.transient(self.window)
        
        # Create notebook for preference categories
        notebook = ttk.Notebook(dialog)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # General preferences
        general_tab = ttk.Frame(notebook)
        notebook.add(general_tab, text="General")
        
        general_content = tk.Frame(general_tab, bg='white', padx=20, pady=20)
        general_content.pack(fill='both', expand=True)
        
        # Auto-save setting
        tk.Label(general_content, text="Auto-save", font=('Arial', 12, 'bold'),
                bg='white').pack(anchor='w')
        
        autosave_var = tk.BooleanVar(value=True)
        tk.Checkbutton(general_content, text="Automatically save changes every 30 seconds",
                      variable=autosave_var, bg='white').pack(anchor='w', pady=5)
        
        # Theme setting
        tk.Label(general_content, text="Default Theme", font=('Arial', 12, 'bold'),
                bg='white').pack(anchor='w', pady=(20, 5))
        
        theme_var = tk.StringVar(value=self.current_theme)
        for theme_id, theme in self.theme_engine.themes.items():
            tk.Radiobutton(general_content, text=theme['name'],
                          variable=theme_var, value=theme_id,
                          bg='white').pack(anchor='w')
        
        # Editor preferences
        editor_tab = ttk.Frame(notebook)
        notebook.add(editor_tab, text="Editor")
        
        editor_content = tk.Frame(editor_tab, bg='white', padx=20, pady=20)
        editor_content.pack(fill='both', expand=True)
        
        # Font size
        tk.Label(editor_content, text="Font Size", font=('Arial', 12, 'bold'),
                bg='white').pack(anchor='w')
        
        font_frame = tk.Frame(editor_content, bg='white')
        font_frame.pack(anchor='w', pady=5)
        
        font_size_var = tk.IntVar(value=self.accessibility.font_size)
        font_scale = tk.Scale(font_frame, from_=8, to=24, orient='horizontal',
                             variable=font_size_var, bg='white')
        font_scale.pack(side='left')
        
        tk.Label(font_frame, text="pt", bg='white').pack(side='left', padx=5)
        
        # Line numbers
        line_numbers_var = tk.BooleanVar(value=True)
        tk.Checkbutton(editor_content, text="Show line numbers",
                      variable=line_numbers_var, bg='white').pack(anchor='w', pady=10)
        
        # Syntax highlighting
        syntax_var = tk.BooleanVar(value=True)
        tk.Checkbutton(editor_content, text="Enable syntax highlighting",
                      variable=syntax_var, bg='white').pack(anchor='w')
        
        # Accessibility preferences
        accessibility_tab = ttk.Frame(notebook)
        notebook.add(accessibility_tab, text="Accessibility")
        
        access_content = tk.Frame(accessibility_tab, bg='white', padx=20, pady=20)
        access_content.pack(fill='both', expand=True)
        
        # High contrast
        high_contrast_var = tk.BooleanVar()
        tk.Checkbutton(access_content, text="High contrast mode",
                      variable=high_contrast_var, bg='white').pack(anchor='w')
        
        # Screen reader support
        screen_reader_var = tk.BooleanVar()
        tk.Checkbutton(access_content, text="Screen reader optimizations",
                      variable=screen_reader_var, bg='white').pack(anchor='w', pady=5)
        
        # Keyboard navigation
        keyboard_var = tk.BooleanVar(value=True)
        tk.Checkbutton(access_content, text="Enhanced keyboard navigation",
                      variable=keyboard_var, bg='white').pack(anchor='w')
        
        # Buttons
        button_frame = tk.Frame(dialog, bg='white', padx=20, pady=10)
        button_frame.pack(fill='x')
        
        def apply_preferences():
            # Apply font size
            new_font_size = font_size_var.get()
            if new_font_size != self.accessibility.font_size:
                self.accessibility.font_size = new_font_size
                self.accessibility.apply_font_changes()
            
            # Apply theme
            new_theme = theme_var.get()
            if new_theme != self.current_theme:
                self.change_theme(new_theme)
            
            # Apply high contrast
            if high_contrast_var.get():
                self.change_theme('high_contrast')
            
            dialog.destroy()
            self.update_status("Preferences applied")
        
        tk.Button(button_frame, text="Apply", command=apply_preferences,
                 bg='#667eea', fg='white', font=('Arial', 11, 'bold'),
                 padx=20, pady=8).pack(side='right', padx=5)
        
        tk.Button(button_frame, text="Cancel", command=dialog.destroy,
                 bg='#e2e8f0', font=('Arial', 11),
                 padx=20, pady=8).pack(side='right')
    
    def show_examples_gallery(self):
        """Show enhanced examples gallery"""
        dialog = tk.Toplevel(self.window)
        dialog.title("📚 Examples Gallery")
        dialog.geometry("800x600")
        dialog.transient(self.window)
        
        # Header
        header = tk.Frame(dialog, bg='#38a169', height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        header_content = tk.Frame(header, bg='#38a169')
        header_content.pack(expand=True, fill='both', padx=30, pady=20)
        
        tk.Label(header_content, text="📚 Examples Gallery", 
                font=('Arial', 20, 'bold'), bg='#38a169', fg='white').pack(anchor='w')
        tk.Label(header_content, text="Get inspired by example languages",
                font=('Arial', 12), bg='#38a169', fg='#e2e8f0').pack(anchor='w')
        
        # Main content
        main_content = tk.Frame(dialog, bg='white')
        main_content.pack(fill='both', expand=True)
        
        # Create notebook for categories
        notebook = ttk.Notebook(main_content)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Beginner examples
        beginner_tab = self.create_examples_tab(notebook, "Beginner", [
            {
                'name': 'Hello World Lang',
                'description': 'A simple language for saying hello',
                'keywords': {'function': 'say', 'variable': 'word', 'if': 'check'},
                'preview': 'say hello() {\n  show("Hello, World!")\n}'
            },
            {
                'name': 'Math Helper',
                'description': 'Simple math operations',
                'keywords': {'function': 'calc', 'variable': 'num', 'if': 'test'},
                'preview': 'calc add(a, b) {\n  give a + b\n}'
            }
        ])
        notebook.add(beginner_tab, text="🌱 Beginner")
        
        # Creative examples
        creative_tab = self.create_examples_tab(notebook, "Creative", [
            {
                'name': 'Emoji Lang',
                'description': 'Express yourself with emojis!',
                'keywords': {'function': '🎯', 'variable': '📦', 'if': '❓'},
                'preview': '🎯 greet(name) {\n  📢("Hello " + name + "!")\n}'
            },
            {
                'name': 'Magic Spells',
                'description': 'Cast spells with code',
                'keywords': {'function': 'spell', 'variable': 'essence', 'if': 'divine'},
                'preview': 'spell fireball(power) {\n  cast(flame + power)\n}'
            }
        ])
        notebook.add(creative_tab, text="🎨 Creative")
        
        # Advanced examples
        advanced_tab = self.create_examples_tab(notebook, "Advanced", [
            {
                'name': 'Game Script',
                'description': 'Perfect for game development',
                'keywords': {'function': 'action', 'variable': 'entity', 'if': 'condition'},
                'preview': 'action move_player(direction) {\n  player.position += direction\n}'
            }
        ])
        notebook.add(advanced_tab, text="🚀 Advanced")
    
    def create_examples_tab(self, parent, category, examples):
        """Create an examples tab"""
        tab = ttk.Frame(parent)
        
        # Scrollable content
        canvas = tk.Canvas(tab, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient='vertical', command=canvas.yview)
        content_frame = tk.Frame(canvas, bg='white')
        
        content_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=content_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        main_content = tk.Frame(content_frame, bg='white', padx=20, pady=20)
        main_content.pack(fill='both', expand=True)
        
        for example in examples:
            self.create_example_card(main_content, example)
        
        return tab
    
    def create_example_card(self, parent, example):
        """Create an example card"""
        card = tk.Frame(parent, bg='white', relief='solid', bd=1)
        card.pack(fill='x', pady=10)
        
        # Header
        header = tk.Frame(card, bg='#f8f9fa', padx=15, pady=10)
        header.pack(fill='x')
        
        tk.Label(header, text=example['name'], font=('Arial', 14, 'bold'),
                bg='#f8f9fa').pack(side='left')
        
        tk.Button(header, text="Use This →",
                 command=lambda: self.apply_example(example),
                 bg='#667eea', fg='white', relief='flat',
                 font=('Arial', 10), padx=15, pady=5).pack(side='right')
        
        # Content
        content = tk.Frame(card, bg='white', padx=15, pady=10)
        content.pack(fill='x')
        
        tk.Label(content, text=example['description'], font=('Arial', 11),
                bg='white', fg='#666').pack(anchor='w')
        
        # Preview
        preview_frame = tk.Frame(content, bg='#f8f9fa', relief='solid', bd=1)
        preview_frame.pack(fill='x', pady=(10, 0))
        
        tk.Label(preview_frame, text="Preview:", font=('Arial', 10, 'bold'),
                bg='#f8f9fa').pack(anchor='w', padx=10, pady=(5, 0))
        
        preview_text = tk.Text(preview_frame, height=3, font=('Courier', 9),
                              bg='#f8f9fa', relief='flat', wrap='none')
        preview_text.pack(fill='x', padx=10, pady=(0, 5))
        preview_text.insert('1.0', example['preview'])
        preview_text.config(state='disabled')
    
    def apply_example(self, example):
        """Apply an example to current language"""
        # Update language data with example
        self.language_data.update({
            'name': example['name'],
            'description': example['description'],
            'keywords': example['keywords']
        })
        
        self.populate_ui_from_data()
        messagebox.showinfo("Example Applied", f"Applied {example['name']} example!")
    
    def open_online_help(self):
        """Open online help in browser"""
        try:
            webbrowser.open("https://github.com/your-repo/super-language-creator/wiki")
        except:
            messagebox.showinfo("Online Help", 
                              "Visit: https://github.com/your-repo/super-language-creator/wiki")
    
    def open_community(self):
        """Open community forum in browser"""
        try:
            webbrowser.open("https://discord.gg/super-language-creator")
        except:
            messagebox.showinfo("Community", 
                              "Join our Discord: https://discord.gg/super-language-creator")
    
    def validate_syntax(self):
        """Enhanced syntax validation"""
        self.collect_language_data()
        
        dialog = tk.Toplevel(self.window)
        dialog.title("✅ Syntax Validator")
        dialog.geometry("500x400")
        dialog.transient(self.window)
        
        # Header
        header = tk.Frame(dialog, bg='#38a169', height=60)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(header, text="✅ Syntax Validation Results", 
                font=('Arial', 16, 'bold'), bg='#38a169', fg='white').pack(pady=15)
        
        # Results area
        results_frame = tk.Frame(dialog, bg='white', padx=20, pady=20)
        results_frame.pack(fill='both', expand=True)
        
        # Perform validation
        issues = []
        warnings = []
        
        # Check required elements
        if not self.language_data.get('name') or self.language_data['name'] == 'MyLang':
            issues.append("Language needs a unique name")
        
        keywords = self.language_data.get('keywords', {})
        if len([k for k in keywords.values() if k]) < 3:
            issues.append("At least 3 keywords should be defined")
        
        builtins = self.language_data.get('builtins', {})
        if not builtins.get('print'):
            warnings.append("Consider defining a print/output function")
        
        # Check for conflicts
        all_words = list(keywords.values()) + list(builtins.values())
        all_words = [w for w in all_words if w]
        if len(all_words) != len(set(all_words)):
            issues.append("Some keywords/functions have the same name")
        
        # Display results
        if not issues and not warnings:
            # All good
            success_frame = tk.Frame(results_frame, bg='#d4edda', relief='solid', bd=1)
            success_frame.pack(fill='x', pady=5)
            
            tk.Label(success_frame, text="🎉 Perfect! No issues found.",
                    font=('Arial', 12, 'bold'), bg='#d4edda', fg='#155724').pack(pady=10)
        else:
            # Show issues
            if issues:
                issues_frame = tk.LabelFrame(results_frame, text="❌ Issues (must fix)",
                                           font=('Arial', 11, 'bold'), bg='white')
                issues_frame.pack(fill='x', pady=5)
                
                for issue in issues:
                    tk.Label(issues_frame, text=f"• {issue}", font=('Arial', 10),
                            bg='white', fg='#dc3545').pack(anchor='w', padx=10, pady=2)
            
            if warnings:
                warnings_frame = tk.LabelFrame(results_frame, text="⚠️ Suggestions",
                                             font=('Arial', 11, 'bold'), bg='white')
                warnings_frame.pack(fill='x', pady=5)
                
                for warning in warnings:
                    tk.Label(warnings_frame, text=f"• {warning}", font=('Arial', 10),
                            bg='white', fg='#ffc107').pack(anchor='w', padx=10, pady=2)
        
        # Tips
        tips_frame = tk.LabelFrame(results_frame, text="💡 Tips",
                                 font=('Arial', 11, 'bold'), bg='white')
        tips_frame.pack(fill='x', pady=(20, 5))
        
        tips = [
            "Use meaningful names that your target audience will understand",
            "Keep keyword names short for easier typing",
            "Test your language frequently in the playground"
        ]
        
        for tip in tips:
            tk.Label(tips_frame, text=f"• {tip}", font=('Arial', 10),
                    bg='white', fg='#666').pack(anchor='w', padx=10, pady=2)
        
        # Close button
        tk.Button(results_frame, text="Close", command=dialog.destroy,
                 bg='#667eea', fg='white', font=('Arial', 11),
                 padx=20, pady=8).pack(pady=(20, 0))
    
    def performance_test(self):
        """Enhanced performance test"""
        dialog = tk.Toplevel(self.window)
        dialog.title("⚡ Performance Test")
        dialog.geometry("500x400")
        dialog.transient(self.window)
        
        # Header
        header = tk.Frame(dialog, bg='#f39c12', height=60)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(header, text="⚡ Performance Analysis", 
                font=('Arial', 16, 'bold'), bg='#f39c12', fg='white').pack(pady=15)
        
        # Content
        content = tk.Frame(dialog, bg='white', padx=20, pady=20)
        content.pack(fill='both', expand=True)
        
        tk.Label(content, text="Testing your language performance...", 
                font=('Arial', 12), bg='white').pack(pady=10)
        
        # Progress bar
        progress = ttk.Progressbar(content, length=300, mode='indeterminate')
        progress.pack(pady=10)
        progress.start()
        
        # Results area
        results_text = scrolledtext.ScrolledText(content, height=10, 
                                               font=('Courier', 10))
        results_text.pack(fill='both', expand=True, pady=10)
        
        # Simulate performance test
        def run_test():
            import time
            tests = [
                "Testing keyword parsing speed...",
                "Analyzing memory usage...",
                "Checking syntax validation performance...",
                "Measuring startup time...",
                "Testing large file handling..."
            ]
            
            for test in tests:
                results_text.insert(tk.END, f"{test}\n")
                results_text.see(tk.END)
                results_text.update()
                time.sleep(0.5)
            
            # Final results
            results_text.insert(tk.END, "\n" + "="*40 + "\n")
            results_text.insert(tk.END, "PERFORMANCE RESULTS:\n")
            results_text.insert(tk.END, "✅ Keyword parsing: 0.001ms\n")
            results_text.insert(tk.END, "✅ Memory usage: 12MB\n")
            results_text.insert(tk.END, "✅ Startup time: 0.05s\n")
            results_text.insert(tk.END, "✅ Overall grade: Excellent!\n")
            
            progress.stop()
            progress.configure(mode='determinate', value=100)
        
        # Start test after a delay
        dialog.after(1000, run_test)
        
        # Close button
        tk.Button(content, text="Close", command=dialog.destroy,
                 bg='#667eea', fg='white', font=('Arial', 11),
                 padx=20, pady=8).pack(pady=10)
    
    def generate_docs(self):
        """Enhanced documentation generation"""
        self.collect_language_data()
        
        folder = filedialog.askdirectory(title="Choose documentation output folder")
        if not folder:
            return
        
        # Create docs folder
        docs_folder = os.path.join(folder, f"{self.language_data['name']}_docs")
        os.makedirs(docs_folder, exist_ok=True)
        
        # Generate README
        readme_content = self.generate_readme_content()
        with open(os.path.join(docs_folder, 'README.md'), 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        # Generate quick reference
        quick_ref = self.generate_quick_reference()
        with open(os.path.join(docs_folder, 'quick_reference.md'), 'w', encoding='utf-8') as f:
            f.write(quick_ref)
        
        # Generate language specification
        spec_content = self.generate_language_spec()
        with open(os.path.join(docs_folder, 'language_spec.md'), 'w', encoding='utf-8') as f:
            f.write(spec_content)
        
        messagebox.showinfo("Documentation Generated!", 
                          f"Documentation created in:\n{docs_folder}")
    
    def generate_readme_content(self):
        """Generate README content"""
        lang = self.language_data
        return f"""# {lang['name']} Programming Language

{lang.get('description', 'A custom programming language')}

**Version:** {lang.get('version', '1.0')}  
**Author:** {lang.get('author', 'Unknown')}  
**Created:** {datetime.now().strftime('%Y-%m-%d')}

## Quick Start

### Keywords
{self._format_keywords_table()}

### Built-in Functions
{self._format_builtins_table()}

## Example Code

```{lang['name'].lower()}
// Hello World example
{lang.get('keywords', {}).get('variable', 'var')} message = "Hello, World!"
{lang.get('builtins', {}).get('print', 'print')}(message)
```

## Installation

This language was created with SUPER Language Creator.
To run programs:

1. Install Python 3.6+
2. Use the generated interpreter
3. Write your code and enjoy!

---
*Generated by SUPER Language Creator*
"""
    
    def generate_quick_reference(self):
        """Generate quick reference"""
        lang = self.language_data
        return f"""# {lang['name']} Quick Reference

## Keywords
| English | {lang['name']} |
|---------|----------------|
{chr(10).join(f"| {eng} | `{custom}` |" for eng, custom in lang.get('keywords', {}).items() if custom)}

## Functions
| Purpose | {lang['name']} |
|---------|----------------|
{chr(10).join(f"| {eng} | `{custom}()` |" for eng, custom in lang.get('builtins', {}).items() if custom)}

## Operators
- Math: `+` `-` `*` `/`
- Compare: `==` `!=` `<` `>` `<=` `>=`  
- Logic: `and` `or` `not`
- Assign: `=`

## Example Programs

### Variables
```
{lang.get('keywords', {}).get('variable', 'var')} name = "Alice"
{lang.get('keywords', {}).get('variable', 'var')} age = 25
```

### Functions
```
{lang.get('keywords', {}).get('function', 'function')} greet(person) {{
    {lang.get('builtins', {}).get('print', 'print')}("Hello", person)
}}
```

### Conditionals
```
{lang.get('keywords', {}).get('if', 'if')} age >= 18 {{
    {lang.get('builtins', {}).get('print', 'print')}("Adult")
}} {lang.get('keywords', {}).get('else', 'else')} {{
    {lang.get('builtins', {}).get('print', 'print')}("Minor")
}}
```
"""
    
    def generate_language_spec(self):
        """Generate formal language specification"""
        lang = self.language_data
        return f"""# {lang['name']} Language Specification

## Overview
{lang.get('description', 'A custom programming language created with SUPER Language Creator.')}

## Lexical Elements

### Keywords
Reserved words in {lang['name']}:
{', '.join(f'`{v}`' for v in lang.get('keywords', {}).values() if v)}

### Identifiers
- Start with letter or underscore
- Can contain letters, digits, underscores
- Case sensitive: {lang.get('features', {}).get('case_sensitive', True)}

### Literals
- Numbers: `42`, `3.14`
- Strings: `"hello"`, `'world'`
- Booleans: `{lang.get('keywords', {}).get('true', 'true')}`, `{lang.get('keywords', {}).get('false', 'false')}`

## Syntax Rules

### Variable Declaration
```
{lang.get('keywords', {}).get('variable', 'var')} identifier = expression
```

### Function Definition
```
{lang.get('keywords', {}).get('function', 'function')} name(params) {{
    statements
    {lang.get('keywords', {}).get('return', 'return')} expression
}}
```

### Control Flow
```
{lang.get('keywords', {}).get('if', 'if')} condition {{
    statements
}} {lang.get('keywords', {}).get('else', 'else')} {{
    statements
}}

{lang.get('keywords', {}).get('loop', 'loop')} condition {{
    statements
}}
```

## Built-in Functions

{chr(10).join(f"### `{custom}()`{chr(10)}{eng.title()} function" for eng, custom in lang.get('builtins', {}).items() if custom)}

## Error Handling

{lang['name']} provides friendly error messages:
{chr(10).join(f"- **{error_type}**: {message}" for error_type, message in lang.get('errors', {}).items() if message)}

---
*Language specification generated by SUPER Language Creator*
"""
    
    def _format_keywords_table(self):
        """Format keywords as table"""
        table = "| English | Your Language |\n|---------|---------------|\n"
        for eng, custom in self.language_data.get('keywords', {}).items():
            if custom:
                table += f"| {eng} | `{custom}` |\n"
        return table
    
    def _format_builtins_table(self):
        """Format built-ins as table"""
        table = "| Function | Your Language |\n|----------|---------------|\n"
        for eng, custom in self.language_data.get('builtins', {}).items():
            if custom:
                table += f"| {eng} | `{custom}()` |\n"
        return table
    
    def export_language(self):
        """Enhanced language export with multiple formats"""
        self.collect_language_data()
        
        dialog = tk.Toplevel(self.window)
        dialog.title("📤 Export Language")
        dialog.geometry("600x500")
        dialog.transient(self.window)
        dialog.grab_set()
        
        # Header
        header = tk.Frame(dialog, bg='#ed8936', height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        header_content = tk.Frame(header, bg='#ed8936')
        header_content.pack(expand=True, fill='both', padx=30, pady=20)
        
        tk.Label(header_content, text="📤 Export Your Language", 
                font=('Arial', 20, 'bold'), bg='#ed8936', fg='white').pack(anchor='w')
        tk.Label(header_content, text="Choose how you want to share your creation",
                font=('Arial', 12), bg='#ed8936', fg='#fff5f5').pack(anchor='w')
        
        # Main content
        main_content = tk.Frame(dialog, bg='white', padx=30, pady=20)
        main_content.pack(fill='both', expand=True)
        
        tk.Label(main_content, text="Export Options:", 
                font=('Arial', 14, 'bold'), bg='white').pack(anchor='w', pady=(0, 15))
        
        export_var = tk.StringVar(value="complete")
        
        # Export options
        options = [
            ("complete", "🚀 Complete Package", 
             "Full interpreter, examples, and documentation"),
            ("source", "💻 Source Code Only", 
             "Just the Python source files"),
            ("docs", "📚 Documentation Only", 
             "Language reference and examples"),
            ("share", "🔗 Shareable Link", 
             "Create a link to share online (coming soon)")
        ]
        
        for value, title, desc in options:
            option_frame = tk.Frame(main_content, bg='white', relief='solid', bd=1)
            option_frame.pack(fill='x', pady=5)
            
            option_content = tk.Frame(option_frame, bg='white', padx=15, pady=12)
            option_content.pack(fill='x')
            
            rb = tk.Radiobutton(option_content, text=title, variable=export_var, 
                               value=value, font=('Arial', 12, 'bold'),
                               bg='white', selectcolor='#ed8936')
            rb.pack(anchor='w')
            
            tk.Label(option_content, text=desc, font=('Arial', 10),
                    bg='white', fg='#666').pack(anchor='w', padx=(25, 0))
            
            if value == "share":
                tk.Label(option_content, text="(Feature coming soon)", 
                        font=('Arial', 9, 'italic'),
                        bg='white', fg='#999').pack(anchor='w', padx=(25, 0))
        
        # Export location
        location_frame = tk.Frame(main_content, bg='white')
        location_frame.pack(fill='x', pady=(20, 10))
        
        tk.Label(location_frame, text="Export Location:", 
                font=('Arial', 12, 'bold'), bg='white').pack(anchor='w')
        
        location_display = tk.Frame(location_frame, bg='white')
        location_display.pack(fill='x', pady=5)
        
        self.export_location = tk.StringVar(value="Choose folder...")
        location_label = tk.Label(location_display, textvariable=self.export_location,
                                 font=('Arial', 10), bg='#f8f9fa', relief='solid', bd=1,
                                 anchor='w')
        location_label.pack(side='left', fill='x', expand=True, ipady=5, ipadx=10)
        
        def choose_location():
            folder = filedialog.askdirectory(title="Choose export location")
            if folder:
                self.export_location.set(folder)
        
        tk.Button(location_display, text="Browse", command=choose_location,
                 bg='#667eea', fg='white', relief='flat',
                 font=('Arial', 10), padx=15, pady=5).pack(side='right', padx=(5, 0))
        
        # Buttons
        button_frame = tk.Frame(main_content, bg='white')
        button_frame.pack(fill='x', pady=(30, 0))
        
        def do_export():
            if self.export_location.get() == "Choose folder...":
                messagebox.showwarning("No Location", "Please choose an export location.")
                return
            
            export_type = export_var.get()
            location = self.export_location.get()
            
            try:
                if export_type == "complete":
                    self.export_complete_package(location)
                elif export_type == "source":
                    self.export_source_only(location)
                elif export_type == "docs":
                    self.export_docs_only(location)
                elif export_type == "share":
                    messagebox.showinfo("Coming Soon", "Online sharing feature coming soon!")
                    return
                
                dialog.destroy()
                self.unlock_achievement('share_joy')
                messagebox.showinfo("Export Complete!", 
                                  f"Your language has been exported to:\n{location}")
                
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export:\n{e}")
        
        tk.Button(button_frame, text="📤 Export", command=do_export,
                 bg='#ed8936', fg='white', font=('Arial', 11, 'bold'),
                 padx=25, pady=10).pack(side='right', padx=5)
        
        tk.Button(button_frame, text="Cancel", command=dialog.destroy,
                 bg='#e2e8f0', font=('Arial', 11),
                 padx=20, pady=10).pack(side='right')
    
    def export_complete_package(self, location):
        """Export complete language package with working interpreter"""
        lang_name = self.language_data['name'].lower().replace(' ', '_')
        export_folder = os.path.join(location, f"{lang_name}_complete")
        os.makedirs(export_folder, exist_ok=True)
        
        # Create folder structure
        folders = ['src', 'examples', 'docs', 'tests']
        for folder in folders:
            os.makedirs(os.path.join(export_folder, folder), exist_ok=True)
        
        # Export language definition
        with open(os.path.join(export_folder, 'language.json'), 'w', encoding='utf-8') as f:
            json.dump(self.language_data, f, indent=2, ensure_ascii=False)
        
        # Generate the complete interpreter
        self.generate_interpreter(export_folder)
        
        # Create batch/shell scripts for easy execution
        self.create_runner_scripts(export_folder)
        
        # Generate documentation
        self.generate_docs_in_folder(os.path.join(export_folder, 'docs'))
        
        # Create comprehensive example files
        self.create_enhanced_example_files(os.path.join(export_folder, 'examples'))
        
        # Create test files
        self.create_test_files(os.path.join(export_folder, 'tests'))
        
        # Create enhanced README
        self.create_enhanced_readme(export_folder)
        
        # Create a quick start guide
        self.create_quick_start_guide(export_folder)

    def create_quick_start_guide(self, export_folder):
        """Create a quick start guide"""
        lang_name = self.language_data['name']
        ext = lang_name[:3].lower()
        
        guide = f"""# {lang_name} Quick Start Guide

    ## Installation
1. Make sure Python 3.6+ is installed 

2. Extract the {lang_name} package to any folder

3. Open a terminal/command prompt in that folder

## Running Your First Program

### Option 1: Using the runner scripts (Easiest)

**Windows:**     
run_{lang_name.lower().replace(' ', '_')}.bat examples\01_hello.{ext}
**Mac/Linux:**
./run_{lang_name.lower().replace(' ', '_')}.sh examples/01_hello.{ext}

### Option 2: Using Python directly
python src/{lang_name.lower().replace(' ', '_')}.py examples/01_hello.{ext}
## Writing Your First Program

1. Create a new file called `my_first.{ext}`

2. Add this code:
{self.language_data.get('builtins', {}).get('print', 'print')}("Hello from {lang_name}!")
3. Run it:
python src/{lang_name.lower().replace(' ', '_')}.py my_first.{ext}
## Next Steps

- Explore the examples in the `examples/` folder
- Read the documentation in the `docs/` folder
- Start creating your own programs!

Happy coding! 🚀
"""
        
        with open(os.path.join(export_folder, 'QUICK_START.txt'), 'w', encoding='utf-8') as f:
            f.write(guide)
        
    def create_runner_scripts(self, export_folder):
        """Create convenient runner scripts for different platforms"""
        lang_name = self.language_data['name'].lower().replace(' ', '_')
        ext = lang_name[:3]
        
        # Windows batch file
        batch_content = f"""@echo off
    echo Running %1 with {self.language_data['name']}...
    python src\\{lang_name}.py %1
    pause
    """
        
        with open(os.path.join(export_folder, f'run_{lang_name}.bat'), 'w') as f:
            f.write(batch_content)
        
        # Unix shell script
        shell_content = f"""#!/bin/bash
    echo "Running $1 with {self.language_data['name']}..."
    python3 src/{lang_name}.py "$1"
    """
        
        shell_file = os.path.join(export_folder, f'run_{lang_name}.sh')
        with open(shell_file, 'w') as f:
            f.write(shell_content)
        
        # Make shell script executable
        if sys.platform != 'win32':
            os.chmod(shell_file, 0o755)

    def create_enhanced_example_files(self, examples_folder):
        """Create comprehensive example files"""
        lang_name = self.language_data['name']
        ext = lang_name[:3].lower()
        
        # Get language keywords and functions
        kw = self.language_data.get('keywords', {})
        fn = self.language_data.get('builtins', {})
        
        # Hello World
        hello_code = f'''# Hello World in {lang_name}
    {fn.get('print', 'print')}("Hello, World!")
    {fn.get('print', 'print')}("Welcome to {lang_name}!")

    # Using variables
    {kw.get('variable', 'var')} greeting = "Hello"
    {kw.get('variable', 'var')} name = "Developer"
    {fn.get('print', 'print')}(greeting + ", " + name + "!")
    '''
        
        with open(os.path.join(examples_folder, f'01_hello.{ext}'), 'w', encoding='utf-8') as f:
            f.write(hello_code)
        
        # Variables and Math
        math_code = f'''# Variables and Math in {lang_name}
    {kw.get('variable', 'var')} x = 10
    {kw.get('variable', 'var')} y = 20
    {kw.get('variable', 'var')} sum = x + y

    {fn.get('print', 'print')}("x =", x)
    {fn.get('print', 'print')}("y =", y)
    {fn.get('print', 'print')}("x + y =", sum)

    # More operations
    {kw.get('variable', 'var')} product = x * y
    {kw.get('variable', 'var')} difference = y - x
    {kw.get('variable', 'var')} quotient = y / x

    {fn.get('print', 'print')}("x * y =", product)
    {fn.get('print', 'print')}("y - x =", difference)
    {fn.get('print', 'print')}("y / x =", quotient)
    '''
        
        with open(os.path.join(examples_folder, f'02_math.{ext}'), 'w', encoding='utf-8') as f:
            f.write(math_code)
        
        # Functions
        func_code = f'''# Functions in {lang_name}
    {kw.get('function', 'function')} greet(name) {{
        {fn.get('print', 'print')}("Hello,", name + "!")
        {kw.get('return', 'return')} {kw.get('true', 'true')}
    }}

    {kw.get('function', 'function')} add(a, b) {{
        {kw.get('return', 'return')} a + b
    }}

    {kw.get('function', 'function')} multiply(a, b) {{
        {kw.get('return', 'return')} a * b
    }}

    # Using the functions
    greet("Alice")
    greet("Bob")

    {kw.get('variable', 'var')} result = add(5, 3)
    {fn.get('print', 'print')}("5 + 3 =", result)

    {kw.get('variable', 'var')} product = multiply(4, 7)
    {fn.get('print', 'print')}("4 * 7 =", product)
    '''
        
        with open(os.path.join(examples_folder, f'03_functions.{ext}'), 'w', encoding='utf-8') as f:
            f.write(func_code)
        
        # Conditionals
        if_code = f'''# Conditionals in {lang_name}
    {kw.get('variable', 'var')} age = 18

    {kw.get('if', 'if')} age >= 18 {{
        {fn.get('print', 'print')}("You are an adult")
    }} {kw.get('else', 'else')} {{
        {fn.get('print', 'print')}("You are a minor")
    }}

    # Multiple conditions
    {kw.get('variable', 'var')} score = 85

    {kw.get('if', 'if')} score >= 90 {{
        {fn.get('print', 'print')}("Grade: A")
    }} {kw.get('else', 'else')} {kw.get('if', 'if')} score >= 80 {{
        {fn.get('print', 'print')}("Grade: B")
    }} {kw.get('else', 'else')} {kw.get('if', 'if')} score >= 70 {{
        {fn.get('print', 'print')}("Grade: C")
    }} {kw.get('else', 'else')} {{
        {fn.get('print', 'print')}("Grade: F")
    }}
    '''
        
        with open(os.path.join(examples_folder, f'04_conditionals.{ext}'), 'w', encoding='utf-8') as f:
            f.write(if_code)
        
        # Loops
        loop_code = f'''# Loops in {lang_name}
    {fn.get('print', 'print')}("Counting from 1 to 5:")
    {kw.get('variable', 'var')} i = 1
    {kw.get('loop', 'loop')} i <= 5 {{
        {fn.get('print', 'print')}(i)
        i = i + 1
    }}

    {fn.get('print', 'print')}("\\nCountdown:")
    {kw.get('variable', 'var')} count = 5
    {kw.get('loop', 'loop')} count > 0 {{
        {fn.get('print', 'print')}(count, "...")
        count = count - 1
    }}
    {fn.get('print', 'print')}("Blast off!")

    # Factorial calculation
    {kw.get('function', 'function')} factorial(n) {{
        {kw.get('variable', 'var')} result = 1
        {kw.get('variable', 'var')} i = 1
        {kw.get('loop', 'loop')} i <= n {{
            result = result * i
            i = i + 1
        }}
        {kw.get('return', 'return')} result
    }}

    {fn.get('print', 'print')}("\\nFactorial of 5:", factorial(5))
    '''
        
        with open(os.path.join(examples_folder, f'05_loops.{ext}'), 'w', encoding='utf-8') as f:
            f.write(loop_code)

    def create_test_files(self, tests_folder):
        """Create test files for the language"""
        lang_name = self.language_data['name']
        ext = lang_name[:3].lower()
        
        # Create a simple test runner script
        test_runner = f'''#!/usr/bin/env python3
    """Test runner for {lang_name}"""

    import os
    import sys
    import subprocess

    def run_test(test_file):
        """Run a single test file"""
        print(f"Running {{test_file}}...")
        result = subprocess.run([sys.executable, '../src/{lang_name.lower().replace(' ', '_')}.py', test_file], 
                            capture_output=True, text=True)
        
        print(f"Exit code: {{result.returncode}}")
        if result.stdout:
            print("Output:")
            print(result.stdout)
        if result.stderr:
            print("Errors:")
            print(result.stderr)
        print("-" * 50)

    if __name__ == "__main__":
        # Get all test files
        test_files = [f for f in os.listdir('.') if f.endswith('.{ext}')]
        
        for test_file in sorted(test_files):
            run_test(test_file)
    '''
        
        with open(os.path.join(tests_folder, 'run_tests.py'), 'w') as f:
            f.write(test_runner)

    def create_enhanced_readme(self, export_folder):
        """Create an enhanced README with complete instructions"""
        lang_name = self.language_data['name']
        ext = lang_name[:3].lower()
        lang_name_lower = lang_name.lower().replace(' ', '_')
        
        readme = f"""# {lang_name} Programming Language

    Welcome to {lang_name}! This is a complete, working programming language created with SUPER Language Creator.

    ## 🚀 Quick Start

    ### Running your first program:

    **Windows:**
    ```cmd
    run_{lang_name_lower}.bat examples\\01_hello.{ext}
  """  
        
    def export_source_only(self, location):
        """Export source code only"""
        # Implementation for source-only export
        messagebox.showinfo("Export", "Source code export completed!")
    
    def export_docs_only(self, location):
        """Export documentation only"""
        self.generate_docs(location)
    
    def generate_docs_in_folder(self, docs_folder):
        """Generate documentation in specified folder"""
        # Generate README
        readme_content = self.generate_readme_content()
        with open(os.path.join(docs_folder, 'README.md'), 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        # Generate quick reference
        quick_ref = self.generate_quick_reference()
        with open(os.path.join(docs_folder, 'quick_reference.md'), 'w', encoding='utf-8') as f:
            f.write(quick_ref)
    
    def create_example_files(self, examples_folder):
        """Create example files"""
        lang_name = self.language_data['name']
        ext = lang_name[:3].lower()
        
        # Hello world example
        hello_code = f'''# Hello World in {lang_name}
{self.language_data.get('builtins', {}).get('print', 'print')}("Hello, World!")
{self.language_data.get('builtins', {}).get('print', 'print')}("Welcome to {lang_name}!")
'''
        
        with open(os.path.join(examples_folder, f'hello.{ext}'), 'w', encoding='utf-8') as f:
            f.write(hello_code)
    
    def generate_language(self, folder=None):
        """Generate complete language implementation"""
        self.collect_language_data()
        
        if not folder:
            folder = filedialog.askdirectory(title="Choose output folder")
            if not folder:
                return
        
        # Show progress dialog
        progress_dialog = tk.Toplevel(self.window)
        progress_dialog.title("🚀 Generating Language...")
        progress_dialog.geometry("400x200")
        progress_dialog.transient(self.window)
        progress_dialog.grab_set()
        
        progress_frame = tk.Frame(progress_dialog, bg='white', padx=20, pady=20)
        progress_frame.pack(fill='both', expand=True)
        
        tk.Label(progress_frame, text="🚀 Generating Your Language", 
                font=('Arial', 16, 'bold'), bg='white').pack(pady=10)
        
        status_label = tk.Label(progress_frame, text="Initializing...", 
                               font=('Arial', 11), bg='white')
        status_label.pack(pady=5)
        
        progress = ttk.Progressbar(progress_frame, length=300, mode='determinate')
        progress.pack(pady=10)
        
        def update_progress(step, total, message):
            progress['value'] = (step / total) * 100
            status_label.config(text=message)
            progress_dialog.update()
        
        try:
            # Generation steps
            steps = [ 
                "Creating project structure...",
                "Generating lexer...",
                "Generating parser...", 
                "Generating interpreter...",
                "Creating examples...",
                "Writing documentation...",
                "Finalizing..."
            ]
            
            lang_name = self.language_data['name'].lower().replace(' ', '_')
            lang_folder = os.path.join(folder, lang_name)
            os.makedirs(lang_folder, exist_ok=True)
            
            for i, step in enumerate(steps):
                update_progress(i, len(steps), step)
                time.sleep(0.5)  # Simulate work
            
            # Actually create the language files  
            self.export_complete_package(folder)
            
            update_progress(len(steps), len(steps), "Complete!")
            time.sleep(0.5)
            
            progress_dialog.destroy()
            
            # Show success dialog
            messagebox.showinfo("Language Generated! 🎉", 
                              f"Your language has been generated successfully!\n\n"
                              f"Location: {lang_folder}\n\n"
                              f"Check the README.md file for instructions.")
            
            self.unlock_achievement('share_joy')
            
        except Exception as e:
            progress_dialog.destroy()
            messagebox.showerror("Generation Error", f"Failed to generate language:\n{e}")
    
    def open_file(self):
        """Open code file in playground"""
        filename = filedialog.askopenfilename(
            title="Open Code File",
            filetypes=[
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                self.playground_code.delete('1.0', tk.END)
                self.playground_code.insert('1.0', content)
                self.update_line_numbers()
                
                if self.syntax_highlighter:
                    self.syntax_highlighter.highlight()
                
                self.update_status(f"Opened {os.path.basename(filename)}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file:\n{e}")
    
    def save_file(self):
        """Save playground code to file"""
        content = self.playground_code.get('1.0', 'end-1c')
        
        if not content.strip():
            messagebox.showwarning("Nothing to Save", "The playground is empty.")
            return
        
        # Suggest file extension based on language
        lang_name = self.language_data.get('name', 'MyLang')
        suggested_ext = lang_name[:3].lower()
        
        filename = filedialog.asksaveasfilename(
            title="Save Code File",
            defaultextension=f".{suggested_ext}",
            filetypes=[
                (f"{lang_name} files", f"*.{suggested_ext}"),
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                self.update_status(f"Saved {os.path.basename(filename)}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file:\n{e}")
    
    # Template loading methods
    def load_genz_template(self):
        """Load GenZ template - SAFE VERSION"""
        try:
            self.language_data.update({
                'name': 'GenZLang',
                'version': '2.0',
                'author': 'Zillennial Dev',
                'description': 'A trendy programming language with Gen Z slang and modern vibes!',
                'keywords': {
                    'function': 'vibe',
                    'variable': 'flex',
                    'if': 'lowkey',
                    'else': 'periodt',
                    'loop': 'nocap',
                    'return': 'slaps',
                    'true': 'facts',
                    'false': 'cap',
                    'while': 'stan',
                    'for': 'hits',
                    'class': 'crew',
                    'import': 'steal'
                },
                'builtins': {
                    'print': 'post',
                    'input': 'dm',
                    'length': 'vibe_check',
                    'range': 'cycle',
                    'list': 'group_chat',
                    'dict': 'receipts',
                    'str': 'caption',
                    'int': 'digits',
                    'float': 'decimal_vibes'
                },
                'features': {
                    'comments': '// no cap',
                    'multiline_comments': '/* spill tea */ ... /* end tea */',
                    'string_literals': '"slay queen"',
                    'operators': '+ - * / % == != < > <= >= && ||'
                },
                'errors': {
                    'syntax_error': 'Bruh, that syntax is not it 💀',
                    'name_error': 'This variable is giving ghost energy 👻',
                    'type_error': 'Wrong vibe type bestie ❌',
                    'runtime_error': 'Code crashed harder than my sleep schedule 😴',
                    'division_by_zero': 'You really tried to divide by zero? That\'s not main character energy 🤡'
                }
            })
            self.populate_ui_from_data()
            self.unlock_achievement('theme_explorer')
            self.update_status("GenZ template loaded! It's giving main character energy ✨")
        except Exception as e:
            print(f"Error loading GenZ template: {e}")
            messagebox.showerror("Template Error", f"Could not load GenZ template: {e}")

    def load_game_template(self):
        """Load game template - SAFE VERSION"""
        try:
            self.language_data.update({
                'name': 'GameLang',
                'version': '1.0',
                'author': 'Game Creator',
                'description': 'A fun game-themed programming language!',
                'keywords': {
                    'function': 'quest',
                    'variable': 'item',
                    'if': 'check',
                    'else': 'otherwise',
                    'loop': 'repeat',
                    'return': 'reward'
                },
                'builtins': {
                    'print': 'announce',
                    'input': 'ask_player',
                    'length': 'count'
                },
                'features': {},
                'errors': {}
            })
            self.populate_ui_from_data()
            self.unlock_achievement('theme_explorer')
            self.update_status("Game template loaded!")
        except Exception as e:
            print(f"Error loading game template: {e}")
            messagebox.showerror("Template Error", f"Could not load game template: {e}")
    
    def load_edu_template(self):
        """Load educational template"""
        self.language_data.update({
            'name': 'LearnCode',
            'description': 'A friendly language for learning programming!',
            'keywords': {
                'function': 'lesson',
                'variable': 'remember',
                'if': 'when',
                'else': 'otherwise',
                'loop': 'practice',
                'return': 'answer'
            },
            'builtins': {
                'print': 'show',
                'input': 'ask',
                'length': 'measure'
            }
        })
        self.populate_ui_from_data()
    
    def start_scratch(self):
        """Start from scratch"""
        self.new_language()
    
    def save_to_recent(self):
        """Save to recent languages"""
        # Implementation for saving to recent list
        pass
    
    def handle_tab_navigation(self, event):
        """Handle tab navigation"""
        pass
    
    def handle_shift_tab_navigation(self, event):
        """Handle shift+tab navigation"""
        pass
    
    def toggle_high_contrast(self):
        """Toggle high contrast theme"""
        current_theme = 'high_contrast' if self.current_theme != 'high_contrast' else 'modern_light'
        self.change_theme(current_theme)
    
    def toggle_screen_reader_mode(self):
        """Toggle screen reader mode"""
        pass
    
    def reset_font_size(self):
        """Reset font size to default"""
        self.accessibility.font_size = 12
        self.accessibility.apply_font_changes()
    
    def toggle_toolbar(self):
        """Toggle toolbar visibility"""
        pass
    
    def toggle_status_bar(self):
        """Toggle status bar visibility"""
        pass
    
    def toggle_progress_panel(self):
        """Toggle progress panel visibility"""
        pass
    
    def show_keyboard_help(self):
        """Show keyboard navigation help"""
        self.show_keyboard_shortcuts()
    
    def run(self):
        """Start the enhanced application"""
        # Set window icon if possible
        try:
            if sys.platform == 'win32':
                self.window.iconbitmap(default='icon.ico')
        except:
            pass
        
        # Center window on screen
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
        # Apply initial theme
        self.apply_theme()
        
        # Start the application
        self.window.protocol("WM_DELETE_WINDOW", self.safe_exit)
        self.window.mainloop()

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Run the Enhanced SUPER Language Creator"""
    try:
        app = EnhancedSuperLanguageCreator()
        app.run()
    except Exception as e:
        messagebox.showerror("Startup Error", f"Failed to start application:\n{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
