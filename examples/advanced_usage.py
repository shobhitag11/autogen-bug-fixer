from main import BugFixingSystem
import json

class AdvancedBugFixingDemo:
    def __init__(self):
        self.bug_fixer = BugFixingSystem()
    
    def demo_multiple_bugs(self):
        """Demo fixing multiple bugs in sequence"""
        print("🔄 Demo: Multiple Bug Fixes")
        
        # Create multiple buggy files
        bugs = [
            {
                'name': 'null_pointer',
                'code': '''
def process_data(data):
    return data.upper().strip()  # Bug: No null check

def main():
    result = process_data(None)  # This will fail
    print(result)
''',
                'error': 'AttributeError: NoneType object has no attribute upper'
            },
            {
                'name': 'index_error',
                'code': '''
def get_first_element(lst):
    return lst[0]  # Bug: No empty list check

def main():
    result = get_first_element([])  # This will fail
    print(result)
''',
                'error': 'IndexError: list index out of range'
            }
        ]
        
        for bug in bugs:
            print(f"\n🐛 Fixing bug: {bug['name']}")
            
            # Create buggy file
            file_path = f"workspace/{bug['name']}.py"
            self.bug_fixer.file_handler.write_file(file_path, bug['code'])
            
            # Fix the bug
            bug_report = {
                'file_path': file_path,
                'error_message': bug['error'],
                'test_input': 'main()',
                'expected_output': 'Should handle edge cases gracefully'
            }
            
            results = self.bug_fixer.fix_bug(bug_report)
            
            if results['status'] == 'success':
                print(f"✅ Fixed {bug['name']}")
            else:
                print(f"❌ Failed to fix {bug['name']}: {results['error']}")
    
    def demo_performance_bug(self):
        """Demo fixing performance-related bugs"""
        print("\n⚡ Demo: Performance Bug Fix")
        
        slow_code = '''
def find_duplicates(numbers):
    """Find duplicate numbers in list - SLOW VERSION"""
    duplicates = []
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] == numbers[j] and numbers[i] not in duplicates:
                duplicates.append(numbers[i])
    return duplicates

def fibonacci_slow(n):
    """Fibonacci with recursion - VERY SLOW"""
    if n <= 1:
        return n
    return fibonacci_slow(n-1) + fibonacci_slow(n-2)

if __name__ == "__main__":
    # This will be very slow for large inputs
    large_list = list(range(1000)) * 2
    dupes = find_duplicates(large_list)
    
    fib_30 = fibonacci_slow(30)  # This will take forever
'''
        
        file_path = "workspace/performance_bug.py"
        self.bug_fixer.file_handler.write_file(file_path, slow_code)
        
        bug_report = {
            'file_path': file_path,
            'error_message': 'Performance issue: O(n²) complexity causing timeout',
            'test_input': 'Large dataset processing',
            'expected_output': 'Should complete in reasonable time',
            'actual_output': 'Times out or takes too long'
        }
        
        results = self.bug_fixer.fix_bug(bug_report)
        
        if results['status'] == 'success':
            print("✅ Performance bug fixed!")
        else:
            print(f"❌ Failed to fix performance bug: {results['error']}")

if __name__ == "__main__":
    demo = AdvancedBugFixingDemo()
    demo.demo_multiple_bugs()
    demo.demo_performance_bug()
