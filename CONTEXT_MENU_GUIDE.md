# Windows Context Menu - Visual Guide

This guide shows you how to use the Windows Explorer context menu integration for Git-SVN Merge.

## Installation Preview

### Step 1: Run Installer as Administrator

```
Right-click on: install-context-menu.bat
Select: "Run as administrator"
```

### Step 2: Installer Window

```
============================================================
Git-SVN Merge - Context Menu Installer
============================================================

[OK] Running as Administrator

Installation directory: C:\Tools\git-svn-merge

Checking required files...
[OK] merge_to_svn.py found
[OK] context-menu-handler.ps1 found

[OK] Python is installed
[OK] Git is installed

============================================================
Creating registry entries...
============================================================

Importing registry entries...
[OK] Registry entries created successfully

============================================================
Installation completed successfully!
============================================================

The context menu has been installed.
You can now right-click on any folder and select:
  "Merge Git branch to SVN trunk"

Press any key to continue . . .
```

## Using the Context Menu

### Method 1: Right-Click on Folder

Context Menu Example:
```
┌────────────────────────────────────┐
│ Open                               │
│ ────────────────────────────────   │
│ Git GUI Here                       │
│ Git Bash Here                      │
│ ► Merge Git branch to SVN trunk ◄  │  ← Click this
│ ────────────────────────────────   │
│ Properties                         │
└────────────────────────────────────┘
```

### Validation: Valid Repository

```
[OK] Git repository found
[OK] git-svn repository detected

Starting merge script...
```

### Validation: Not a Git Repository

```
Error: This is not a Git repository!
Press any key to exit...
```

---

**Need Help?** Check the main [README.md](README.md) or open an issue on GitHub.
