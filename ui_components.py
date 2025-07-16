"""
UI Components Module for LangGen
Contains: Menu bars, toolbars, tabs, dialogs, cards, and other UI elements
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

class UIComponentFactory:
    """Factory class for creating UI components with consistent styling"""
    
    def __init__(self, root, theme_engine, language_data):
        self.root = root
        self.theme_engine = theme_engine
        self.language_data = language_data
        self.current_theme = None
    
    def apply_theme(self, theme_name):
        """Apply theme to all components"""
        self.current_theme = theme_name
        if theme_name in self.theme_engine.themes:
            self.theme_colors = self.theme_engine.themes[theme_name]

class MenuBarCreator:
    """Creates and manages menu bars"""
    
    def __init__(self, root, callbacks, theme_engine):
        self.root = root
        self.callbacks = callbacks
        self.theme_engine = theme_engine
    
    def create_enhanced_menu_bar(self):
        """Create the main application menu with enhanced features"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Language", command=self.callbacks.get('new_language', lambda: None), accelerator="Ctrl+N")
        file_menu.add_command(label="Open...", command=self.callbacks.get('load_language', lambda: None), accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.callbacks.get('save_language', lambda: None), accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=self.callbacks.get('save_as_language', lambda: None), accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Export Language...", command=self.callbacks.get('export_language', lambda: None), accelerator="Ctrl+E")
        file_menu.add_command(label="Import Language...", command=self.callbacks.get('import_language', lambda: None))
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.callbacks.get('safe_exit', lambda: None), accelerator="Ctrl+Q")
        
        # Edit Menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Generate Keywords", command=self.callbacks.get('show_keyword_generator', lambda: None), accelerator="Ctrl+G")
        edit_menu.add_command(label="Validate Syntax", command=self.callbacks.get('validate_syntax', lambda: None), accelerator="F5")
        edit_menu.add_separator()
        edit_menu.add_command(label="Preferences", command=self.callbacks.get('show_preferences', lambda: None), accelerator="Ctrl+,")
        
        # View Menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        
        # Theme submenu
        theme_menu = tk.Menu(view_menu, tearoff=0)
        view_menu.add_cascade(label="Themes", menu=theme_menu)
        for theme_name, theme_data in self.theme_engine.themes.items():
            theme_menu.add_command(
                label=theme_data['name'],
                command=lambda t=theme_name: self.callbacks.get('apply_theme', lambda x: None)(t)
            )
        
        view_menu.add_separator()
        view_menu.add_command(label="Show Statistics", command=self.callbacks.get('show_statistics', lambda: None))
        view_menu.add_command(label="Examples Gallery", command=self.callbacks.get('show_examples_gallery', lambda: None))
        
        # Tools Menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Performance Test", command=self.callbacks.get('performance_test', lambda: None))
        tools_menu.add_command(label="Achievement Center", command=self.callbacks.get('show_achievements', lambda: None))
        tools_menu.add_command(label="Theme Creator", command=self.callbacks.get('show_theme_picker', lambda: None))
        
        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Keyboard Shortcuts", command=self.callbacks.get('show_keyboard_shortcuts', lambda: None), accelerator="F1")
        help_menu.add_command(label="Tutorial", command=self.callbacks.get('show_help_menu', lambda: None))
        help_menu.add_separator()
        help_menu.add_command(label="About", command=self.callbacks.get('show_about', lambda: None))
        
        return menubar

class ToolbarCreator:
    """Creates and manages toolbars"""
    
    def __init__(self, root, callbacks, theme_colors):
        self.root = root
        self.callbacks = callbacks
        self.theme_colors = theme_colors
    
    def create_modern_toolbar(self):
        """Create modern toolbar with enhanced buttons"""
        toolbar = tk.Frame(self.root, bg=self.theme_colors.get('toolbar', '#ffffff'), height=50)
        toolbar.pack(fill='x', pady=(0, 1))
        toolbar.pack_propagate(False)
        
        # Left section - File operations
        left_frame = tk.Frame(toolbar, bg=self.theme_colors.get('toolbar', '#ffffff'))
        left_frame.pack(side='left', padx=10, pady=8)
        
        buttons = [
            ("🆕", "New Language", self.callbacks.get('new_language', lambda: None)),
            ("📂", "Open", self.callbacks.get('load_language', lambda: None)),
            ("💾", "Save", self.callbacks.get('save_language', lambda: None)),
            ("📤", "Export", self.callbacks.get('export_language', lambda: None)),
        ]
        
        for emoji, tooltip, command in buttons:
            btn = self.create_modern_button(left_frame, emoji, tooltip, command)
            btn.pack(side='left', padx=2)
        
        # Center section - Actions
        center_frame = tk.Frame(toolbar, bg=self.theme_colors.get('toolbar', '#ffffff'))
        center_frame.pack(side='left', padx=20, pady=8)
        
        action_buttons = [
            ("🎲", "Generate Keywords", self.callbacks.get('show_keyword_generator', lambda: None)),
            ("✅", "Validate", self.callbacks.get('validate_syntax', lambda: None)),
            ("▶️", "Test", self.callbacks.get('run_playground', lambda: None)),
        ]
        
        for emoji, tooltip, command in action_buttons:
            btn = self.create_modern_button(center_frame, emoji, tooltip, command)
            btn.pack(side='left', padx=2)
        
        # Right section - Settings
        right_frame = tk.Frame(toolbar, bg=self.theme_colors.get('toolbar', '#ffffff'))
        right_frame.pack(side='right', padx=10, pady=8)
        
        settings_buttons = [
            ("🎨", "Themes", self.callbacks.get('show_theme_picker', lambda: None)),
            ("⚙️", "Settings", self.callbacks.get('show_preferences', lambda: None)),
            ("❓", "Help", self.callbacks.get('show_help_menu', lambda: None)),
        ]
        
        for emoji, tooltip, command in settings_buttons:
            btn = self.create_modern_button(right_frame, emoji, tooltip, command)
            btn.pack(side='right', padx=2)
        
        return toolbar
    
    def create_modern_button(self, parent, text, tooltip, command):
        """Create a modern styled button with hover effects"""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=('Arial', 12),
            bg=self.theme_colors.get('card', '#ffffff'),
            fg=self.theme_colors.get('fg', '#000000'),
            border=0,
            padx=12,
            pady=8,
            cursor='hand2',
            relief='flat'
        )
        
        # Hover effects
        def on_enter(e):
            btn.config(bg=self.darken_color(self.theme_colors.get('card', '#ffffff')))
        
        def on_leave(e):
            btn.config(bg=self.theme_colors.get('card', '#ffffff'))
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        
        # Tooltip
        self.create_tooltip(btn, tooltip)
        
        return btn
    
    def darken_color(self, color):
        """Darken a color for hover effects"""
        if color.startswith('#'):
            color = color[1:]
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        darkened = tuple(max(0, c - 20) for c in rgb)
        return f'#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}'
    
    def create_tooltip(self, widget, text):
        """Create a tooltip for a widget"""
        def on_enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            label = tk.Label(tooltip, text=text, background="black", foreground="white", font=('Arial', 9))
            label.pack()
            widget.tooltip = tooltip
        
        def on_leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                del widget.tooltip
        
        widget.bind('<Enter>', on_enter)
        widget.bind('<Leave>', on_leave)

class TabCreator:
    """Creates and manages notebook tabs"""
    
    def __init__(self, notebook, callbacks, theme_colors, language_data):
        self.notebook = notebook
        self.callbacks = callbacks
        self.theme_colors = theme_colors
        self.language_data = language_data
    
    def create_welcome_tab(self):
        """Create the welcome tab with hero section"""
        welcome_frame = tk.Frame(self.notebook, bg=self.theme_colors.get('bg', '#ffffff'))
        
        # Hero section
        hero_frame = tk.Frame(welcome_frame, bg=self.theme_colors.get('primary', '#667eea'), height=200)
        hero_frame.pack(fill='x')
        hero_frame.pack_propagate(False)
        
        # Title
        title = tk.Label(
            hero_frame,
            text="🚀 SUPER Language Creator",
            font=('Arial', 24, 'bold'),
            bg=self.theme_colors.get('primary', '#667eea'),
            fg='white'
        )
        title.pack(pady=(40, 10))
        
        # Subtitle
        subtitle = tk.Label(
            hero_frame,
            text="Create your own programming language in minutes!",
            font=('Arial', 14),
            bg=self.theme_colors.get('primary', '#667eea'),
            fg='white'
        )
        subtitle.pack()
        
        # Quick actions
        actions_frame = tk.Frame(welcome_frame, bg=self.theme_colors.get('bg', '#ffffff'))
        actions_frame.pack(fill='both', expand=True, padx=40, pady=30)
        
        # Create action cards
        actions = [
            ("🆕 New Language", "Start creating a new programming language", self.callbacks.get('new_language', lambda: None)),
            ("📂 Open Project", "Open an existing language project", self.callbacks.get('load_language', lambda: None)),
            ("🎨 Explore Themes", "Browse and customize themes", self.callbacks.get('show_theme_picker', lambda: None)),
            ("📚 View Examples", "See example languages for inspiration", self.callbacks.get('show_examples_gallery', lambda: None)),
        ]
        
        for i, (title, desc, command) in enumerate(actions):
            card = self.create_action_card(actions_frame, title, desc, command)
            card.grid(row=i//2, column=i%2, padx=20, pady=15, sticky='ew')
        
        actions_frame.columnconfigure(0, weight=1)
        actions_frame.columnconfigure(1, weight=1)
        
        return welcome_frame
    
    def create_info_tab(self):
        """Create the language information tab"""
        info_frame = tk.Frame(self.notebook, bg=self.theme_colors.get('bg', '#ffffff'))
        
        # Scrollable frame
        canvas = tk.Canvas(info_frame, bg=self.theme_colors.get('bg', '#ffffff'))
        scrollbar = ttk.Scrollbar(info_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.theme_colors.get('bg', '#ffffff'))
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Content
        self.create_info_form(scrollable_frame)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        return info_frame
    
    def create_keywords_tab(self):
        """Create the keywords configuration tab"""
        keywords_frame = tk.Frame(self.notebook, bg=self.theme_colors.get('bg', '#ffffff'))
        
        # Header
        header = tk.Label(
            keywords_frame,
            text="🔤 Language Keywords",
            font=('Arial', 18, 'bold'),
            bg=self.theme_colors.get('bg', '#ffffff'),
            fg=self.theme_colors.get('fg', '#000000')
        )
        header.pack(pady=20)
        
        # Content area with form
        content = tk.Frame(keywords_frame, bg=self.theme_colors.get('bg', '#ffffff'))
        content.pack(fill='both', expand=True, padx=40)
        
        self.create_keywords_form(content)
        
        return keywords_frame
    
    def create_playground_tab(self):
        """Create the code playground tab"""
        playground_frame = tk.Frame(self.notebook, bg=self.theme_colors.get('bg', '#ffffff'))
        
        # Header with controls
        header_frame = tk.Frame(playground_frame, bg=self.theme_colors.get('toolbar', '#ffffff'), height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Title
        tk.Label(
            header_frame,
            text="🎮 Code Playground",
            font=('Arial', 16, 'bold'),
            bg=self.theme_colors.get('toolbar', '#ffffff'),
            fg=self.theme_colors.get('fg', '#000000')
        ).pack(side='left', padx=20, pady=15)
        
        # Controls
        controls = tk.Frame(header_frame, bg=self.theme_colors.get('toolbar', '#ffffff'))
        controls.pack(side='right', padx=20, pady=10)
        
        # Run button
        run_btn = tk.Button(
            controls,
            text="▶ Run Code",
            command=self.callbacks.get('run_playground', lambda: None),
            bg=self.theme_colors.get('success', '#51cf66'),
            fg='white',
            font=('Arial', 11, 'bold'),
            padx=20,
            pady=8,
            cursor='hand2'
        )
        run_btn.pack(side='left', padx=5)
        
        # Clear button
        clear_btn = tk.Button(
            controls,
            text="🗑 Clear",
            command=self.callbacks.get('clear_output', lambda: None),
            bg=self.theme_colors.get('border', '#e9ecef'),
            fg=self.theme_colors.get('fg', '#000000'),
            font=('Arial', 11),
            padx=15,
            pady=8,
            cursor='hand2'
        )
        clear_btn.pack(side='left', padx=5)
        
        # Main content area
        main_frame = tk.Frame(playground_frame, bg=self.theme_colors.get('bg', '#ffffff'))
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Create paned window for code editor and output
        paned_window = tk.PanedWindow(main_frame, orient=tk.HORIZONTAL, bg=self.theme_colors.get('bg', '#ffffff'))
        paned_window.pack(fill='both', expand=True)
        
        # Code editor area
        editor_frame = tk.Frame(paned_window, bg=self.theme_colors.get('bg', '#ffffff'))
        
        tk.Label(
            editor_frame,
            text="Code Editor:",
            font=('Arial', 12, 'bold'),
            bg=self.theme_colors.get('bg', '#ffffff'),
            fg=self.theme_colors.get('fg', '#000000')
        ).pack(anchor='w', pady=(0, 5))
        
        # Code text area
        self.code_editor = tk.Text(
            editor_frame,
            font=('Courier', 11),
            bg=self.theme_colors.get('card', '#f8f9fa'),
            fg=self.theme_colors.get('fg', '#000000'),
            insertbackground=self.theme_colors.get('accent', '#667eea'),
            selectbackground=self.theme_colors.get('accent', '#667eea'),
            selectforeground='white',
            wrap='none',
            undo=True,
            maxundo=20
        )
        self.code_editor.pack(fill='both', expand=True, pady=(0, 10))
        
        # Insert sample code
        sample_code = """// Write your code here using your language's keywords
// Example:
variable greeting = "Hello, World!"
print(greeting)

function sayHello(name) {
    print("Hello, " + name + "!")
}

sayHello("Coder")"""
        
        self.code_editor.insert('1.0', sample_code)
        
        # Output area
        output_frame = tk.Frame(paned_window, bg=self.theme_colors.get('bg', '#ffffff'))
        
        tk.Label(
            output_frame,
            text="Output:",
            font=('Arial', 12, 'bold'),
            bg=self.theme_colors.get('bg', '#ffffff'),
            fg=self.theme_colors.get('fg', '#000000')
        ).pack(anchor='w', pady=(0, 5))
        
        # Output text area
        self.output_text = tk.Text(
            output_frame,
            font=('Courier', 11),
            bg=self.theme_colors.get('card', '#f8f9fa'),
            fg=self.theme_colors.get('fg', '#000000'),
            wrap='word',
            state='disabled',
            height=20
        )
        self.output_text.pack(fill='both', expand=True, pady=(0, 10))
        
        # Add scrollbars
        editor_scrollbar = tk.Scrollbar(editor_frame)
        editor_scrollbar.pack(side='right', fill='y')
        self.code_editor.config(yscrollcommand=editor_scrollbar.set)
        editor_scrollbar.config(command=self.code_editor.yview)
        
        output_scrollbar = tk.Scrollbar(output_frame)
        output_scrollbar.pack(side='right', fill='y')
        self.output_text.config(yscrollcommand=output_scrollbar.set)
        output_scrollbar.config(command=self.output_text.yview)
        
        # Add frames to paned window
        paned_window.add(editor_frame, width=400)
        paned_window.add(output_frame, width=400)
        
        return playground_frame
    
    def create_action_card(self, parent, title, description, command):
        """Create an action card for the welcome tab"""
        card = tk.Frame(
            parent,
            bg=self.theme_colors.get('card', '#f8f9fa'),
            relief='solid',
            bd=1,
            cursor='hand2'
        )
        
        # Title
        title_label = tk.Label(
            card,
            text=title,
            font=('Arial', 14, 'bold'),
            bg=self.theme_colors.get('card', '#f8f9fa'),
            fg=self.theme_colors.get('fg', '#000000')
        )
        title_label.pack(pady=(20, 5), padx=20)
        
        # Description
        desc_label = tk.Label(
            card,
            text=description,
            font=('Arial', 10),
            bg=self.theme_colors.get('card', '#f8f9fa'),
            fg=self.theme_colors.get('fg', '#666666'),
            wraplength=200
        )
        desc_label.pack(pady=(0, 20), padx=20)
        
        # Click binding
        def on_click(event):
            command()
        
        card.bind('<Button-1>', on_click)
        title_label.bind('<Button-1>', on_click)
        desc_label.bind('<Button-1>', on_click)
        
        # Hover effects
        def on_enter(event):
            card.config(bg=self.darken_color(self.theme_colors.get('card', '#f8f9fa')))
            title_label.config(bg=self.darken_color(self.theme_colors.get('card', '#f8f9fa')))
            desc_label.config(bg=self.darken_color(self.theme_colors.get('card', '#f8f9fa')))
        
        def on_leave(event):
            card.config(bg=self.theme_colors.get('card', '#f8f9fa'))
            title_label.config(bg=self.theme_colors.get('card', '#f8f9fa'))
            desc_label.config(bg=self.theme_colors.get('card', '#f8f9fa'))
        
        card.bind('<Enter>', on_enter)
        card.bind('<Leave>', on_leave)
        
        return card
    
    def create_info_form(self, parent):
        """Create the language information form"""
        # Store entry widgets for later updates
        self.info_entries = {}
        
        # Language Name
        tk.Label(
            parent,
            text="Language Name:",
            font=('Arial', 12, 'bold'),
            bg=self.theme_colors.get('bg', '#ffffff'),
            fg=self.theme_colors.get('fg', '#000000')
        ).pack(anchor='w', pady=(10, 5))
        
        self.info_entries['name'] = tk.Entry(
            parent,
            font=('Arial', 12),
            bg=self.theme_colors.get('card', '#f8f9fa'),
            fg=self.theme_colors.get('fg', '#000000'),
            width=50
        )
        self.info_entries['name'].pack(anchor='w', pady=(0, 15))
        self.info_entries['name'].insert(0, self.language_data.get('name', 'MyLang'))
        
        # Version
        tk.Label(
            parent,
            text="Version:",
            font=('Arial', 12, 'bold'),
            bg=self.theme_colors.get('bg', '#ffffff'),
            fg=self.theme_colors.get('fg', '#000000')
        ).pack(anchor='w', pady=(0, 5))
        
        self.info_entries['version'] = tk.Entry(
            parent,
            font=('Arial', 12),
            bg=self.theme_colors.get('card', '#f8f9fa'),
            fg=self.theme_colors.get('fg', '#000000'),
            width=20
        )
        self.info_entries['version'].pack(anchor='w', pady=(0, 15))
        self.info_entries['version'].insert(0, self.language_data.get('version', '1.0'))
        
        # Author
        tk.Label(
            parent,
            text="Author:",
            font=('Arial', 12, 'bold'),
            bg=self.theme_colors.get('bg', '#ffffff'),
            fg=self.theme_colors.get('fg', '#000000')
        ).pack(anchor='w', pady=(0, 5))
        
        self.info_entries['author'] = tk.Entry(
            parent,
            font=('Arial', 12),
            bg=self.theme_colors.get('card', '#f8f9fa'),
            fg=self.theme_colors.get('fg', '#000000'),
            width=50
        )
        self.info_entries['author'].pack(anchor='w', pady=(0, 15))
        self.info_entries['author'].insert(0, self.language_data.get('author', 'Young Coder'))
        
        # Description
        tk.Label(
            parent,
            text="Description:",
            font=('Arial', 12, 'bold'),
            bg=self.theme_colors.get('bg', '#ffffff'),
            fg=self.theme_colors.get('fg', '#000000')
        ).pack(anchor='w', pady=(0, 5))
        
        self.info_entries['description'] = tk.Text(
            parent,
            font=('Arial', 12),
            bg=self.theme_colors.get('card', '#f8f9fa'),
            fg=self.theme_colors.get('fg', '#000000'),
            width=60,
            height=5
        )
        self.info_entries['description'].pack(anchor='w', pady=(0, 15))
        self.info_entries['description'].insert('1.0', self.language_data.get('description', 'My awesome programming language!'))
    
    def create_keywords_form(self, parent):
        """Create the keywords configuration form"""
        # Store keyword entries for later updates
        self.keyword_entries = {}
        
        # Instructions
        tk.Label(
            parent,
            text="Define keywords for your language:",
            font=('Arial', 12),
            bg=self.theme_colors.get('bg', '#ffffff'),
            fg=self.theme_colors.get('fg', '#000000')
        ).pack(anchor='w', pady=(10, 20))
        
        # Common keywords
        keywords = [
            ('variable', 'Variable declaration keyword'),
            ('function', 'Function definition keyword'),
            ('if', 'Conditional statement keyword'),
            ('else', 'Else statement keyword'),
            ('while', 'While loop keyword'),
            ('for', 'For loop keyword'),
            ('return', 'Return statement keyword'),
            ('print', 'Print/output keyword'),
            ('input', 'Input keyword'),
            ('true', 'Boolean true keyword'),
            ('false', 'Boolean false keyword'),
            ('null', 'Null/empty value keyword')
        ]
        
        for keyword, description in keywords:
            self._create_keyword_entry(parent, keyword, description)
    
    def _create_keyword_entry(self, parent, keyword, description):
        """Create a single keyword entry"""
        frame = tk.Frame(parent, bg=self.theme_colors.get('bg', '#ffffff'))
        frame.pack(fill='x', pady=5)
        
        # Label
        tk.Label(
            frame,
            text=f"{keyword.capitalize()}:",
            font=('Arial', 10, 'bold'),
            bg=self.theme_colors.get('bg', '#ffffff'),
            fg=self.theme_colors.get('fg', '#000000'),
            width=12,
            anchor='w'
        ).pack(side='left')
        
        # Entry
        entry = tk.Entry(
            frame,
            font=('Arial', 10),
            bg=self.theme_colors.get('card', '#f8f9fa'),
            fg=self.theme_colors.get('fg', '#000000'),
            width=20
        )
        entry.pack(side='left', padx=(10, 20))
        
        # Store reference
        self.keyword_entries[keyword] = entry
        
        # Set default value
        current_value = self.language_data.get('keywords', {}).get(keyword, keyword)
        entry.insert(0, current_value)
        
        # Description
        tk.Label(
            frame,
            text=description,
            font=('Arial', 9),
            bg=self.theme_colors.get('bg', '#ffffff'),
            fg=self.theme_colors.get('secondary', '#666666')
        ).pack(side='left')
    
    def update_info_tab(self, language_data):
        """Update the info tab with new language data"""
        if hasattr(self, 'info_entries'):
            # Clear and update entries
            for key, widget in self.info_entries.items():
                if key == 'description':
                    widget.delete('1.0', tk.END)
                    widget.insert('1.0', language_data.get(key, ''))
                else:
                    widget.delete(0, tk.END)
                    widget.insert(0, language_data.get(key, ''))
    
    def update_keywords_tab(self, language_data):
        """Update the keywords tab with new language data"""
        if hasattr(self, 'keyword_entries'):
            keywords_data = language_data.get('keywords', {})
            for keyword, entry in self.keyword_entries.items():
                entry.delete(0, tk.END)
                entry.insert(0, keywords_data.get(keyword, keyword))
    
    def update_operators_tab(self, language_data):
        """Update the operators tab with new language data"""
        if hasattr(self, 'operator_entries'):
            operators_data = language_data.get('operators', {})
            for operator, entry in self.operator_entries.items():
                entry.delete(0, tk.END)
                default_value = self._get_default_operator_value(operator)
                entry.insert(0, operators_data.get(operator, default_value))
    
    def update_builtins_tab(self, language_data):
        """Update the built-ins tab with new language data"""
        if hasattr(self, 'builtin_entries'):
            builtins_data = language_data.get('builtins', {})
            for builtin, entry in self.builtin_entries.items():
                entry.delete(0, tk.END)
                entry.insert(0, builtins_data.get(builtin, builtin))
    
    def update_errors_tab(self, language_data):
        """Update the errors tab with new language data"""
        if hasattr(self, 'error_entries'):
            errors_data = language_data.get('errors', {})
            for error, entry in self.error_entries.items():
                entry.delete(0, tk.END)
                default_message = self._get_default_error_message(error)
                entry.insert(0, errors_data.get(error, default_message))
    
    def _get_default_operator_value(self, operator):
        """Get default value for operator"""
        defaults = {
            'addition': '+', 'subtraction': '-', 'multiplication': '*', 'division': '/',
            'modulo': '%', 'power': '**', 'equal': '==', 'not_equal': '!=',
            'less_than': '<', 'greater_than': '>', 'less_equal': '<=', 'greater_equal': '>=',
            'and': '&&', 'or': '||', 'not': '!', 'assign': '=', 'plus_assign': '+=', 'minus_assign': '-='
        }
        return defaults.get(operator, '=')
    
    def _get_default_error_message(self, error):
        """Get default error message"""
        defaults = {
            'syntax_error': 'Syntax Error: Invalid syntax',
            'name_error': 'Name Error: Variable not defined',
            'type_error': 'Type Error: Invalid type operation',
            'value_error': 'Value Error: Invalid value',
            'index_error': 'Index Error: Index out of range',
            'key_error': 'Key Error: Key not found',
            'division_error': 'Division Error: Division by zero',
            'import_error': 'Import Error: Module not found',
            'runtime_error': 'Runtime Error: Execution failed',
            'memory_error': 'Memory Error: Out of memory',
            'recursion_error': 'Recursion Error: Maximum recursion depth exceeded',
            'file_error': 'File Error: File not found or access denied',
            'permission_error': 'Permission Error: Access denied',
            'timeout_error': 'Timeout Error: Operation timed out',
            'validation_error': 'Validation Error: Input validation failed'
        }
        return defaults.get(error, 'Error: Unknown error')
    
    def create_operators_tab(self):
        """Create the operators configuration tab"""
        operators_frame = tk.Frame(self.notebook, bg=self.theme_colors.get('bg', '#ffffff'))
        
        # Header
        header = tk.Label(
            operators_frame,
            text="➕ Language Operators",
            font=('Arial', 18, 'bold'),
            bg=self.theme_colors.get('bg', '#ffffff'),
            fg=self.theme_colors.get('fg', '#000000')
        )
        header.pack(pady=20)
        
        # Description
        desc = tk.Label(
            operators_frame,
            text="Define the operators your language will support",
            font=('Arial', 11),
            bg=self.theme_colors.get('bg', '#ffffff'),
            fg=self.theme_colors.get('secondary', '#666666')
        )
        desc.pack(pady=(0, 20))
        
        # Scrollable content
        canvas = tk.Canvas(operators_frame, bg=self.theme_colors.get('bg', '#ffffff'))
        scrollbar = ttk.Scrollbar(operators_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.theme_colors.get('bg', '#ffffff'))
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Content area
        content = tk.Frame(scrollable_frame, bg=self.theme_colors.get('bg', '#ffffff'))
        content.pack(fill='both', expand=True, padx=40)
        
        self.create_operators_form(content)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        return operators_frame
    
    def create_operators_form(self, parent):
        """Create the operators configuration form"""
        # Store operator entries for later updates
        self.operator_entries = {}
        
        # Instructions
        tk.Label(
            parent,
            text="Configure operators for your language:",
            font=('Arial', 12),
            bg=self.theme_colors.get('bg', '#ffffff'),
            fg=self.theme_colors.get('fg', '#000000')
        ).pack(anchor='w', pady=(10, 20))
        
        # Operator categories
        categories = [
            ("Arithmetic", [
                ('addition', '+', 'Addition operator'),
                ('subtraction', '-', 'Subtraction operator'),
                ('multiplication', '*', 'Multiplication operator'),
                ('division', '/', 'Division operator'),
                ('modulo', '%', 'Modulo operator'),
                ('power', '**', 'Power operator')
            ]),
            ("Comparison", [
                ('equal', '==', 'Equal to operator'),
                ('not_equal', '!=', 'Not equal to operator'),
                ('less_than', '<', 'Less than operator'),
                ('greater_than', '>', 'Greater than operator'),
                ('less_equal', '<=', 'Less than or equal operator'),
                ('greater_equal', '>=', 'Greater than or equal operator')
            ]),
            ("Logical", [
                ('and', '&&', 'Logical AND operator'),
                ('or', '||', 'Logical OR operator'),
                ('not', '!', 'Logical NOT operator')
            ]),
            ("Assignment", [
                ('assign', '=', 'Assignment operator'),
                ('plus_assign', '+=', 'Plus assignment operator'),
                ('minus_assign', '-=', 'Minus assignment operator')
            ])
        ]
        
        for category_name, operators in categories:
            # Category header
            category_frame = tk.Frame(parent, bg=self.theme_colors.get('bg', '#ffffff'))
            category_frame.pack(fill='x', pady=(20, 10))
            
            tk.Label(
                category_frame,
                text=f"{category_name} Operators",
                font=('Arial', 14, 'bold'),
                bg=self.theme_colors.get('bg', '#ffffff'),
                fg=self.theme_colors.get('primary', '#667eea')
            ).pack(anchor='w')
            
            # Operators in this category
            for op_key, default_op, description in operators:
                self._create_operator_entry(parent, op_key, default_op, description)
    
    def _create_operator_entry(self, parent, op_key, default_op, description):
        """Create a single operator entry"""
        frame = tk.Frame(parent, bg=self.theme_colors.get('bg', '#ffffff'))
        frame.pack(fill='x', pady=5)
        
        # Label
        tk.Label(
            frame,
            text=f"{op_key.replace('_', ' ').title()}:",
            font=('Arial', 10, 'bold'),
            bg=self.theme_colors.get('bg', '#ffffff'),
            fg=self.theme_colors.get('fg', '#000000'),
            width=15,
            anchor='w'
        ).pack(side='left')
        
        # Entry
        entry = tk.Entry(
            frame,
            font=('Arial', 10),
            bg=self.theme_colors.get('card', '#f8f9fa'),
            fg=self.theme_colors.get('fg', '#000000'),
            width=10
        )
        entry.pack(side='left', padx=(10, 20))
        
        # Store reference
        self.operator_entries[op_key] = entry
        
        # Set default value
        current_value = self.language_data.get('operators', {}).get(op_key, default_op)
        entry.insert(0, current_value)
        
        # Description
        tk.Label(
            frame,
            text=description,
            font=('Arial', 9),
            bg=self.theme_colors.get('bg', '#ffffff'),
            fg=self.theme_colors.get('secondary', '#666666')
        ).pack(side='left')
    
    def create_builtins_tab(self):
        """Create the built-in functions tab"""
        builtins_frame = tk.Frame(self.notebook, bg=self.theme_colors.get('bg', '#ffffff'))
        
        # Header
        header = tk.Label(
            builtins_frame,
            text="🛠️ Built-in Functions",
            font=('Arial', 18, 'bold'),
            bg=self.theme_colors.get('bg', '#ffffff'),
            fg=self.theme_colors.get('fg', '#000000')
        )
        header.pack(pady=20)
        
        # Description
        desc = tk.Label(
            builtins_frame,
            text="Define the built-in functions available in your language",
            font=('Arial', 11),
            bg=self.theme_colors.get('bg', '#ffffff'),
            fg=self.theme_colors.get('secondary', '#666666')
        )
        desc.pack(pady=(0, 20))
        
        # Scrollable content
        canvas = tk.Canvas(builtins_frame, bg=self.theme_colors.get('bg', '#ffffff'))
        scrollbar = ttk.Scrollbar(builtins_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.theme_colors.get('bg', '#ffffff'))
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Content area
        content = tk.Frame(scrollable_frame, bg=self.theme_colors.get('bg', '#ffffff'))
        content.pack(fill='both', expand=True, padx=40)
        
        self.create_builtins_form(content)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        return builtins_frame
    
    def create_builtins_form(self, parent):
        """Create the built-in functions form"""
        # Store builtin entries for later updates
        self.builtin_entries = {}
        
        # Instructions
        tk.Label(
            parent,
            text="Define built-in functions for your language:",
            font=('Arial', 12),
            bg=self.theme_colors.get('bg', '#ffffff'),
            fg=self.theme_colors.get('fg', '#000000')
        ).pack(anchor='w', pady=(10, 20))
        
        # Built-in functions
        builtins = [
            ('print', 'print', 'Output/display function'),
            ('input', 'input', 'User input function'),
            ('len', 'len', 'Get length of string/array'),
            ('str', 'str', 'Convert to string'),
            ('int', 'int', 'Convert to integer'),
            ('float', 'float', 'Convert to float'),
            ('bool', 'bool', 'Convert to boolean'),
            ('type', 'type', 'Get type of variable'),
            ('range', 'range', 'Generate range of numbers'),
            ('max', 'max', 'Get maximum value'),
            ('min', 'min', 'Get minimum value'),
            ('sum', 'sum', 'Sum of numbers'),
            ('abs', 'abs', 'Absolute value'),
            ('round', 'round', 'Round number'),
            ('random', 'random', 'Random number generator'),
            ('upper', 'upper', 'Convert to uppercase'),
            ('lower', 'lower', 'Convert to lowercase'),
            ('split', 'split', 'Split string'),
            ('join', 'join', 'Join strings'),
            ('replace', 'replace', 'Replace substring')
        ]
        
        for builtin_key, default_name, description in builtins:
            self._create_builtin_entry(parent, builtin_key, default_name, description)
    
    def _create_builtin_entry(self, parent, builtin_key, default_name, description):
        """Create a single built-in function entry"""
        frame = tk.Frame(parent, bg=self.theme_colors.get('bg', '#ffffff'))
        frame.pack(fill='x', pady=5)
        
        # Label
        tk.Label(
            frame,
            text=f"{builtin_key.capitalize()}:",
            font=('Arial', 10, 'bold'),
            bg=self.theme_colors.get('bg', '#ffffff'),
            fg=self.theme_colors.get('fg', '#000000'),
            width=12,
            anchor='w'
        ).pack(side='left')
        
        # Entry
        entry = tk.Entry(
            frame,
            font=('Arial', 10),
            bg=self.theme_colors.get('card', '#f8f9fa'),
            fg=self.theme_colors.get('fg', '#000000'),
            width=20
        )
        entry.pack(side='left', padx=(10, 20))
        
        # Store reference
        self.builtin_entries[builtin_key] = entry
        
        # Set default value
        current_value = self.language_data.get('builtins', {}).get(builtin_key, default_name)
        entry.insert(0, current_value)
        
        # Description
        tk.Label(
            frame,
            text=description,
            font=('Arial', 9),
            bg=self.theme_colors.get('bg', '#ffffff'),
            fg=self.theme_colors.get('secondary', '#666666')
        ).pack(side='left')
    
    def create_errors_tab(self):
        """Create the error messages tab"""
        errors_frame = tk.Frame(self.notebook, bg=self.theme_colors.get('bg', '#ffffff'))
        
        # Header
        header = tk.Label(
            errors_frame,
            text="❌ Error Messages",
            font=('Arial', 18, 'bold'),
            bg=self.theme_colors.get('bg', '#ffffff'),
            fg=self.theme_colors.get('fg', '#000000')
        )
        header.pack(pady=20)
        
        # Description
        desc = tk.Label(
            errors_frame,
            text="Customize error messages for your language",
            font=('Arial', 11),
            bg=self.theme_colors.get('bg', '#ffffff'),
            fg=self.theme_colors.get('secondary', '#666666')
        )
        desc.pack(pady=(0, 20))
        
        # Scrollable content
        canvas = tk.Canvas(errors_frame, bg=self.theme_colors.get('bg', '#ffffff'))
        scrollbar = ttk.Scrollbar(errors_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.theme_colors.get('bg', '#ffffff'))
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Content area
        content = tk.Frame(scrollable_frame, bg=self.theme_colors.get('bg', '#ffffff'))
        content.pack(fill='both', expand=True, padx=40)
        
        self.create_errors_form(content)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        return errors_frame
    
    def create_errors_form(self, parent):
        """Create the error messages form"""
        # Store error entries for later updates
        self.error_entries = {}
        
        # Instructions
        tk.Label(
            parent,
            text="Define custom error messages for your language:",
            font=('Arial', 12),
            bg=self.theme_colors.get('bg', '#ffffff'),
            fg=self.theme_colors.get('fg', '#000000')
        ).pack(anchor='w', pady=(10, 20))
        
        # Error types
        errors = [
            ('syntax_error', 'Syntax Error: Invalid syntax'),
            ('name_error', 'Name Error: Variable not defined'),
            ('type_error', 'Type Error: Invalid type operation'),
            ('value_error', 'Value Error: Invalid value'),
            ('index_error', 'Index Error: Index out of range'),
            ('key_error', 'Key Error: Key not found'),
            ('division_error', 'Division Error: Division by zero'),
            ('import_error', 'Import Error: Module not found'),
            ('runtime_error', 'Runtime Error: Execution failed'),
            ('memory_error', 'Memory Error: Out of memory'),
            ('recursion_error', 'Recursion Error: Maximum recursion depth exceeded'),
            ('file_error', 'File Error: File not found or access denied'),
            ('permission_error', 'Permission Error: Access denied'),
            ('timeout_error', 'Timeout Error: Operation timed out'),
            ('validation_error', 'Validation Error: Input validation failed')
        ]
        
        for error_key, default_message in errors:
            self._create_error_entry(parent, error_key, default_message)
    
    def _create_error_entry(self, parent, error_key, default_message):
        """Create a single error message entry"""
        frame = tk.Frame(parent, bg=self.theme_colors.get('bg', '#ffffff'))
        frame.pack(fill='x', pady=8)
        
        # Label
        tk.Label(
            frame,
            text=f"{error_key.replace('_', ' ').title()}:",
            font=('Arial', 10, 'bold'),
            bg=self.theme_colors.get('bg', '#ffffff'),
            fg=self.theme_colors.get('fg', '#000000'),
            width=18,
            anchor='w'
        ).pack(anchor='w')
        
        # Entry
        entry = tk.Entry(
            frame,
            font=('Arial', 10),
            bg=self.theme_colors.get('card', '#f8f9fa'),
            fg=self.theme_colors.get('fg', '#000000'),
            width=80
        )
        entry.pack(fill='x', pady=(5, 0))
        
        # Store reference
        self.error_entries[error_key] = entry
        
        # Set default value
        current_value = self.language_data.get('errors', {}).get(error_key, default_message)
        entry.insert(0, current_value)
    
    def create_preview_tab(self):
        """Create the language preview tab"""
        preview_frame = tk.Frame(self.notebook, bg=self.theme_colors.get('bg', '#ffffff'))
        
        # Header
        header_frame = tk.Frame(preview_frame, bg=self.theme_colors.get('primary', '#667eea'), height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title = tk.Label(
            header_frame,
            text="👀 Language Preview",
            font=('Arial', 18, 'bold'),
            bg=self.theme_colors.get('primary', '#667eea'),
            fg='white'
        )
        title.pack(pady=25)
        
        # Main content area
        main_frame = tk.Frame(preview_frame, bg=self.theme_colors.get('bg', '#ffffff'))
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Refresh button
        refresh_frame = tk.Frame(main_frame, bg=self.theme_colors.get('bg', '#ffffff'))
        refresh_frame.pack(fill='x', pady=(0, 20))
        
        refresh_btn = tk.Button(
            refresh_frame,
            text="🔄 Refresh Preview",
            command=self._refresh_preview,
            bg=self.theme_colors.get('accent', '#667eea'),
            fg='white',
            font=('Arial', 11, 'bold'),
            padx=20,
            pady=8
        )
        refresh_btn.pack(side='left')
        
        # Create scrollable preview area
        canvas = tk.Canvas(main_frame, bg=self.theme_colors.get('bg', '#ffffff'))
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        self.preview_content = tk.Frame(canvas, bg=self.theme_colors.get('bg', '#ffffff'))
        
        self.preview_content.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.preview_content, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Initial preview generation
        self._generate_preview()
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        return preview_frame
    
    def _refresh_preview(self):
        """Refresh the language preview"""
        # Clear existing content
        for widget in self.preview_content.winfo_children():
            widget.destroy()
        
        # Regenerate preview
        self._generate_preview()
    
    def _generate_preview(self):
        """Generate the language preview content"""
        # Language Overview Section
        self._create_preview_section(
            "📋 Language Overview",
            self._create_language_overview
        )
        
        # Keywords Section
        self._create_preview_section(
            "🔤 Keywords",
            self._create_keywords_preview
        )
        
        # Operators Section
        self._create_preview_section(
            "➕ Operators",
            self._create_operators_preview
        )
        
        # Built-ins Section
        self._create_preview_section(
            "🛠️ Built-in Functions",
            self._create_builtins_preview
        )
        
        # Error Messages Section
        self._create_preview_section(
            "❌ Error Messages",
            self._create_errors_preview
        )
        
        # Sample Code Section
        self._create_preview_section(
            "💻 Sample Code",
            self._create_sample_code_preview
        )
    
    def _create_preview_section(self, title, content_generator):
        """Create a preview section with title and content"""
        # Section frame
        section_frame = tk.Frame(
            self.preview_content,
            bg=self.theme_colors.get('card', '#f8f9fa'),
            relief='raised',
            bd=1
        )
        section_frame.pack(fill='x', pady=10, padx=10)
        
        # Section title
        title_label = tk.Label(
            section_frame,
            text=title,
            font=('Arial', 14, 'bold'),
            bg=self.theme_colors.get('card', '#f8f9fa'),
            fg=self.theme_colors.get('fg', '#000000')
        )
        title_label.pack(pady=(15, 10), padx=20, anchor='w')
        
        # Section content
        content_frame = tk.Frame(section_frame, bg=self.theme_colors.get('card', '#f8f9fa'))
        content_frame.pack(fill='both', expand=True, padx=20, pady=(0, 15))
        
        content_generator(content_frame)
    
    def _create_language_overview(self, parent):
        """Create language overview content"""
        info_text = f"""
Name: {self.language_data.get('name', 'Untitled')}
Version: {self.language_data.get('version', '1.0')}
Author: {self.language_data.get('author', 'Unknown')}
Created: {self.language_data.get('created', 'Unknown')}

Description:
{self.language_data.get('description', 'No description available')}
"""
        
        text_widget = tk.Text(
            parent,
            height=8,
            font=('Arial', 10),
            bg=self.theme_colors.get('bg', '#ffffff'),
            fg=self.theme_colors.get('fg', '#000000'),
            wrap='word',
            state='disabled'
        )
        text_widget.pack(fill='x')
        
        text_widget.config(state='normal')
        text_widget.insert('1.0', info_text)
        text_widget.config(state='disabled')
    
    def _create_keywords_preview(self, parent):
        """Create keywords preview content"""
        keywords = self.language_data.get('keywords', {})
        
        if not keywords:
            tk.Label(
                parent,
                text="No keywords defined yet",
                font=('Arial', 10),
                bg=self.theme_colors.get('card', '#f8f9fa'),
                fg=self.theme_colors.get('secondary', '#666666')
            ).pack(anchor='w')
            return
        
        # Create grid of keywords
        for i, (key, value) in enumerate(keywords.items()):
            row = i // 3
            col = i % 3
            
            keyword_frame = tk.Frame(parent, bg=self.theme_colors.get('card', '#f8f9fa'))
            keyword_frame.grid(row=row, column=col, padx=10, pady=5, sticky='w')
            
            tk.Label(
                keyword_frame,
                text=f"{key}:",
                font=('Arial', 10, 'bold'),
                bg=self.theme_colors.get('card', '#f8f9fa'),
                fg=self.theme_colors.get('fg', '#000000')
            ).pack(side='left')
            
            tk.Label(
                keyword_frame,
                text=value,
                font=('Arial', 10),
                bg=self.theme_colors.get('accent', '#667eea'),
                fg='white',
                padx=8,
                pady=2
            ).pack(side='left', padx=(5, 0))
    
    def _create_operators_preview(self, parent):
        """Create operators preview content"""
        operators = self.language_data.get('operators', {})
        
        if not operators:
            tk.Label(
                parent,
                text="No operators defined yet",
                font=('Arial', 10),
                bg=self.theme_colors.get('card', '#f8f9fa'),
                fg=self.theme_colors.get('secondary', '#666666')
            ).pack(anchor='w')
            return
        
        # Group operators by type
        operator_text = ""
        for key, value in operators.items():
            operator_text += f"{key.replace('_', ' ').title()}: {value}\n"
        
        text_widget = tk.Text(
            parent,
            height=6,
            font=('Arial', 10),
            bg=self.theme_colors.get('bg', '#ffffff'),
            fg=self.theme_colors.get('fg', '#000000'),
            wrap='word',
            state='disabled'
        )
        text_widget.pack(fill='x')
        
        text_widget.config(state='normal')
        text_widget.insert('1.0', operator_text)
        text_widget.config(state='disabled')
    
    def _create_builtins_preview(self, parent):
        """Create built-ins preview content"""
        builtins = self.language_data.get('builtins', {})
        
        if not builtins:
            tk.Label(
                parent,
                text="No built-in functions defined yet",
                font=('Arial', 10),
                bg=self.theme_colors.get('card', '#f8f9fa'),
                fg=self.theme_colors.get('secondary', '#666666')
            ).pack(anchor='w')
            return
        
        # Show built-ins in a formatted way
        builtin_text = ""
        for key, value in builtins.items():
            builtin_text += f"{value}() - {key.replace('_', ' ').title()}\n"
        
        text_widget = tk.Text(
            parent,
            height=8,
            font=('Arial', 10),
            bg=self.theme_colors.get('bg', '#ffffff'),
            fg=self.theme_colors.get('fg', '#000000'),
            wrap='word',
            state='disabled'
        )
        text_widget.pack(fill='x')
        
        text_widget.config(state='normal')
        text_widget.insert('1.0', builtin_text)
        text_widget.config(state='disabled')
    
    def _create_errors_preview(self, parent):
        """Create errors preview content"""
        errors = self.language_data.get('errors', {})
        
        if not errors:
            tk.Label(
                parent,
                text="No error messages defined yet",
                font=('Arial', 10),
                bg=self.theme_colors.get('card', '#f8f9fa'),
                fg=self.theme_colors.get('secondary', '#666666')
            ).pack(anchor='w')
            return
        
        # Show first few error messages
        error_text = ""
        for key, value in list(errors.items())[:5]:  # Show first 5
            error_text += f"{key.replace('_', ' ').title()}: {value}\n"
        
        if len(errors) > 5:
            error_text += f"... and {len(errors) - 5} more error messages"
        
        text_widget = tk.Text(
            parent,
            height=6,
            font=('Arial', 10),
            bg=self.theme_colors.get('bg', '#ffffff'),
            fg=self.theme_colors.get('fg', '#000000'),
            wrap='word',
            state='disabled'
        )
        text_widget.pack(fill='x')
        
        text_widget.config(state='normal')
        text_widget.insert('1.0', error_text)
        text_widget.config(state='disabled')
    
    def _create_sample_code_preview(self, parent):
        """Create sample code preview"""
        # Generate sample code using the language's keywords
        keywords = self.language_data.get('keywords', {})
        
        var_keyword = keywords.get('variable', 'variable')
        func_keyword = keywords.get('function', 'function')
        if_keyword = keywords.get('if', 'if')
        print_keyword = keywords.get('print', 'print')
        
        sample_code = f"""// Sample code in {self.language_data.get('name', 'MyLang')}

{var_keyword} greeting = "Hello, World!"
{var_keyword} name = "Programmer"

{func_keyword} sayHello(person) {{
    {print_keyword}(greeting + " " + person + "!")
}}

{if_keyword} (name != "") {{
    sayHello(name)
}}

{print_keyword}("Welcome to {self.language_data.get('name', 'MyLang')}!")"""
        
        text_widget = tk.Text(
            parent,
            height=12,
            font=('Courier', 10),
            bg=self.theme_colors.get('bg', '#ffffff'),
            fg=self.theme_colors.get('fg', '#000000'),
            wrap='none',
            state='disabled'
        )
        text_widget.pack(fill='x')
        
        text_widget.config(state='normal')
        text_widget.insert('1.0', sample_code)
        text_widget.config(state='disabled')
    
    def darken_color(self, color):
        """Darken a color for hover effects"""
        if color.startswith('#'):
            color = color[1:]
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        darkened = tuple(max(0, c - 15) for c in rgb)
        return f'#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}'

class DialogCreator:
    """Creates and manages dialog windows"""
    
    def __init__(self, root, theme_colors, callbacks):
        self.root = root
        self.theme_colors = theme_colors
        self.callbacks = callbacks
    
    def show_about_dialog(self):
        """Show the about dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("About SUPER Language Creator")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Content
        tk.Label(
            dialog,
            text="🚀 SUPER Language Creator",
            font=('Arial', 18, 'bold'),
            fg=self.theme_colors.get('primary', '#667eea')
        ).pack(pady=20)
        
        tk.Label(
            dialog,
            text="Create your own programming languages with ease!",
            font=('Arial', 12)
        ).pack(pady=10)
        
        tk.Label(
            dialog,
            text="Version 2.0",
            font=('Arial', 10)
        ).pack(pady=5)
        
        tk.Button(
            dialog,
            text="Close",
            command=dialog.destroy,
            bg=self.theme_colors.get('primary', '#667eea'),
            fg='white',
            padx=20,
            pady=8
        ).pack(pady=20)
        
        dialog.focus()
    
    def show_preferences_dialog(self):
        """Show the preferences dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("⚙️ Settings & Preferences")
        dialog.geometry("600x500")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg=self.theme_colors.get('bg', '#ffffff'))
        
        # Create notebook for different settings categories
        notebook = ttk.Notebook(dialog)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # General Settings Tab
        general_frame = ttk.Frame(notebook)
        notebook.add(general_frame, text="🏠 General")
        
        # Theme settings
        theme_frame = tk.LabelFrame(general_frame, text="🎨 Theme Settings", font=('Arial', 10, 'bold'))
        theme_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(theme_frame, text="Application Theme:").pack(anchor='w', padx=10, pady=5)
        
        theme_var = tk.StringVar(value="Dark")
        theme_options = ["Light", "Dark", "Blue", "Green", "Purple", "Orange"]
        theme_combo = ttk.Combobox(theme_frame, textvariable=theme_var, values=theme_options, state='readonly')
        theme_combo.pack(anchor='w', padx=10, pady=5)
        
        # Auto-save settings
        autosave_frame = tk.LabelFrame(general_frame, text="💾 Auto-Save", font=('Arial', 10, 'bold'))
        autosave_frame.pack(fill='x', padx=10, pady=5)
        
        autosave_var = tk.BooleanVar(value=True)
        autosave_check = tk.Checkbutton(autosave_frame, text="Enable auto-save every 5 minutes", 
                                       variable=autosave_var, font=('Arial', 9))
        autosave_check.pack(anchor='w', padx=10, pady=5)
        
        backup_var = tk.BooleanVar(value=True)
        backup_check = tk.Checkbutton(autosave_frame, text="Create backup files", 
                                     variable=backup_var, font=('Arial', 9))
        backup_check.pack(anchor='w', padx=10, pady=5)
        
        # Editor Settings Tab
        editor_frame = ttk.Frame(notebook)
        notebook.add(editor_frame, text="📝 Editor")
        
        # Font settings
        font_frame = tk.LabelFrame(editor_frame, text="🔤 Font Settings", font=('Arial', 10, 'bold'))
        font_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(font_frame, text="Font Family:").pack(anchor='w', padx=10, pady=2)
        font_var = tk.StringVar(value="Arial")
        font_combo = ttk.Combobox(font_frame, textvariable=font_var, 
                                 values=["Arial", "Courier New", "Times New Roman", "Consolas", "Monaco"], 
                                 state='readonly')
        font_combo.pack(anchor='w', padx=10, pady=2)
        
        tk.Label(font_frame, text="Font Size:").pack(anchor='w', padx=10, pady=2)
        size_var = tk.StringVar(value="10")
        size_combo = ttk.Combobox(font_frame, textvariable=size_var, 
                                 values=["8", "9", "10", "11", "12", "14", "16", "18"], 
                                 state='readonly')
        size_combo.pack(anchor='w', padx=10, pady=2)
        
        # Code editor settings
        code_frame = tk.LabelFrame(editor_frame, text="💻 Code Editor", font=('Arial', 10, 'bold'))
        code_frame.pack(fill='x', padx=10, pady=5)
        
        line_numbers_var = tk.BooleanVar(value=True)
        line_numbers_check = tk.Checkbutton(code_frame, text="Show line numbers", 
                                          variable=line_numbers_var, font=('Arial', 9))
        line_numbers_check.pack(anchor='w', padx=10, pady=2)
        
        syntax_highlight_var = tk.BooleanVar(value=True)
        syntax_highlight_check = tk.Checkbutton(code_frame, text="Enable syntax highlighting", 
                                               variable=syntax_highlight_var, font=('Arial', 9))
        syntax_highlight_check.pack(anchor='w', padx=10, pady=2)
        
        autocomplete_var = tk.BooleanVar(value=True)
        autocomplete_check = tk.Checkbutton(code_frame, text="Enable auto-completion", 
                                          variable=autocomplete_var, font=('Arial', 9))
        autocomplete_check.pack(anchor='w', padx=10, pady=2)
        
        # Export Settings Tab
        export_frame = ttk.Frame(notebook)
        notebook.add(export_frame, text="📤 Export")
        
        # Default export settings
        export_defaults_frame = tk.LabelFrame(export_frame, text="🎯 Default Export Options", font=('Arial', 10, 'bold'))
        export_defaults_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(export_defaults_frame, text="Default File Extension:").pack(anchor='w', padx=10, pady=2)
        extension_var = tk.StringVar(value=".lang")
        extension_entry = tk.Entry(export_defaults_frame, textvariable=extension_var, font=('Arial', 9))
        extension_entry.pack(anchor='w', padx=10, pady=2)
        
        include_docs_var = tk.BooleanVar(value=True)
        include_docs_check = tk.Checkbutton(export_defaults_frame, text="Include documentation by default", 
                                          variable=include_docs_var, font=('Arial', 9))
        include_docs_check.pack(anchor='w', padx=10, pady=2)
        
        include_examples_var = tk.BooleanVar(value=True)
        include_examples_check = tk.Checkbutton(export_defaults_frame, text="Include example files by default", 
                                               variable=include_examples_var, font=('Arial', 9))
        include_examples_check.pack(anchor='w', padx=10, pady=2)
        
        # Advanced Settings Tab
        advanced_frame = ttk.Frame(notebook)
        notebook.add(advanced_frame, text="🔧 Advanced")
        
        # Performance settings
        performance_frame = tk.LabelFrame(advanced_frame, text="⚡ Performance", font=('Arial', 10, 'bold'))
        performance_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(performance_frame, text="Memory Usage Mode:").pack(anchor='w', padx=10, pady=2)
        memory_var = tk.StringVar(value="Balanced")
        memory_combo = ttk.Combobox(performance_frame, textvariable=memory_var, 
                                   values=["Low", "Balanced", "High Performance"], 
                                   state='readonly')
        memory_combo.pack(anchor='w', padx=10, pady=2)
        
        debug_var = tk.BooleanVar(value=False)
        debug_check = tk.Checkbutton(performance_frame, text="Enable debug mode", 
                                    variable=debug_var, font=('Arial', 9))
        debug_check.pack(anchor='w', padx=10, pady=2)
        
        # Developer options
        dev_frame = tk.LabelFrame(advanced_frame, text="👨‍💻 Developer Options", font=('Arial', 10, 'bold'))
        dev_frame.pack(fill='x', padx=10, pady=5)
        
        verbose_var = tk.BooleanVar(value=False)
        verbose_check = tk.Checkbutton(dev_frame, text="Verbose logging", 
                                     variable=verbose_var, font=('Arial', 9))
        verbose_check.pack(anchor='w', padx=10, pady=2)
        
        experimental_var = tk.BooleanVar(value=False)
        experimental_check = tk.Checkbutton(dev_frame, text="Enable experimental features", 
                                           variable=experimental_var, font=('Arial', 9))
        experimental_check.pack(anchor='w', padx=10, pady=2)
        
        # Buttons frame
        buttons_frame = tk.Frame(dialog, bg=self.theme_colors.get('bg', '#ffffff'))
        buttons_frame.pack(fill='x', padx=10, pady=10)
        
        # Save and Cancel buttons
        def save_preferences():
            # Save preferences logic would go here
            messagebox.showinfo("Settings", "Preferences saved successfully!")
            dialog.destroy()
        
        def reset_defaults():
            result = messagebox.askyesno("Reset", "Reset all settings to default values?")
            if result:
                theme_var.set("Dark")
                autosave_var.set(True)
                backup_var.set(True)
                font_var.set("Arial")
                size_var.set("10")
                line_numbers_var.set(True)
                syntax_highlight_var.set(True)
                autocomplete_var.set(True)
                extension_var.set(".lang")
                include_docs_var.set(True)
                include_examples_var.set(True)
                memory_var.set("Balanced")
                debug_var.set(False)
                verbose_var.set(False)
                experimental_var.set(False)
                messagebox.showinfo("Reset", "Settings reset to defaults!")
        
        tk.Button(buttons_frame, text="🔄 Reset Defaults", command=reset_defaults,
                 bg=self.theme_colors.get('accent', '#4CAF50'), fg='white',
                 font=('Arial', 9, 'bold')).pack(side='left', padx=5)
        
        tk.Button(buttons_frame, text="❌ Cancel", command=dialog.destroy,
                 bg=self.theme_colors.get('secondary', '#757575'), fg='white',
                 font=('Arial', 9, 'bold')).pack(side='right', padx=5)
        
        tk.Button(buttons_frame, text="💾 Save Settings", command=save_preferences,
                 bg=self.theme_colors.get('primary', '#2196F3'), fg='white',
                 font=('Arial', 9, 'bold')).pack(side='right', padx=5)
        
        dialog.focus()

class StatusBarCreator:
    """Creates and manages status bars"""
    
    def __init__(self, root, theme_colors):
        self.root = root
        self.theme_colors = theme_colors
    
    def create_status_bar(self):
        """Create the main status bar"""
        status_bar = tk.Frame(
            self.root,
            bg=self.theme_colors.get('toolbar', '#ffffff'),
            height=25,
            relief='sunken',
            bd=1
        )
        status_bar.pack(side='bottom', fill='x')
        status_bar.pack_propagate(False)
        
        # Status label
        self.status_label = tk.Label(
            status_bar,
            text="Ready",
            bg=self.theme_colors.get('toolbar', '#ffffff'),
            fg=self.theme_colors.get('fg', '#000000'),
            font=('Arial', 9)
        )
        self.status_label.pack(side='left', padx=10)
        
        # Progress info
        self.progress_label = tk.Label(
            status_bar,
            text="",
            bg=self.theme_colors.get('toolbar', '#ffffff'),
            fg=self.theme_colors.get('fg', '#666666'),
            font=('Arial', 9)
        )
        self.progress_label.pack(side='right', padx=10)
        
        return status_bar
    
    def update_status(self, message):
        """Update the status message"""
        if hasattr(self, 'status_label'):
            self.status_label.config(text=message)
    
    def update_progress(self, progress_text):
        """Update the progress information"""
        if hasattr(self, 'progress_label'):
            self.progress_label.config(text=progress_text)

# Additional utility classes would go here for other UI components
# Such as CardCreator, FormCreator, etc.