import os
import json
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
import autogen
from utils.file_handler import FileHandler, CodeAnalyzer
from utils.code_executor import CodeExecutor
from agents.bug_analyzer import BugAnalyzerAgent
from agents.code_reviewer import CodeReviewerAgent
from agents.tester import TesterAgent
from agents.fixer import FixerAgent

class BugFixingSystem:
    def __init__(self, config_path: str = "config/config.json"):
        # Load environment variables
        load_dotenv()
        
        # Load configuration
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        # Setup Azure OpenAI configuration
        self.llm_config = self._setup_llm_config()
        
        # Initialize utilities
        self.file_handler = FileHandler(self.config['code_execution_config']['work_dir'])
        self.code_executor = CodeExecutor(self.config['code_execution_config']['timeout'])
        self.code_analyzer = CodeAnalyzer()
        
        # Initialize agents
        self._initialize_agents()
        
        # Setup group chat
        self._setup_group_chat()
    
    def _setup_llm_config(self) -> Dict[str, Any]:
        """Setup Azure OpenAI configuration"""
        return {
            "model": os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            "api_key": os.getenv("AZURE_OPENAI_API_KEY"),
            "base_url": os.getenv("AZURE_OPENAI_ENDPOINT"),
            "api_type": "azure",
            "api_version": os.getenv("AZURE_OPENAI_API_VERSION"),
            "temperature": self.config['llm_config']['temperature'],
            "max_tokens": self.config['llm_config']['max_tokens'],
            "timeout": self.config['llm_config']['timeout']
        }
    
    def _initialize_agents(self):
        """Initialize all specialized agents"""
        self.bug_analyzer = BugAnalyzerAgent(self.llm_config)
        self.code_reviewer = CodeReviewerAgent(self.llm_config)
        self.tester = TesterAgent(self.llm_config)
        self.fixer = FixerAgent(self.llm_config)
        
        # Create coordinator agent
        self.coordinator = autogen.AssistantAgent(
            name="Coordinator",
            system_message="""You are the Bug Fixing Coordinator. Your role is to:
            
            1. **Orchestrate the bug fixing workflow**
            2. **Coordinate between different specialized agents**
            3. **Ensure proper sequence of operations**
            4. **Validate final results**
            5. **Provide status updates and summaries**
            
            Workflow sequence:
            1. BugAnalyzer analyzes the bug
            2. CodeReviewer reviews problematic code
            3. Tester creates test cases
            4. BugFixer implements the fix
            5. Final validation and testing
            
            Always ensure each step is completed before moving to the next.
            """,
            llm_config=self.llm_config,
            human_input_mode="NEVER"
        )
        
        # Create user proxy for interaction
        self.user_proxy = autogen.UserProxyAgent(
            name="UserProxy",
            system_message="You represent the user in the bug fixing process.",
            human_input_mode="NEVER",
            code_execution_config=self.config['code_execution_config'],
            max_consecutive_auto_reply=self.config['agents_config']['max_consecutive_auto_reply']
        )
    
    def _setup_group_chat(self):
        """Setup group chat for agent collaboration"""
        self.agents = [
            self.coordinator,
            self.bug_analyzer.agent,
            self.code_reviewer.agent,
            self.tester.agent,
            self.fixer.agent,
            self.user_proxy
        ]
        
        self.group_chat = autogen.GroupChat(
            agents=self.agents,
            messages=[],
            max_round=20,
            speaker_selection_method="auto"
        )
        
        self.group_chat_manager = autogen.GroupChatManager(
            groupchat=self.group_chat,
            llm_config=self.llm_config
        )
    
    def fix_bug(self, bug_report: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main bug fixing workflow
        
        Args:
            bug_report: Dictionary containing:
                - file_path: Path to the buggy file
                - error_message: Error message
                - stack_trace: Stack trace (optional)
                - test_input: Input that caused the bug (optional)
                - expected_output: Expected result (optional)
        
        Returns:
            Dictionary with fix results and analysis
        """
        print("🐛 Starting Bug Fixing Process...")
        
        # Read the buggy file
        file_content = self.file_handler.read_file(bug_report['file_path'])
        if not file_content or "Error reading file" in file_content:
            return {"error": f"Could not read file: {bug_report['file_path']}"}
        
        # Create backup
        backup_path = self.file_handler.backup_file(bug_report['file_path'])
        print(f"📁 Created backup: {backup_path}")
        
        # Prepare bug information
        bug_info = {
            'file_path': bug_report['file_path'],
            'error_message': bug_report.get('error_message', ''),
            'stack_trace': bug_report.get('stack_trace', ''),
            'code_snippet': file_content,
            'input_data': bug_report.get('test_input', ''),
            'expected_output': bug_report.get('expected_output', ''),
            'actual_output': bug_report.get('actual_output', '')
        }
        
        # Start the collaborative bug fixing process
        initial_message = f"""
        We need to fix a bug in the file: {bug_report['file_path']}
        
        Error: {bug_report.get('error_message', 'No error message provided')}
        
        Let's work together to:
        1. Analyze the bug thoroughly
        2. Review the code quality
        3. Create comprehensive tests
        4. Implement a proper fix
        5. Validate the solution
        
        File content:
        ```
        {file_content}
        ```
        """
        
        try:
            # Start group chat
            self.user_proxy.initiate_chat(
                self.group_chat_manager,
                message=initial_message,
                clear_history=True
            )
            
            # Process the conversation and extract results
            results = self._process_results(bug_report['file_path'])
            
            return {
                "status": "success",
                "backup_path": backup_path,
                "results": results,
                "conversation_history": self.group_chat.messages
            }
            
        except Exception as e:
            print(f"❌ Error during bug fixing: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "backup_path": backup_path
            }
    
    def _process_results(self, file_path: str) -> Dict[str, Any]:
        """Process conversation results and extract key information"""
        messages = self.group_chat.messages
        
        results = {
            "analysis": "",
            "review": "",
            "tests": "",
            "fix": "",
            "validation": ""
        }
        
        # Extract information from conversation
        for message in messages:
            sender = message.get("name", "")
            content = message.get("content", "")
            
            if sender == "BugAnalyzer" and "analysis" in content.lower():
                results["analysis"] = content
            elif sender == "CodeReviewer" and "review" in content.lower():
                results["review"] = content
            elif sender == "Tester" and ("test" in content.lower() or "pytest" in content.lower()):
                results["tests"] = content
            elif sender == "BugFixer" and "fix" in content.lower():
                results["fix"] = content
        
        return results
    
    def create_sample_bug(self, file_path: str = "workspace/sample_buggy.py"):
        """Create a sample buggy file for testing"""
        buggy_code = '''
def divide_numbers(a, b):
    """Divide two numbers"""
    result = a / b  # Bug: No check for division by zero
    return result

def calculate_average(numbers):
    """Calculate average of a list of numbers"""
    total = sum(numbers)
    count = len(numbers)  # Bug: No check for empty list
    return total / count

def find_maximum(numbers):
    """Find maximum number in list"""
    max_num = numbers[0]  # Bug: No check for empty list
    for num in numbers[1:]:
        if num > max_num:
            max_num = num
    return max_num

def fibonacci(n):
    """Generate fibonacci sequence"""
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    return fib

# Test the functions (this will cause errors)
if __name__ == "__main__":
    print("Testing divide_numbers:")
    print(divide_numbers(10, 2))
    print(divide_numbers(10, 0))  # This will cause ZeroDivisionError
    
    print("Testing calculate_average:")
    print(calculate_average([1, 2, 3, 4, 5]))
    print(calculate_average([]))  # This will cause ZeroDivisionError
    
    print("Testing find_maximum:")
    print(find_maximum([1, 5, 3, 9, 2]))
    print(find_maximum([]))  # This will cause IndexError
'''
        
        self.file_handler.write_file(file_path, buggy_code)
        print(f"📝 Created sample buggy file: {file_path}")
        return file_path

# Example usage and testing
if __name__ == "__main__":
    # Initialize the bug fixing system
    bug_fixer = BugFixingSystem()
    
    # Create a sample buggy file
    sample_file = bug_fixer.create_sample_bug()
    
    # Define bug report
    bug_report = {
        'file_path': sample_file,
        'error_message': 'ZeroDivisionError: division by zero',
        'stack_trace': '''Traceback (most recent call last):
  File "workspace/sample_buggy.py", line 32, in <module>
    print(divide_numbers(10, 0))
  File "workspace/sample_buggy.py", line 4, in <module>
    result = a / b
ZeroDivisionError: division by zero''',
        'test_input': 'divide_numbers(10, 0)',
        'expected_output': 'Should handle division by zero gracefully',
        'actual_output': 'ZeroDivisionError exception'
    }
    
    print("🚀 Starting Bug Fixing Demo...")
    print("="*60)
    
    # Fix the bug
    results = bug_fixer.fix_bug(bug_report)
    
    # Display results
    print("\n" + "="*60)
    print("📊 BUG FIXING RESULTS")
    print("="*60)
    
    if results['status'] == 'success':
        print("✅ Bug fixing completed successfully!")
        print(f"📁 Backup created at: {results['backup_path']}")
        
        print("\n🔍 ANALYSIS:")
        print("-" * 40)
        print(results['results'].get('analysis', 'No analysis found')[:500] + "...")
        
        print("\n👀 CODE REVIEW:")
        print("-" * 40)
        print(results['results'].get('review', 'No review found')[:500] + "...")
        
        print("\n🧪 TESTS:")
        print("-" * 40)
        print(results['results'].get('tests', 'No tests found')[:500] + "...")
        
        print("\n🔧 FIX:")
        print("-" * 40)
        print(results['results'].get('fix', 'No fix found')[:500] + "...")
        
    else:
        print(f"❌ Bug fixing failed: {results['error']}")
    
    print("\n" + "="*60)
    print("Demo completed! Check the workspace directory for generated files.")
