#!/usr/bin/env python3
"""
Quick Start Script for Pizza Customer Service Agent

This script checks all requirements and helps you get started.
"""

import os
import sys
import subprocess
from pathlib import Path


def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def check_python_packages():
    """Check if required Python packages are installed"""
    required = ['langchain', 'ollama', 'chromadb', 'sentence_transformers']
    missing = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    return missing


def check_ollama():
    """Check if Ollama is installed and running"""
    # Check if Ollama is installed
    try:
        result = subprocess.run(['which', 'ollama'], capture_output=True, text=True)
        if result.returncode != 0:
            return False, "not_installed"
    except:
        return False, "not_installed"
    
    # Check if Ollama is running
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            return True, "running"
        else:
            return False, "not_running"
    except subprocess.TimeoutExpired:
        return False, "not_running"
    except:
        return False, "error"


def check_ollama_model(model_name="llama3.2"):
    """Check if the specified model is downloaded"""
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=5)
        if model_name in result.stdout:
            return True
        return False
    except:
        return False


def main():
    """Main function"""
    print_header("Pizza Customer Service Agent - Quick Start")
    
    print("\nChecking requirements...")
    print("-" * 60)
    
    # Check Python packages
    print("\n1. Checking Python packages...")
    missing_packages = check_python_packages()
    if missing_packages:
        print(f"   ✗ Missing packages: {', '.join(missing_packages)}")
        print("\n   To install, run:")
        print("   pip install -r requirements.txt")
        has_packages = False
    else:
        print("   ✓ All Python packages installed")
        has_packages = True
    
    # Check Ollama
    print("\n2. Checking Ollama...")
    ollama_status, ollama_reason = check_ollama()
    if not ollama_status:
        if ollama_reason == "not_installed":
            print("   ✗ Ollama is not installed")
            print("\n   To install Ollama:")
            print("   curl -fsSL https://ollama.com/install.sh | sh")
            print("   Or visit: https://ollama.com")
        elif ollama_reason == "not_running":
            print("   ✗ Ollama is not running")
            print("\n   To start Ollama:")
            print("   ollama serve")
        has_ollama = False
    else:
        print("   ✓ Ollama is running")
        has_ollama = True
    
    # Check model
    print("\n3. Checking AI model...")
    if has_ollama:
        if check_ollama_model("llama3.2"):
            print("   ✓ Model 'llama3.2' is downloaded")
            has_model = True
        else:
            print("   ✗ Model 'llama3.2' not found")
            print("\n   To download the model:")
            print("   ollama pull llama3.2")
            has_model = False
    else:
        print("   ⊘ Skipped (Ollama not running)")
        has_model = False
    
    # Summary
    print("\n" + "=" * 60)
    
    if has_packages and has_ollama and has_model:
        print("✓ All requirements met!")
        print("\nYou can now run the agent:")
        print("  cd workshop")
        print("  python agent.py")
    elif has_packages:
        print("✓ Python packages are installed")
        print("\nYou can run the demo without Ollama:")
        print("  python demo.py --demo          # Show all tools")
        print("  python demo.py --interactive   # Interactive mode")
        
        if not has_ollama or not has_model:
            print("\nTo use the full AI agent, complete the setup above.")
    else:
        print("⚠ Setup incomplete")
        print("\nComplete the steps above to get started.")
    
    print("\nFor detailed instructions, see: README.md")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup check cancelled.\n")
    except Exception as e:
        print(f"\nError: {e}\n")
