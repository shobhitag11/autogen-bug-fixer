import os
import shutil
from typing import Dict, List, Optional
import json

class FileHandler:
    def __init__(self, workspace_dir: str = "workspace"):
        self.workspace_dir = workspace_dir
        self.ensure_workspace()
    
    def ensure_workspace(self):
        """Ensure workspace directory exists"""
        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)
    
    def read_file(self, file_path: str) -> Optional[str]:
        """Read file content"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"
    
    def write_file(self, file_path: str, content: str) -> bool:
        """Write content to file"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error writing file: {str(e)}")
            return False
    
    def list_files(self, directory: str, extensions: List[str] = None) -> List[str]:
        """List files in directory with optional extension filter"""
        files = []
        if not os.path.exists(directory):
            return files
        
        for root, dirs, filenames in os.walk(directory):
            for filename in filenames:
                if extensions is None or any(filename.endswith(ext) for ext in extensions):
                    files.append(os.path.join(root, filename))
        return files
    
    def backup_file(self, file_path: str) -> str:
        """Create backup of file"""
        backup_path = f"{file_path}.backup"
        try:
            shutil.copy2(file_path, backup_path)
            return backup_path
        except Exception as e:
            return f"Error creating backup: {str(e)}"

class CodeAnalyzer:
    @staticmethod
    def extract_functions(code: str) -> List[Dict]:
        """Extract function definitions from code"""
        import ast
        import inspect
        
        functions = []
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_code = ast.get_source_segment(code, node)
                    functions.append({
                        'name': node.name,
                        'line_start': node.lineno,
                        'line_end': node.end_lineno,
                        'code': func_code or '',
                        'args': [arg.arg for arg in node.args.args]
                    })
        except Exception as e:
            print(f"Error parsing code: {str(e)}")
        
        return functions
    
    @staticmethod
    def get_imports(code: str) -> List[str]:
        """Extract import statements from code"""
        import ast
        
        imports = []
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(f"import {alias.name}")
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ''
                    for alias in node.names:
                        imports.append(f"from {module} import {alias.name}")
        except Exception as e:
            print(f"Error extracting imports: {str(e)}")
        
        return imports
