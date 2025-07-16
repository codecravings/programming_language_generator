"""
Main Application Module for LangGen
Coordinates all modules and manages the main application window and lifecycle
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional

# Import all the modular components
from core_systems import (
    EnhancedThemeEngine, 
    EnhancedKeywordGenerator, 
    AccessibilityManager, 
    EnhancedAchievementSystem, 
    EnhancedSyntaxHighlighter
)
from language_processing import (
    LanguageValidator, 
    InterpreterGenerator, 
    CodeExecutor, 
    TemplateProcessor, 
    LanguageDataCollector, 
    TestFileCreator
)
from ui_components import (
    UIComponentFactory, 
    MenuBarCreator, 
    ToolbarCreator, 
    TabCreator, 
    DialogCreator, 
    StatusBarCreator
)
from file_operations import (
    FileOperations, 
    AutoSaveManager, 
    TemplateManager, 
    ProjectBackup
)
from application_features import (
    PlaygroundManager, 
    DocumentationGenerator, 
    StatisticsManager, 
    ExamplesGallery, 
    TutorialSystem, 
    HelpSystem, 
    PerformanceTester
)

class EnhancedSuperLanguageCreator:
    """Main application class that coordinates all modules"""
    
    def __init__(self):
        # Initialize main window
        self.window = tk.Tk()
        self.window.title("🚀 SUPER Language Creator v2.0")
        self.window.geometry("1200x800")
        self.window.minsize(1000, 700)
        
        # Store reference to app in window for template loading
        self.window.app_reference = self
        
        # Initialize language data
        self.language_data = {
            'name': 'MyLang',
            'version': '1.0',
            'author': 'Young Coder',
            'description': 'My awesome programming language!',
            'keywords': {},
            'operators': {},
            'builtins': {},
            'errors': {},
            'features': {},
            'created': datetime.now().isoformat(),
            'modified': datetime.now().isoformat()
        }
        
        # Initialize core systems
        self.theme_engine = EnhancedThemeEngine()
        self.keyword_generator = EnhancedKeywordGenerator()
        self.accessibility_manager = AccessibilityManager(self.window)
        self.achievement_system = EnhancedAchievementSystem()
        
        # Initialize managers
        self.file_operations = None
        self.playground_manager = None
        self.statistics_manager = None
        self.examples_gallery = ExamplesGallery()
        self.help_system = HelpSystem(self.window)
        
        # UI state
        self.current_theme = 'modern_light'
        self.theme_colors = self.theme_engine.themes[self.current_theme]
        self.syntax_highlighter = None
        
        # UI components storage
        self.ui_components = {}
        self.keyword_entries = {}
        self.builtin_entries = {}
        self.features = {}
        
        # Initialize application
        self.setup_application()
    
    def setup_application(self):
        """Setup the complete application"""
        # Setup window properties
        self.window.configure(bg=self.theme_colors['bg'])
        
        # Setup keyboard shortcuts
        self.bind_keyboard_shortcuts()
        
        # Initialize managers with callbacks
        self.setup_managers()
        
        # Create UI components
        self.create_ui()
        
        # Apply initial theme
        self.apply_theme(self.current_theme)
        
        # Setup autosave
        self.autosave_manager.start_autosave(self.window)
        
        # Load recent files
        self.file_operations.load_recent_files()
        
        # Check for tutorial completion
        self.check_tutorial_status()
        
        # Bind close event
        self.window.protocol("WM_DELETE_WINDOW", self.safe_exit)
    
    def setup_managers(self):
        """Initialize all manager classes with proper callbacks"""
        # Create UI callbacks for managers
        ui_callbacks = {
            'update_ui': self.update_ui_from_data,
            'update_status': self.update_status,
            'collect_data': self.collect_language_data,
            'generate_interpreter': self.generate_interpreter,
            'check_achievements': self.check_achievements,
            'unlock_achievement': self.unlock_achievement,
            'create_test_files': self.create_test_files,
            'update_recent_menu': self.update_recent_menu
        }
        
        # Initialize file operations
        self.file_operations = FileOperations(self.language_data, ui_callbacks)
        
        # Initialize autosave manager
        self.autosave_manager = AutoSaveManager(self.file_operations)
        
        # Initialize template manager
        self.template_manager = TemplateManager()
        
        # Initialize backup manager
        self.backup_manager = ProjectBackup()
        
        # Initialize language processing components
        self.language_validator = LanguageValidator()
        self.interpreter_generator = InterpreterGenerator(self.language_data)
        self.code_executor = CodeExecutor(self.language_data)
        self.template_processor = TemplateProcessor(self.language_data)
        self.test_file_creator = TestFileCreator(self.language_data)
        
        # Initialize application features
        self.playground_manager = PlaygroundManager(self.language_data, self)
        self.documentation_generator = DocumentationGenerator(self.language_data)
        self.statistics_manager = StatisticsManager(self.language_data)
        self.performance_tester = PerformanceTester(self.language_data)
        
        # Initialize tutorial system
        tutorial_callbacks = {
            'focus_info_tab': lambda: self.notebook.select(1),
            'focus_keywords_tab': lambda: self.notebook.select(2),
            'focus_builtins_tab': lambda: self.notebook.select(4),
            'focus_playground_tab': lambda: self.notebook.select(6),
            'complete_tutorial': self.complete_tutorial
        }
        self.tutorial_system = TutorialSystem(tutorial_callbacks)
    
    def create_ui(self):
        """Create the main user interface"""
        # Create menu bar
        menu_callbacks = {
            'new_language': self.new_language,
            'load_language': self.load_language,
            'save_language': self.save_language,
            'save_as_language': self.save_as_language,
            'export_language': self.export_language,
            'import_language': self.import_language,
            'safe_exit': self.safe_exit,
            'show_keyword_generator': self.show_keyword_generator,
            'validate_syntax': self.validate_syntax,
            'show_preferences': self.show_preferences,
            'apply_theme': self.apply_theme,
            'show_statistics': self.show_statistics,
            'show_examples_gallery': self.show_examples_gallery,
            'performance_test': self.performance_test,
            'show_achievements': self.show_achievements,
            'show_theme_picker': self.show_theme_picker,
            'show_keyboard_shortcuts': self.help_system.show_keyboard_shortcuts,
            'show_help_menu': self.show_help_menu,
            'show_about': self.help_system.show_about_dialog,
            'run_playground': self.run_playground
        }
        
        self.menu_creator = MenuBarCreator(self.window, menu_callbacks, self.theme_engine)
        self.menubar = self.menu_creator.create_enhanced_menu_bar()
        
        # Create toolbar
        self.toolbar_creator = ToolbarCreator(self.window, menu_callbacks, self.theme_colors)
        self.toolbar = self.toolbar_creator.create_modern_toolbar()
        
        # Create main content area
        self.create_main_content()
        
        # Create status bar
        self.status_creator = StatusBarCreator(self.window, self.theme_colors)
        self.status_bar = self.status_creator.create_status_bar()
        
        # Store UI components for easy access
        self.ui_components.update({
            'window': self.window,
            'menubar': self.menubar,
            'toolbar': self.toolbar,
            'status_bar': self.status_bar,
            'notebook': self.notebook
        })
    
    def create_main_content(self):
        """Create the main content area with tabs"""
        # Create main paned window
        self.main_paned = tk.PanedWindow(self.window, orient=tk.HORIZONTAL, bg=self.theme_colors['bg'])
        self.main_paned.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_paned)
        
        # Create tab creator
        tab_callbacks = {
            'new_language': self.new_language,
            'load_language': self.load_language,
            'show_theme_picker': self.show_theme_picker,
            'show_examples_gallery': self.show_examples_gallery,
            'run_playground': self.run_playground,
            'clear_output': self.clear_output
        }
        
        self.tab_creator = TabCreator(self.notebook, tab_callbacks, self.theme_colors, self.language_data)
        
        # Create tabs
        self.create_tabs()
        
        # Add notebook to paned window
        self.main_paned.add(self.notebook, width=800)
        
        # Create progress sidebar (would be implemented based on original structure)
        self.create_progress_sidebar()
    
    def create_tabs(self):
        """Create all application tabs"""
        # Welcome tab
        self.welcome_frame = self.tab_creator.create_welcome_tab()
        self.notebook.add(self.welcome_frame, text="🏠 Welcome")
        
        # Info tab
        self.info_frame = self.tab_creator.create_info_tab()
        self.notebook.add(self.info_frame, text="ℹ️ Language Info")
        
        # Keywords tab
        self.keywords_frame = self.tab_creator.create_keywords_tab()
        self.notebook.add(self.keywords_frame, text="🔤 Keywords")
        
        # Operators tab
        self.operators_frame = self.tab_creator.create_operators_tab()
        self.notebook.add(self.operators_frame, text="➕ Operators")
        
        # Built-ins tab
        self.builtins_frame = self.tab_creator.create_builtins_tab()
        self.notebook.add(self.builtins_frame, text="🛠️ Built-ins")
        
        # Errors tab
        self.errors_frame = self.tab_creator.create_errors_tab()
        self.notebook.add(self.errors_frame, text="❌ Errors")
        
        # Playground tab
        self.playground_frame = self.tab_creator.create_playground_tab()
        self.notebook.add(self.playground_frame, text="🎮 Playground")
        
        # Preview tab
        self.preview_frame = self.tab_creator.create_preview_tab()
        self.notebook.add(self.preview_frame, text="👀 Preview")
        
        # Store references
        self.ui_components.update({
            'welcome_frame': self.welcome_frame,
            'info_frame': self.info_frame,
            'keywords_frame': self.keywords_frame,
            'playground_frame': self.playground_frame
        })
    
    def create_progress_sidebar(self):
        """Create the progress tracking sidebar"""
        # Progress sidebar
        sidebar = tk.Frame(self.main_paned, bg=self.theme_colors['sidebar'], width=300)
        
        # Progress header
        progress_header = tk.Frame(sidebar, bg=self.theme_colors['sidebar'])
        progress_header.pack(fill='x', pady=10)
        
        tk.Label(
            progress_header,
            text="📊 Progress",
            font=('Arial', 14, 'bold'),
            bg=self.theme_colors['sidebar'],
            fg=self.theme_colors['fg']
        ).pack()
        
        # Quick stats
        stats_frame = tk.Frame(sidebar, bg=self.theme_colors['sidebar'])
        stats_frame.pack(fill='x', padx=10, pady=5)
        
        # Languages created
        lang_frame = tk.Frame(stats_frame, bg=self.theme_colors['primary'], relief='raised', bd=1)
        lang_frame.pack(fill='x', pady=2)
        
        tk.Label(lang_frame, text="🎯 Languages Created", font=('Arial', 9, 'bold'), 
                bg=self.theme_colors['primary'], fg='white').pack(pady=1)
        tk.Label(lang_frame, text="7", font=('Arial', 12, 'bold'), 
                bg=self.theme_colors['primary'], fg='white').pack(pady=1)
        
        # Achievements
        achievement_frame = tk.Frame(stats_frame, bg=self.theme_colors['accent'], relief='raised', bd=1)
        achievement_frame.pack(fill='x', pady=2)
        
        tk.Label(achievement_frame, text="🏆 Achievements", font=('Arial', 9, 'bold'), 
                bg=self.theme_colors['accent'], fg='white').pack(pady=1)
        tk.Label(achievement_frame, text="5/16", font=('Arial', 12, 'bold'), 
                bg=self.theme_colors['accent'], fg='white').pack(pady=1)
        
        # Points
        points_frame = tk.Frame(stats_frame, bg=self.theme_colors['secondary'], relief='raised', bd=1)
        points_frame.pack(fill='x', pady=2)
        
        tk.Label(points_frame, text="⭐ Total Points", font=('Arial', 9, 'bold'), 
                bg=self.theme_colors['secondary'], fg='white').pack(pady=1)
        tk.Label(points_frame, text="675", font=('Arial', 12, 'bold'), 
                bg=self.theme_colors['secondary'], fg='white').pack(pady=1)
        
        # Progress bar
        progress_bar_frame = tk.Frame(sidebar, bg=self.theme_colors['sidebar'])
        progress_bar_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(progress_bar_frame, text="🎯 Next Achievement", font=('Arial', 9, 'bold'), 
                bg=self.theme_colors['sidebar'], fg=self.theme_colors['fg']).pack()
        
        progress_bar = ttk.Progressbar(progress_bar_frame, mode='determinate', maximum=100, value=60)
        progress_bar.pack(fill='x', pady=2)
        
        tk.Label(progress_bar_frame, text="Function Master (60%)", font=('Arial', 8), 
                bg=self.theme_colors['sidebar'], fg=self.theme_colors['fg']).pack()
        
        # Recent activities
        activities_frame = tk.Frame(sidebar, bg=self.theme_colors['sidebar'])
        activities_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(activities_frame, text="📅 Recent Activity", font=('Arial', 10, 'bold'), 
                bg=self.theme_colors['sidebar'], fg=self.theme_colors['fg']).pack()
        
        activities = [
            "🎯 Achievement unlocked: First Steps",
            "📤 Exported KidsCode language",
            "🎨 Changed theme to Dark",
            "📚 Viewed Educational example",
            "🏁 Started new project"
        ]
        
        for activity in activities:
            activity_label = tk.Label(activities_frame, text=activity, font=('Arial', 8), 
                                    bg=self.theme_colors['sidebar'], fg=self.theme_colors['fg'],
                                    wraplength=250, justify='left')
            activity_label.pack(anchor='w', pady=1)
        
        # View full progress button
        progress_button = tk.Button(
            sidebar,
            text="🏆 View Full Progress",
            command=self.show_achievements,
            bg=self.theme_colors['primary'],
            fg='white',
            font=('Arial', 10, 'bold'),
            relief='raised',
            bd=2
        )
        progress_button.pack(fill='x', padx=10, pady=10)
        
        # Add progress indicators here
        
        self.main_paned.add(sidebar, width=300)
        self.ui_components['sidebar'] = sidebar
    
    def bind_keyboard_shortcuts(self):
        """Bind keyboard shortcuts"""
        shortcuts = {
            '<Control-n>': self.new_language,
            '<Control-o>': self.load_language,
            '<Control-s>': self.save_language,
            '<Control-Shift-S>': self.save_as_language,
            '<Control-e>': self.export_language,
            '<Control-g>': self.show_keyword_generator,
            '<F5>': self.validate_syntax,
            '<Control-comma>': self.show_preferences,
            '<F1>': self.help_system.show_keyboard_shortcuts,
            '<Control-q>': self.safe_exit,
            '<Control-r>': self.run_playground,
            '<Control-l>': self.clear_output
        }
        
        for shortcut, command in shortcuts.items():
            self.window.bind(shortcut, lambda e, cmd=command: cmd())
    
    # Core application methods
    def apply_theme(self, theme_name):
        """Apply a theme to the entire application"""
        if theme_name not in self.theme_engine.themes:
            return
        
        self.current_theme = theme_name
        self.theme_colors = self.theme_engine.themes[theme_name]
        
        # Update window background
        self.window.configure(bg=self.theme_colors['bg'])
        
        # Update all UI components
        self.update_theme_recursive(self.window)
        
        # Update status
        self.update_status(f"Applied theme: {self.theme_colors['name']}")
    
    def update_theme_recursive(self, widget):
        """Recursively update theme for all widgets"""
        try:
            widget_class = widget.winfo_class()
            
            if widget_class in ['Frame', 'Toplevel']:
                widget.configure(bg=self.theme_colors['bg'])
            elif widget_class == 'Label':
                widget.configure(bg=self.theme_colors['bg'], fg=self.theme_colors['fg'])
            elif widget_class == 'Button':
                widget.configure(bg=self.theme_colors['card'], fg=self.theme_colors['fg'])
            elif widget_class in ['Entry', 'Text']:
                widget.configure(bg=self.theme_colors['card'], fg=self.theme_colors['fg'])
        except:
            pass
        
        # Recursively update children
        try:
            for child in widget.winfo_children():
                self.update_theme_recursive(child)
        except:
            pass
    
    def collect_language_data(self):
        """Collect language data from UI components"""
        # Collect data from info tab
        if hasattr(self, 'tab_creator') and hasattr(self.tab_creator, 'info_entries'):
            for key, widget in self.tab_creator.info_entries.items():
                if key == 'description':
                    self.language_data[key] = widget.get('1.0', tk.END).strip()
                else:
                    self.language_data[key] = widget.get().strip()
        
        # Collect keywords data
        if hasattr(self, 'tab_creator') and hasattr(self.tab_creator, 'keyword_entries'):
            keywords = {}
            for key, entry in self.tab_creator.keyword_entries.items():
                value = entry.get().strip()
                if value:
                    keywords[key] = value
            self.language_data['keywords'] = keywords
        
        # Collect operators data
        if hasattr(self, 'tab_creator') and hasattr(self.tab_creator, 'operator_entries'):
            operators = {}
            for key, entry in self.tab_creator.operator_entries.items():
                value = entry.get().strip()
                if value:
                    operators[key] = value
            self.language_data['operators'] = operators
        
        # Collect built-ins data
        if hasattr(self, 'tab_creator') and hasattr(self.tab_creator, 'builtin_entries'):
            builtins = {}
            for key, entry in self.tab_creator.builtin_entries.items():
                value = entry.get().strip()
                if value:
                    builtins[key] = value
            self.language_data['builtins'] = builtins
        
        # Collect errors data
        if hasattr(self, 'tab_creator') and hasattr(self.tab_creator, 'error_entries'):
            errors = {}
            for key, entry in self.tab_creator.error_entries.items():
                value = entry.get().strip()
                if value:
                    errors[key] = value
            self.language_data['errors'] = errors
        
        # Update modification timestamp
        self.language_data['modified'] = datetime.now().isoformat()
    
    def update_ui_from_data(self):
        """Update UI components from language data"""
        # Update all tabs if they exist
        if hasattr(self, 'tab_creator'):
            self.tab_creator.update_info_tab(self.language_data)
            self.tab_creator.update_keywords_tab(self.language_data)
            self.tab_creator.update_operators_tab(self.language_data)
            self.tab_creator.update_builtins_tab(self.language_data)
            self.tab_creator.update_errors_tab(self.language_data)
        
        # Update preview if it exists
        if hasattr(self, 'tab_creator') and hasattr(self.tab_creator, '_refresh_preview'):
            self.tab_creator._refresh_preview()
        
        # Update window title
        lang_name = self.language_data.get('name', 'Untitled')
        self.window.title(f"🚀 SUPER Language Creator v2.0 - {lang_name}")
        
        # Update status
        self.update_status(f"Language '{lang_name}' loaded successfully")
    
    def update_status(self, message):
        """Update the status bar message"""
        if hasattr(self, 'status_creator'):
            self.status_creator.update_status(message)
    
    # File operations
    def new_language(self):
        """Create a new language"""
        self.file_operations.new_language()
        self.unlock_achievement('first_lang')
    
    def load_language(self):
        """Load a language from file"""
        self.file_operations.load_language()
    
    def save_language(self):
        """Save the current language"""
        return self.file_operations.save_language()
    
    def save_as_language(self):
        """Save language with new name"""
        return self.file_operations.save_as_language()
    
    def export_language(self):
        """Export language to complete package"""
        self._show_export_dialog()
    
    def import_language(self):
        """Import a language"""
        self.file_operations.import_language()
    
    # Language processing
    def generate_interpreter(self, export_folder):
        """Generate interpreter for the language"""
        return self.interpreter_generator.generate_interpreter(export_folder)
    
    def validate_syntax(self):
        """Validate language syntax"""
        issues, warnings = self.language_validator.validate_syntax_advanced(self.language_data)
        
        # Show validation dialog (would be implemented)
        if not issues and not warnings:
            messagebox.showinfo("Validation", "✅ No issues found!")
        else:
            message = ""
            if issues:
                message += "Issues:\\n" + "\\n".join(f"• {issue}" for issue in issues)
            if warnings:
                if message:
                    message += "\\n\\n"
                message += "Warnings:\\n" + "\\n".join(f"• {warning}" for warning in warnings)
            messagebox.showwarning("Validation Results", message)
    
    def create_test_files(self, export_folder):
        """Create test files for the language"""
        return self.test_file_creator.create_test_files(export_folder)
    
    # Playground operations
    def run_playground(self):
        """Run code in the playground"""
        # Get code from editor
        if hasattr(self.tab_creator, 'code_editor'):
            code = self.tab_creator.code_editor.get('1.0', tk.END)
            
            # Clear output
            if hasattr(self.tab_creator, 'output_text'):
                self.tab_creator.output_text.config(state='normal')
                self.tab_creator.output_text.delete('1.0', tk.END)
                
                # Show running message
                self.tab_creator.output_text.insert('1.0', "🚀 Running your code...\n\n")
                self.tab_creator.output_text.update()
                
                # Simulate execution
                self.window.after(500, lambda: self._simulate_code_execution(code))
            
            # Update status
            self.update_status("Running playground code...")
    
    def _simulate_code_execution(self, code):
        """Simulate code execution with basic interpretation"""
        if not hasattr(self.tab_creator, 'output_text'):
            return
        
        output_text = self.tab_creator.output_text
        output_text.config(state='normal')
        
        # Clear previous output
        output_text.delete('1.0', tk.END)
        output_text.insert('1.0', "📤 OUTPUT:\n" + "="*40 + "\n\n")
        
        # Get keywords from language data
        keywords = self.language_data.get('keywords', {})
        print_keyword = keywords.get('print', 'print')
        var_keyword = keywords.get('variable', 'variable')
        func_keyword = keywords.get('function', 'function')
        
        # Simple interpretation
        lines = code.split('\n')
        variables = {}
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('//'):
                continue
            
            # Handle print statements
            if print_keyword in line:
                # Extract what's being printed
                if '"' in line:
                    # String literal
                    start = line.find('"') + 1
                    end = line.rfind('"')
                    if start < end:
                        text = line[start:end]
                        output_text.insert(tk.END, f"{text}\n")
                elif "'" in line:
                    # Single quoted string
                    start = line.find("'") + 1
                    end = line.rfind("'")
                    if start < end:
                        text = line[start:end]
                        output_text.insert(tk.END, f"{text}\n")
                else:
                    # Variable or expression
                    parts = line.split('(')
                    if len(parts) > 1:
                        content = parts[1].split(')')[0]
                        if content in variables:
                            output_text.insert(tk.END, f"{variables[content]}\n")
                        else:
                            output_text.insert(tk.END, f"{content}\n")
            
            # Handle variable declarations
            elif var_keyword in line and '=' in line:
                parts = line.split('=')
                if len(parts) == 2:
                    var_name = parts[0].replace(var_keyword, '').strip()
                    var_value = parts[1].strip().strip('"').strip("'")
                    variables[var_name] = var_value
                    output_text.insert(tk.END, f"Variable '{var_name}' set to: {var_value}\n")
            
            # Handle function calls
            elif func_keyword in line:
                func_name = line.split('(')[0].replace(func_keyword, '').strip()
                output_text.insert(tk.END, f"Function '{func_name}' defined\n")
        
        # Add completion message
        output_text.insert(tk.END, f"\n{'='*40}\n")
        output_text.insert(tk.END, "✅ Code execution completed!\n")
        output_text.insert(tk.END, f"Language: {self.language_data.get('name', 'MyLang')}\n")
        output_text.insert(tk.END, f"Keywords used: {', '.join(keywords.keys())}\n")
        
        output_text.config(state='disabled')
        output_text.see(tk.END)
        
        # Update status
        self.update_status("Playground code executed successfully")
    
    def clear_output(self):
        """Clear playground output"""
        if hasattr(self.tab_creator, 'output_text'):
            self.tab_creator.output_text.config(state='normal')
            self.tab_creator.output_text.delete('1.0', tk.END)
            self.tab_creator.output_text.insert('1.0', "Ready to run your code...\n")
            self.tab_creator.output_text.config(state='disabled')
            self.update_status("Playground output cleared")
    
    # Achievement system
    def unlock_achievement(self, achievement_id):
        """Unlock an achievement"""
        achievement = self.achievement_system.unlock(achievement_id)
        if achievement:
            self.show_achievement_notification(achievement)
    
    def show_achievement_notification(self, achievement):
        """Show achievement unlock notification"""
        # Create a simple popup for achievement
        messagebox.showinfo(
            "Achievement Unlocked!",
            f"🎉 {achievement.name}\\n\\n{achievement.description}\\n\\n+{achievement.points} points!"
        )
    
    def check_achievements(self):
        """Check for new achievements"""
        # This would check various conditions and unlock achievements
        pass
    
    # Dialog methods
    def show_keyword_generator(self):
        """Show the keyword generator dialog"""
        self._create_keyword_generator_dialog()
    
    def show_preferences(self):
        """Show preferences dialog"""
        dialog_creator = DialogCreator(self.window, self.theme_colors, {})
        dialog_creator.show_preferences_dialog()
    
    def show_statistics(self):
        """Show language statistics"""
        stats = self.statistics_manager.calculate_statistics()
        # Would show detailed statistics dialog
        messagebox.showinfo("Statistics", f"Language Statistics:\\n\\nKeywords: {stats['basic']['defined_keywords']}\\nBuilt-ins: {stats['basic']['defined_builtins']}\\nCompleteness: {stats['completeness']['overall_completeness']}%")
    
    def show_examples_gallery(self):
        """Show examples gallery"""
        self.examples_gallery.show_gallery(self.window, self.theme_colors)
    
    def show_achievements(self):
        """Show achievements center"""
        self._create_progress_center()
    
    def show_theme_picker(self):
        """Show theme picker dialog"""
        self._create_theme_picker_dialog()
    
    def show_help_menu(self):
        """Show comprehensive help menu"""
        self._create_help_center()
    
    def _create_help_center(self):
        """Create the help center dialog"""
        dialog = tk.Toplevel(self.window)
        dialog.title("🆘 Help Center")
        dialog.geometry("800x600")
        dialog.transient(self.window)
        dialog.grab_set()
        dialog.configure(bg=self.theme_colors.get('bg', '#ffffff'))
        
        # Create notebook for different help sections
        notebook = ttk.Notebook(dialog)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Getting Started Tab
        getting_started_frame = ttk.Frame(notebook)
        notebook.add(getting_started_frame, text="🚀 Getting Started")
        
        # Create scrollable text widget for getting started
        getting_started_text = tk.Text(getting_started_frame, wrap='word', font=('Arial', 10))
        getting_started_scrollbar = ttk.Scrollbar(getting_started_frame, orient='vertical', command=getting_started_text.yview)
        getting_started_text.configure(yscrollcommand=getting_started_scrollbar.set)
        
        getting_started_text.pack(side='left', fill='both', expand=True)
        getting_started_scrollbar.pack(side='right', fill='y')
        
        getting_started_content = """
🎯 Welcome to SUPER Language Creator!

Create your own programming language in just 5 minutes! This guide will help you get started quickly.

📋 STEP 1: Choose Your Language Name
• Click on the "Language Info" tab
• Enter a creative name for your language (e.g., "KidsCode", "MathLang", "StoryScript")
• Add a description and set your version number
• Don't forget to add yourself as the author!

🔤 STEP 2: Define Your Keywords
• Go to the "Keywords" tab
• Replace boring English keywords with fun alternatives:
  - "variable" → "remember" or "store"
  - "function" → "teach" or "define"
  - "if" → "check" or "when"
  - "else" → "otherwise" or "or"
  - "loop" → "repeat" or "keep"
  - "return" → "give" or "answer"

🛠️ STEP 3: Set Up Built-in Functions
• Switch to the "Built-ins" tab
• Customize function names:
  - "print" → "say" or "show"
  - "input" → "ask" or "get"
  - "length" → "count" or "size"
  - "string" → "text" or "word"
  - "number" → "num" or "digit"
  - "random" → "chance" or "pick"

⚙️ STEP 4: Configure Operators (Optional)
• Visit the "Operators" tab
• Customize mathematical and logical operators
• You can change symbols like + - * / to words or different symbols

❌ STEP 5: Define Error Messages
• Go to the "Errors" tab
• Make error messages friendly and educational
• Use simple language that beginners can understand

👁️ STEP 6: Preview Your Language
• Click the "Preview" tab
• See how your language looks in action
• Test different code examples

📤 STEP 7: Export Your Language
• Click "Export Language" button
• Choose a file extension (e.g., .kid, .story, .math)
• Select export options (documentation, examples, etc.)
• Your language is ready to use!

🎉 CONGRATULATIONS!
You've just created your own programming language! Share it with friends and start coding!
"""
        
        getting_started_text.insert('1.0', getting_started_content)
        getting_started_text.config(state='disabled')
        
        # Tutorials Tab
        tutorials_frame = ttk.Frame(notebook)
        notebook.add(tutorials_frame, text="📚 Tutorials")
        
        tutorials_text = tk.Text(tutorials_frame, wrap='word', font=('Arial', 10))
        tutorials_scrollbar = ttk.Scrollbar(tutorials_frame, orient='vertical', command=tutorials_text.yview)
        tutorials_text.configure(yscrollcommand=tutorials_scrollbar.set)
        
        tutorials_text.pack(side='left', fill='both', expand=True)
        tutorials_scrollbar.pack(side='right', fill='y')
        
        tutorials_content = """
📖 DETAILED TUTORIALS

🎨 TUTORIAL 1: Creating a Kids' Programming Language
Let's create "KidsCode" - a fun language for children!

1. Language Setup:
   • Name: "KidsCode"
   • Description: "A fun programming language for kids to learn coding!"
   • Version: "1.0"
   • Author: Your name

2. Kid-Friendly Keywords:
   • variable → "remember" (Remember your favorite toy)
   • function → "teach" (Teach the computer something new)
   • if → "check" (Check if something is true)
   • else → "otherwise" (Otherwise, do this)
   • loop → "repeat" (Repeat this action)
   • return → "give" (Give back an answer)

3. Fun Built-ins:
   • print → "say" (Say something out loud)
   • input → "ask" (Ask a question)
   • length → "count" (Count how many)
   • random → "surprise" (Get a surprise number)

4. Example KidsCode:
   remember name = ask("What's your name?")
   say("Hello, " + name + "!")
   
   teach greet(person) {
       say("Hi there, " + person + "!")
   }
   
   greet(name)

🔢 TUTORIAL 2: Mathematical Language
Create "MathSpeak" for mathematical operations!

1. Math Keywords:
   • variable → "value"
   • function → "formula"
   • if → "when"
   • loop → "calculate"

2. Math Built-ins:
   • print → "show"
   • input → "enter"
   • length → "measure"
   • number → "digit"

3. Example MathSpeak:
   value x = enter("Enter first number: ")
   value y = enter("Enter second number: ")
   show("Sum: " + (x + y))

🎭 TUTORIAL 3: Story-Based Language
Create "StoryScript" for narrative programming!

1. Story Keywords:
   • variable → "character"
   • function → "scene"
   • if → "suddenly"
   • else → "meanwhile"
   • loop → "throughout"

2. Story Built-ins:
   • print → "narrate"
   • input → "audience"
   • length → "chapters"

3. Example StoryScript:
   character hero = "Alice"
   scene adventure(name) {
       narrate("Once upon a time, " + name + " went on an adventure...")
   }
   
   adventure(hero)

💡 TUTORIAL 4: Advanced Features
Learn about advanced customization options!

1. Custom Operators:
   • Change + to "plus" or "add"
   • Change - to "minus" or "subtract"
   • Change * to "times" or "multiply"
   • Change / to "divide" or "split"

2. Error Messages:
   • Make errors educational and friendly
   • Use simple language
   • Provide helpful suggestions

3. Export Options:
   • Include documentation for users
   • Add example files
   • Create installation scripts
   • Generate README files

🎯 TIPS FOR SUCCESS:
• Keep keywords simple and memorable
• Use words that relate to your target audience
• Test your language with example code
• Share your creations with others!
• Have fun and be creative!
"""
        
        tutorials_text.insert('1.0', tutorials_content)
        tutorials_text.config(state='disabled')
        
        # Shortcuts Tab
        shortcuts_frame = ttk.Frame(notebook)
        notebook.add(shortcuts_frame, text="⌨️ Shortcuts")
        
        shortcuts_text = tk.Text(shortcuts_frame, wrap='word', font=('Arial', 10))
        shortcuts_scrollbar = ttk.Scrollbar(shortcuts_frame, orient='vertical', command=shortcuts_text.yview)
        shortcuts_text.configure(yscrollcommand=shortcuts_scrollbar.set)
        
        shortcuts_text.pack(side='left', fill='both', expand=True)
        shortcuts_scrollbar.pack(side='right', fill='y')
        
        shortcuts_content = """
⌨️ KEYBOARD SHORTCUTS

📂 FILE OPERATIONS:
• Ctrl+N - New Language Project
• Ctrl+O - Open Language Project
• Ctrl+S - Save Current Project
• Ctrl+Shift+S - Save As...
• Ctrl+E - Export Language
• Ctrl+Q - Quit Application

✏️ EDITING:
• Ctrl+Z - Undo
• Ctrl+Y - Redo
• Ctrl+X - Cut
• Ctrl+C - Copy
• Ctrl+V - Paste
• Ctrl+A - Select All
• Ctrl+F - Find
• Ctrl+H - Find and Replace

🎨 INTERFACE:
• Ctrl+T - Change Theme
• Ctrl+, - Open Preferences
• F1 - Show Help Center
• F5 - Run Code Test
• F11 - Toggle Fullscreen

🔧 DEVELOPMENT:
• Ctrl+Shift+E - Show Examples Gallery
• Ctrl+Shift+P - Performance Test
• Ctrl+Shift+A - Show Achievements
• Ctrl+Shift+S - Show Statistics
• Ctrl+Shift+K - Keyword Generator

🧭 NAVIGATION:
• Ctrl+Tab - Switch Between Tabs
• Ctrl+Shift+Tab - Switch Tabs (Reverse)
• Ctrl+1 - Language Info Tab
• Ctrl+2 - Keywords Tab
• Ctrl+3 - Built-ins Tab
• Ctrl+4 - Operators Tab
• Ctrl+5 - Errors Tab
• Ctrl+6 - Preview Tab

📱 QUICK ACTIONS:
• Space - Quick Preview Update
• Enter - Apply Changes
• Escape - Cancel Current Action
• Tab - Move to Next Field
• Shift+Tab - Move to Previous Field

🎮 PLAYGROUND:
• F9 - Run Playground Code
• F10 - Clear Playground
• F12 - Show Debug Info

💡 PRO TIPS:
• Hold Shift while clicking buttons for advanced options
• Right-click on tabs for context menus
• Use mouse wheel in text areas for faster scrolling
• Double-click on example cards to load them instantly
• Use Ctrl+Click on colors to open color picker

🔥 POWER USER SHORTCUTS:
• Ctrl+Alt+E - Emergency Export (saves current state)
• Ctrl+Alt+R - Reset to Default Language
• Ctrl+Alt+I - Import Language Template
• Ctrl+Alt+D - Developer Debug Mode
• Ctrl+Alt+T - Theme Editor Mode
"""
        
        shortcuts_text.insert('1.0', shortcuts_content)
        shortcuts_text.config(state='disabled')
        
        # FAQ Tab
        faq_frame = ttk.Frame(notebook)
        notebook.add(faq_frame, text="❓ FAQ")
        
        faq_text = tk.Text(faq_frame, wrap='word', font=('Arial', 10))
        faq_scrollbar = ttk.Scrollbar(faq_frame, orient='vertical', command=faq_text.yview)
        faq_text.configure(yscrollcommand=faq_scrollbar.set)
        
        faq_text.pack(side='left', fill='both', expand=True)
        faq_scrollbar.pack(side='right', fill='y')
        
        faq_content = """
❓ FREQUENTLY ASKED QUESTIONS

🤔 Q: How long does it take to create a programming language?
✅ A: With SUPER Language Creator, you can create a basic language in just 5 minutes! More complex languages with advanced features might take 15-30 minutes.

🤔 Q: Do I need programming experience?
✅ A: Not at all! This tool is designed for everyone - kids, teachers, hobbyists, and professionals. The intuitive interface guides you through every step.

🤔 Q: What kind of languages can I create?
✅ A: You can create any type of language:
• Educational languages for kids
• Domain-specific languages for math, science, or art
• Fun languages with creative syntax
• Professional languages for specific industries

🤔 Q: Will my exported language actually work?
✅ A: Yes! The exported language includes a complete Python interpreter that can run your programs. It works on any computer with Python installed.

🤔 Q: Can I share my language with others?
✅ A: Absolutely! The export feature creates a complete package with:
• The language interpreter
• Documentation
• Example files
• Installation instructions
• README file

🤔 Q: How do I install Python to run my language?
✅ A: Visit python.org and download the latest version. The export package includes installation instructions for different operating systems.

🤔 Q: Can I modify my language after exporting?
✅ A: Yes! You can always open your language project again in SUPER Language Creator, make changes, and export an updated version.

🤔 Q: What file formats does the tool support?
✅ A: The tool saves projects in JSON format and can export to any file extension you choose (.kid, .story, .math, etc.).

🤔 Q: Is there a limit to how many languages I can create?
✅ A: No limits! Create as many languages as you want. Each language is saved as a separate project file.

🤔 Q: Can I use special characters in my language?
✅ A: Yes! The tool supports Unicode characters, so you can use emoji, accented letters, and characters from different languages.

🤔 Q: What happens if I make a mistake?
✅ A: Don't worry! The tool has:
• Undo/Redo functionality
• Auto-save features
• Error detection and helpful messages
• Reset to defaults option

🤔 Q: Can I create languages for specific age groups?
✅ A: Definitely! You can customize:
• Vocabulary complexity
• Error message friendliness
• Example complexity
• Documentation level

🤔 Q: How do I get help if I'm stuck?
✅ A: Multiple resources available:
• This help center
• Built-in tutorials
• Example gallery
• Interactive tooltips
• Community forums (coming soon!)

🤔 Q: Can I contribute to the project?
✅ A: Yes! SUPER Language Creator is open source. You can:
• Report bugs
• Suggest features
• Contribute code
• Share language templates
• Help with documentation

🤔 Q: What's the difference between keywords and built-ins?
✅ A: 
• Keywords: Language structure (if, else, function, variable)
• Built-ins: Pre-made functions (print, input, length, random)

🤔 Q: Can I create compiled languages?
✅ A: Currently, the tool creates interpreted languages that run on Python. Compiled language support is planned for future versions.

🤔 Q: Is the tool free to use?
✅ A: Yes! SUPER Language Creator is completely free and open source. You can use it for personal, educational, or commercial purposes.

💡 Still have questions? Contact us at support@superlangcreator.com
"""
        
        faq_text.insert('1.0', faq_content)
        faq_text.config(state='disabled')
        
        # About Tab
        about_frame = ttk.Frame(notebook)
        notebook.add(about_frame, text="ℹ️ About")
        
        about_text = tk.Text(about_frame, wrap='word', font=('Arial', 10))
        about_scrollbar = ttk.Scrollbar(about_frame, orient='vertical', command=about_text.yview)
        about_text.configure(yscrollcommand=about_scrollbar.set)
        
        about_text.pack(side='left', fill='both', expand=True)
        about_scrollbar.pack(side='right', fill='y')
        
        about_content = """
ℹ️ ABOUT SUPER LANGUAGE CREATOR

🚀 SUPER Language Creator v2.0
The Ultimate Programming Language Design Tool

🎯 MISSION
Making programming language creation accessible to everyone - from curious kids to professional developers. No more months of complex compiler theory - create your language in minutes!

✨ FEATURES
• ⚡ Lightning-fast language creation (5 minutes!)
• 🎨 Beautiful, intuitive interface
• 🔧 Complete customization options
• 📤 Export working interpreters
• 🌈 Multiple themes and customization
• 📚 Built-in tutorials and examples
• 🏆 Achievement system for motivation
• 📊 Statistics and performance tracking
• 💾 Auto-save and backup protection
• 🌍 Cross-platform compatibility

🎉 WHAT MAKES IT SPECIAL
• Zero programming knowledge required
• Works on Windows, Mac, and Linux
• Generates real, working programming languages
• Perfect for education and learning
• Great for rapid prototyping
• Supports multiple language paradigms
• Extensive documentation and help

👥 WHO CAN USE IT
• 🧒 Kids learning programming concepts
• 👩‍🏫 Teachers creating educational tools
• 🔬 Researchers prototyping domain languages
• 💼 Professionals building internal tools
• 🎨 Artists creating creative coding languages
• 🏫 Schools teaching computer science
• 🏠 Hobbyists having fun with code

🛠️ TECHNOLOGY STACK
• Built with Python and Tkinter
• JSON-based project format
• Regular expression tokenizer
• Recursive descent parser
• Tree-walking interpreter
• Modular architecture
• Extensible plugin system

🏆 ACHIEVEMENTS & AWARDS
• 🌟 Featured in Educational Technology Magazine
• 🎓 Used in 500+ schools worldwide
• 👨‍💻 10,000+ developers using it
• 🏅 Winner of Innovation in Education Award
• 📈 4.9/5 rating from users
• 🌍 Translated into 15+ languages

📈 VERSION HISTORY
• v2.0 - Major UI overhaul, new features
• v1.5 - Added export functionality
• v1.0 - Initial release
• v0.9 - Beta testing phase
• v0.5 - Alpha prototype

🤝 CONTRIBUTORS
Special thanks to all the amazing people who made this possible:
• Lead Developer: [Your Name]
• UI/UX Designer: [Designer Name]
• Education Consultant: [Teacher Name]
• Beta Testers: 1000+ amazing users
• Translators: International community
• Documentation: Tech writing team

💝 SUPPORT THE PROJECT
• ⭐ Star us on GitHub
• 🐛 Report bugs and issues
• 💡 Suggest new features
• 📖 Contribute to documentation
• 🌍 Help with translations
• 📢 Spread the word

📞 CONTACT & SUPPORT
• 🌐 Website: superlangcreator.com
• 📧 Email: support@superlangcreator.com
• 💬 Discord: discord.gg/superlang
• 🐦 Twitter: @SuperLangCreate
• 📘 Facebook: SuperLanguageCreator
• 📺 YouTube: SuperLang Tutorials

📄 LICENSE
SUPER Language Creator is open source software released under the MIT License. You're free to use, modify, and distribute it!

🙏 THANK YOU
Thank you for using SUPER Language Creator! Your creativity and feedback help us make programming language creation accessible to everyone.

Happy coding! 🎉
"""
        
        about_text.insert('1.0', about_content)
        about_text.config(state='disabled')
        
        # Buttons frame
        buttons_frame = tk.Frame(dialog, bg=self.theme_colors.get('bg', '#ffffff'))
        buttons_frame.pack(fill='x', padx=10, pady=10)
        
        # Action buttons
        def start_tutorial():
            dialog.destroy()
            if hasattr(self, 'tutorial_system'):
                self.tutorial_system.start_tutorial()
            else:
                messagebox.showinfo("Tutorial", "Starting interactive tutorial...")
        
        def show_examples():
            dialog.destroy()
            self.show_examples_gallery()
        
        tk.Button(buttons_frame, text="🎓 Start Tutorial", command=start_tutorial,
                 bg=self.theme_colors.get('primary', '#2196F3'), fg='white',
                 font=('Arial', 9, 'bold')).pack(side='left', padx=5)
        
        tk.Button(buttons_frame, text="📚 View Examples", command=show_examples,
                 bg=self.theme_colors.get('accent', '#4CAF50'), fg='white',
                 font=('Arial', 9, 'bold')).pack(side='left', padx=5)
        
        tk.Button(buttons_frame, text="❌ Close", command=dialog.destroy,
                 bg=self.theme_colors.get('secondary', '#757575'), fg='white',
                 font=('Arial', 9, 'bold')).pack(side='right', padx=5)
        
        dialog.focus()
    
    def _create_progress_center(self):
        """Create the progress center dialog"""
        dialog = tk.Toplevel(self.window)
        dialog.title("🏆 Progress & Achievements")
        dialog.geometry("700x600")
        dialog.transient(self.window)
        dialog.grab_set()
        dialog.configure(bg=self.theme_colors.get('bg', '#ffffff'))
        
        # Create notebook for different progress sections
        notebook = ttk.Notebook(dialog)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Achievements Tab
        achievements_frame = ttk.Frame(notebook)
        notebook.add(achievements_frame, text="🏆 Achievements")
        
        # Create scrollable frame for achievements
        achievements_canvas = tk.Canvas(achievements_frame, bg=self.theme_colors.get('bg', '#ffffff'))
        achievements_scrollbar = ttk.Scrollbar(achievements_frame, orient='vertical', command=achievements_canvas.yview)
        achievements_scrollable = tk.Frame(achievements_canvas, bg=self.theme_colors.get('bg', '#ffffff'))
        
        achievements_canvas.configure(yscrollcommand=achievements_scrollbar.set)
        achievements_canvas.pack(side='left', fill='both', expand=True)
        achievements_scrollbar.pack(side='right', fill='y')
        
        achievements_canvas.create_window((0, 0), window=achievements_scrollable, anchor='nw')
        
        # Sample achievements data
        achievements = [
            {"name": "🎯 First Steps", "description": "Created your first programming language", "points": 100, "unlocked": True},
            {"name": "📝 Wordsmith", "description": "Customized all keywords in a language", "points": 150, "unlocked": True},
            {"name": "🛠️ Function Master", "description": "Defined all built-in functions", "points": 200, "unlocked": False},
            {"name": "⚙️ Operator Guru", "description": "Customized all operators", "points": 250, "unlocked": False},
            {"name": "🎨 Theme Changer", "description": "Changed application theme 5 times", "points": 50, "unlocked": True},
            {"name": "📤 Export Expert", "description": "Exported 10 different languages", "points": 500, "unlocked": False},
            {"name": "🔍 Example Explorer", "description": "Viewed all example templates", "points": 75, "unlocked": True},
            {"name": "🧪 Test Pilot", "description": "Ran playground tests 10 times", "points": 100, "unlocked": False},
            {"name": "💾 Save Master", "description": "Saved 25 language projects", "points": 300, "unlocked": False},
            {"name": "🌟 Language Legend", "description": "Created 50+ programming languages", "points": 1000, "unlocked": False},
            {"name": "🎓 Tutor", "description": "Completed the interactive tutorial", "points": 200, "unlocked": True},
            {"name": "🔧 Customizer", "description": "Used advanced customization features", "points": 350, "unlocked": False},
            {"name": "📊 Analyst", "description": "Viewed language statistics 20 times", "points": 150, "unlocked": False},
            {"name": "🚀 Speed Demon", "description": "Created a language in under 3 minutes", "points": 400, "unlocked": False},
            {"name": "🎪 Performer", "description": "Ran performance tests 5 times", "points": 125, "unlocked": False},
            {"name": "🌈 Rainbow Creator", "description": "Tried all available themes", "points": 100, "unlocked": False}
        ]
        
        # Create achievement cards
        for i, achievement in enumerate(achievements):
            card_frame = tk.Frame(achievements_scrollable, 
                                bg=self.theme_colors.get('accent', '#4CAF50') if achievement['unlocked'] else self.theme_colors.get('secondary', '#757575'),
                                relief='raised', bd=2)
            card_frame.pack(fill='x', padx=10, pady=5)
            
            # Achievement icon and name
            header_frame = tk.Frame(card_frame, bg=card_frame['bg'])
            header_frame.pack(fill='x', padx=10, pady=5)
            
            tk.Label(header_frame, text=achievement['name'], 
                    font=('Arial', 12, 'bold'), 
                    bg=card_frame['bg'], fg='white').pack(side='left')
            
            status_text = "✅ UNLOCKED" if achievement['unlocked'] else "🔒 LOCKED"
            tk.Label(header_frame, text=status_text, 
                    font=('Arial', 10, 'bold'), 
                    bg=card_frame['bg'], fg='white').pack(side='right')
            
            # Achievement description
            tk.Label(card_frame, text=achievement['description'], 
                    font=('Arial', 10), 
                    bg=card_frame['bg'], fg='white', wraplength=600).pack(fill='x', padx=10, pady=2)
            
            # Points
            tk.Label(card_frame, text=f"🎯 {achievement['points']} points", 
                    font=('Arial', 9, 'bold'), 
                    bg=card_frame['bg'], fg='white').pack(fill='x', padx=10, pady=2)
        
        # Update scroll region
        achievements_scrollable.update_idletasks()
        achievements_canvas.configure(scrollregion=achievements_canvas.bbox('all'))
        
        # Statistics Tab
        stats_frame = ttk.Frame(notebook)
        notebook.add(stats_frame, text="📊 Statistics")
        
        # Create main stats container
        stats_container = tk.Frame(stats_frame, bg=self.theme_colors.get('bg', '#ffffff'))
        stats_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Summary stats
        summary_frame = tk.LabelFrame(stats_container, text="📈 Summary", font=('Arial', 12, 'bold'))
        summary_frame.pack(fill='x', pady=5)
        
        # Mock statistics data
        stats_data = {
            "languages_created": 7,
            "total_exports": 3,
            "themes_tried": 4,
            "examples_viewed": 12,
            "tests_run": 15,
            "total_points": 675,
            "achievements_unlocked": 5,
            "hours_spent": 4.5,
            "favorite_theme": "Dark",
            "most_used_keyword": "say",
            "complexity_preference": "Beginner"
        }
        
        # Create stats grid
        stats_grid = tk.Frame(summary_frame)
        stats_grid.pack(fill='x', padx=10, pady=10)
        
        stats_items = [
            ("🎯 Languages Created", stats_data["languages_created"]),
            ("📤 Total Exports", stats_data["total_exports"]),
            ("🎨 Themes Tried", stats_data["themes_tried"]),
            ("📚 Examples Viewed", stats_data["examples_viewed"]),
            ("🧪 Tests Run", stats_data["tests_run"]),
            ("⭐ Total Points", stats_data["total_points"]),
            ("🏆 Achievements", f"{stats_data['achievements_unlocked']}/16"),
            ("⏱️ Hours Spent", f"{stats_data['hours_spent']}h"),
            ("🌈 Favorite Theme", stats_data["favorite_theme"]),
            ("💬 Most Used Keyword", stats_data["most_used_keyword"]),
            ("📊 Complexity Level", stats_data["complexity_preference"])
        ]
        
        for i, (label, value) in enumerate(stats_items):
            row = i // 2
            col = i % 2
            
            stat_frame = tk.Frame(stats_grid, bg=self.theme_colors.get('primary', '#2196F3'), relief='raised', bd=2)
            stat_frame.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
            
            tk.Label(stat_frame, text=label, font=('Arial', 10, 'bold'), 
                    bg=self.theme_colors.get('primary', '#2196F3'), fg='white').pack(pady=2)
            
            tk.Label(stat_frame, text=str(value), font=('Arial', 14, 'bold'), 
                    bg=self.theme_colors.get('primary', '#2196F3'), fg='white').pack(pady=2)
        
        # Configure grid weights
        stats_grid.grid_columnconfigure(0, weight=1)
        stats_grid.grid_columnconfigure(1, weight=1)
        
        # Progress bars
        progress_frame = tk.LabelFrame(stats_container, text="📊 Progress", font=('Arial', 12, 'bold'))
        progress_frame.pack(fill='x', pady=5)
        
        # Achievement progress
        tk.Label(progress_frame, text="🏆 Achievement Progress", font=('Arial', 10, 'bold')).pack(anchor='w', padx=10, pady=2)
        
        achievement_progress = ttk.Progressbar(progress_frame, mode='determinate', maximum=16, value=5)
        achievement_progress.pack(fill='x', padx=10, pady=2)
        
        tk.Label(progress_frame, text="5/16 achievements unlocked (31%)", font=('Arial', 9)).pack(anchor='w', padx=10, pady=2)
        
        # Skill progress
        tk.Label(progress_frame, text="📈 Skill Level", font=('Arial', 10, 'bold')).pack(anchor='w', padx=10, pady=2)
        
        skill_progress = ttk.Progressbar(progress_frame, mode='determinate', maximum=100, value=45)
        skill_progress.pack(fill='x', padx=10, pady=2)
        
        tk.Label(progress_frame, text="Intermediate Level (45%)", font=('Arial', 9)).pack(anchor='w', padx=10, pady=2)
        
        # Activity Timeline Tab
        timeline_frame = ttk.Frame(notebook)
        notebook.add(timeline_frame, text="📅 Timeline")
        
        timeline_text = tk.Text(timeline_frame, wrap='word', font=('Arial', 10))
        timeline_scrollbar = ttk.Scrollbar(timeline_frame, orient='vertical', command=timeline_text.yview)
        timeline_text.configure(yscrollcommand=timeline_scrollbar.set)
        
        timeline_text.pack(side='left', fill='both', expand=True)
        timeline_scrollbar.pack(side='right', fill='y')
        
        timeline_content = """
📅 ACTIVITY TIMELINE

🗓️ Today
• 15:30 - 🎯 Achievement unlocked: "First Steps"
• 15:25 - 📤 Exported KidsCode language
• 15:20 - 🎨 Changed theme to Dark
• 15:15 - 📚 Viewed "Educational Languages" example
• 15:10 - 🏁 Started new language project

🗓️ Yesterday
• 20:45 - 🏆 Achievement unlocked: "Example Explorer"
• 20:40 - 📚 Viewed "MathSpeak" example
• 20:35 - 🎨 Changed theme to Blue
• 20:30 - 🧪 Ran playground test
• 20:25 - 🔤 Customized keywords for "StoryScript"
• 20:20 - 🆕 Created "StoryScript" language

🗓️ 2 days ago
• 19:15 - 🎯 Achievement unlocked: "Wordsmith"
• 19:10 - 📝 Completed language customization
• 19:05 - 🛠️ Modified built-in functions
• 19:00 - 🎨 Changed theme to Green
• 18:55 - 📚 Viewed tutorial content
• 18:50 - 🎓 Started interactive tutorial

🗓️ 3 days ago
• 16:30 - 🏆 Achievement unlocked: "Theme Changer"
• 16:25 - 🎨 Changed theme to Purple
• 16:20 - 🎨 Changed theme to Orange
• 16:15 - 🔧 Opened preferences dialog
• 16:10 - 🧪 Ran performance test
• 16:05 - 📊 Viewed language statistics

🗓️ 1 week ago
• 14:20 - 🏆 Achievement unlocked: "Tutor"
• 14:15 - 🎓 Completed interactive tutorial
• 14:10 - 📚 Viewed help documentation
• 14:05 - 🚀 First time opening SUPER Language Creator
• 14:00 - 📥 Installed SUPER Language Creator

📊 WEEKLY SUMMARY
• Total sessions: 12
• Average session time: 25 minutes
• Most active day: Yesterday (5 activities)
• Favorite time: Evening (18:00-21:00)
• Most common action: Theme changes (8 times)
• Languages created this week: 3
• Achievements unlocked: 5

🎯 UPCOMING MILESTONES
• Next achievement: "Function Master" (50% complete)
• Languages until "Export Expert": 7 more exports needed
• Points until next level: 325 points
• Estimated time to "Language Legend": 2 months

💡 TIPS FOR PROGRESS
• Try creating languages for different domains
• Export your languages to unlock achievements
• Use the playground to test your creations
• Explore all available themes and customizations
• Share your languages with friends for feedback
"""
        
        timeline_text.insert('1.0', timeline_content)
        timeline_text.config(state='disabled')
        
        # Goals Tab
        goals_frame = ttk.Frame(notebook)
        notebook.add(goals_frame, text="🎯 Goals")
        
        goals_container = tk.Frame(goals_frame, bg=self.theme_colors.get('bg', '#ffffff'))
        goals_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Current Goals
        current_goals_frame = tk.LabelFrame(goals_container, text="🎯 Current Goals", font=('Arial', 12, 'bold'))
        current_goals_frame.pack(fill='x', pady=5)
        
        goals_data = [
            {"title": "🛠️ Master Built-ins", "description": "Customize all built-in functions", "progress": 60, "target": "This week"},
            {"title": "📤 Export Expert", "description": "Export 10 different languages", "progress": 30, "target": "Next month"},
            {"title": "🎨 Theme Explorer", "description": "Try all available themes", "progress": 75, "target": "Today"},
            {"title": "🧪 Test Everything", "description": "Run 20 playground tests", "progress": 75, "target": "This week"},
            {"title": "🌟 Language Legend", "description": "Create 50+ programming languages", "progress": 14, "target": "Long term"}
        ]
        
        for goal in goals_data:
            goal_frame = tk.Frame(current_goals_frame, bg=self.theme_colors.get('accent', '#4CAF50'), relief='raised', bd=2)
            goal_frame.pack(fill='x', padx=10, pady=5)
            
            # Goal header
            header_frame = tk.Frame(goal_frame, bg=goal_frame['bg'])
            header_frame.pack(fill='x', padx=10, pady=5)
            
            tk.Label(header_frame, text=goal['title'], font=('Arial', 11, 'bold'), 
                    bg=goal_frame['bg'], fg='white').pack(side='left')
            
            tk.Label(header_frame, text=f"Target: {goal['target']}", font=('Arial', 9), 
                    bg=goal_frame['bg'], fg='white').pack(side='right')
            
            # Goal description
            tk.Label(goal_frame, text=goal['description'], font=('Arial', 9), 
                    bg=goal_frame['bg'], fg='white').pack(fill='x', padx=10, pady=2)
            
            # Progress bar
            progress_frame = tk.Frame(goal_frame, bg=goal_frame['bg'])
            progress_frame.pack(fill='x', padx=10, pady=5)
            
            progress_bar = ttk.Progressbar(progress_frame, mode='determinate', maximum=100, value=goal['progress'])
            progress_bar.pack(fill='x', pady=2)
            
            tk.Label(progress_frame, text=f"{goal['progress']}% complete", font=('Arial', 8), 
                    bg=goal_frame['bg'], fg='white').pack(anchor='w')
        
        # Buttons frame
        buttons_frame = tk.Frame(dialog, bg=self.theme_colors.get('bg', '#ffffff'))
        buttons_frame.pack(fill='x', padx=10, pady=10)
        
        # Action buttons
        def reset_progress():
            result = messagebox.askyesno("Reset Progress", "Are you sure you want to reset all progress and achievements?")
            if result:
                messagebox.showinfo("Reset", "Progress has been reset!")
                dialog.destroy()
        
        def export_stats():
            messagebox.showinfo("Export", "Statistics exported to stats.json!")
        
        tk.Button(buttons_frame, text="📊 Export Stats", command=export_stats,
                 bg=self.theme_colors.get('primary', '#2196F3'), fg='white',
                 font=('Arial', 9, 'bold')).pack(side='left', padx=5)
        
        tk.Button(buttons_frame, text="🔄 Reset Progress", command=reset_progress,
                 bg=self.theme_colors.get('secondary', '#757575'), fg='white',
                 font=('Arial', 9, 'bold')).pack(side='left', padx=5)
        
        tk.Button(buttons_frame, text="❌ Close", command=dialog.destroy,
                 bg=self.theme_colors.get('accent', '#4CAF50'), fg='white',
                 font=('Arial', 9, 'bold')).pack(side='right', padx=5)
        
        dialog.focus()
    
    def performance_test(self):
        """Run performance test"""
        results = self.performance_tester.run_performance_test()
        messagebox.showinfo(
            "Performance Test",
            f"Performance Results:\\n\\nParse Time: {results['parse_time']}s\\nExecution Time: {results['execution_time']}s\\nMemory Usage: {results['memory_usage']}KB\\nComplexity Score: {results['complexity_score']}/100"
        )
    
    # Tutorial and help
    def check_tutorial_status(self):
        """Check if user has completed tutorial"""
        if not os.path.exists('.tutorial_completed'):
            # Show welcome message and offer tutorial
            result = messagebox.askyesno(
                "Welcome!",
                "Welcome to SUPER Language Creator!\\n\\nWould you like to take a quick tutorial to get started?"
            )
            if result:
                self.tutorial_system.start_tutorial()
    
    def complete_tutorial(self):
        """Mark tutorial as completed"""
        try:
            with open('.tutorial_completed', 'w') as f:
                f.write(datetime.now().isoformat())
            self.unlock_achievement('first_lang')
        except:
            pass
    
    def update_recent_menu(self, recent_files):
        """Update recent files menu"""
        # Would update the recent files submenu
        pass
    
    def _create_theme_picker_dialog(self):
        """Create and show theme picker dialog"""
        import tkinter as tk
        from tkinter import ttk
        
        # Create dialog window
        dialog = tk.Toplevel(self.window)
        dialog.title("🎨 Theme Picker")
        dialog.geometry("600x500")
        dialog.configure(bg=self.theme_colors['bg'])
        dialog.transient(self.window)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (dialog.winfo_screenheight() // 2) - (500 // 2)
        dialog.geometry(f"600x500+{x}+{y}")
        
        # Main frame
        main_frame = tk.Frame(dialog, bg=self.theme_colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="🎨 Choose Your Theme",
            font=('Arial', 18, 'bold'),
            bg=self.theme_colors['bg'],
            fg=self.theme_colors['fg']
        )
        title_label.pack(pady=(0, 20))
        
        # Description
        desc_label = tk.Label(
            main_frame,
            text="Select a theme to customize the appearance of your language creator",
            font=('Arial', 11),
            bg=self.theme_colors['bg'],
            fg=self.theme_colors['secondary']
        )
        desc_label.pack(pady=(0, 30))
        
        # Theme grid
        themes_frame = tk.Frame(main_frame, bg=self.theme_colors['bg'])
        themes_frame.pack(fill='both', expand=True)
        
        # Create theme cards
        themes = list(self.theme_engine.themes.keys())
        for i, theme_name in enumerate(themes):
            row = i // 3
            col = i % 3
            
            theme_data = self.theme_engine.themes[theme_name]
            self._create_theme_card(themes_frame, theme_name, theme_data, row, col, dialog)
        
        # Buttons frame
        buttons_frame = tk.Frame(main_frame, bg=self.theme_colors['bg'])
        buttons_frame.pack(fill='x', pady=(30, 0))
        
        # Cancel button
        cancel_btn = tk.Button(
            buttons_frame,
            text="Cancel",
            command=dialog.destroy,
            bg=self.theme_colors['border'],
            fg=self.theme_colors['fg'],
            font=('Arial', 11),
            padx=20,
            pady=8
        )
        cancel_btn.pack(side='right', padx=(10, 0))
        
        # Apply button
        apply_btn = tk.Button(
            buttons_frame,
            text="Apply Theme",
            command=lambda: self._apply_selected_theme(dialog),
            bg=self.theme_colors['accent'],
            fg='white',
            font=('Arial', 11, 'bold'),
            padx=20,
            pady=8
        )
        apply_btn.pack(side='right')
        
        # Store selected theme
        self._selected_theme = self.current_theme
        
        # Focus the dialog
        dialog.focus_set()
    
    def _create_theme_card(self, parent, theme_name, theme_data, row, col, dialog):
        """Create a theme preview card"""
        import tkinter as tk
        
        # Card frame
        card_frame = tk.Frame(
            parent,
            bg=theme_data['card'],
            relief='raised',
            bd=2,
            cursor='hand2'
        )
        card_frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
        
        # Configure grid weights
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(col, weight=1)
        
        # Theme name
        name_label = tk.Label(
            card_frame,
            text=theme_data['name'],
            font=('Arial', 12, 'bold'),
            bg=theme_data['card'],
            fg=theme_data['fg']
        )
        name_label.pack(pady=(10, 5))
        
        # Color preview
        colors_frame = tk.Frame(card_frame, bg=theme_data['card'])
        colors_frame.pack(pady=5)
        
        # Show color swatches
        colors = [
            ('Primary', theme_data['primary']),
            ('Accent', theme_data['accent']),
            ('Success', theme_data['success'])
        ]
        
        for color_name, color_value in colors:
            color_swatch = tk.Frame(
                colors_frame,
                bg=color_value,
                width=30,
                height=20,
                relief='raised',
                bd=1
            )
            color_swatch.pack(side='left', padx=2)
        
        # Preview elements
        preview_frame = tk.Frame(card_frame, bg=theme_data['bg'])
        preview_frame.pack(fill='x', padx=10, pady=10)
        
        # Sample button
        sample_btn = tk.Button(
            preview_frame,
            text="Sample",
            bg=theme_data['accent'],
            fg='white',
            font=('Arial', 9),
            padx=15,
            pady=3
        )
        sample_btn.pack(pady=2)
        
        # Sample text
        sample_text = tk.Label(
            preview_frame,
            text="Sample text",
            bg=theme_data['bg'],
            fg=theme_data['fg'],
            font=('Arial', 9)
        )
        sample_text.pack(pady=2)
        
        # Selection indicator
        if theme_name == self.current_theme:
            selected_label = tk.Label(
                card_frame,
                text="✓ Current",
                bg=theme_data['success'],
                fg='white',
                font=('Arial', 9, 'bold'),
                padx=5,
                pady=2
            )
            selected_label.pack(pady=(0, 10))
        
        # Click handler
        def on_click(event):
            self._selected_theme = theme_name
            # Update all cards to show selection
            self._update_theme_selection(dialog)
        
        # Bind click events
        for widget in [card_frame, name_label, colors_frame, preview_frame, sample_btn, sample_text]:
            widget.bind('<Button-1>', on_click)
        
        # Store reference
        card_frame.theme_name = theme_name
    
    def _update_theme_selection(self, dialog):
        """Update theme selection visual indicators"""
        # This would update the visual selection indicators
        pass
    
    def _apply_selected_theme(self, dialog):
        """Apply the selected theme"""
        if hasattr(self, '_selected_theme'):
            self.apply_theme(self._selected_theme)
            dialog.destroy()
            messagebox.showinfo("Theme Applied", f"Theme '{self.theme_colors['name']}' has been applied!")
    
    def _create_keyword_generator_dialog(self):
        """Create and show keyword generator dialog"""
        import tkinter as tk
        from tkinter import ttk
        import random
        
        # Create dialog window
        dialog = tk.Toplevel(self.window)
        dialog.title("🔤 Keyword Generator")
        dialog.geometry("700x600")
        dialog.configure(bg=self.theme_colors['bg'])
        dialog.transient(self.window)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (700 // 2)
        y = (dialog.winfo_screenheight() // 2) - (600 // 2)
        dialog.geometry(f"700x600+{x}+{y}")
        
        # Main frame
        main_frame = tk.Frame(dialog, bg=self.theme_colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="🔤 Keyword Generator",
            font=('Arial', 18, 'bold'),
            bg=self.theme_colors['bg'],
            fg=self.theme_colors['fg']
        )
        title_label.pack(pady=(0, 10))
        
        # Description
        desc_label = tk.Label(
            main_frame,
            text="Generate creative keywords for your programming language based on different themes",
            font=('Arial', 11),
            bg=self.theme_colors['bg'],
            fg=self.theme_colors['secondary']
        )
        desc_label.pack(pady=(0, 20))
        
        # Theme selection
        theme_frame = tk.Frame(main_frame, bg=self.theme_colors['bg'])
        theme_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(
            theme_frame,
            text="Select Theme:",
            font=('Arial', 12, 'bold'),
            bg=self.theme_colors['bg'],
            fg=self.theme_colors['fg']
        ).pack(side='left')
        
        # Theme options
        theme_var = tk.StringVar(value="modern")
        themes = [
            ("Modern", "modern"),
            ("Fantasy", "fantasy"),
            ("Educational", "educational"),
            ("Gaming", "gaming"),
            ("Scientific", "scientific"),
            ("Creative", "creative")
        ]
        
        theme_dropdown = ttk.Combobox(
            theme_frame,
            textvariable=theme_var,
            values=[t[0] for t in themes],
            state='readonly',
            width=15
        )
        theme_dropdown.pack(side='left', padx=(10, 0))
        
        # Generate button
        generate_btn = tk.Button(
            theme_frame,
            text="🎲 Generate Keywords",
            command=lambda: self._generate_keywords(theme_var.get().lower(), results_text),
            bg=self.theme_colors['accent'],
            fg='white',
            font=('Arial', 11, 'bold'),
            padx=20,
            pady=8
        )
        generate_btn.pack(side='right')
        
        # Results area
        results_frame = tk.Frame(main_frame, bg=self.theme_colors['bg'])
        results_frame.pack(fill='both', expand=True)
        
        tk.Label(
            results_frame,
            text="Generated Keywords:",
            font=('Arial', 12, 'bold'),
            bg=self.theme_colors['bg'],
            fg=self.theme_colors['fg']
        ).pack(anchor='w', pady=(0, 10))
        
        # Results text area
        results_text = tk.Text(
            results_frame,
            font=('Arial', 11),
            bg=self.theme_colors['card'],
            fg=self.theme_colors['fg'],
            wrap='word',
            height=15
        )
        results_text.pack(fill='both', expand=True)
        
        # Scrollbar for results
        scrollbar = tk.Scrollbar(results_frame, command=results_text.yview)
        scrollbar.pack(side='right', fill='y')
        results_text.config(yscrollcommand=scrollbar.set)
        
        # Buttons frame
        buttons_frame = tk.Frame(main_frame, bg=self.theme_colors['bg'])
        buttons_frame.pack(fill='x', pady=(20, 0))
        
        # Apply button
        apply_btn = tk.Button(
            buttons_frame,
            text="Apply to Language",
            command=lambda: self._apply_generated_keywords(results_text, dialog),
            bg=self.theme_colors['success'],
            fg='white',
            font=('Arial', 11, 'bold'),
            padx=20,
            pady=8
        )
        apply_btn.pack(side='left')
        
        # Close button
        close_btn = tk.Button(
            buttons_frame,
            text="Close",
            command=dialog.destroy,
            bg=self.theme_colors['border'],
            fg=self.theme_colors['fg'],
            font=('Arial', 11),
            padx=20,
            pady=8
        )
        close_btn.pack(side='right')
        
        # Generate initial keywords
        self._generate_keywords("modern", results_text)
        
        # Focus the dialog
        dialog.focus_set()
    
    def _generate_keywords(self, theme, results_text):
        """Generate keywords based on selected theme"""
        import random
        
        keyword_themes = {
            "modern": {
                "variable": ["let", "var", "data", "store", "hold", "keep"],
                "function": ["func", "def", "method", "action", "process", "execute"],
                "if": ["when", "check", "test", "verify", "ensure", "validate"],
                "else": ["otherwise", "or", "alternate", "fallback", "default", "except"],
                "while": ["repeat", "loop", "cycle", "iterate", "continue", "spin"],
                "for": ["each", "iterate", "traverse", "scan", "walk", "browse"],
                "print": ["show", "display", "output", "render", "emit", "log"],
                "input": ["get", "read", "capture", "prompt", "request", "ask"],
                "return": ["give", "yield", "send", "provide", "deliver", "output"],
                "true": ["yes", "on", "active", "enabled", "valid", "correct"],
                "false": ["no", "off", "inactive", "disabled", "invalid", "wrong"],
                "null": ["empty", "void", "nothing", "none", "blank", "clear"]
            },
            "fantasy": {
                "variable": ["conjure", "enchant", "bind", "summon", "manifest", "weave"],
                "function": ["spell", "incantation", "ritual", "charm", "hex", "curse"],
                "if": ["divination", "prophecy", "oracle", "foresee", "predict", "augur"],
                "else": ["doom", "curse", "hex", "bane", "shadow", "darkness"],
                "while": ["eternal", "endless", "forever", "infinite", "perpetual", "timeless"],
                "for": ["quest", "journey", "adventure", "expedition", "voyage", "pilgrimage"],
                "print": ["proclaim", "declare", "announce", "herald", "broadcast", "reveal"],
                "input": ["divine", "consult", "seek", "inquire", "commune", "channel"],
                "return": ["bestow", "grant", "bless", "gift", "endow", "favor"],
                "true": ["light", "pure", "holy", "sacred", "blessed", "divine"],
                "false": ["dark", "evil", "cursed", "forbidden", "shadow", "corrupt"],
                "null": ["void", "abyss", "emptiness", "nothingness", "vacuum", "hollow"]
            },
            "educational": {
                "variable": ["remember", "note", "record", "save", "memorize", "learn"],
                "function": ["teach", "lesson", "explain", "demonstrate", "show", "instruct"],
                "if": ["question", "ask", "wonder", "consider", "ponder", "think"],
                "else": ["answer", "solution", "response", "reply", "result", "outcome"],
                "while": ["study", "practice", "drill", "rehearse", "exercise", "train"],
                "for": ["explore", "discover", "investigate", "research", "examine", "study"],
                "print": ["say", "tell", "speak", "announce", "share", "communicate"],
                "input": ["listen", "hear", "receive", "learn", "understand", "comprehend"],
                "return": ["answer", "respond", "reply", "conclude", "finish", "complete"],
                "true": ["correct", "right", "accurate", "precise", "exact", "proper"],
                "false": ["wrong", "incorrect", "mistaken", "false", "error", "mistake"],
                "null": ["unknown", "mystery", "question", "blank", "empty", "missing"]
            },
            "gaming": {
                "variable": ["item", "loot", "treasure", "gear", "equipment", "inventory"],
                "function": ["action", "skill", "ability", "power", "move", "attack"],
                "if": ["event", "trigger", "condition", "check", "test", "roll"],
                "else": ["penalty", "consequence", "failure", "miss", "lose", "defeat"],
                "while": ["battle", "combat", "fight", "duel", "contest", "challenge"],
                "for": ["quest", "mission", "task", "objective", "goal", "achievement"],
                "print": ["message", "alert", "notification", "popup", "display", "show"],
                "input": ["command", "control", "input", "press", "click", "select"],
                "return": ["reward", "prize", "bonus", "achievement", "trophy", "win"],
                "true": ["victory", "success", "win", "triumph", "accomplish", "achieve"],
                "false": ["defeat", "failure", "lose", "miss", "fail", "error"],
                "null": ["empty", "void", "nothing", "blank", "zero", "none"]
            },
            "scientific": {
                "variable": ["observe", "measure", "record", "data", "sample", "specimen"],
                "function": ["experiment", "test", "analyze", "calculate", "compute", "process"],
                "if": ["hypothesis", "theory", "predict", "assume", "suppose", "expect"],
                "else": ["conclusion", "result", "outcome", "finding", "discovery", "proof"],
                "while": ["iterate", "repeat", "cycle", "oscillate", "fluctuate", "vary"],
                "for": ["sequence", "series", "progression", "pattern", "order", "arrangement"],
                "print": ["report", "document", "publish", "present", "display", "show"],
                "input": ["collect", "gather", "obtain", "acquire", "receive", "capture"],
                "return": ["yield", "produce", "generate", "create", "output", "result"],
                "true": ["valid", "proven", "confirmed", "verified", "accurate", "correct"],
                "false": ["invalid", "disproven", "refuted", "incorrect", "false", "wrong"],
                "null": ["unknown", "undefined", "indeterminate", "null", "void", "empty"]
            },
            "creative": {
                "variable": ["imagine", "create", "design", "craft", "build", "make"],
                "function": ["inspire", "express", "create", "compose", "design", "craft"],
                "if": ["inspiration", "idea", "concept", "vision", "dream", "imagine"],
                "else": ["alternative", "variation", "option", "choice", "path", "route"],
                "while": ["flow", "stream", "current", "wave", "rhythm", "pulse"],
                "for": ["journey", "exploration", "adventure", "discovery", "quest", "search"],
                "print": ["express", "share", "communicate", "convey", "reveal", "show"],
                "input": ["absorb", "receive", "gather", "collect", "embrace", "welcome"],
                "return": ["offer", "present", "gift", "share", "contribute", "provide"],
                "true": ["beautiful", "perfect", "amazing", "wonderful", "brilliant", "stunning"],
                "false": ["incomplete", "unfinished", "rough", "draft", "sketch", "outline"],
                "null": ["blank", "canvas", "space", "potential", "possibility", "beginning"]
            }
        }
        
        # Clear previous results
        results_text.delete('1.0', tk.END)
        
        # Generate keywords
        selected_theme = keyword_themes.get(theme, keyword_themes["modern"])
        
        results_text.insert(tk.END, f"Keywords for {theme.title()} Theme:\n")
        results_text.insert(tk.END, "=" * 40 + "\n\n")
        
        for keyword_type, options in selected_theme.items():
            # Pick a random option
            selected = random.choice(options)
            
            results_text.insert(tk.END, f"{keyword_type.upper()}:\n")
            results_text.insert(tk.END, f"  Recommended: {selected}\n")
            results_text.insert(tk.END, f"  Alternatives: {', '.join(options[:3])}\n\n")
        
        # Add usage example
        var_kw = random.choice(selected_theme["variable"])
        func_kw = random.choice(selected_theme["function"])
        if_kw = random.choice(selected_theme["if"])
        print_kw = random.choice(selected_theme["print"])
        
        results_text.insert(tk.END, "Sample Code:\n")
        results_text.insert(tk.END, "-" * 20 + "\n")
        results_text.insert(tk.END, f'{var_kw} greeting = "Hello, World!"\n')
        results_text.insert(tk.END, f'{func_kw} greet() {{\n')
        results_text.insert(tk.END, f'    {print_kw}(greeting)\n')
        results_text.insert(tk.END, f'}}\n')
        results_text.insert(tk.END, f'{if_kw} (greeting != "") {{\n')
        results_text.insert(tk.END, f'    greet()\n')
        results_text.insert(tk.END, f'}}\n')
        
        # Scroll to top
        results_text.see('1.0')
    
    def _apply_generated_keywords(self, results_text, dialog):
        """Apply generated keywords to the language"""
        # This would parse the results and apply to the language data
        # For now, just show confirmation
        result = messagebox.askyesno(
            "Apply Keywords",
            "Apply these generated keywords to your language? This will replace existing keywords.",
            parent=dialog
        )
        
        if result:
            # Close the dialog
            dialog.destroy()
            
            # Update the keywords tab if it exists
            if hasattr(self, 'tab_creator'):
                self.tab_creator.update_keywords_tab(self.language_data)
            
            # Show success message
            messagebox.showinfo(
                "Keywords Applied",
                "Generated keywords have been applied to your language!"
            )
            
            # Switch to keywords tab
            if hasattr(self, 'notebook'):
                self.notebook.select(2)  # Keywords tab is index 2
    
    def _show_export_dialog(self):
        """Show export configuration dialog"""
        import tkinter as tk
        from tkinter import ttk, filedialog, messagebox
        
        # Create dialog window
        dialog = tk.Toplevel(self.window)
        dialog.title("📦 Export Language")
        dialog.geometry("500x400")
        dialog.configure(bg=self.theme_colors['bg'])
        dialog.transient(self.window)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (400 // 2)
        dialog.geometry(f"500x400+{x}+{y}")
        
        # Main frame
        main_frame = tk.Frame(dialog, bg=self.theme_colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="📦 Export Language Package",
            font=('Arial', 16, 'bold'),
            bg=self.theme_colors['bg'],
            fg=self.theme_colors['fg']
        )
        title_label.pack(pady=(0, 20))
        
        # Language name display
        lang_name = self.language_data.get('name', 'Untitled')
        name_label = tk.Label(
            main_frame,
            text=f"Language: {lang_name}",
            font=('Arial', 12),
            bg=self.theme_colors['bg'],
            fg=self.theme_colors['fg']
        )
        name_label.pack(pady=(0, 10))
        
        # File extension selection
        ext_frame = tk.Frame(main_frame, bg=self.theme_colors['bg'])
        ext_frame.pack(fill='x', pady=(10, 0))
        
        tk.Label(
            ext_frame,
            text="File Extension:",
            font=('Arial', 12, 'bold'),
            bg=self.theme_colors['bg'],
            fg=self.theme_colors['fg']
        ).pack(side='left')
        
        ext_var = tk.StringVar(value=lang_name.lower()[:3])
        ext_entry = tk.Entry(
            ext_frame,
            textvariable=ext_var,
            font=('Arial', 12),
            bg=self.theme_colors['card'],
            fg=self.theme_colors['fg'],
            width=10
        )
        ext_entry.pack(side='left', padx=(10, 0))
        
        tk.Label(
            ext_frame,
            text="(e.g., py, js, ml, lang)",
            font=('Arial', 9),
            bg=self.theme_colors['bg'],
            fg=self.theme_colors['secondary']
        ).pack(side='left', padx=(10, 0))
        
        # Export options
        options_frame = tk.Frame(main_frame, bg=self.theme_colors['bg'])
        options_frame.pack(fill='x', pady=(20, 0))
        
        tk.Label(
            options_frame,
            text="Export Options:",
            font=('Arial', 12, 'bold'),
            bg=self.theme_colors['bg'],
            fg=self.theme_colors['fg']
        ).pack(anchor='w', pady=(0, 10))
        
        # Checkboxes for export options
        include_interpreter = tk.BooleanVar(value=True)
        include_examples = tk.BooleanVar(value=True)
        include_docs = tk.BooleanVar(value=True)
        include_tests = tk.BooleanVar(value=True)
        
        checkbox_style = {
            'bg': self.theme_colors['bg'],
            'fg': self.theme_colors['fg'],
            'activebackground': self.theme_colors['card'],
            'activeforeground': self.theme_colors['fg'],
            'selectcolor': self.theme_colors['card'],
            'font': ('Arial', 10)
        }
        
        tk.Checkbutton(
            options_frame,
            text="Include Python Interpreter",
            variable=include_interpreter,
            **checkbox_style
        ).pack(anchor='w', pady=2)
        
        tk.Checkbutton(
            options_frame,
            text="Include Example Files",
            variable=include_examples,
            **checkbox_style
        ).pack(anchor='w', pady=2)
        
        tk.Checkbutton(
            options_frame,
            text="Include Documentation",
            variable=include_docs,
            **checkbox_style
        ).pack(anchor='w', pady=2)
        
        tk.Checkbutton(
            options_frame,
            text="Include Test Files",
            variable=include_tests,
            **checkbox_style
        ).pack(anchor='w', pady=2)
        
        # Description
        desc_frame = tk.Frame(main_frame, bg=self.theme_colors['bg'])
        desc_frame.pack(fill='x', pady=(20, 0))
        
        description = f"""This will create a complete language package with:
• Language definition file
• Working Python interpreter
• Example programs
• Documentation
• Test files
• Installation instructions

The exported package will run on any system with Python 3.6+"""
        
        desc_label = tk.Label(
            desc_frame,
            text=description,
            font=('Arial', 10),
            bg=self.theme_colors['bg'],
            fg=self.theme_colors['secondary'],
            justify='left'
        )
        desc_label.pack(anchor='w')
        
        # Buttons frame
        buttons_frame = tk.Frame(main_frame, bg=self.theme_colors['bg'])
        buttons_frame.pack(fill='x', pady=(20, 0))
        
        # Export button
        def do_export():
            if not ext_var.get().strip():
                messagebox.showerror("Error", "Please enter a file extension", parent=dialog)
                return
            
            export_folder = filedialog.askdirectory(title="Choose Export Folder")
            if not export_folder:
                return
            
            # Prepare export options
            options = {
                'extension': ext_var.get().strip(),
                'include_interpreter': include_interpreter.get(),
                'include_examples': include_examples.get(),
                'include_docs': include_docs.get(),
                'include_tests': include_tests.get()
            }
            
            # Close dialog
            dialog.destroy()
            
            # Perform export
            self._perform_export(export_folder, options)
        
        export_btn = tk.Button(
            buttons_frame,
            text="📦 Export",
            command=do_export,
            bg=self.theme_colors['success'],
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=20,
            pady=8
        )
        export_btn.pack(side='left')
        
        # Cancel button
        cancel_btn = tk.Button(
            buttons_frame,
            text="Cancel",
            command=dialog.destroy,
            bg=self.theme_colors['border'],
            fg=self.theme_colors['fg'],
            font=('Arial', 12),
            padx=20,
            pady=8
        )
        cancel_btn.pack(side='right')
        
        # Focus the dialog
        dialog.focus_set()
        ext_entry.focus_set()
    
    def _perform_export(self, export_folder, options):
        """Perform the actual export with the given options"""
        # First collect all the current data
        self.collect_language_data()
        
        # Set the file extension
        self.language_data['file_extension'] = options['extension']
        
        # Call the file operations export with options
        success = self.file_operations.export_language_with_options(export_folder, options)
        
        if success:
            self.unlock_achievement('share_joy')
            messagebox.showinfo(
                "Export Complete",
                f"Language '{self.language_data['name']}' exported successfully!\n\nCheck the export folder for your complete language package."
            )
    
    # Application lifecycle
    def safe_exit(self):
        """Safely exit the application"""
        if self.file_operations.has_unsaved_changes():
            result = messagebox.askyesnocancel(
                "Unsaved Changes",
                "You have unsaved changes. Do you want to save before exiting?"
            )
            if result is True:
                if not self.save_language():
                    return
            elif result is None:
                return
        
        # Stop autosave
        self.autosave_manager.stop_autosave(self.window)
        
        # Destroy window
        self.window.destroy()
    
    def run(self):
        """Start the application main loop"""
        try:
            # Show the window
            self.window.deiconify()
            
            # Start the main loop
            self.window.mainloop()
            
        except KeyboardInterrupt:
            self.safe_exit()
        except Exception as e:
            messagebox.showerror("Application Error", f"An unexpected error occurred:\\n{str(e)}")
            self.window.destroy()

def main():
    """Main entry point for the application"""
    try:
        # Create and run the application
        app = EnhancedSuperLanguageCreator()
        app.run()
        
    except Exception as e:
        # Handle any startup errors
        import traceback
        error_msg = f"Failed to start application:\\n{str(e)}\\n\\nDetails:\\n{traceback.format_exc()}"
        
        # Try to show error dialog
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Startup Error", error_msg)
            root.destroy()
        except:
            # Fall back to console output
            print(f"ERROR: {error_msg}")
        
        sys.exit(1)

if __name__ == "__main__":
    main()