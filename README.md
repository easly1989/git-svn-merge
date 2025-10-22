# Git-SVN Branch Merge Automation Script

A powerful Python script that automates the process of merging Git branches into SVN trunk with interactive conflict resolution. This tool streamlines the git-svn workflow, making it easier to manage local Git branches while maintaining synchronization with a central SVN repository.

## If you like my work
Help me pay off my home loan → [Donate on PayPal](https://paypal.me/ruggierocarlo)

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Workflow](#workflow)
- [Conflict Resolution](#conflict-resolution)
- [Command Line Output](#command-line-output)
- [Troubleshooting](#troubleshooting)
- [How It Works](#how-it-works)
- [Contributing](#contributing)
- [License](#license)

## Features

✨ **Automated Workflow**
- Automatically switches branches
- Performs SVN rebase before and after merge
- Commits changes to SVN repository
- Optional branch cleanup after merge

🔍 **Smart Conflict Detection**
- Detects conflicts during merge and rebase operations
- Provides real-time notification of conflicted files
- Shows detailed diff information for each conflict

🛠️ **Interactive Conflict Resolution**

Three different resolution modes:
1. **One-by-one interactive resolution** - Handle each conflict individually with multiple options
2. **Batch resolution with merge tool** - Open all conflicts in your configured merge tool
3. **Manual resolution** - Pause the script and resolve conflicts manually

🎨 **User-Friendly Interface**
- Colored output for better readability
- Clear step-by-step progress indicators
- Comprehensive error messages
- Safety confirmations before critical operations

🔒 **Safety Features**
- Validates Git repository before starting
- Checks for uncommitted changes
- Allows operation cancellation at any point
- Clean abort of merge/rebase on interruption

## Prerequisites

### Required Software

1. **Python 3.8 or higher**
   - Download from [python.org](https://www.python.org/downloads/)
   - Verify installation: `python --version`

2. **Git with SVN support (git-svn)**
   - Git must be installed and configured
   - git-svn extension must be available
   - Verify: `git svn --version`

3. **SVN Repository Configuration**
   - Your repository must be properly configured for git-svn
   - SVN credentials should be set up

### Optional but Recommended

- **TortoiseMerge** or another merge tool for conflict resolution
  - TortoiseMerge path: `C:\Program Files\TortoiseGit\bin\TortoiseGitMerge.exe`
  - Or configure your preferred merge tool: `git config --global merge.tool <your-tool>`

## Installation

> 📋 **Quick Start**: See [INSTALL.md](INSTALL.md) for step-by-step installation instructions.

### Option 1: Global Installation (Recommended)

This allows you to run the script from anywhere on your system.

#### Windows

1. **Download the script**
   ```bash
   # Download to a permanent location
   mkdir C:\Tools
   # Copy merge_to_svn.py to C:\Tools
   ```

2. **Add to PATH**
   - Right-click on "This PC" or "My Computer" → Properties
   - Click "Advanced system settings"
   - Click "Environment Variables"
   - Under "System variables", find and select "Path", then click "Edit"
   - Click "New" and add: `C:\Tools`
   - Click "OK" on all dialogs

3. **Create a batch wrapper (optional, for easier usage)**
   
   Create a file `C:\Tools\merge-svn.bat` with this content:
   ```batch
   @echo off
   python C:\Tools\merge_to_svn.py %*
   ```

4. **Verify installation**
   ```bash
   # Open a new command prompt
   python C:\Tools\merge_to_svn.py --version
   # or if you created the batch file
   merge-svn --version
   ```

#### Linux / macOS

1. **Download the script**
   ```bash
   # Download to a permanent location
   sudo curl -o /usr/local/bin/merge-svn https://raw.githubusercontent.com/yourusername/git-svn-merge-automation/main/merge_to_svn.py
   ```

2. **Make it executable**
   ```bash
   sudo chmod +x /usr/local/bin/merge-svn
   ```

3. **Verify installation**
   ```bash
   merge-svn --version
   ```

### Option 2: Local Installation (Per Repository)

If you prefer to keep the script with each repository:

1. **Copy the script to your repository**
   ```bash
   cd /path/to/your/git-svn-repository
   # Copy merge_to_svn.py here
   ```

2. **Make it executable (Linux/macOS)**
   ```bash
   chmod +x merge_to_svn.py
   ```

3. **Run from repository directory**
   ```bash
   python merge_to_svn.py
   # or
   ./merge_to_svn.py
   ```

### Option 3: Python Package Installation

For advanced users who want to install it as a Python package:

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/git-svn-merge-automation.git
   cd git-svn-merge-automation
   ```

2. **Create a setup.py** (if not already present)
   ```python
   from setuptools import setup
   
   setup(
       name='git-svn-merge',
       version='1.0.0',
       py_modules=['merge_to_svn'],
       entry_points={
           'console_scripts': [
               'merge-svn=merge_to_svn:main',
           ],
       },
   )
   ```

3. **Install**
   ```bash
   pip install .
   # or for development
   pip install -e .
   ```

4. **Run from anywhere**
   ```bash
   merge-svn /path/to/repository
   ```

### Option 4: Windows Context Menu Integration (Windows Only)

Add a right-click menu option to Windows Explorer for quick access.

#### Features
- Right-click on any folder and select "Merge Git branch to SVN trunk"
- Automatically validates that the folder is a git-svn repository
- Shows clear error messages if requirements are not met
- Works from anywhere in Windows Explorer

#### Installation Steps

1. **Download all files** to a permanent location (e.g., `C:\Tools\git-svn-merge`)

2. **Run the installer as Administrator**
   ```batch
   # Right-click on install-context-menu.bat and select "Run as administrator"
   ```

3. **Follow the on-screen prompts**
   - The installer will check for Python and Git
   - It will create the necessary registry entries
   - No manual registry editing required!

4. **Test the installation**
   - Navigate to any git-svn repository folder
   - Right-click on the folder (or inside the folder on empty space)
   - You should see "Merge Git branch to SVN trunk" option

#### Manual Installation (Alternative)

If you prefer to manually install:

1. **Edit `install-context-menu.reg`**
   - Open the file in a text editor
   - Replace `C:\\Tools\\git-svn-merge\\` with your installation path
   - Make sure to use double backslashes (`\\`)

2. **Double-click `install-context-menu.reg`**
   - Click "Yes" when prompted
   - Click "OK" to confirm

#### Uninstallation

To remove the context menu integration:

```batch
# Method 1: Run the uninstaller as Administrator
# Right-click on uninstall-context-menu.bat and select "Run as administrator"

# Method 2: Double-click the registry file
# Double-click uninstall-context-menu.reg
```

#### How It Works

When you right-click and select the menu option:

1. **Validation Phase**
   - Checks if the folder is a Git repository (`.git` folder exists)
   - Verifies git-svn configuration
   - Ensures Python and Git are installed

2. **Execution Phase**
   - If all checks pass, runs the merge script
   - Shows interactive prompts in a console window
   - Waits for you to complete the operation

3. **Error Handling**
   - If the folder is not a git-svn repository, shows a clear error
   - If Python or Git is missing, provides installation instructions
   - Allows cancellation at any point

## Windows Context Menu Integration

You can add a convenient right-click context menu option to Windows Explorer, allowing you to run the script directly on any folder.

### Features

- ✅ Right-click on any folder to merge Git branches to SVN
- ✅ Automatic validation of Git/git-svn repository
- ✅ User-friendly error messages
- ✅ Optional: Show only for git-svn repositories
- ✅ Optional: Show only with Shift+Right-Click to reduce clutter

### Installation Methods

#### Method 1: Automatic Installation (Recommended) ⭐

1. **Run PowerShell as Administrator**
   - Right-click on `install_context_menu.ps1`
   - Select "Run with PowerShell"
   - Or: Open PowerShell as Admin and run:
   ```powershell
   .\install_context_menu.ps1
   ```

2. The script will:
   - ✓ Automatically detect Python installation
   - ✓ Automatically find merge_to_svn.py
   - ✓ Create registry entries
   - ✓ Set up proper icons

#### Method 2: Using Smart Launcher (Most User-Friendly)

This method validates the repository before running the script.

1. **Copy files to installation folder**
   ```
   C:\Tools\git-svn-merge\
   ├── merge_to_svn.py
   └── context_menu_launcher.bat
   ```

2. **Edit `install_context_menu_recommended.reg`**
   - Open the file in a text editor
   - Replace `C:\\Tools\\git-svn-merge\\` with your installation path
   - Use double backslashes: `C:\\My Folder\\`

3. **Install**
   - Double-click `install_context_menu_recommended.reg`
   - Click "Yes" when prompted
   - Click "OK" to confirm

#### Method 3: Manual Registry Installation

1. **Edit `install_context_menu.reg`**
   - Open in a text editor
   - Find line: `@="cmd.exe /c \"cd /d \"%1\" && python C:\\Tools\\...`
   - Replace path with your actual script location
   - Use double backslashes

2. **Install**
   - Double-click the `.reg` file
   - Confirm the registry changes

### Usage

Once installed, you have two ways to access the feature:

#### Option A: Standard Right-Click (if Extended is removed)
1. Right-click on any folder
2. Select "Merge Git Branch to SVN"
3. The script runs in that folder

#### Option B: Shift+Right-Click (if Extended is present - Recommended)
1. Hold **Shift** key
2. Right-click on any folder
3. Select "Merge Git Branch to SVN"
4. The script runs in that folder

### Visual Example

```
📁 my-git-svn-repo/
   └── [Right-Click or Shift+Right-Click]
       └── Context Menu:
           ├── Open
           ├── Open in new window
           ├── ...
           └── Merge Git Branch to SVN  ⭐ (New option)
```

### Configuration Options

You can customize the behavior by editing the registry files:

#### Always Show Menu (Remove Shift Requirement)
Remove this line from the `.reg` file:
```registry
"Extended"=""
```

#### Show Only for Folders with .git
Add this line to the `.reg` file:
```registry
"AppliesTo"="System.ItemPathDisplay:*.git"
```

#### Custom Icon
Change the icon path:
```registry
"Icon"="C:\\Path\\To\\Your\\Icon.ico"
```

### Smart Launcher Features

The `context_menu_launcher.bat` script provides:

1. **Repository Validation**
   - Checks if `.git` folder exists
   - Verifies git-svn configuration
   - Shows clear error messages

2. **Python Check**
   - Verifies Python is installed
   - Shows installation instructions if missing

3. **User Confirmation**
   - Asks before running on non-git-svn repositories
   - Allows cancellation at any point

### Example Error Messages

```batch
[ERROR] This is not a Git repository!

The folder "C:\Projects\my-folder"
does not contain a .git folder.

Please right-click on a Git repository folder.
```

```batch
[WARNING] This appears to be a regular Git repository, not git-svn.

The script is designed for git-svn repositories.
Do you want to continue anyway?

Continue [Y/N]?
```

### Uninstallation

#### Using PowerShell (Automatic)
```powershell
# Run as Administrator
.\uninstall_context_menu.ps1
```

#### Using Registry File
Double-click `uninstall_context_menu.reg`

#### Manual Removal
1. Open Registry Editor (Win+R → `regedit`)
2. Navigate to:
   - `HKEY_CLASSES_ROOT\Directory\shell\GitSvnMerge`
   - `HKEY_CLASSES_ROOT\Directory\Background\shell\GitSvnMerge`
3. Delete these keys

### Troubleshooting

#### "Cannot find script" error
- Verify the script path in the registry
- Use full absolute paths
- Use double backslashes in registry: `C:\\Tools\\script.py`

#### Option doesn't appear in context menu
- Restart Windows Explorer:
  - Open Task Manager (Ctrl+Shift+Esc)
  - Find "Windows Explorer"
  - Right-click → Restart
- Or restart your computer

#### "Access Denied" when installing
- Run PowerShell/Command Prompt as Administrator
- Right-click → "Run as Administrator"

#### Script runs but doesn't work
- Check Python is in PATH: `python --version`
- Verify script location is correct
- Check script has correct permissions

### Files for Context Menu

The following files are provided for context menu integration:

| File | Purpose |
|------|---------|
| `install_context_menu.ps1` | Automatic PowerShell installer (Recommended) |
| `uninstall_context_menu.ps1` | Automatic PowerShell uninstaller |
| `install_context_menu_recommended.reg` | Registry file with smart launcher |
| `install_context_menu.reg` | Basic registry file |
| `install_context_menu_smart.reg` | Advanced registry with conditions |
| `uninstall_context_menu.reg` | Registry file to remove entries |
| `context_menu_launcher.bat` | Smart batch launcher with validation |

### Security Note

Registry files modify your Windows Registry. Always review `.reg` files before running them. The provided files only add context menu entries and don't modify system settings or install software.

## Usage

### Basic Usage

The script can be run in three ways:

#### 1. From within the repository (no arguments)

```bash
cd /path/to/your/git-svn-repository
python merge_to_svn.py
```

#### 2. From anywhere with repository path

```bash
# Using full path
python merge_to_svn.py /path/to/your/git-svn-repository

# Using relative path
python merge_to_svn.py ../my-project

# Windows example
python merge_to_svn.py C:\Users\user\projects\my-repo
```

#### 3. Using global installation (if installed globally)

```bash
# Linux/macOS
merge-svn /path/to/repository

# Windows (with batch wrapper)
merge-svn C:\projects\my-repo

# Or from within repository
cd /path/to/repository
merge-svn
```

### Command Line Options

```bash
# Show help
python merge_to_svn.py --help

# Show version
python merge_to_svn.py --version

# Specify repository path
python merge_to_svn.py [repository_path]
```

### Complete Usage Examples

```bash
# Example 1: Run from current directory
cd ~/projects/my-svn-repo
python merge_to_svn.py

# Example 2: Run from another location
python merge_to_svn.py ~/projects/my-svn-repo

# Example 3: Windows absolute path
python merge_to_svn.py "C:\Users\John\Documents\Projects\MyRepo"

# Example 4: Using installed command
merge-svn ~/projects/my-svn-repo
```

### Interactive Prompts

The script will guide you through the process with interactive prompts:

1. **Select branch to merge**
   ```
   Available branches:
     1. master (current)
     2. feature-login
     3. bugfix-validation
   
   Which branch do you want to merge into trunk? (number or name):
   ```

2. **Specify trunk branch**
   ```
   Trunk branch name (default: master):
   ```

3. **Confirm operation**
   ```
   Operation summary:
     1. SVN Rebase on master
     2. Merge feature-login into master
     3. Final SVN Rebase
     4. SVN DCommit to SVN repository
   
   Do you want to proceed? (y/n):
   ```

### Example Session

```bash
$ python merge_to_svn.py ~/projects/my-repo

ℹ Working in repository: /home/user/projects/my-repo

=== Git Branch → SVN Trunk Merge Script ===
=== With interactive conflict management ===

➜ Verifying we are in a Git repository...
✓ Git repository found

Current branch: master

➜ Checking for uncommitted changes...
✓ No uncommitted changes

Available branches:
  1. master (current)
  2. feature-new-api
  3. bugfix-security

Which branch do you want to merge into trunk? (number or name): 2

Trunk branch name (default: master): 

Operation summary:
  1. SVN Rebase on master
  2. Merge feature-new-api into master
  3. Final SVN Rebase
  4. SVN DCommit to SVN repository

ℹ  The script will automatically handle any conflicts

Do you want to proceed? (y/n): y

➜ Performing SVN Rebase to sync with SVN repository...
✓ SVN Rebase completed successfully

➜ Merging branch feature-new-api...
✓ Branch feature-new-api merged successfully

➜ Performing SVN Rebase to sync with SVN repository...
✓ SVN Rebase completed successfully

➜ Sending changes to SVN repository (SVN DCommit)...
⚠ This operation may take several minutes...
✓ Changes successfully sent to SVN repository!

Do you want to delete the local branch feature-new-api? (y/n): y

➜ Deleting branch feature-new-api...
✓ Branch feature-new-api deleted

✓ Operation completed successfully!
```

### Using Windows Context Menu

If you installed the context menu integration, you can use it like this:

1. **In Windows Explorer, navigate to your git-svn repository folder**

2. **Right-click on the folder** (or right-click inside the folder on empty space)

3. **Select "Merge Git branch to SVN trunk"** from the context menu

   ```
   ┌─────────────────────────────────────┐
   │  Open                               │
   │  Open in new window                 │
   │  ────────────────────────────────   │
   │  Git GUI Here                       │
   │  Git Bash Here                      │
   │  ► Merge Git branch to SVN trunk ◄  │  ← This option
   │  ────────────────────────────────   │
   │  TortoiseGit                        │
   │  Properties                         │
   └─────────────────────────────────────┘
   ```

4. **The script will automatically validate** the repository and run if valid:

   ```
   ============================================================
   Git-SVN Merge - Context Menu Handler
   ============================================================

   Repository path: C:\Users\user\projects\my-repo

   Checking repository...
   [OK] Git repository found
   [OK] git-svn repository detected

   ============================================================
   Starting merge script...
   ============================================================

   [... normal script execution continues ...]
   ```

5. **If the folder is not a git-svn repository**, you'll see:

   ```
   Error: This is not a Git repository!
   The .git folder was not found in: C:\Users\user\projects\my-folder

   Press any key to exit...
   ```

## Workflow

The script follows this precise workflow:

```
1. Validation
   ├─ Check if in Git repository
   ├─ Verify no uncommitted changes
   └─ List available branches

2. Branch Selection
   ├─ Select branch to merge
   ├─ Specify trunk branch (default: master)
   └─ Confirm operation

3. Switch to Trunk
   └─ git checkout <trunk>

4. SVN Rebase (Pre-merge)
   ├─ git svn rebase
   └─ [Handle conflicts if any]

5. Merge Branch
   ├─ git merge --no-ff <branch>
   └─ [Handle conflicts if any]

6. SVN Rebase (Post-merge)
   ├─ git svn rebase
   └─ [Handle conflicts if any]

7. SVN DCommit
   └─ git svn dcommit

8. Cleanup (Optional)
   └─ git branch -d <branch>
```

## Conflict Resolution

### When Conflicts Occur

If conflicts are detected during merge or rebase, the script presents three resolution options:

```
⚠ Found 2 conflicted files!

Conflicted files:
  1. src/main.py
  2. config/settings.ini

Available options:
  1. Resolve conflicts one by one (interactive)
  2. Open all conflicted files with merge tool
  3. Resolve manually and resume later
  4. Cancel operation

Choose an option (1-4):
```

### Option 1: Interactive One-by-One Resolution

Handle each conflict individually with detailed information:

```
============================================================
Conflict 1/2: src/main.py
============================================================

[Shows git diff of the conflict]

Options:
  1. Open with merge tool
  2. Use current version (ours)
  3. Use incoming version (theirs)
  4. Resolve manually and continue
  5. Skip this file (resolve later)

What do you want to do? (1-5):
```

**Sub-options explained:**
- **Option 1**: Opens the file in your configured merge tool (TortoiseMerge or git mergetool)
- **Option 2**: Keeps your current version (`git checkout --ours`)
- **Option 3**: Uses the incoming version (`git checkout --theirs`)
- **Option 4**: Pause, manually edit the file, then continue
- **Option 5**: Skip for now and resolve later

### Option 2: Batch Resolution with Merge Tool

Opens all conflicted files sequentially in your merge tool:
- Processes each file one at a time
- Waits for confirmation after each resolution
- Automatically marks resolved files with `git add`

### Option 3: Manual Resolution

Pauses the script and provides instructions:

```
============================================================
MANUAL CONFLICT RESOLUTION
============================================================

Conflicted files to resolve:
  - src/main.py
  - config/settings.ini

Instructions:
  1. Manually resolve conflicts in the listed files
  2. After resolving, run: git add <resolved-file>
  3. Verify with: git status
  4. Return here and press ENTER to continue

Useful commands:
  git diff --name-only --diff-filter=U    # List conflicted files
  git checkout --ours <file>              # Use current version
  git checkout --theirs <file>            # Use incoming version
  git add <file>                          # Mark as resolved

Press ENTER when you have resolved all conflicts...
```

### Conflict Resolution Workflow

```
Conflict Detected
    ↓
Choose Resolution Mode
    ↓
┌───────────────┬─────────────────┬──────────────────┐
│  Interactive  │  Merge Tool     │  Manual          │
│  (One-by-one) │  (Batch)        │  (Pause script)  │
└───────┬───────┴────────┬────────┴────────┬─────────┘
        ↓                ↓                  ↓
    Resolve          Resolve all       Edit manually
    each file        with tool         + git add
        ↓                ↓                  ↓
        └────────────────┴──────────────────┘
                         ↓
                Verify resolution
                         ↓
                Continue workflow
```

## Command Line Output

The script uses color-coded output for clarity:

- 🔵 **Blue**: Step indicators (what's being done)
- 🟢 **Green**: Success messages
- 🟡 **Yellow**: Warnings and prompts
- 🔴 **Red**: Errors
- 🔷 **Cyan**: Informational messages
- 🟣 **Magenta**: Conflict details

### Output Symbols

- `➜` Step in progress
- `✓` Success
- `✗` Error
- `⚠` Warning
- `ℹ` Information

## Troubleshooting

### Common Issues

#### 1. "Path does not exist" or "Path is not a directory"

**Problem**: The specified path is invalid.

**Solution**:
```bash
# Verify the path exists
ls /path/to/repository  # Linux/macOS
dir C:\path\to\repository  # Windows

# Use absolute paths if relative paths don't work
python merge_to_svn.py /absolute/path/to/repository

# Check current directory
pwd  # Linux/macOS
cd  # Windows
```

#### 2. "Not in a Git repository!"

**Problem**: Script is not running in a Git repository or wrong path specified.

**Solution**:
```bash
# Verify it's a Git repository
cd /path/to/your/repository
git status

# Check if .git folder exists
ls -la  # Linux/macOS
dir /a  # Windows

# Use the correct path
python merge_to_svn.py /correct/path/to/repository
```

#### 3. "Cannot change to directory"

**Problem**: Permission issues or path contains special characters.

**Solution**:
```bash
# Check permissions
ls -ld /path/to/repository  # Linux/macOS

# Use quotes for paths with spaces
python merge_to_svn.py "/path/with spaces/repository"
python merge_to_svn.py "C:\Users\My Name\Projects\My Repo"

# On Windows, use forward slashes or escaped backslashes
python merge_to_svn.py C:/Users/user/projects/repo
python merge_to_svn.py "C:\\Users\\user\\projects\\repo"
```

#### 4. "There are uncommitted changes!"

**Problem**: There are uncommitted changes in the working directory.

**Solution**:
```bash
# Commit your changes
git add .
git commit -m "Your commit message"

# Or stash them temporarily
git stash
# Run the script
python merge_to_svn.py
# Restore changes later
git stash pop
```

#### 5. "git svn rebase failed"

**Problem**: SVN rebase encountered errors.

**Solution**:
- Check your SVN credentials
- Ensure you have network connectivity to SVN server
- Verify git-svn configuration: `git config --get-regexp svn`

#### 6. Merge tool doesn't open

**Problem**: TortoiseMerge or configured merge tool isn't opening.

**Solution**:
```bash
# Check if merge tool is configured
git config --get merge.tool

# Configure a merge tool
git config --global merge.tool <tool-name>

# For TortoiseMerge on Windows
git config --global merge.tool tortoisemerge
git config --global mergetool.tortoisemerge.cmd '"C:/Program Files/TortoiseGit/bin/TortoiseGitMerge.exe" -base:"$BASE" -mine:"$LOCAL" -theirs:"$REMOTE" -merged:"$MERGED"'
```

#### 7. Script interrupted (Ctrl+C)

**Problem**: Script was interrupted during merge/rebase.

**Solution**: The script automatically offers to clean up:
```
Operation interrupted by user.

Do you want to abort the merge in progress? (y/n): y
✓ Merge aborted
```

Or manually:
```bash
# If in merge
git merge --abort

# If in rebase
git rebase --abort
```

### Getting More Information

Enable verbose output by modifying git commands in the script or run git commands manually:

```bash
# Check repository status
git status

# View recent commits
git log --oneline -10

# Check SVN info
git svn info

# View all branches
git branch -a
```

## How It Works

### Technical Details

The script uses Python's `subprocess` module to execute Git commands and parse their output. Here's a breakdown of key functions:

#### Conflict Detection
```python
def get_conflicted_files():
    """Detects files in conflict state"""
    output, code, _ = run_command("git diff --name-only --diff-filter=U", check=False)
    # Returns list of files with unresolved conflicts
```

#### Merge Process
```python
def merge_branch(branch_name, no_ff=True):
    """Performs merge with conflict handling"""
    # 1. Attempt merge
    # 2. If conflicts detected, invoke interactive resolution
    # 3. Complete merge after resolution
```

#### SVN Synchronization
```python
def svn_rebase():
    """Syncs with SVN repository"""
    # 1. Execute git svn rebase
    # 2. Handle conflicts if they occur
    # 3. Verify successful completion
```

### Safety Mechanisms

1. **Pre-flight Checks**: Validates repository state before starting
2. **Atomic Operations**: Each step is verified before proceeding
3. **Rollback Capability**: Can abort operations if issues arise
4. **State Preservation**: Never leaves repository in inconsistent state

### Git-SVN Bridge

The script maintains the bidirectional synchronization between Git and SVN:

```
Local Git Branch
       ↓
   git merge
       ↓
  Git Master ←→ git svn rebase/dcommit ←→ SVN Trunk
```

## Project Structure

```
git-svn-merge-automation/
├── merge_to_svn.py                          # Main Python script
├── merge-svn.bat                            # Windows wrapper script
├── merge-svn.sh                             # Linux/macOS wrapper script
├── setup.py                                 # Python package setup file
├── README.md                                # This file - comprehensive documentation
├── INSTALL.md                               # Quick installation guide
├── .gitignore                               # Git ignore file
├── LICENSE                                  # MIT License file
│
└── Context Menu Integration (Windows):
    ├── install_context_menu.ps1            # Automatic installer (PowerShell)
    ├── uninstall_context_menu.ps1          # Automatic uninstaller (PowerShell)
    ├── install_context_menu_recommended.reg # Smart launcher registry (Recommended)
    ├── install_context_menu.reg            # Basic registry file
    ├── install_context_menu_smart.reg      # Advanced conditional registry
    ├── uninstall_context_menu.reg          # Uninstall registry entries
    └── context_menu_launcher.bat           # Smart validation launcher
```

### File Descriptions

**Core Files:**
- **merge_to_svn.py**: The main Python script that performs all operations
- **merge-svn.bat**: Windows batch file wrapper for easier execution
- **merge-svn.sh**: Unix shell script wrapper for Linux/macOS
- **setup.py**: Allows installation as a Python package with `pip install`

**Documentation:**
- **README.md**: Complete documentation with usage examples and troubleshooting
- **INSTALL.md**: Step-by-step installation instructions for all platforms
- **LICENSE**: MIT License for the project
- **.gitignore**: Git ignore patterns for Python projects

**Windows Context Menu Integration:**
- **install_context_menu.ps1**: Automatic PowerShell script that detects Python and script location, then creates registry entries (Recommended for easy installation)
- **uninstall_context_menu.ps1**: Removes all context menu entries automatically
- **install_context_menu_recommended.reg**: Uses smart launcher for repository validation (Best user experience)
- **install_context_menu.reg**: Basic registry file for simple installation
- **install_context_menu_smart.reg**: Advanced registry with conditional display
- **uninstall_context_menu.reg**: Registry file to remove context menu entries
- **context_menu_launcher.bat**: Validates git-svn repository before launching script
- **.gitignore**: Git ignore patterns for Python projects

**Windows Context Menu Integration:**
- **context-menu-handler.ps1**: PowerShell script that validates repository before running
- **install-context-menu.bat**: Automatic installer (recommended) - run as admin
- **uninstall-context-menu.bat**: Automatic uninstaller - run as admin
- **install-context-menu.reg**: Manual registry installer (alternative method)
- **uninstall-context-menu.reg**: Manual registry uninstaller (alternative method)

## Contributing

Contributions are welcome! Here's how you can help:

### Reporting Issues

If you encounter a bug or have a feature request:

1. Check if the issue already exists
2. Create a new issue with:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - Python version and OS
   - Git and git-svn versions

### Submitting Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Commit with clear messages
6. Push to your fork
7. Create a pull request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add docstrings to new functions
- Maintain backward compatibility
- Update README for new features
- Test on multiple platforms if possible

## License

This project is released under the MIT License.

```
MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## Acknowledgments

- Inspired by the need to simplify git-svn workflows
- Built with Python's standard library for maximum compatibility
- Designed for developers working in hybrid Git-SVN environments

## Support

If you need help or have questions:

- 📖 Check the [Troubleshooting](#troubleshooting) section
- 🐛 Open an [issue](https://github.com/yourusername/git-svn-merge-automation/issues)
- 💬 Start a [discussion](https://github.com/yourusername/git-svn-merge-automation/discussions)

## Roadmap

Future enhancements planned:

- [ ] Configuration file support for default settings
- [ ] Support for multiple trunk branches
- [ ] Integration with more merge tools
- [ ] Dry-run mode for testing
- [ ] Logging to file for audit trails
- [ ] GUI version for non-command-line users

---

**Made with ❤️ for developers stuck in git-svn workflows**

## If you like my work
Help me pay off my home loan → [Donate on PayPal](https://paypal.me/ruggierocarlo)
