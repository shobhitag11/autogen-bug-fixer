#!/usr/bin/env python3
"""
Quick Start Script for AutoGen Bug Fixing System
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME')
AZURE_OPENAI_API_VERSION = os.getenv('AZURE_OPENAI_API_VERSION')

def check_environment():
    """Check if environment is properly set up"""
    required_env_vars = [
        'AZURE_OPENAI_API_KEY',
        'AZURE_OPENAI_ENDPOINT',
        'AZURE_OPENAI_DEPLOYMENT_NAME'
    ]
    
    missing_vars = []
    for var in required_env_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease set these in your .env file or environment.")
        return False
    
    print("✅ Environment variables configured correctly!")
    return True

def create_env_template():
    """Create .env template file"""
    template = """# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_API_VERSION=2024-02-15-preview
"""
    
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write(template)
        print("📝 Created .env template file. Please fill in your Azure OpenAI credentials.")
    else:
        print("📁 .env file already exists.")

def run_demo():
    """Run the bug fixing demo"""
    print("🚀 Starting AutoGen Bug Fixing Demo...")
    
    try:
        from main import BugFixingSystem
        
        # Initialize system
        bug_fixer = BugFixingSystem()
        
        # Create sample bug
        sample_file = bug_fixer.create_sample_bug()
        
        # Simple bug report
        bug_report = {
            'file_path': sample_file,
            'error_message': 'ZeroDivisionError: division by zero',
            'test_input': 'divide_numbers(10, 0)',
            'expected_output': 'Should handle division by zero gracefully'
        }
        
        # Fix the bug
        results = bug_fixer.fix_bug(bug_report)
        
        if results['status'] == 'success':
            print("🎉 Bug fixing completed successfully!")
            print("Check the workspace/ directory for results.")
        else:
            print(f"❌ Bug fixing failed: {results['error']}")
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please run: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("AutoGen Multi-Agent Bug Fixing System")
    print("=" * 50)
    
    # # Check if .env exists, create template if not
    # if not os.path.exists('.env'):
    #     create_env_template()
    #     print("\n⚠️  Please configure your .env file with Azure OpenAI credentials before running.")
    #     sys.exit(1)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Run demo
    run_demo()
