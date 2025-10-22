# Quick Installation Guide

This guide will help you install the Git-SVN Merge Automation Script globally on your system.

## Windows Installation

### Quick Method (Recommended)

1. **Download all files** to a permanent location (e.g., `C:\Tools\git-svn-merge`)

2. **Add to PATH**:
   ```batch
   # Run as Administrator in PowerShell
   $path = [Environment]::GetEnvironmentVariable("Path", "Machine")
   $path += ";C:\Tools\git-svn-merge"
   [Environment]::SetEnvironmentVariable("Path", $path, "Machine")
   ```

3. **Verify installation**:
   ```batch
   # Close and reopen Command Prompt/PowerShell
   merge-svn --version
   ```

### Manual Method

1. Download files to `C:\Tools\git-svn-merge`
2. Right-click "This PC" → Properties → Advanced system settings
3. Environment Variables → System variables → Path → Edit
4. Add new entry: `C:\Tools\git-svn-merge`
5. Click OK on all dialogs
6. Open new Command Prompt and test: `merge-svn --version`

## Linux / macOS Installation

### Quick Method (Recommended)

```bash
# Download the files (adjust URL to your repository)
sudo mkdir -p /usr/local/bin
sudo curl -o /usr/local/bin/merge-svn https://raw.githubusercontent.com/yourusername/git-svn-merge-automation/main/merge-svn.sh
sudo curl -o /usr/local/bin/merge_to_svn.py https://raw.githubusercontent.com/yourusername/git-svn-merge-automation/main/merge_to_svn.py

# Make executable
sudo chmod +x /usr/local/bin/merge-svn
sudo chmod +x /usr/local/bin/merge_to_svn.py

# Verify installation
merge-svn --version
```

### Alternative: Clone Repository

```bash
# Clone the repository
git clone https://github.com/yourusername/git-svn-merge-automation.git
cd git-svn-merge-automation

# Create symbolic links
sudo ln -s "$(pwd)/merge-svn.sh" /usr/local/bin/merge-svn
sudo ln -s "$(pwd)/merge_to_svn.py" /usr/local/bin/merge_to_svn.py

# Make executable
chmod +x merge-svn.sh merge_to_svn.py

# Verify installation
merge-svn --version
```

## Python Package Installation

For users who prefer pip installation:

```bash
# From repository directory
pip install .

# Or install directly from git (when published)
pip install git+https://github.com/yourusername/git-svn-merge-automation.git

# Or for development
pip install -e .
```

Then use:
```bash
merge-svn /path/to/repository
```

## Verification

After installation, verify it works:

```bash
# Show help
merge-svn --help

# Show version
merge-svn --version

# Test with a repository
merge-svn /path/to/your/git-svn-repo
```

## Troubleshooting

### "Command not found" (Linux/macOS)
- Check if `/usr/local/bin` is in your PATH: `echo $PATH`
- Try restarting your terminal
- Check file permissions: `ls -l /usr/local/bin/merge-svn`

### "Python not found" (Windows)
- Install Python from https://www.python.org/downloads/
- During installation, check "Add Python to PATH"
- Restart Command Prompt after installation

### "Permission denied" (Linux/macOS)
- Use `sudo` for commands that require root access
- Check script permissions: `chmod +x merge-svn.sh`

## Uninstallation

### Windows
1. Remove `C:\Tools\git-svn-merge` folder
2. Remove the path from Environment Variables

### Linux/macOS
```bash
sudo rm /usr/local/bin/merge-svn
sudo rm /usr/local/bin/merge_to_svn.py
```

### Python Package
```bash
pip uninstall git-svn-merge
```

## Windows Context Menu Integration

### Installation

**Automatic Method (Recommended):**

1. Download all files to `C:\Tools\git-svn-merge` (or your preferred location)

2. Right-click on `install-context-menu.bat` and select **"Run as administrator"**

3. Follow the on-screen prompts

4. Test by right-clicking on any git-svn repository folder

**Manual Method:**

1. Edit `install-context-menu.reg` and update the path to match your installation

2. Double-click `install-context-menu.reg` and click "Yes" to add to registry

### Uninstallation

**Automatic Method:**

Right-click on `uninstall-context-menu.bat` and select **"Run as administrator"**

**Manual Method:**

Double-click `uninstall-context-menu.reg` and click "Yes"

### How It Works

The context menu integration adds a "Merge Git branch to SVN trunk" option when you:
- Right-click on a folder in Windows Explorer
- Right-click on empty space inside a folder

Before running the script, it automatically:
- ✓ Checks if the folder is a Git repository
- ✓ Verifies it's a git-svn repository
- ✓ Ensures Python and Git are installed
- ✗ Shows clear error messages if requirements are not met

### Troubleshooting Context Menu

**"Context menu option doesn't appear"**
- Run the installer as Administrator
- Check if the registry entries were created: Open Registry Editor and navigate to `HKEY_CLASSES_ROOT\Directory\shell\GitSvnMerge`
- Try logging out and back in to Windows

**"Script not found" error**
- Verify the installation path is correct in the registry entries
- Ensure `merge_to_svn.py` and `context-menu-handler.ps1` are in the same folder
- Check that the path in the registry uses double backslashes (`\\`)

**"Access denied" when installing**
- Make sure you run the installer as Administrator
- Check if your user has permissions to modify the registry

**"Python not found" error**
- Install Python from https://www.python.org/downloads/
- During installation, check "Add Python to PATH"
- Restart your terminal/Explorer after installation

## Getting Help

If you encounter issues:
- Check the main [README.md](README.md) for detailed documentation
- Open an issue on GitHub
- Check the [Troubleshooting](README.md#troubleshooting) section
