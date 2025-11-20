#!/usr/bin/env python3
"""
Installation script for Playwright browsers
"""
import subprocess
import sys
import os

def install_playwright_browsers():
    """Install Playwright browsers"""
    try:
        print("Installing Playwright browsers...")
        result = subprocess.run([
            sys.executable, "-m", "playwright", "install"
        ], check=True, capture_output=True, text=True)
        
        print("✅ Playwright browsers installed successfully!")
        print(result.stdout)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing Playwright browsers: {e}")
        print(f"Error output: {e.stderr}")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ Playwright not found. Please install it first:")
        print("pip install playwright")
        sys.exit(1)

def install_system_dependencies():
    """Install system dependencies for Playwright"""
    try:
        print("Installing system dependencies...")
        result = subprocess.run([
            sys.executable, "-m", "playwright", "install-deps"
        ], check=True, capture_output=True, text=True)
        
        print("✅ System dependencies installed successfully!")
        print(result.stdout)
        
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Warning: Could not install system dependencies: {e}")
        print("You may need to install them manually for your system.")
    except FileNotFoundError:
        print("❌ Playwright not found. Please install it first:")
        print("pip install playwright")
        sys.exit(1)

if __name__ == "__main__":
    print("🚀 Setting up Playwright for Roku Movie Automation")
    print("=" * 50)
    
    # Install Playwright browsers
    install_playwright_browsers()
    
    # Install system dependencies
    install_system_dependencies()
    
    print("\n🎉 Setup complete! You can now run the automation:")
    print("python main.py")
