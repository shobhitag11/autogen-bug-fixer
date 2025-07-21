# Step 1: Import Libraries
from autogen import (
    UserProxyAgent,
    ConversableAgent,
    GroupChat,
    GroupChatManager
)

# Step 2: Define the User (You)
user = UserProxyAgent(
    name="User",
    is_termination_msg=lambda msg: "exit" in msg.lower() or "task complete" in msg.lower(),
    human_input_mode="NEVER"  # Disable terminal input
)

# Step 3: Define the Coder Agent (writes or fixes code)
coder = ConversableAgent(
    name="CodeFixer",
    system_message="You are a helpful software engineer. Your job is to fix buggy Python code provided by the user. Ensure the fixed code runs correctly.",
    llm_config={"model": "gpt-4", "temperature": 0},
    memory=True
)

# Step 4: Define the Reviewer Agent (checks for correctness)
reviewer = ConversableAgent(
    name="CodeReviewer",
    system_message="You are a strict code reviewer. Review the code provided by the CodeFixer. If the bug is fixed, say 'task complete'. Otherwise, give feedback.",
    llm_config={"model": "gpt-4", "temperature": 0.2},
    memory=True
)

# Step 5: Setup the GroupChat
group_chat = GroupChat(
    agents=[user, coder, reviewer],
    messages=[],
    max_round=6
)

# Step 6: Setup the GroupChatManager
manager = GroupChatManager(groupchat=group_chat)

# Step 7: Provide the buggy code
buggy_code = """
def divide(a, b):
    return a / b

print(divide(10, 0))  # This causes ZeroDivisionError
"""

initial_message = f"Fix the following Python code that has a bug:\n\n{buggy_code}"

# Step 8: Start the chat
user.initiate_chat(manager, message=initial_message)