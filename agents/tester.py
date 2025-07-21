import autogen
from typing import Dict, Any

class TesterAgent:
    def __init__(self, llm_config: Dict[str, Any]):
        self.agent = autogen.AssistantAgent(
            name="Tester",
            system_message="""You are a QA Testing Expert. Your role involves:
            
            1. **Test Case Generation**: Create comprehensive test cases
            2. **Edge Case Identification**: Find boundary conditions and corner cases
            3. **Test Automation**: Write automated tests using pytest
            4. **Regression Testing**: Ensure fixes don't break existing functionality
            5. **Performance Testing**: Create tests for performance validation
            
            When creating tests:
            - Cover positive and negative test cases
            - Include edge cases and boundary conditions
            - Test error handling and exceptions
            - Validate input/output specifications
            - Create mock objects when needed
            - Follow testing best practices
            
            Generate tests that are:
            - Readable and maintainable
            - Independent and isolated
            - Deterministic and repeatable
            - Fast and efficient
            """,
            llm_config=llm_config,
            human_input_mode="NEVER"
        )
    
    def create_test_prompt(self, function_code: str, bug_info: str = "") -> str:
        """Create test generation prompt"""
        prompt = f"""
        Please create comprehensive test cases for the following function:
        
        **Function Code:**
        ```
        {function_code}
        ```
        
        **Bug Context:**
        {bug_info}
        
        Please generate:
        1. **Unit Tests**: Using pytest framework
        2. **Edge Case Tests**: Boundary conditions and corner cases
        3. **Error Handling Tests**: Exception scenarios
        4. **Integration Tests**: If applicable
        
        Requirements:
        - Use pytest fixtures where appropriate
        - Include descriptive test names
        - Add docstrings explaining test purpose
        - Cover at least 90% code coverage
        - Include parameterized tests for multiple inputs
        
        Format as complete Python test file with imports.
        """
        return prompt
