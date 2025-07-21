from setuptools import setup, find_packages

setup(
    name="autogen-bug-fixer",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pyautogen>=0.2.16",
        "openai>=1.6.1",
        "python-dotenv>=1.0.0",
        "docker>=7.0.0",
        "gitpython>=3.1.40",
        "autopep8>=2.0.4",
        "flake8>=6.1.0",
        "pytest>=7.4.3",
        "black>=23.12.1"
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="AutoGen Multi-Agent Bug Fixing System",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/shobhitag11/autogen-bug-fixer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
