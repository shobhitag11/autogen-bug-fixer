import autogen
from typing import Dict, Any

class FixerAgent:
    def __init__(self, llm_config: Dict[str, Any]):
        self.agent = autogen.AssistantAgent(
            name="BugFixer",
            system_message="""You are a Bug Fixing Specialist. Your expertise includes:
            
            1. **Bug Resolution**: Implement precise fixes based on analysis
            2. **Code Refactoring**: Improve code structure while fixing issues
            3. **Backwards Compatibility**: Ensure fixes don't break existing code
            4. **Performance Optimization**: Fix bugs while improving performance
            5. **Documentation Updates**: Update comments and docstrings
            
            When fixing bugs:
            - Make minimal, targeted changes
            - Preserve existing functionality
            - Add appropriate error handling
            - Follow existing code style
            - Include comprehensive comments
            - Consider performance implications
            
            Your fixes should be:
            - Correct and complete
            - Well-documented
            - Tested and validated
            - Maintainable
            - Following best practices
            """,
            llm_config=llm_config,
            human_input_mode="NEVER"
        )
    
    def create_fix_prompt(self, bug_analysis: str, original_code: str, test_cases: str = "") -> str:
        """Create bug fix prompt"""
        prompt = f"""
        Please fix the bug based on the following analysis:
        
        **Bug Analysis:**
        {bug_analysis}
        
        **Original Code:**
        ```
        {original_code}
        ```
        
        **Test Cases:**
        ```
        {test_cases}
        ```
        
        Please provide:
        1. **Fixed Code**: Complete corrected version
        2. **Change Summary**: What was changed and why
        3. **Validation**: How to verify the fix works
        4. **Impact Assessment**: Any side effects or considerations
        
        Requirements:
        - Fix the specific bug identified
        - Maintain code style and structure
        - Add error handling if missing
        - Include helpful comments
        - Ensure all test cases pass
        """
        return prompt
