"""
Setup script for Math Motion
Helps users set up the development environment.
"""

import subprocess
import sys
import os
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible."""
    print("Checking Python version...")
    version = sys.version_info
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"✗ Python {version.major}.{version.minor} is not supported (requires 3.8+)")
        return False
    
    print(f"✓ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True


def check_ffmpeg():
    """Check if FFmpeg is installed."""
    print("\nChecking FFmpeg installation...")
    try:
        result = subprocess.run(["ffmpeg", "-version"], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✓ FFmpeg is installed")
            # Extract version
            first_line = result.stdout.split('\n')[0]
            print(f"  {first_line}")
            return True
        else:
            print("✗ FFmpeg is not installed or not in PATH")
            return False
    except FileNotFoundError:
        print("✗ FFmpeg is not found in PATH")
        return False
    except subprocess.TimeoutExpired:
        print("✗ FFmpeg check timed out")
        return False


def install_dependencies():
    """Install Python dependencies."""
    print("\nInstalling Python dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                      check=True)
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install dependencies: {e}")
        return False


def check_manim():
    """Check if Manim is installed."""
    print("\nChecking Manim installation...")
    try:
        result = subprocess.run(["manim", "--version"], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✓ Manim is installed")
            return True
        else:
            print("⚠ Manim might not be properly installed")
            return False
    except FileNotFoundError:
        print("⚠ Manim command not found (may need to install)")
        return False
    except subprocess.TimeoutExpired:
        print("⚠ Manim check timed out")
        return False


def create_directories():
    """Create necessary directories."""
    print("\nCreating project directories...")
    
    directories = [
        "output",
        "projects",
        "assets/music",
        "assets/fonts",
        "assets/textures"
    ]
    
    for directory in directories:
        path = Path(directory)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            print(f"✓ Created {directory}")
        else:
            print(f"  {directory} already exists")


def run_tests():
    """Run basic pipeline tests."""
    print("\nRunning basic pipeline tests...")
    try:
        subprocess.run([sys.executable, "test_pipeline.py"], check=True)
        print("✓ Pipeline tests passed")
        return True
    except subprocess.CalledProcessError:
        print("⚠ Pipeline tests failed (may be due to missing dependencies)")
        return False


def main():
    """Main setup function."""
    print("=" * 60)
    print("Math Motion Setup")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        print("\nPlease install Python 3.8 or higher to continue.")
        return False
    
    # Check FFmpeg
    ffmpeg_ok = check_ffmpeg()
    if not ffmpeg_ok:
        print("\nPlease install FFmpeg:")
        print("  Windows: Download from https://ffmpeg.org/download.html")
        print("  macOS: brew install ffmpeg")
        print("  Linux: sudo apt install ffmpeg")
        print("\nAdd FFmpeg to your system PATH and run this script again.")
        return False
    
    # Install dependencies
    if not install_dependencies():
        print("\nFailed to install dependencies. Please check your internet connection.")
        return False
    
    # Check Manim
    manim_ok = check_manim()
    if not manim_ok:
        print("\nManim might not be installed. Installing...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "manim"], check=True)
            print("✓ Manim installed")
        except subprocess.CalledProcessError:
            print("⚠ Could not install Manim automatically")
    
    # Create directories
    create_directories()
    
    # Run tests
    run_tests()
    
    print("\n" + "=" * 60)
    print("Setup Complete!")
    print("=" * 60)
    print("\nYou can now run Math Motion:")
    print("  python app/main.py")
    print("\nOr test the pipeline:")
    print("  python test_pipeline.py")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
