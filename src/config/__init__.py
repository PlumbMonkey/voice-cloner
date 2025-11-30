"""
Configuration file initialization
"""
import os
from pathlib import Path

# Create .env from .env.example if it doesn't exist
env_file = Path(".env")
env_example = Path(".env.example")

if not env_file.exists() and env_example.exists():
    with open(env_example, "r") as f:
        content = f.read()
    with open(env_file, "w") as f:
        f.write(content)
    print("✓ Created .env from .env.example")
else:
    print("✓ .env configuration file exists")
