import autogen
from typing import Dict, Any

class CodeReviewerAgent:
    def __init__(self, llm_config: Dict[str, Any]):
        self.agent = autogen.AssistantAgent(
            name="CodeReviewer",
            system_message="""You are a Senior Code Reviewer. Your responsibilities include:
            
            1. **Code Quality Assessment**: Review code for best practices, readability, maintainability
            2. **Security Review**: Identify potential security vulnerabilities
            3. **Performance Analysis**: Spot performance bottlenecks and inefficiencies
            4. **Design Pattern Validation**: Ensure proper use of design patterns
            5. **Documentation Review**: Check for adequate documentation and comments
            
            When reviewing code:
            - Follow PEP 8 style guidelines for Python
            - Check for proper error handling
            - Validate input sanitization
            - Ensure proper resource management
            - Look for code duplication
            - Verify edge case handling
            
            Provide constructive feedback with:
            - Specific line-by-line comments
            - Severity levels (Critical, Major, Minor)
            - Suggested improvements
            - Code examples when applicable
            """,
            llm_config=llm_config,
            human_input_mode="NEVER"
        )
    
    def create_review_prompt(self, code: str, context: str = "") -> str:
        """Create code review prompt"""
        prompt = f"""
        Please review the following code:
        
        **Context:** {context}
        
        **Code to Review:**
        ```
        {code}
        ```
        
        Please provide a detailed review covering:
        1. Code quality and style
        2. Potential bugs or issues
        3. Security considerations
        4. Performance implications
        5. Suggestions for improvement
        
        Format your response as:
        - **Overall Assessment**: Brief summary
        - **Issues Found**: List with severity levels
        - **Recommendations**: Specific improvement suggestions
        - **Refactored Code**: Improved version if needed
        """
        return prompt
