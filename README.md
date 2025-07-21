# AutoGen Multi-Agent Bug Fixing System

## Description
This project implements a sophisticated multi-agent system using AutoGen to automatically analyze, test, and fix bugs in Python code. The system orchestrates a team of specialized AI agents that collaborate to resolve software defects.

The core workflow involves the following agents:
- **Coordinator**: Manages the overall bug-fixing process and ensures agents work in the correct sequence.
- **BugAnalyzer**: Examines the bug report, error messages, and code to understand the root cause.
- **CodeReviewer**: Reviews the problematic code for quality, style, and potential issues.
- **Tester**: Generates comprehensive `pytest` test cases to replicate the bug and verify the fix.
- **Fixer**: Implements the code changes required to resolve the bug.
- **UserProxy**: A proxy agent that initiates the process and can execute code.

## ✨ Features
- **Multi-Agent Collaboration**: Leverages a group chat of specialized agents for a structured approach to bug fixing.
- **Automated Bug Analysis**: Intelligently analyzes bug reports and stack traces.
- **Dynamic Test Generation**: Creates relevant unit and edge-case tests based on the bug.
- **Code Implementation & Review**: Writes the fix and validates it through a review process.
- **Configurable & Extensible**: Easily configure LLM parameters and agent behavior through JSON configuration.

## Project Structure
```
bug-fix-autogen/
├── agents/             # Definitions for each specialized agent
├── config/             # Configuration files (e.g., config.json)
├── utils/              # Helper classes for file handling, code execution
├── workspace/          # Ephemeral directory for code execution and file generation
├── main.py             # Main entry point for the bug-fixing system
├── setup.py            # Project setup and dependencies
└── README.md           # This file
```

## 🚀 Setup Instructions

### 1. Clone the Repo
```bash
git clone bug-fix-autogen.git
cd bug-fix-autogen
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Agent Script
```bash
python quick_start.py
```

> The terminal output from running these commands is stored in `terminal_output.txt`.

## Credits
Developed by **Shobhit Agarwal**.  
Follow on Medium: [https://iamshobhitagarwal.medium.com/](https://iamshobhitagarwal.medium.com/)

If you use this project, please consider citing or sharing feedback.  
Contributions, suggestions, and bug reports are welcome via GitHub issues or pull requests.


