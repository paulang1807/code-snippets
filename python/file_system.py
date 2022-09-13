"""
Code snippets related to the directory and file structures
"""

import os

# Get current working directory
path = os.getcwd()

# List contents of the current directory
os.listdir(path)

# Check if a subdirectory exist in a given directory
if os.path.exists('.'):
  subpathexists = True

# Go to the parent directory
os.chdir('../')