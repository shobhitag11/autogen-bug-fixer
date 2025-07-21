import subprocess
import tempfile
import os
from typing import Tuple, Dict, Any

class CodeExecutor:
    def __init__(self, timeout: int = 60):
        self.timeout = timeout
    
    def execute_python(self, code: str, file_path: str = None) -> Tuple[bool, str, str]:
        """Execute Python code and return success, stdout, stderr"""
        if file_path:
            return self._execute_file(file_path)
        else:
            return self._execute_string(code)
    
    def _execute_string(self, code: str) -> Tuple[bool, str, str]:
        """Execute Python code string"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        try:
            result = self._execute_file(temp_file)
        finally:
            os.unlink(temp_file)
        
        return result
    
    def _execute_file(self, file_path: str) -> Tuple[bool, str, str]:
        """Execute Python file"""
        try:
            result = subprocess.run(
                ['python', file_path],
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            
            success = result.returncode == 0
            return success, result.stdout, result.stderr
            
        except subprocess.TimeoutExpired:
            return False, "", "Execution timeout"
        except Exception as e:
            return False, "", str(e)
    
    def run_tests(self, test_file: str) -> Tuple[bool, str]:
        """Run pytest on test file"""
        try:
            result = subprocess.run(
                ['pytest', test_file, '-v'],
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            
            success = result.returncode == 0
            output = result.stdout + result.stderr
            return success, output
            
        except subprocess.TimeoutExpired:
            return False, "Test execution timeout"
        except Exception as e:
            return False, str(e)
    
    def lint_code(self, file_path: str) -> Tuple[bool, str]:
        """Run flake8 linting on code"""
        try:
            result = subprocess.run(
                ['flake8', file_path, '--max-line-length=88', '--ignore=E203,W503'],
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            
            clean = result.returncode == 0
            return clean, result.stdout
            
        except Exception as e:
            return False, str(e)
