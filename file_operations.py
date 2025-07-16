"""
File Operations Module for LangGen
Contains: Save/Load, Import/Export, Recent projects, Template management, and Autosave functionality
"""

import json
import os
import sys
import shutil
import zipfile
import tempfile
from datetime import datetime
from typing import Dict, List, Any, Optional
import tkinter as tk
from tkinter import messagebox, filedialog

class FileOperations:
    """Handles all file operations for language projects"""
    
    def __init__(self, language_data, ui_callbacks=None):
        self.language_data = language_data
        self.ui_callbacks = ui_callbacks or {}
        self.current_file = None
        self.recent_files = []
        self.autosave_enabled = True
        self.load_recent_files()
    
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
        self.language_data.clear()
        self.language_data.update({
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
        })
        
        self.current_file = None
        
        # Update UI if callback provided
        if 'update_ui' in self.ui_callbacks:
            self.ui_callbacks['update_ui']()
        
        # Update status
        if 'update_status' in self.ui_callbacks:
            self.ui_callbacks['update_status']("New language created")
    
    def save_language(self, filename=None):
        """Save the current language to file"""
        try:
            if filename is None:
                if self.current_file:
                    filename = self.current_file
                else:
                    return self.save_as_language()
            
            # Collect current data
            if 'collect_data' in self.ui_callbacks:
                self.ui_callbacks['collect_data']()
            
            # Ensure required fields
            self.language_data['modified'] = datetime.now().isoformat()
            if 'created' not in self.language_data:
                self.language_data['created'] = datetime.now().isoformat()
            
            # Save to file
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.language_data, f, indent=2, ensure_ascii=False)
            
            self.current_file = filename
            self.add_to_recent_files(filename)
            
            # Update UI
            if 'update_status' in self.ui_callbacks:
                self.ui_callbacks['update_status'](f"Saved to {os.path.basename(filename)}")
            
            # Check achievements
            if 'check_achievements' in self.ui_callbacks:
                self.ui_callbacks['check_achievements']()
            
            return True
            
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save language:\\n{str(e)}")
            return False
    
    def save_as_language(self):
        """Save language with a new filename"""
        filename = filedialog.asksaveasfilename(
            title="Save Language As",
            defaultextension=".slang",
            filetypes=[
                ("SUPER Language files", "*.slang"),
                ("JSON files", "*.json"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            return self.save_language(filename)
        return False
    
    def load_language(self, filename=None):
        """Load a language from file"""
        try:
            if filename is None:
                filename = filedialog.askopenfilename(
                    title="Open Language",
                    filetypes=[
                        ("SUPER Language files", "*.slang"),
                        ("JSON files", "*.json"),
                        ("All files", "*.*")
                    ]
                )
            
            if not filename:
                return False
            
            # Check for unsaved changes
            if self.has_unsaved_changes():
                result = messagebox.askyesnocancel(
                    "Unsaved Changes",
                    "You have unsaved changes. Do you want to save before opening a new file?"
                )
                if result is True:
                    if not self.save_language():
                        return False
                elif result is None:
                    return False
            
            # Load the file
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Validate data
            if not self.validate_language_data(data):
                messagebox.showerror("Invalid File", "This file doesn't contain valid language data.")
                return False
            
            # Update language data
            self.language_data.clear()
            self.language_data.update(data)
            self.current_file = filename
            self.add_to_recent_files(filename)
            
            # Update UI
            if 'update_ui' in self.ui_callbacks:
                self.ui_callbacks['update_ui']()
            
            if 'update_status' in self.ui_callbacks:
                self.ui_callbacks['update_status'](f"Loaded {os.path.basename(filename)}")
            
            return True
            
        except Exception as e:
            messagebox.showerror("Load Error", f"Failed to load language:\\n{str(e)}")
            return False
    
    def import_language(self):
        """Import language from various formats"""
        filename = filedialog.askopenfilename(
            title="Import Language",
            filetypes=[
                ("All supported", "*.slang;*.json;*.zip"),
                ("SUPER Language files", "*.slang"),
                ("JSON files", "*.json"),
                ("ZIP archives", "*.zip"),
                ("All files", "*.*")
            ]
        )
        
        if not filename:
            return False
        
        try:
            if filename.lower().endswith('.zip'):
                return self.import_from_zip(filename)
            else:
                return self.load_language(filename)
        except Exception as e:
            messagebox.showerror("Import Error", f"Failed to import language:\\n{str(e)}")
            return False
    
    def import_from_zip(self, zip_filename):
        """Import language from a ZIP archive"""
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
                
                # Look for language files
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        if file.endswith(('.slang', '.json')):
                            lang_file = os.path.join(root, file)
                            try:
                                with open(lang_file, 'r', encoding='utf-8') as f:
                                    data = json.load(f)
                                
                                if self.validate_language_data(data):
                                    self.language_data.clear()
                                    self.language_data.update(data)
                                    self.current_file = None  # Imported, not saved yet
                                    
                                    if 'update_ui' in self.ui_callbacks:
                                        self.ui_callbacks['update_ui']()
                                    
                                    messagebox.showinfo("Import Success", 
                                                      f"Language '{data.get('name', 'Unknown')}' imported successfully!")
                                    return True
                            except:
                                continue
                
                messagebox.showerror("Import Error", "No valid language files found in the archive.")
                return False
                
        except Exception as e:
            messagebox.showerror("Import Error", f"Failed to import from ZIP:\\n{str(e)}")
            return False
    
    def export_language(self):
        """Export language to a complete package"""
        if not self.language_data.get('name'):
            messagebox.showerror("Export Error", "Please save your language first.")
            return False
        
        export_folder = filedialog.askdirectory(title="Choose Export Folder")
        if not export_folder:
            return False
        
        try:
            lang_name = self.language_data['name'].lower().replace(' ', '_')
            project_folder = os.path.join(export_folder, f"{lang_name}_language")
            
            # Create project structure
            os.makedirs(project_folder, exist_ok=True)
            os.makedirs(os.path.join(project_folder, 'src'), exist_ok=True)
            os.makedirs(os.path.join(project_folder, 'examples'), exist_ok=True)
            os.makedirs(os.path.join(project_folder, 'docs'), exist_ok=True)
            
            # Save language definition
            lang_file = os.path.join(project_folder, 'language.json')
            with open(lang_file, 'w', encoding='utf-8') as f:
                json.dump(self.language_data, f, indent=2, ensure_ascii=False)
            
            # Generate interpreter
            if 'generate_interpreter' in self.ui_callbacks:
                self.ui_callbacks['generate_interpreter'](project_folder)
            
            # Create example files
            self.create_example_files(project_folder)
            
            # Create documentation
            self.create_documentation(project_folder)
            
            # Create README
            self.create_readme(project_folder)
            
            # Create test runner
            if 'create_test_files' in self.ui_callbacks:
                self.ui_callbacks['create_test_files'](project_folder)
            
            messagebox.showinfo("Export Success", 
                              f"Language exported to:\\n{project_folder}")
            
            # Check achievements
            if 'unlock_achievement' in self.ui_callbacks:
                self.ui_callbacks['unlock_achievement']('share_joy')
            
            return True
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export language:\\n{str(e)}")
            return False
    
    def export_language_with_options(self, export_folder, options):
        """Export language with specific options"""
        if not self.language_data.get('name'):
            messagebox.showerror("Export Error", "Please save your language first.")
            return False
        
        try:
            lang_name = self.language_data['name'].lower().replace(' ', '_')
            project_folder = os.path.join(export_folder, f"{lang_name}_language")
            
            # Create project structure
            os.makedirs(project_folder, exist_ok=True)
            
            if options['include_interpreter']:
                os.makedirs(os.path.join(project_folder, 'src'), exist_ok=True)
            
            if options['include_examples']:
                os.makedirs(os.path.join(project_folder, 'examples'), exist_ok=True)
            
            if options['include_docs']:
                os.makedirs(os.path.join(project_folder, 'docs'), exist_ok=True)
            
            if options['include_tests']:
                os.makedirs(os.path.join(project_folder, 'tests'), exist_ok=True)
            
            # Save language definition
            lang_file = os.path.join(project_folder, 'language.json')
            with open(lang_file, 'w', encoding='utf-8') as f:
                json.dump(self.language_data, f, indent=2, ensure_ascii=False)
            
            # Generate interpreter if requested
            if options['include_interpreter'] and 'generate_interpreter' in self.ui_callbacks:
                self.ui_callbacks['generate_interpreter'](project_folder)
                
                # Create launcher script
                self.create_launcher_script(project_folder, options['extension'])
            
            # Create example files if requested
            if options['include_examples']:
                self.create_example_files_with_extension(project_folder, options['extension'])
            
            # Create documentation if requested
            if options['include_docs']:
                self.create_enhanced_documentation(project_folder, options['extension'])
            
            # Create README
            self.create_enhanced_readme(project_folder, options['extension'])
            
            # Create test files if requested
            if options['include_tests'] and 'create_test_files' in self.ui_callbacks:
                self.ui_callbacks['create_test_files'](project_folder)
            
            # Create installation script
            self.create_installation_script(project_folder, options['extension'])
            
            messagebox.showinfo("Export Success", 
                              f"Language exported to:\\n{project_folder}\\n\\nTo run your language:\\n1. Open terminal in the export folder\\n2. Run: python install.py\\n3. Use: python run_{lang_name}.py file.{options['extension']}")
            
            return True
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Error exporting language: {str(e)}")
            return False
    
    def create_example_files(self, project_folder):
        """Create example files for the language"""
        examples_dir = os.path.join(project_folder, 'examples')
        lang_name = self.language_data['name'].lower().replace(' ', '_')
        file_ext = lang_name[:3]
        
        # Hello World example
        hello_world = f'''# Hello World in {self.language_data['name']}
{self.language_data.get('builtins', {}).get('print', 'print')}("Hello, World!")
{self.language_data.get('builtins', {}).get('print', 'print')}("Welcome to {self.language_data['name']}!")
'''
        
        with open(os.path.join(examples_dir, f'hello.{file_ext}'), 'w', encoding='utf-8') as f:
            f.write(hello_world)
        
        # Variables example
        if self.language_data.get('keywords', {}).get('variable'):
            var_example = f'''# Variables in {self.language_data['name']}
{self.language_data['keywords']['variable']} name = "World"
{self.language_data['keywords']['variable']} age = 25
{self.language_data.get('builtins', {}).get('print', 'print')}("Hello", name)
{self.language_data.get('builtins', {}).get('print', 'print')}("You are", age, "years old")
'''
            
            with open(os.path.join(examples_dir, f'variables.{file_ext}'), 'w', encoding='utf-8') as f:
                f.write(var_example)
    
    def create_documentation(self, project_folder):
        """Create language documentation"""
        docs_dir = os.path.join(project_folder, 'docs')
        
        # Language specification
        spec = f"""# {self.language_data['name']} Language Specification

## Overview
{self.language_data.get('description', 'A custom programming language')}

**Version:** {self.language_data.get('version', '1.0')}
**Author:** {self.language_data.get('author', 'Unknown')}

## Keywords
"""
        
        keywords = self.language_data.get('keywords', {})
        for standard, custom in keywords.items():
            if custom:
                spec += f"- `{custom}` - {standard}\\n"
        
        spec += "\\n## Built-in Functions\\n"
        builtins = self.language_data.get('builtins', {})
        for standard, custom in builtins.items():
            if custom:
                spec += f"- `{custom}()` - {standard}\\n"
        
        with open(os.path.join(docs_dir, 'specification.md'), 'w', encoding='utf-8') as f:
            f.write(spec)
    
    def create_readme(self, project_folder):
        """Create README file for the exported project"""
        lang_name = self.language_data['name']
        readme = f"""# {lang_name} Programming Language

{self.language_data.get('description', 'A custom programming language created with SUPER Language Creator')}

## Quick Start

1. **Run examples:**
   ```bash
   python src/{lang_name.lower().replace(' ', '_')}.py examples/hello.{lang_name.lower().replace(' ', '_')[:3]}
   ```

2. **Run tests:**
   ```bash
   python run_tests.py
   ```

## Language Features

### Keywords
"""
        
        keywords = self.language_data.get('keywords', {})
        for standard, custom in keywords.items():
            if custom:
                readme += f"- `{custom}` (instead of `{standard}`)\\n"
        
        readme += "\\n### Built-in Functions\\n"
        builtins = self.language_data.get('builtins', {})
        for standard, custom in builtins.items():
            if custom:
                readme += f"- `{custom}()` (instead of `{standard}()`)\\n"
        
        readme += f"""

## Project Structure

- `src/` - Interpreter source code
- `examples/` - Example programs
- `docs/` - Documentation
- `language.json` - Language definition
- `run_tests.py` - Test runner

## About

Created with [SUPER Language Creator](https://github.com/yourusername/super-language-creator)

**Version:** {self.language_data.get('version', '1.0')}
**Author:** {self.language_data.get('author', 'Unknown')}
**Created:** {self.language_data.get('created', 'Unknown')}
"""
        
        with open(os.path.join(project_folder, 'README.md'), 'w', encoding='utf-8') as f:
            f.write(readme)
    
    def validate_language_data(self, data):
        """Validate loaded language data"""
        required_fields = ['name', 'version', 'author']
        return all(field in data for field in required_fields)
    
    def has_unsaved_changes(self):
        """Check if there are unsaved changes"""
        if not hasattr(self, 'language_data'):
            return False
        
        current_data = self.language_data.copy()
        
        # Compare with last saved state or default
        if self.current_file:
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
    
    def add_to_recent_files(self, filename):
        """Add file to recent files list"""
        if filename in self.recent_files:
            self.recent_files.remove(filename)
        
        self.recent_files.insert(0, filename)
        self.recent_files = self.recent_files[:10]  # Keep only 10 recent files
        self.save_recent_files()
        
        # Update UI if callback provided
        if 'update_recent_menu' in self.ui_callbacks:
            self.ui_callbacks['update_recent_menu'](self.recent_files)
    
    def load_recent_files(self):
        """Load recent files list"""
        try:
            if os.path.exists('.recent_files.json'):
                with open('.recent_files.json', 'r', encoding='utf-8') as f:
                    self.recent_files = json.load(f)
                # Filter out non-existent files
                self.recent_files = [f for f in self.recent_files if os.path.exists(f)]
        except:
            self.recent_files = []
    
    def save_recent_files(self):
        """Save recent files list"""
        try:
            with open('.recent_files.json', 'w', encoding='utf-8') as f:
                json.dump(self.recent_files, f)
        except:
            pass
    
    def get_recent_files(self):
        """Get list of recent files"""
        return self.recent_files.copy()
    
    def create_launcher_script(self, project_folder, extension):
        """Create a launcher script for the language"""
        lang_name = self.language_data['name'].lower().replace(' ', '_')
        launcher_file = os.path.join(project_folder, f'run_{lang_name}.py')
        
        launcher_code = f'''#!/usr/bin/env python3
"""
{self.language_data['name']} Language Launcher
Usage: python run_{lang_name}.py <file.{extension}>
"""

import sys
import os

def main():
    if len(sys.argv) != 2:
        print("Usage: python run_{lang_name}.py <file.{extension}>")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    if not os.path.exists(filename):
        print(f"Error: File '{{filename}}' not found")
        sys.exit(1)
    
    if not filename.endswith('.{extension}'):
        print(f"Warning: File should have .{extension} extension")
    
    # Import the interpreter
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
    from {lang_name} import {self.language_data['name'].replace(' ', '')}Interpreter
    
    # Create interpreter instance
    interpreter = {self.language_data['name'].replace(' ', '')}Interpreter()
    
    # Run the file
    try:
        interpreter.run_file(filename)
    except Exception as e:
        print(f"Error running {{filename}}: {{e}}")
        sys.exit(1)

if __name__ == "__main__":
    main()
'''
        
        with open(launcher_file, 'w', encoding='utf-8') as f:
            f.write(launcher_code)
    
    def create_example_files_with_extension(self, project_folder, extension):
        """Create example files with the specified extension"""
        examples_folder = os.path.join(project_folder, 'examples')
        
        # Get language keywords
        keywords = self.language_data.get('keywords', {})
        var_kw = keywords.get('variable', 'variable')
        func_kw = keywords.get('function', 'function')
        if_kw = keywords.get('if', 'if')
        print_kw = keywords.get('print', 'print')
        
        # Hello World example
        hello_file = os.path.join(examples_folder, f'hello_world.{extension}')
        hello_code = f'''// Hello World in {self.language_data['name']}
{print_kw}("Hello, World!")
{print_kw}("Welcome to {self.language_data['name']}!")
'''
        
        with open(hello_file, 'w', encoding='utf-8') as f:
            f.write(hello_code)
        
        # Variables example
        vars_file = os.path.join(examples_folder, f'variables.{extension}')
        vars_code = f'''// Variables example in {self.language_data['name']}
{var_kw} name = "Alice"
{var_kw} age = 25
{var_kw} greeting = "Hello, " + name + "!"

{print_kw}(greeting)
{print_kw}("Age: " + age)
'''
        
        with open(vars_file, 'w', encoding='utf-8') as f:
            f.write(vars_code)
        
        # Function example
        func_file = os.path.join(examples_folder, f'functions.{extension}')
        func_code = f'''// Functions example in {self.language_data['name']}
{func_kw} greet(name) {{
    {print_kw}("Hello, " + name + "!")
}}

{func_kw} add(a, b) {{
    return a + b
}}

{var_kw} result = add(5, 3)
greet("World")
{print_kw}("5 + 3 = " + result)
'''
        
        with open(func_file, 'w', encoding='utf-8') as f:
            f.write(func_code)
        
        # Control flow example
        control_file = os.path.join(examples_folder, f'control_flow.{extension}')
        control_code = f'''// Control flow example in {self.language_data['name']}
{var_kw} number = 10

{if_kw} (number > 0) {{
    {print_kw}("Number is positive")
}} else {{
    {print_kw}("Number is not positive")
}}

{var_kw} i = 0
while (i < 5) {{
    {print_kw}("Count: " + i)
    i = i + 1
}}
'''
        
        with open(control_file, 'w', encoding='utf-8') as f:
            f.write(control_code)
    
    def create_enhanced_documentation(self, project_folder, extension):
        """Create enhanced documentation"""
        docs_folder = os.path.join(project_folder, 'docs')
        
        # Language reference
        reference_file = os.path.join(docs_folder, 'language_reference.md')
        reference_content = f'''# {self.language_data['name']} Language Reference

## Overview
{self.language_data.get('description', 'A custom programming language.')}

**Version:** {self.language_data.get('version', '1.0')}
**Author:** {self.language_data.get('author', 'Unknown')}
**File Extension:** .{extension}

## Keywords

'''
        
        # Add keywords section
        keywords = self.language_data.get('keywords', {})
        for key, value in keywords.items():
            reference_content += f'- **{key}**: `{value}`\\n'
        
        reference_content += '''
## Operators

'''
        
        # Add operators section
        operators = self.language_data.get('operators', {})
        for key, value in operators.items():
            reference_content += f'- **{key.replace("_", " ").title()}**: `{value}`\\n'
        
        reference_content += '''
## Built-in Functions

'''
        
        # Add built-ins section
        builtins = self.language_data.get('builtins', {})
        for key, value in builtins.items():
            reference_content += f'- **{value}()**: {key.replace("_", " ").title()}\\n'
        
        reference_content += f'''
## Usage

To run a {self.language_data['name']} program:

```bash
python run_{self.language_data['name'].lower().replace(' ', '_')}.py program.{extension}
```

## Examples

See the `examples/` folder for sample programs.
'''
        
        with open(reference_file, 'w', encoding='utf-8') as f:
            f.write(reference_content)
    
    def create_enhanced_readme(self, project_folder, extension):
        """Create enhanced README"""
        readme_file = os.path.join(project_folder, 'README.md')
        lang_name = self.language_data['name']
        script_name = self.language_data['name'].lower().replace(' ', '_')
        
        readme_content = f'''# {lang_name} Programming Language

{self.language_data.get('description', 'A custom programming language created with SUPER Language Creator.')}

## Quick Start

### Prerequisites
- Python 3.6 or higher

### Installation
1. Clone or download this repository
2. Run the installation script:
   ```bash
   python install.py
   ```

### Running Programs
```bash
python run_{script_name}.py program.{extension}
```

### Examples
Try the example programs:
```bash
python run_{script_name}.py examples/hello_world.{extension}
python run_{script_name}.py examples/variables.{extension}
python run_{script_name}.py examples/functions.{extension}
```

## Language Features

### Keywords
'''
        
        # Add keywords
        keywords = self.language_data.get('keywords', {})
        for key, value in keywords.items():
            readme_content += f'- `{value}` - {key.replace("_", " ").title()}\\n'
        
        readme_content += '''
### Built-in Functions
'''
        
        # Add built-ins
        builtins = self.language_data.get('builtins', {})
        for key, value in builtins.items():
            readme_content += f'- `{value}()` - {key.replace("_", " ").title()}\\n'
        
        readme_content += f'''
## File Structure
```
{script_name}_language/
├── src/                    # Interpreter source code
├── examples/              # Example programs
├── docs/                  # Documentation
├── tests/                 # Test files
├── language.json          # Language definition
├── run_{script_name}.py   # Language runner
├── install.py            # Installation script
└── README.md             # This file
```

## Language Information
- **Version:** {self.language_data.get('version', '1.0')}
- **Author:** {self.language_data.get('author', 'Unknown')}
- **Created:** {self.language_data.get('created', 'Unknown')}
- **File Extension:** .{extension}

## Development
This language was created using [SUPER Language Creator](https://github.com/your-repo/super-lang-creator).

## License
This project is open source and available under the MIT License.
'''
        
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
    
    def create_installation_script(self, project_folder, extension):
        """Create installation script"""
        install_file = os.path.join(project_folder, 'install.py')
        lang_name = self.language_data['name']
        script_name = self.language_data['name'].lower().replace(' ', '_')
        
        install_code = f'''#!/usr/bin/env python3
"""
Installation script for {lang_name}
"""

import os
import sys
import shutil

def main():
    print("Installing {lang_name}...")
    
    # Check Python version
    if sys.version_info < (3, 6):
        print("Error: Python 3.6 or higher is required")
        sys.exit(1)
    
    # Check if all required files exist
    required_files = [
        'src/{script_name}.py',
        'language.json',
        'run_{script_name}.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("Error: Missing required files:")
        for file in missing_files:
            print(f"  - {{file}}")
        sys.exit(1)
    
    # Make runner script executable (on Unix-like systems)
    if os.name != 'nt':
        try:
            os.chmod('run_{script_name}.py', 0o755)
        except:
            pass
    
    print("✓ {lang_name} installed successfully!")
    print()
    print("Usage:")
    print(f"  python run_{script_name}.py program.{extension}")
    print()
    print("Examples:")
    print(f"  python run_{script_name}.py examples/hello_world.{extension}")
    print(f"  python run_{script_name}.py examples/variables.{extension}")
    print()
    print("Documentation:")
    print("  See docs/language_reference.md for complete language reference")

if __name__ == "__main__":
    main()
'''
        
        with open(install_file, 'w', encoding='utf-8') as f:
            f.write(install_code)

class AutoSaveManager:
    """Manages automatic saving functionality"""
    
    def __init__(self, file_operations, interval_minutes=2):
        self.file_operations = file_operations
        self.interval_minutes = interval_minutes
        self.last_save_time = datetime.now()
        self.auto_save_enabled = True
        self.timer_id = None
    
    def start_autosave(self, root):
        """Start the autosave timer"""
        if self.auto_save_enabled:
            self.schedule_autosave(root)
    
    def schedule_autosave(self, root):
        """Schedule the next autosave"""
        if self.timer_id:
            root.after_cancel(self.timer_id)
        
        # Schedule autosave after interval
        interval_ms = self.interval_minutes * 60 * 1000
        self.timer_id = root.after(interval_ms, lambda: self.perform_autosave(root))
    
    def perform_autosave(self, root):
        """Perform autosave if needed"""
        try:
            if (self.auto_save_enabled and 
                self.file_operations.has_unsaved_changes() and
                self.file_operations.current_file):
                
                # Create autosave file
                autosave_file = self.file_operations.current_file + '.autosave'
                
                # Collect current data if callback available
                if 'collect_data' in self.file_operations.ui_callbacks:
                    self.file_operations.ui_callbacks['collect_data']()
                
                # Save autosave file
                with open(autosave_file, 'w', encoding='utf-8') as f:
                    json.dump(self.file_operations.language_data, f, indent=2)
                
                self.last_save_time = datetime.now()
                
                # Update status
                if 'update_status' in self.file_operations.ui_callbacks:
                    self.file_operations.ui_callbacks['update_status']("Auto-saved")
        
        except Exception as e:
            print(f"Autosave failed: {e}")
        
        finally:
            # Schedule next autosave
            self.schedule_autosave(root)
    
    def stop_autosave(self, root):
        """Stop the autosave timer"""
        if self.timer_id:
            root.after_cancel(self.timer_id)
            self.timer_id = None
    
    def toggle_autosave(self):
        """Toggle autosave on/off"""
        self.auto_save_enabled = not self.auto_save_enabled
        return self.auto_save_enabled

class TemplateManager:
    """Manages language templates"""
    
    def __init__(self):
        self.templates_dir = "templates"
        self.ensure_templates_dir()
    
    def ensure_templates_dir(self):
        """Ensure templates directory exists"""
        if not os.path.exists(self.templates_dir):
            os.makedirs(self.templates_dir)
            self.create_default_templates()
    
    def create_default_templates(self):
        """Create default language templates"""
        templates = {
            'simple_language': {
                'name': 'SimpleLang',
                'version': '1.0',
                'author': 'Template Author',
                'description': 'A simple programming language template',
                'keywords': {
                    'variable': 'var',
                    'function': 'func',
                    'if': 'if',
                    'else': 'else',
                    'loop': 'while',
                    'return': 'return',
                    'true': 'true',
                    'false': 'false',
                    'null': 'null'
                },
                'builtins': {
                    'print': 'print',
                    'input': 'input',
                    'length': 'len',
                    'string': 'str',
                    'number': 'num',
                    'random': 'rand'
                },
                'errors': {
                    'syntax': 'Syntax error',
                    'runtime': 'Runtime error',
                    'type': 'Type error'
                }
            },
            'kids_language': {
                'name': 'KidsLang',
                'version': '1.0',
                'author': 'Template Author',
                'description': 'A kid-friendly programming language',
                'keywords': {
                    'variable': 'remember',
                    'function': 'teach',
                    'if': 'when',
                    'else': 'otherwise',
                    'loop': 'repeat',
                    'return': 'give',
                    'true': 'yes',
                    'false': 'no',
                    'null': 'nothing'
                },
                'builtins': {
                    'print': 'say',
                    'input': 'ask',
                    'length': 'count',
                    'string': 'words',
                    'number': 'number',
                    'random': 'surprise'
                },
                'errors': {
                    'syntax': 'Oops! Something is wrong with your code',
                    'runtime': 'Something went wrong while running',
                    'type': 'Wrong type of information'
                }
            }
        }
        
        for template_name, template_data in templates.items():
            template_file = os.path.join(self.templates_dir, f"{template_name}.json")
            with open(template_file, 'w', encoding='utf-8') as f:
                json.dump(template_data, f, indent=2)
    
    def get_available_templates(self):
        """Get list of available templates"""
        templates = []
        if os.path.exists(self.templates_dir):
            for file in os.listdir(self.templates_dir):
                if file.endswith('.json'):
                    try:
                        template_path = os.path.join(self.templates_dir, file)
                        with open(template_path, 'r', encoding='utf-8') as f:
                            template_data = json.load(f)
                        
                        templates.append({
                            'filename': file,
                            'name': template_data.get('name', file[:-5]),
                            'description': template_data.get('description', 'No description'),
                            'path': template_path
                        })
                    except:
                        continue
        
        return templates
    
    def load_template(self, template_path):
        """Load a template and return its data"""
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise Exception(f"Failed to load template: {e}")
    
    def save_as_template(self, language_data, template_name):
        """Save current language as a template"""
        try:
            template_data = language_data.copy()
            # Remove instance-specific data
            template_data.pop('created', None)
            template_data.pop('modified', None)
            
            template_file = os.path.join(self.templates_dir, f"{template_name}.json")
            with open(template_file, 'w', encoding='utf-8') as f:
                json.dump(template_data, f, indent=2)
            
            return True
        except Exception as e:
            raise Exception(f"Failed to save template: {e}")

class ProjectBackup:
    """Manages project backups"""
    
    def __init__(self, max_backups=5):
        self.backup_dir = "backups"
        self.max_backups = max_backups
        self.ensure_backup_dir()
    
    def ensure_backup_dir(self):
        """Ensure backup directory exists"""
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
    
    def create_backup(self, language_data, filename_hint=""):
        """Create a backup of the current language"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"backup_{filename_hint}_{timestamp}.json"
            backup_path = os.path.join(self.backup_dir, backup_name)
            
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(language_data, f, indent=2)
            
            # Clean old backups
            self.cleanup_old_backups()
            
            return backup_path
        except Exception as e:
            print(f"Failed to create backup: {e}")
            return None
    
    def cleanup_old_backups(self):
        """Remove old backup files"""
        try:
            backups = []
            for file in os.listdir(self.backup_dir):
                if file.startswith('backup_') and file.endswith('.json'):
                    backup_path = os.path.join(self.backup_dir, file)
                    backups.append((os.path.getmtime(backup_path), backup_path))
            
            # Sort by modification time (newest first)
            backups.sort(reverse=True)
            
            # Remove old backups
            for i, (_, backup_path) in enumerate(backups[self.max_backups:]):
                try:
                    os.remove(backup_path)
                except:
                    pass
        except:
            pass
    
    def get_available_backups(self):
        """Get list of available backups"""
        backups = []
        try:
            if os.path.exists(self.backup_dir):
                for file in os.listdir(self.backup_dir):
                    if file.startswith('backup_') and file.endswith('.json'):
                        backup_path = os.path.join(self.backup_dir, file)
                        mtime = os.path.getmtime(backup_path)
                        backups.append({
                            'filename': file,
                            'path': backup_path,
                            'modified': datetime.fromtimestamp(mtime)
                        })
                
                # Sort by modification time (newest first)
                backups.sort(key=lambda x: x['modified'], reverse=True)
        except:
            pass
        
        return backups