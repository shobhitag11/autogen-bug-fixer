import autogen
from typing import Dict, Any, List

class BugAnalyzerAgent:
    def __init__(self, llm_config: Dict[str, Any]):
        self.agent = autogen.AssistantAgent(
            name="BugAnalyzer",
            system_message="""You are a Bug Analyzer expert. Your role is to:
            
            1. **Analyze Error Reports**: Examine error messages, stack traces, and logs
            2. **Identify Root Causes**: Determine the underlying cause of bugs
            3. **Categorize Issues**: Classify bugs (logic error, syntax error, runtime error, etc.)
            4. **Provide Context**: Explain the impact and severity of the bug
            5. **Suggest Investigation Areas**: Point to specific code sections to examine
            
            When analyzing bugs:
            - Read error messages carefully
            - Trace the execution path
            - Identify the exact line/function where error occurs
            - Consider edge cases and input validation
            - Look for common anti-patterns
            
            Always provide structured analysis with:
            - Bug type and severity
            - Root cause explanation
            - Affected components
            - Recommended fix approach
            """,
            llm_config=llm_config,
            human_input_mode="NEVER"
        )
    
    def create_analysis_prompt(self, error_info: Dict[str, Any]) -> str:
        """Create detailed analysis prompt"""
        prompt = f"""
        Please analyze the following bug:
        
        **Error Information:**
        - Error Message: {error_info.get('error_message', 'N/A')}
        - Stack Trace: {error_info.get('stack_trace', 'N/A')}
        - File: {error_info.get('file_path', 'N/A')}
        - Line: {error_info.get('line_number', 'N/A')}
        
        **Code Context:**
        ```
        {error_info.get('code_snippet', 'N/A')}
        ```
        
        **Additional Context:**
        - Input/Test Case: {error_info.get('input_data', 'N/A')}
        - Expected Output: {error_info.get('expected_output', 'N/A')}
        - Actual Output: {error_info.get('actual_output', 'N/A')}
        
        Please provide a comprehensive analysis including:
        1. Bug classification and severity
        2. Root cause analysis
        3. Impact assessment
        4. Recommended fix strategy
        """
        return prompt
