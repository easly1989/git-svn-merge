# Project Files Manifest

Complete list of all files included in the Git-SVN Merge Automation project.

## Core Files (Required)

### merge_to_svn.py
- **Type**: Python Script
- **Purpose**: Main script that performs the merge operations
- **Required**: Yes
- **Platform**: All (Windows, Linux, macOS)
- **Dependencies**: Python 3.8+, Git, git-svn

### merge-svn.bat
- **Type**: Windows Batch File
- **Purpose**: Wrapper script for Windows to make execution easier
- **Required**: No (optional convenience)
- **Platform**: Windows only
- **Usage**: `merge-svn.bat C:\path\to\repo`

### merge-svn.sh
- **Type**: Shell Script
- **Purpose**: Wrapper script for Linux/macOS to make execution easier
- **Required**: No (optional convenience)
- **Platform**: Linux, macOS
- **Usage**: `./merge-svn.sh /path/to/repo`
- **Note**: Make executable with `chmod +x merge-svn.sh`

## Documentation Files

### README.md
- **Type**: Markdown Documentation
- **Purpose**: Complete project documentation
- **Contents**:
  - Feature overview
  - Installation instructions (4 methods)
  - Usage examples
  - Conflict resolution guide
  - Troubleshooting
  - Contributing guidelines

### INSTALL.md
- **Type**: Markdown Documentation
- **Purpose**: Quick installation guide with step-by-step instructions
- **Contents**:
  - Platform-specific installation
  - Copy-paste ready commands
  - Verification steps
  - Troubleshooting tips

### CONTEXT_MENU_GUIDE.md
- **Type**: Markdown Documentation
- **Purpose**: Visual guide for Windows context menu integration
- **Contents**:
  - Installation screenshots/mockups
  - Usage examples
  - Validation scenarios
  - Customization tips

### LICENSE
- **Type**: Text File
- **Purpose**: MIT License for the project
- **Important**: Keep this file if you redistribute the software

## Windows Context Menu Integration Files

### context-menu-handler.ps1
- **Type**: PowerShell Script
- **Purpose**: Validates repository before running merge script
- **Required**: Yes (for context menu integration)
- **Platform**: Windows only
- **What it does**:
  - Checks if folder is a Git repository
  - Verifies git-svn configuration
  - Ensures Python and Git are installed
  - Runs merge script if all checks pass

### install-context-menu.bat
- **Type**: Windows Batch Installer
- **Purpose**: Automatically installs context menu integration
- **Required**: Yes (for context menu installation)
- **Platform**: Windows only
- **Usage**: Right-click → "Run as administrator"
- **Recommended**: Use this instead of manual registry editing

### uninstall-context-menu.bat
- **Type**: Windows Batch Uninstaller
- **Purpose**: Removes context menu integration
- **Required**: Yes (for context menu removal)
- **Platform**: Windows only
- **Usage**: Right-click → "Run as administrator"

### install-context-menu.reg
- **Type**: Windows Registry File
- **Purpose**: Manual registry installation (alternative method)
- **Required**: No (use .bat installer instead)
- **Platform**: Windows only
- **Usage**: Double-click after editing paths
- **Note**: Must edit file to update installation paths

### uninstall-context-menu.reg
- **Type**: Windows Registry File
- **Purpose**: Manual registry uninstallation (alternative method)
- **Required**: No (use .bat uninstaller instead)
- **Platform**: Windows only
- **Usage**: Double-click to remove registry entries

## Python Package Files

### setup.py
- **Type**: Python Setup Script
- **Purpose**: Allows installation as Python package
- **Required**: No (only for pip installation method)
- **Platform**: All
- **Usage**: `pip install .`
- **Creates**: Global command `merge-svn`

### .gitignore
- **Type**: Git Configuration
- **Purpose**: Specifies files/folders to ignore in version control
- **Required**: No (only if using Git for this project)
- **Platform**: All
- **Contains**: Python-specific ignore patterns

## Installation Matrix

| Method | Required Files | Platform | Complexity |
|--------|---------------|----------|------------|
| **Direct Script** | merge_to_svn.py | All | Low |
| **Wrapper Script** | merge_to_svn.py + merge-svn.bat/.sh | All | Low |
| **Global PATH** | merge_to_svn.py + wrapper | All | Medium |
| **Context Menu** | merge_to_svn.py + context-menu-handler.ps1 + installer | Windows | Medium |
| **Pip Package** | All + setup.py | All | Low |

## Minimal Installation

**Absolute minimum to run the script:**
```
merge_to_svn.py
```

**Recommended for Windows:**
```
merge_to_svn.py
merge-svn.bat
```

**Recommended for Linux/macOS:**
```
merge_to_svn.py
merge-svn.sh
```

**Full Windows installation with context menu:**
```
merge_to_svn.py
merge-svn.bat
context-menu-handler.ps1
install-context-menu.bat
uninstall-context-menu.bat
README.md
INSTALL.md
```

## File Sizes (Approximate)

| File | Size |
|------|------|
| merge_to_svn.py | ~20 KB |
| context-menu-handler.ps1 | ~6 KB |
| install-context-menu.bat | ~4 KB |
| uninstall-context-menu.bat | ~2 KB |
| install-context-menu.reg | ~1 KB |
| uninstall-context-menu.reg | ~0.5 KB |
| merge-svn.bat | ~1 KB |
| merge-svn.sh | ~0.5 KB |
| setup.py | ~2 KB |
| README.md | ~50 KB |
| INSTALL.md | ~15 KB |
| CONTEXT_MENU_GUIDE.md | ~10 KB |
| LICENSE | ~1 KB |
| .gitignore | ~1 KB |
| **Total** | **~114 KB** |

## Download Recommendations

### For End Users (Just want to use it)
Download:
- merge_to_svn.py
- merge-svn.bat (Windows) or merge-svn.sh (Linux/macOS)
- README.md
- INSTALL.md

### For Windows Users (Want context menu)
Download:
- merge_to_svn.py
- merge-svn.bat
- context-menu-handler.ps1
- install-context-menu.bat
- uninstall-context-menu.bat
- README.md
- INSTALL.md
- CONTEXT_MENU_GUIDE.md

### For Developers (Want to contribute)
Download or clone entire repository:
```bash
git clone https://github.com/yourusername/git-svn-merge-automation.git
```

### For Python Package Users
Only need repository for pip install:
```bash
pip install git+https://github.com/yourusername/git-svn-merge-automation.git
```

## File Dependencies

```
merge_to_svn.py (standalone)

merge-svn.bat
└── requires: merge_to_svn.py

merge-svn.sh
└── requires: merge_to_svn.py

context-menu-handler.ps1
└── requires: merge_to_svn.py

install-context-menu.bat
└── creates registry entries for: context-menu-handler.ps1

setup.py
└── installs: merge_to_svn.py
```

## Version Control

If you want to fork or modify this project:

**Include in Git:**
- ✅ All .py files
- ✅ All .ps1 files
- ✅ All .bat files
- ✅ All .sh files
- ✅ All .md files
- ✅ LICENSE
- ✅ .gitignore
- ✅ setup.py

**Exclude from Git (already in .gitignore):**
- ❌ __pycache__/
- ❌ *.pyc
- ❌ .vscode/
- ❌ .idea/
- ❌ dist/
- ❌ build/
- ❌ *.egg-info/

## Checksums

For security verification, you can generate checksums:

```bash
# Windows (PowerShell)
Get-FileHash merge_to_svn.py -Algorithm SHA256

# Linux/macOS
sha256sum merge_to_svn.py
```

Keep these checksums to verify file integrity after download.

---

**Last Updated**: October 2024  
**Project Version**: 1.0.0  
**Total Files**: 14
