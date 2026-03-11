"""
Pizza Customer Service Agent - Main Entry Point

Launches the Gradio web interface.
"""

def main():
    import subprocess
    import sys
    
    print("Launching Pizza Customer Service Agent...")
    print("Opening web interface at http://localhost:7860")
    subprocess.run([sys.executable, "app.py"])


if __name__ == "__main__":
    main()

