#!/usr/bin/env python3
"""
Release preparation script for C-Keeper
Prepares the project for GitHub release
"""

import os
import sys
import subprocess
import json
from datetime import datetime
from pathlib import Path

def run_command(cmd, description=""):
    """Run a command and return the result"""
    print(f"🔧 {description or cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        return None

def check_git_status():
    """Check if there are uncommitted changes"""
    result = run_command("git status --porcelain")
    if result:
        print("⚠️  You have uncommitted changes:")
        print(result)
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            sys.exit(1)

def update_version():
    """Update version information"""
    version_file = Path("VERSION")
    if not version_file.exists():
        version = "1.0.0"
        version_file.write_text(version)
    else:
        version = version_file.read_text().strip()
    
    print(f"📋 Current version: {version}")
    new_version = input(f"Enter new version (current: {version}): ").strip()
    
    if new_version:
        version_file.write_text(new_version)
        print(f"✅ Version updated to: {new_version}")
        return new_version
    return version

def create_release_notes():
    """Create release notes"""
    release_notes = f"""# C-Keeper Release Notes

## Version {update_version()} - {datetime.now().strftime('%Y-%m-%d')}

### 🚀 Features
- Modern GUI Interface (2025 Edition) with enhanced styling
- Enhanced CLI Interface with colorized output
- Docker integration for zero-dependency installation
- One-click deployment scripts for Windows and Linux/macOS
- Comprehensive testing suite

### 🔧 Technical Improvements
- Containerized deployment with Docker
- Automated CI/CD pipeline
- Health checks and error detection
- Cross-platform compatibility
- Persistent data volumes

### 📦 Installation
Choose your preferred method:

#### Docker (Recommended)
```bash
# Windows: double-click quick-start.bat
# Linux/macOS: ./quick-start.sh
```

#### Manual Installation
```bash
git clone https://github.com/jamwal69/C-Keeper.git
cd C-Keeper
pip install -r requirements.txt
python scripts/init_db.py
python ckeeper.py --cli
```

### 🛡️ Security
- Containerized execution environment
- Network isolation
- Non-privileged user execution
- Security scanning in CI/CD

### 📚 Documentation
- Comprehensive installation guide
- Docker deployment instructions
- Platform-specific setup guides
- API documentation

---

For complete installation instructions, see [INSTALLATION.md](INSTALLATION.md)
"""
    
    with open("RELEASE_NOTES.md", "w") as f:
        f.write(release_notes)
    
    print("✅ Release notes created: RELEASE_NOTES.md")

def run_tests():
    """Run comprehensive tests"""
    print("🧪 Running tests...")
    
    # Python syntax check
    result = run_command("python -m py_compile ckeeper.py", "Checking main file syntax")
    if result is None:
        return False
    
    # Run error check
    result = run_command("python error_check.py", "Running error check")
    if result is None:
        return False
    
    # Docker test (if Docker is available)
    if run_command("docker --version") is not None:
        print("🐳 Testing Docker build...")
        result = run_command("docker build -t ckeeper-test .", "Building Docker image")
        if result is not None:
            run_command("docker run --rm ckeeper-test python docker_test.py", "Testing Docker environment")
    
    print("✅ All tests passed!")
    return True

def prepare_git():
    """Prepare Git repository"""
    # Add all files
    run_command("git add .", "Adding all files to Git")
    
    # Show status
    status = run_command("git status --short")
    if status:
        print("📋 Files to be committed:")
        print(status)
        
        response = input("Commit these changes? (Y/n): ")
        if response.lower() != 'n':
            commit_msg = input("Enter commit message (or press Enter for default): ").strip()
            if not commit_msg:
                commit_msg = f"Release preparation - {datetime.now().strftime('%Y-%m-%d')}"
            
            run_command(f'git commit -m "{commit_msg}"', "Committing changes")
            print("✅ Changes committed!")
        else:
            print("⏭️  Skipping commit")
    else:
        print("ℹ️  No changes to commit")

def main():
    """Main release preparation function"""
    print("🚀 C-Keeper Release Preparation")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("ckeeper.py").exists():
        print("❌ Error: Not in C-Keeper project directory")
        sys.exit(1)
    
    # Check Git status
    check_git_status()
    
    # Run tests
    if not run_tests():
        print("❌ Tests failed. Fix issues before release.")
        sys.exit(1)
    
    # Update version and create release notes
    create_release_notes()
    
    # Prepare Git
    prepare_git()
    
    print("\n" + "=" * 50)
    print("🎉 Release preparation complete!")
    print("\nNext steps:")
    print("1. Push to GitHub: git push origin main")
    print("2. Create a new release on GitHub")
    print("3. Upload Docker image to registry (optional)")
    print("4. Update documentation if needed")

if __name__ == "__main__":
    main()
