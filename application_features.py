"""
Application Features Module for LangGen
Contains: Playground, Documentation generation, Statistics, Examples gallery, Tutorial system, and Help dialogs
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
import webbrowser
import random
import time
import threading
from datetime import datetime
from typing import Dict, List, Any, Optional

class PlaygroundManager:
    """Manages the code playground functionality"""
    
    def __init__(self, language_data, ui_components):
        self.language_data = language_data
        self.ui_components = ui_components
        self.playground_running = False
        self.test_count = 0
    
    def run_playground(self):
        """Enhanced playground execution with better feedback"""
        if self.playground_running:
            return
        
        self.playground_running = True
        
        # Update UI state
        if hasattr(self.ui_components, 'run_button'):
            self.ui_components.run_button.config(text="⏳ Running...", state='disabled')
        if hasattr(self.ui_components, 'stop_button'):
            self.ui_components.stop_button.config(state='normal')
        
        # Clear previous output
        if hasattr(self.ui_components, 'output_text'):
            self.ui_components.output_text.delete('1.0', tk.END)
            self.ui_components.output_text.insert('1.0', "🚀 Initializing your language...\\n\\n")
            self.ui_components.output_text.update()
        
        # Show progress
        def show_progress():
            steps = [
                "📝 Analyzing code...",
                "🔤 Processing keywords...",
                "🛠️ Loading functions...",
                "▶️ Executing program..."
            ]
            
            for i, step in enumerate(steps):
                if hasattr(self.ui_components, 'output_text'):
                    self.ui_components.output_text.insert(tk.END, f"{step}\\n")
                    self.ui_components.output_text.see(tk.END)
                    self.ui_components.output_text.update()
                time.sleep(0.3)  # Simulate processing time
            
            # Simulate actual execution
            if hasattr(self.ui_components, 'window'):
                self.ui_components.window.after(500, self.execute_playground_code)
        
        # Start progress in a thread-like manner
        if hasattr(self.ui_components, 'window'):
            self.ui_components.window.after(100, show_progress)
        
        # Track testing for achievements
        self.test_count += 1
        if self.test_count >= 5 and hasattr(self.ui_components, 'unlock_achievement'):
            self.ui_components.unlock_achievement('test_pilot')
    
    def execute_playground_code(self):
        """Execute the playground code with enhanced simulation"""
        if not hasattr(self.ui_components, 'playground_code'):
            return
        
        code = self.ui_components.playground_code.get('1.0', 'end-1c')
        
        if hasattr(self.ui_components, 'output_text'):
            self.ui_components.output_text.insert(tk.END, "\\n" + "="*40 + "\\n")
            self.ui_components.output_text.insert(tk.END, "📤 OUTPUT:\\n\\n")
        
        # Enhanced code simulation
        print_func = self.language_data.get('builtins', {}).get('print', 'print')
        input_func = self.language_data.get('builtins', {}).get('input', 'input')
        
        lines = code.split('\\n')
        output_generated = False
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Simulate print statements
            if print_func in line:
                output_generated = True
                self._simulate_print_statement(line, print_func)
            
            # Simulate variable assignments
            var_keyword = self.language_data.get('keywords', {}).get('variable', 'var')
            if var_keyword in line and '=' in line:
                output_generated = True
                self._simulate_variable_assignment(line, var_keyword)
        
        if not output_generated and hasattr(self.ui_components, 'output_text'):
            self.ui_components.output_text.insert(tk.END, "✨ Program completed successfully!\\n")
            self.ui_components.output_text.insert(tk.END, "(No output produced)\\n")
        
        if hasattr(self.ui_components, 'output_text'):
            self.ui_components.output_text.insert(tk.END, "\\n" + "="*40 + "\\n")
            self.ui_components.output_text.insert(tk.END, "✅ Execution finished!\\n")
        
        # Restore buttons
        self.playground_running = False
        if hasattr(self.ui_components, 'run_button'):
            self.ui_components.run_button.config(text="▶ Run Code", state='normal')
        if hasattr(self.ui_components, 'stop_button'):
            self.ui_components.stop_button.config(state='disabled')
        
        # Update progress
        if hasattr(self.ui_components, 'update_progress'):
            self.ui_components.update_progress()
    
    def _simulate_print_statement(self, line, print_func):
        """Simulate print statement execution"""
        import re
        
        if not hasattr(self.ui_components, 'output_text'):
            return
        
        # Extract content between quotes or parentheses
        matches = re.findall(r'["\']([^"\']*)["\']', line)
        if matches:
            output_text = ' '.join(matches)
            self.ui_components.output_text.insert(tk.END, f"{output_text}\\n")
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
                self.ui_components.output_text.insert(tk.END, f"{output_text}\\n")
    
    def _simulate_variable_assignment(self, line, var_keyword):
        """Simulate variable assignment"""
        if not hasattr(self.ui_components, 'output_text'):
            return
        
        parts = line.split('=')
        if len(parts) == 2:
            var_name = parts[0].replace(var_keyword, '').strip()
            var_value = parts[1].strip().strip('"\'')
            self.ui_components.output_text.insert(tk.END, f"📦 {var_name} = {var_value}\\n")
    
    def stop_playground(self):
        """Stop playground execution"""
        if self.playground_running:
            self.playground_running = False
            if hasattr(self.ui_components, 'run_button'):
                self.ui_components.run_button.config(text="▶ Run Code", state='normal')
            if hasattr(self.ui_components, 'stop_button'):
                self.ui_components.stop_button.config(state='disabled')
            if hasattr(self.ui_components, 'output_text'):
                self.ui_components.output_text.insert(tk.END, "\\n⏹️ Execution stopped by user.\\n")
    
    def clear_output(self):
        """Clear playground output"""
        if hasattr(self.ui_components, 'output_text'):
            self.ui_components.output_text.delete('1.0', tk.END)

class DocumentationGenerator:
    """Generates documentation for languages"""
    
    def __init__(self, language_data):
        self.language_data = language_data
    
    def generate_full_documentation(self):
        """Generate complete documentation"""
        docs = {
            'specification': self.generate_specification(),
            'tutorial': self.generate_tutorial(),
            'reference': self.generate_reference(),
            'examples': self.generate_examples()
        }
        return docs
    
    def generate_specification(self):
        """Generate language specification"""
        spec = f"""# {self.language_data.get('name', 'Unknown')} Language Specification

## Overview
{self.language_data.get('description', 'A custom programming language')}

**Version:** {self.language_data.get('version', '1.0')}
**Author:** {self.language_data.get('author', 'Unknown')}
**Created:** {self.language_data.get('created', 'Unknown')}

## Language Elements

### Keywords
The following keywords are defined in {self.language_data.get('name', 'this language')}:

"""
        
        keywords = self.language_data.get('keywords', {})
        for standard, custom in keywords.items():
            if custom:
                spec += f"- **{custom}** - {standard.replace('_', ' ').title()}\\n"
        
        spec += "\\n### Built-in Functions\\n"
        builtins = self.language_data.get('builtins', {})
        for standard, custom in builtins.items():
            if custom:
                spec += f"- **{custom}()** - {standard.replace('_', ' ').title()} function\\n"
        
        spec += "\\n### Error Messages\\n"
        errors = self.language_data.get('errors', {})
        for error_type, message in errors.items():
            if message:
                spec += f"- **{error_type.title()} Error:** {message}\\n"
        
        return spec
    
    def generate_tutorial(self):
        """Generate a beginner tutorial"""
        lang_name = self.language_data.get('name', 'MyLang')
        
        tutorial = f"""# {lang_name} Tutorial

Welcome to {lang_name}! This tutorial will help you get started with the basics.

## Your First Program

Let's start with the classic "Hello, World!" program:

```{lang_name.lower()}
{self.language_data.get('builtins', {}).get('print', 'print')}("Hello, World!")
```

This will output: `Hello, World!`

## Variables

You can store values in variables:

```{lang_name.lower()}
{self.language_data.get('keywords', {}).get('variable', 'var')} name = "Alice"
{self.language_data.get('keywords', {}).get('variable', 'var')} age = 25
{self.language_data.get('builtins', {}).get('print', 'print')}("Hello", name)
```

## Functions

Define your own functions:

```{lang_name.lower()}
{self.language_data.get('keywords', {}).get('function', 'function')} greet(name) {{
    {self.language_data.get('builtins', {}).get('print', 'print')}("Hello", name)
}}

greet("World")
```

## Conditional Statements

Make decisions in your code:

```{lang_name.lower()}
{self.language_data.get('keywords', {}).get('variable', 'var')} score = 85

{self.language_data.get('keywords', {}).get('if', 'if')} score >= 90 {{
    {self.language_data.get('builtins', {}).get('print', 'print')}("Excellent!")
}} {self.language_data.get('keywords', {}).get('else', 'else')} {{
    {self.language_data.get('builtins', {}).get('print', 'print')}("Good job!")
}}
```

## Loops

Repeat actions:

```{lang_name.lower()}
{self.language_data.get('keywords', {}).get('variable', 'var')} count = 0

{self.language_data.get('keywords', {}).get('loop', 'while')} count < 5 {{
    {self.language_data.get('builtins', {}).get('print', 'print')}(count)
    count = count + 1
}}
```

## Next Steps

Now you know the basics! Try experimenting with these concepts and build your own programs.
"""
        
        return tutorial
    
    def generate_reference(self):
        """Generate language reference"""
        reference = f"""# {self.language_data.get('name', 'Unknown')} Language Reference

## Complete Keyword Reference

"""
        
        keywords = self.language_data.get('keywords', {})
        for standard, custom in keywords.items():
            if custom:
                reference += f"### {custom}\\n"
                reference += f"**Standard equivalent:** {standard}\\n"
                reference += f"**Usage:** {self._get_keyword_usage(standard)}\\n\\n"
        
        reference += "## Built-in Function Reference\\n\\n"
        builtins = self.language_data.get('builtins', {})
        for standard, custom in builtins.items():
            if custom:
                reference += f"### {custom}()\\n"
                reference += f"**Standard equivalent:** {standard}()\\n"
                reference += f"**Description:** {self._get_builtin_description(standard)}\\n\\n"
        
        return reference
    
    def _get_keyword_usage(self, standard):
        """Get usage description for a keyword"""
        usage_map = {
            'variable': 'Declares a new variable',
            'function': 'Defines a new function',
            'if': 'Conditional execution',
            'else': 'Alternative execution path',
            'loop': 'Repetitive execution',
            'return': 'Returns a value from function',
            'true': 'Boolean true value',
            'false': 'Boolean false value',
            'null': 'Null/empty value'
        }
        return usage_map.get(standard, 'No description available')
    
    def _get_builtin_description(self, standard):
        """Get description for a built-in function"""
        desc_map = {
            'print': 'Outputs text to console',
            'input': 'Gets input from user',
            'length': 'Returns length of string/array',
            'string': 'Converts value to string',
            'number': 'Converts value to number',
            'random': 'Generates random number'
        }
        return desc_map.get(standard, 'No description available')
    
    def generate_examples(self):
        """Generate example programs"""
        examples = f"""# {self.language_data.get('name', 'Unknown')} Examples

## Example 1: Calculator

```{self.language_data.get('name', 'lang').lower()}
{self.language_data.get('keywords', {}).get('function', 'function')} add(a, b) {{
    {self.language_data.get('keywords', {}).get('return', 'return')} a + b
}}

{self.language_data.get('keywords', {}).get('variable', 'var')} result = add(10, 5)
{self.language_data.get('builtins', {}).get('print', 'print')}("Result:", result)
```

## Example 2: Number Guessing Game

```{self.language_data.get('name', 'lang').lower()}
{self.language_data.get('keywords', {}).get('variable', 'var')} secret = 7
{self.language_data.get('keywords', {}).get('variable', 'var')} guess = 0

{self.language_data.get('keywords', {}).get('loop', 'while')} guess != secret {{
    guess = {self.language_data.get('builtins', {}).get('number', 'number')}({self.language_data.get('builtins', {}).get('input', 'input')}("Guess: "))
    
    {self.language_data.get('keywords', {}).get('if', 'if')} guess < secret {{
        {self.language_data.get('builtins', {}).get('print', 'print')}("Too low!")
    }} {self.language_data.get('keywords', {}).get('else', 'else')} {self.language_data.get('keywords', {}).get('if', 'if')} guess > secret {{
        {self.language_data.get('builtins', {}).get('print', 'print')}("Too high!")
    }}
}}

{self.language_data.get('builtins', {}).get('print', 'print')}("Correct!")
```

## Example 3: Simple Loop

```{self.language_data.get('name', 'lang').lower()}
{self.language_data.get('keywords', {}).get('variable', 'var')} i = 1

{self.language_data.get('keywords', {}).get('loop', 'while')} i <= 10 {{
    {self.language_data.get('builtins', {}).get('print', 'print')}("Number:", i)
    i = i + 1
}}
```
"""
        
        return examples

class StatisticsManager:
    """Manages language statistics and analytics"""
    
    def __init__(self, language_data):
        self.language_data = language_data
    
    def calculate_statistics(self):
        """Calculate comprehensive language statistics"""
        stats = {
            'basic': self._calculate_basic_stats(),
            'complexity': self._calculate_complexity(),
            'completeness': self._calculate_completeness(),
            'recommendations': self._generate_recommendations()
        }
        return stats
    
    def _calculate_basic_stats(self):
        """Calculate basic statistics"""
        keywords = self.language_data.get('keywords', {})
        builtins = self.language_data.get('builtins', {})
        errors = self.language_data.get('errors', {})
        
        defined_keywords = len([k for k in keywords.values() if k])
        defined_builtins = len([b for b in builtins.values() if b])
        defined_errors = len([e for e in errors.values() if e])
        
        return {
            'total_keywords': len(keywords),
            'defined_keywords': defined_keywords,
            'total_builtins': len(builtins),
            'defined_builtins': defined_builtins,
            'total_errors': len(errors),
            'defined_errors': defined_errors,
            'description_length': len(self.language_data.get('description', '')),
            'creation_date': self.language_data.get('created', 'Unknown'),
            'last_modified': self.language_data.get('modified', 'Unknown')
        }
    
    def _calculate_complexity(self):
        """Calculate language complexity metrics"""
        keywords = self.language_data.get('keywords', {})
        builtins = self.language_data.get('builtins', {})
        
        # Count unique words
        all_words = []
        all_words.extend([k for k in keywords.values() if k])
        all_words.extend([b for b in builtins.values() if b])
        
        unique_words = len(set(all_words))
        total_words = len(all_words)
        
        # Calculate average word length
        avg_word_length = sum(len(word) for word in all_words) / max(total_words, 1)
        
        # Complexity score (arbitrary metric)
        complexity_score = (unique_words * 2 + total_words + avg_word_length) / 10
        
        return {
            'unique_words': unique_words,
            'total_words': total_words,
            'average_word_length': round(avg_word_length, 1),
            'complexity_score': round(complexity_score, 1),
            'duplicate_words': total_words - unique_words
        }
    
    def _calculate_completeness(self):
        """Calculate language completeness percentage"""
        essential_keywords = ['variable', 'function', 'if', 'loop', 'return']
        essential_builtins = ['print', 'input']
        
        keywords = self.language_data.get('keywords', {})
        builtins = self.language_data.get('builtins', {})
        
        # Check essential keywords
        defined_essential_keywords = sum(1 for k in essential_keywords if keywords.get(k))
        keyword_completeness = (defined_essential_keywords / len(essential_keywords)) * 100
        
        # Check essential builtins
        defined_essential_builtins = sum(1 for b in essential_builtins if builtins.get(b))
        builtin_completeness = (defined_essential_builtins / len(essential_builtins)) * 100
        
        # Overall completeness
        overall = (keyword_completeness + builtin_completeness) / 2
        
        return {
            'keyword_completeness': round(keyword_completeness, 1),
            'builtin_completeness': round(builtin_completeness, 1),
            'overall_completeness': round(overall, 1),
            'missing_keywords': [k for k in essential_keywords if not keywords.get(k)],
            'missing_builtins': [b for b in essential_builtins if not builtins.get(b)]
        }
    
    def _generate_recommendations(self):
        """Generate improvement recommendations"""
        recommendations = []
        
        stats = self._calculate_basic_stats()
        completeness = self._calculate_completeness()
        
        # Basic recommendations
        if stats['defined_keywords'] < 5:
            recommendations.append("Consider defining more keywords to make your language more expressive")
        
        if stats['defined_builtins'] < 3:
            recommendations.append("Add more built-in functions for better functionality")
        
        if stats['description_length'] < 50:
            recommendations.append("Add a more detailed description of your language")
        
        # Completeness recommendations
        if completeness['overall_completeness'] < 80:
            missing_kw = completeness['missing_keywords']
            missing_bf = completeness['missing_builtins']
            
            if missing_kw:
                recommendations.append(f"Define these essential keywords: {', '.join(missing_kw)}")
            
            if missing_bf:
                recommendations.append(f"Define these essential functions: {', '.join(missing_bf)}")
        
        if not recommendations:
            recommendations.append("Great job! Your language definition looks complete.")
        
        return recommendations

class ExamplesGallery:
    """Manages the examples gallery and showcase"""
    
    def __init__(self):
        self.examples = self._load_example_languages()
    
    def _load_example_languages(self):
        """Load example languages for showcase"""
        return [
            {
                'name': 'KidsCode',
                'description': 'A programming language designed for children',
                'author': 'Education Team',
                'theme': 'Educational',
                'keywords': {
                    'variable': 'remember',
                    'function': 'teach',
                    'if': 'when',
                    'else': 'otherwise',
                    'print': 'say'
                },
                'sample_code': '''remember name = "Alice"
teach greet() {
    say("Hello", name)
}
greet()''',
                'features': ['Kid-friendly syntax', 'Simple keywords', 'Educational focus']
            },
            {
                'name': 'MathLang',
                'description': 'A language optimized for mathematical computations',
                'author': 'Math Department',
                'theme': 'Mathematical',
                'keywords': {
                    'variable': 'define',
                    'function': 'formula',
                    'if': 'check',
                    'print': 'display'
                },
                'sample_code': '''define x = 5
define y = 3
formula add(a, b) {
    return a + b
}
display(add(x, y))''',
                'features': ['Math-focused', 'Formula definitions', 'Calculation-friendly']
            },
            {
                'name': 'StoryScript',
                'description': 'A narrative-focused programming language',
                'author': 'Creative Writing',
                'theme': 'Creative',
                'keywords': {
                    'variable': 'character',
                    'function': 'scene',
                    'if': 'suddenly',
                    'print': 'narrate'
                },
                'sample_code': '''character hero = "Alice"
scene introduction() {
    narrate("Once upon a time, there was", hero)
}
introduction()''',
                'features': ['Narrative syntax', 'Story-telling focus', 'Creative expression']
            },
            {
                'name': 'GameScript',
                'description': 'A language designed for game development',
                'author': 'Game Developers',
                'theme': 'Gaming',
                'keywords': {
                    'variable': 'item',
                    'function': 'action',
                    'if': 'event',
                    'print': 'message'
                },
                'sample_code': '''item score = 0
action jump() {
    score = score + 10
    message("Score:", score)
}
jump()''',
                'features': ['Game-oriented', 'Action-based syntax', 'Interactive focus']
            }
        ]
    
    def get_examples_by_theme(self):
        """Get examples grouped by theme"""
        themes = {}
        for example in self.examples:
            theme = example['theme']
            if theme not in themes:
                themes[theme] = []
            themes[theme].append(example)
        return themes
    
    def get_all_examples(self):
        """Get all example languages"""
        return self.examples.copy()
    
    def get_example_by_name(self, name):
        """Get specific example by name"""
        for example in self.examples:
            if example['name'] == name:
                return example.copy()
        return None
    
    def show_gallery(self, parent_window, theme_colors):
        """Show the examples gallery window"""
        import tkinter as tk
        from tkinter import ttk
        
        # Create gallery window
        gallery_window = tk.Toplevel(parent_window)
        gallery_window.title("🎨 Examples Gallery")
        gallery_window.geometry("800x600")
        gallery_window.configure(bg=theme_colors['bg'])
        
        # Center the window
        gallery_window.transient(parent_window)
        gallery_window.grab_set()
        
        # Create main frame
        main_frame = tk.Frame(gallery_window, bg=theme_colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="🎨 Programming Language Examples",
            font=('Arial', 16, 'bold'),
            bg=theme_colors['bg'],
            fg=theme_colors['fg']
        )
        title_label.pack(pady=(0, 20))
        
        # Description
        desc_label = tk.Label(
            main_frame,
            text="Get inspired by these example languages and load them as templates for your own creations!",
            font=('Arial', 10),
            bg=theme_colors['bg'],
            fg=theme_colors['fg'],
            wraplength=600
        )
        desc_label.pack(pady=(0, 20))
        
        # Create scrollable frame
        canvas = tk.Canvas(main_frame, bg=theme_colors['bg'])
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=theme_colors['bg'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add examples
        for i, example in enumerate(self.examples):
            self._create_example_card(scrollable_frame, example, theme_colors, gallery_window, parent_window)
        
        # Pack scrollable components
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Close button
        close_btn = tk.Button(
            main_frame,
            text="Close",
            command=gallery_window.destroy,
            bg=theme_colors['accent'],
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=20,
            pady=5
        )
        close_btn.pack(pady=(20, 0))
        
        # Focus the window
        gallery_window.focus_set()
    
    def _create_example_card(self, parent, example, theme_colors, gallery_window, main_window):
        """Create a card for each example language"""
        import tkinter as tk
        from tkinter import messagebox
        
        # Create card frame
        card_frame = tk.Frame(
            parent,
            bg=theme_colors['card'],
            relief='raised',
            bd=1
        )
        card_frame.pack(fill='x', pady=10, padx=10)
        
        # Header frame
        header_frame = tk.Frame(card_frame, bg=theme_colors['card'])
        header_frame.pack(fill='x', padx=15, pady=(15, 5))
        
        # Title and author
        title_label = tk.Label(
            header_frame,
            text=f"🚀 {example['name']}",
            font=('Arial', 14, 'bold'),
            bg=theme_colors['card'],
            fg=theme_colors['fg']
        )
        title_label.pack(anchor='w')
        
        author_label = tk.Label(
            header_frame,
            text=f"by {example['author']} • {example['theme']}",
            font=('Arial', 9),
            bg=theme_colors['card'],
            fg=theme_colors['secondary']
        )
        author_label.pack(anchor='w')
        
        # Description
        desc_label = tk.Label(
            card_frame,
            text=example['description'],
            font=('Arial', 10),
            bg=theme_colors['card'],
            fg=theme_colors['fg'],
            wraplength=700,
            justify='left'
        )
        desc_label.pack(anchor='w', padx=15, pady=(0, 10))
        
        # Sample code frame
        code_frame = tk.Frame(card_frame, bg=theme_colors['card'])
        code_frame.pack(fill='x', padx=15, pady=(0, 10))
        
        code_label = tk.Label(
            code_frame,
            text="Sample Code:",
            font=('Arial', 9, 'bold'),
            bg=theme_colors['card'],
            fg=theme_colors['fg']
        )
        code_label.pack(anchor='w')
        
        # Code display
        code_text = tk.Text(
            code_frame,
            height=6,
            width=80,
            font=('Courier', 9),
            bg=theme_colors['bg'],
            fg=theme_colors['fg'],
            wrap='word',
            state='disabled'
        )
        code_text.pack(pady=(5, 0))
        
        # Insert and format code
        code_text.config(state='normal')
        code_text.insert('1.0', example['sample_code'])
        code_text.config(state='disabled')
        
        # Features
        features_frame = tk.Frame(card_frame, bg=theme_colors['card'])
        features_frame.pack(fill='x', padx=15, pady=(0, 10))
        
        features_label = tk.Label(
            features_frame,
            text="Features: " + " • ".join(example['features']),
            font=('Arial', 9),
            bg=theme_colors['card'],
            fg=theme_colors['secondary']
        )
        features_label.pack(anchor='w')
        
        # Buttons frame
        buttons_frame = tk.Frame(card_frame, bg=theme_colors['card'])
        buttons_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        # View Details button
        view_btn = tk.Button(
            buttons_frame,
            text="View Details",
            command=lambda: self._show_example_details(example, theme_colors, gallery_window),
            bg=theme_colors['accent'],
            fg='white',
            font=('Arial', 9, 'bold'),
            padx=15,
            pady=5
        )
        view_btn.pack(side='left', padx=(0, 10))
        
        # Load as Template button
        load_btn = tk.Button(
            buttons_frame,
            text="Load as Template",
            command=lambda: self._load_example_as_template(example, gallery_window, main_window),
            bg=theme_colors['success'],
            fg='white',
            font=('Arial', 9, 'bold'),
            padx=15,
            pady=5
        )
        load_btn.pack(side='left')
    
    def _show_example_details(self, example, theme_colors, parent_window):
        """Show detailed information about an example"""
        import tkinter as tk
        from tkinter import messagebox
        
        details = f"""
🚀 {example['name']}
by {example['author']}

📖 Description:
{example['description']}

🎯 Theme: {example['theme']}

🔤 Keywords:
"""
        for key, value in example['keywords'].items():
            details += f"  • {key} → {value}\n"
        
        details += f"""
💡 Features:
"""
        for feature in example['features']:
            details += f"  • {feature}\n"
        
        details += f"""
💻 Sample Code:
{example['sample_code']}
"""
        
        # Show in a scrollable message box
        detail_window = tk.Toplevel(parent_window)
        detail_window.title(f"Details: {example['name']}")
        detail_window.geometry("600x500")
        detail_window.configure(bg=theme_colors['bg'])
        
        # Create text widget with scrollbar
        text_frame = tk.Frame(detail_window, bg=theme_colors['bg'])
        text_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        text_widget = tk.Text(
            text_frame,
            wrap='word',
            font=('Arial', 10),
            bg=theme_colors['card'],
            fg=theme_colors['fg']
        )
        text_widget.pack(side='left', fill='both', expand=True)
        
        scrollbar = tk.Scrollbar(text_frame, command=text_widget.yview)
        scrollbar.pack(side='right', fill='y')
        text_widget.config(yscrollcommand=scrollbar.set)
        
        # Insert details
        text_widget.insert('1.0', details)
        text_widget.config(state='disabled')
        
        # Close button
        close_btn = tk.Button(
            detail_window,
            text="Close",
            command=detail_window.destroy,
            bg=theme_colors['accent'],
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=20,
            pady=5
        )
        close_btn.pack(pady=(0, 20))
    
    def _load_example_as_template(self, example, gallery_window, main_window):
        """Load an example as a template for new language"""
        from tkinter import messagebox
        
        # Confirm loading
        result = messagebox.askyesno(
            "Load Template",
            f"Load '{example['name']}' as a template for your new language?\n\nThis will replace your current language data.",
            parent=gallery_window
        )
        
        if result:
            # Close gallery window
            gallery_window.destroy()
            
            # Get the main application instance and update language data
            # We need to access the main app through the window's reference
            main_app = None
            for widget in main_window.winfo_children():
                if hasattr(widget, 'master') and hasattr(widget.master, 'language_data'):
                    main_app = widget.master
                    break
            
            # If we can't find the app reference, try a different approach
            if main_app is None:
                # Try to find the app through the window reference
                if hasattr(main_window, 'app_reference'):
                    main_app = main_window.app_reference
                else:
                    # Fallback: store the template data in the window for retrieval
                    main_window.template_data = example
                    messagebox.showinfo(
                        "Template Loaded",
                        f"'{example['name']}' template loaded! Please restart the application to apply changes.",
                        parent=main_window
                    )
                    return
            
            # Update the language data with template data
            if main_app:
                self._apply_template_to_language_data(main_app, example)
                
                # Show success message
                messagebox.showinfo(
                    "Template Loaded",
                    f"'{example['name']}' has been loaded as a template!\n\nYou can now modify it to create your own language.",
                    parent=main_window
                )
                
                # Switch to info tab to show the loaded data
                if hasattr(main_app, 'notebook'):
                    main_app.notebook.select(1)  # Info tab is index 1
    
    def _apply_template_to_language_data(self, main_app, example):
        """Apply template data to the main application's language data"""
        from datetime import datetime
        
        # Update the language data with template information
        main_app.language_data.update({
            'name': example['name'],
            'version': '1.0',
            'author': example['author'],
            'description': example['description'],
            'keywords': example['keywords'].copy(),
            'operators': {
                'addition': '+',
                'subtraction': '-',
                'multiplication': '*',
                'division': '/',
                'equal': '==',
                'not_equal': '!=',
                'less_than': '<',
                'greater_than': '>',
                'assign': '='
            },
            'builtins': {
                'print': example['keywords'].get('print', 'print'),
                'input': 'input',
                'len': 'len',
                'str': 'str',
                'int': 'int',
                'float': 'float'
            },
            'errors': {
                'syntax_error': 'Syntax Error: Invalid syntax',
                'name_error': 'Name Error: Variable not defined',
                'type_error': 'Type Error: Invalid type operation'
            },
            'features': example.get('features', []),
            'theme': example.get('theme', 'General'),
            'sample_code': example.get('sample_code', ''),
            'created': datetime.now().isoformat(),
            'modified': datetime.now().isoformat()
        })
        
        # Update the UI to reflect the new data
        main_app.update_ui_from_data()
        
        # Update the window title
        main_app.window.title(f"🚀 SUPER Language Creator v2.0 - {example['name']}")
        
        # Update status
        main_app.update_status(f"Template '{example['name']}' loaded successfully")

class TutorialSystem:
    """Manages the interactive tutorial system"""
    
    def __init__(self, callbacks):
        self.callbacks = callbacks
        self.tutorial_steps = self._create_tutorial_steps()
        self.current_step = 0
        self.tutorial_active = False
    
    def _create_tutorial_steps(self):
        """Create tutorial steps"""
        return [
            {
                'title': 'Welcome to SUPER Language Creator!',
                'content': '''Welcome! This tutorial will guide you through creating your first programming language.

You'll learn how to:
• Define language keywords
• Set up built-in functions  
• Configure error messages
• Test your language in the playground

Ready to start? Click Next to continue!''',
                'action': None,
                'highlight': None
            },
            {
                'title': 'Step 1: Language Information',
                'content': '''Let's start by giving your language a name and description.

1. Click on the "Language Info" tab
2. Enter a creative name for your language
3. Add a description explaining what makes it special
4. Set the version and author information

Good language names are memorable and reflect the purpose!''',
                'action': 'focus_info_tab',
                'highlight': 'info_tab'
            },
            {
                'title': 'Step 2: Define Keywords',
                'content': '''Keywords are the building blocks of your language!

1. Click on the "Keywords" tab
2. Replace the default keywords with your own creative words
3. Try the random generator for inspiration
4. Make sure keywords are easy to remember

For example, instead of "function", you could use "magic", "recipe", or "action"!''',
                'action': 'focus_keywords_tab',
                'highlight': 'keywords_tab'
            },
            {
                'title': 'Step 3: Built-in Functions',
                'content': '''Built-in functions provide core functionality.

1. Click on the "Built-ins" tab
2. Customize the names of essential functions like print and input
3. These should match your language theme

For a cooking-themed language, "print" could become "serve" or "present"!''',
                'action': 'focus_builtins_tab',
                'highlight': 'builtins_tab'
            },
            {
                'title': 'Step 4: Test Your Language',
                'content': '''Time to see your language in action!

1. Click on the "Playground" tab
2. Try the example templates or write your own code
3. Click "Run Code" to test your language
4. Experiment with different programs

The playground shows how your custom keywords work in real code!''',
                'action': 'focus_playground_tab',
                'highlight': 'playground_tab'
            },
            {
                'title': 'Step 5: Save and Export',
                'content': '''Don't lose your amazing creation!

1. Use Ctrl+S to save your language
2. Use File → Export to create a complete language package
3. Share your language with friends and family

You can always come back and make improvements later!''',
                'action': None,
                'highlight': 'file_menu'
            },
            {
                'title': 'Congratulations! 🎉',
                'content': '''You've successfully created your first programming language!

Here are some ideas for your next steps:
• Try different themes and color schemes
• Experiment with the achievement system
• Browse the examples gallery for inspiration
• Create multiple languages for different purposes

Keep creating and have fun with your new programming languages!''',
                'action': 'complete_tutorial',
                'highlight': None
            }
        ]
    
    def start_tutorial(self):
        """Start the interactive tutorial"""
        self.tutorial_active = True
        self.current_step = 0
        self.show_current_step()
    
    def show_current_step(self):
        """Show the current tutorial step"""
        if not self.tutorial_active or self.current_step >= len(self.tutorial_steps):
            return
        
        step = self.tutorial_steps[self.current_step]
        
        # Create tutorial dialog
        dialog = tk.Toplevel()
        dialog.title(f"Tutorial - Step {self.current_step + 1}")
        dialog.geometry("500x400")
        dialog.transient()
        dialog.grab_set()
        
        # Header
        header = tk.Frame(dialog, bg='#667eea', height=60)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text=step['title'],
            font=('Arial', 16, 'bold'),
            bg='#667eea',
            fg='white'
        ).pack(pady=15)
        
        # Content
        content_frame = tk.Frame(dialog, bg='white', padx=30, pady=20)
        content_frame.pack(fill='both', expand=True)
        
        content_text = scrolledtext.ScrolledText(
            content_frame,
            wrap=tk.WORD,
            font=('Arial', 11),
            height=12,
            bg='white',
            relief='flat'
        )
        content_text.pack(fill='both', expand=True)
        content_text.insert('1.0', step['content'])
        content_text.config(state='disabled')
        
        # Buttons
        button_frame = tk.Frame(content_frame, bg='white')
        button_frame.pack(fill='x', pady=(20, 0))
        
        if self.current_step > 0:
            tk.Button(
                button_frame,
                text="← Previous",
                command=lambda: self.previous_step(dialog),
                bg='#e9ecef',
                fg='#495057',
                padx=20,
                pady=8
            ).pack(side='left')
        
        tk.Button(
            button_frame,
            text="Skip Tutorial",
            command=lambda: self.end_tutorial(dialog),
            bg='#6c757d',
            fg='white',
            padx=20,
            pady=8
        ).pack(side='left', padx=(10, 0))
        
        if self.current_step < len(self.tutorial_steps) - 1:
            tk.Button(
                button_frame,
                text="Next →",
                command=lambda: self.next_step(dialog),
                bg='#667eea',
                fg='white',
                padx=20,
                pady=8
            ).pack(side='right')
        else:
            tk.Button(
                button_frame,
                text="Finish Tutorial",
                command=lambda: self.end_tutorial(dialog),
                bg='#51cf66',
                fg='white',
                padx=20,
                pady=8
            ).pack(side='right')
        
        # Execute step action
        if step['action'] and step['action'] in self.callbacks:
            dialog.after(500, self.callbacks[step['action']])
        
        dialog.focus()
    
    def next_step(self, current_dialog):
        """Move to next tutorial step"""
        current_dialog.destroy()
        self.current_step += 1
        self.show_current_step()
    
    def previous_step(self, current_dialog):
        """Move to previous tutorial step"""
        current_dialog.destroy()
        self.current_step -= 1
        self.show_current_step()
    
    def end_tutorial(self, current_dialog):
        """End the tutorial"""
        current_dialog.destroy()
        self.tutorial_active = False
        
        # Mark tutorial as completed
        if 'complete_tutorial' in self.callbacks:
            self.callbacks['complete_tutorial']()
        
        # Show completion message
        messagebox.showinfo(
            "Tutorial Complete",
            "Great job completing the tutorial! You're now ready to create amazing programming languages."
        )

class HelpSystem:
    """Manages help dialogs and documentation"""
    
    def __init__(self, root):
        self.root = root
    
    def show_keyboard_shortcuts(self):
        """Show keyboard shortcuts dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Keyboard Shortcuts")
        dialog.geometry("400x500")
        dialog.transient(self.root)
        
        # Header
        header = tk.Frame(dialog, bg='#667eea', height=50)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="⌨️ Keyboard Shortcuts",
            font=('Arial', 14, 'bold'),
            bg='#667eea',
            fg='white'
        ).pack(pady=12)
        
        # Content
        content = tk.Frame(dialog, bg='white', padx=20, pady=20)
        content.pack(fill='both', expand=True)
        
        shortcuts = [
            ("Ctrl+N", "New Language"),
            ("Ctrl+O", "Open Language"),
            ("Ctrl+S", "Save Language"),
            ("Ctrl+Shift+S", "Save As"),
            ("Ctrl+E", "Export Language"),
            ("Ctrl+G", "Generate Keywords"),
            ("F5", "Validate Syntax"),
            ("Ctrl+,", "Preferences"),
            ("F1", "Show This Help"),
            ("Ctrl+Q", "Exit Application"),
            ("", ""),
            ("Playground:", ""),
            ("Ctrl+R", "Run Code"),
            ("Ctrl+L", "Clear Output"),
            ("", ""),
            ("Navigation:", ""),
            ("Ctrl+1-9", "Switch Tabs"),
            ("Tab", "Next Field"),
            ("Shift+Tab", "Previous Field"),
        ]
        
        for shortcut, description in shortcuts:
            if not shortcut and not description:
                # Separator
                tk.Frame(content, height=1, bg='#e9ecef').pack(fill='x', pady=10)
            elif description and not shortcut:
                # Section header
                tk.Label(
                    content,
                    text=description,
                    font=('Arial', 11, 'bold'),
                    bg='white',
                    fg='#495057'
                ).pack(anchor='w', pady=(10, 5))
            else:
                # Shortcut row
                row = tk.Frame(content, bg='white')
                row.pack(fill='x', pady=2)
                
                tk.Label(
                    row,
                    text=shortcut,
                    font=('Consolas', 10),
                    bg='#f8f9fa',
                    fg='#495057',
                    width=15,
                    anchor='w',
                    padx=8,
                    pady=2
                ).pack(side='left')
                
                tk.Label(
                    row,
                    text=description,
                    font=('Arial', 10),
                    bg='white',
                    fg='#495057',
                    anchor='w'
                ).pack(side='left', padx=(10, 0))
        
        # Close button
        tk.Button(
            content,
            text="Close",
            command=dialog.destroy,
            bg='#667eea',
            fg='white',
            padx=20,
            pady=8
        ).pack(pady=(20, 0))
    
    def show_about_dialog(self):
        """Show about dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("About SUPER Language Creator")
        dialog.geometry("450x350")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Header with gradient effect
        header = tk.Frame(dialog, bg='#667eea', height=120)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="🚀 SUPER Language Creator",
            font=('Arial', 20, 'bold'),
            bg='#667eea',
            fg='white'
        ).pack(pady=(25, 5))
        
        tk.Label(
            header,
            text="Create Programming Languages with Ease",
            font=('Arial', 12),
            bg='#667eea',
            fg='white'
        ).pack()
        
        # Content
        content = tk.Frame(dialog, bg='white', padx=30, pady=20)
        content.pack(fill='both', expand=True)
        
        info_text = '''Version 2.0 - Enhanced Edition

SUPER Language Creator empowers you to design and build your own programming languages with an intuitive interface and powerful features.

Features:
• Visual language designer
• Interactive code playground
• Complete interpreter generation
• Export to standalone packages
• Achievement system
• Multiple themes
• Examples gallery

Perfect for educators, students, and programming enthusiasts who want to explore language design!'''
        
        tk.Label(
            content,
            text=info_text,
            font=('Arial', 10),
            bg='white',
            fg='#495057',
            justify='left',
            wraplength=380
        ).pack(pady=(0, 20))
        
        # Buttons
        button_frame = tk.Frame(content, bg='white')
        button_frame.pack(fill='x')
        
        tk.Button(
            button_frame,
            text="🌐 Visit Website",
            command=lambda: webbrowser.open("https://github.com/yourusername/super-language-creator"),
            bg='#667eea',
            fg='white',
            padx=15,
            pady=8
        ).pack(side='left')
        
        tk.Button(
            button_frame,
            text="Close",
            command=dialog.destroy,
            bg='#6c757d',
            fg='white',
            padx=20,
            pady=8
        ).pack(side='right')
    
    def show_tips_dialog(self):
        """Show tips and tricks dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Tips & Tricks")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        
        # Implementation would go here
        # Placeholder for brevity
        
        tk.Label(dialog, text="Tips & Tricks coming soon!", font=('Arial', 16)).pack(pady=50)
        tk.Button(dialog, text="Close", command=dialog.destroy).pack()

class PerformanceTester:
    """Tests language performance and provides metrics"""
    
    def __init__(self, language_data):
        self.language_data = language_data
    
    def run_performance_test(self):
        """Run comprehensive performance tests"""
        results = {
            'parse_time': self._test_parse_time(),
            'execution_time': self._test_execution_time(),
            'memory_usage': self._test_memory_usage(),
            'complexity_score': self._calculate_complexity_score()
        }
        return results
    
    def _test_parse_time(self):
        """Test parsing performance"""
        # Simulate parsing time based on language complexity
        keywords = len([k for k in self.language_data.get('keywords', {}).values() if k])
        builtins = len([b for b in self.language_data.get('builtins', {}).values() if b])
        
        # Simple simulation
        base_time = 0.001  # 1ms base
        complexity_factor = (keywords + builtins) * 0.0001
        
        return round(base_time + complexity_factor, 4)
    
    def _test_execution_time(self):
        """Test execution performance"""
        # Simulate execution time
        return round(random.uniform(0.005, 0.050), 4)
    
    def _test_memory_usage(self):
        """Test memory usage"""
        # Simulate memory usage in KB
        base_memory = 128  # 128KB base
        language_size = len(str(self.language_data))
        
        return round(base_memory + (language_size * 0.001), 2)
    
    def _calculate_complexity_score(self):
        """Calculate overall complexity score"""
        keywords = self.language_data.get('keywords', {})
        builtins = self.language_data.get('builtins', {})
        
        defined_elements = len([k for k in keywords.values() if k]) + len([b for b in builtins.values() if b])
        
        # Score from 1-100
        score = min(100, max(1, defined_elements * 5))
        return score