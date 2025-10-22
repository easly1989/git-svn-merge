#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to automate merging a local Git branch into SVN trunk
using TortoiseGit/Git from command line.
Version with interactive conflict management.

Usage:
    merge_to_svn.py [repository_path]
    
    repository_path: Optional path to the git-svn repository.
                     If not provided, uses the current directory.
                     
Examples:
    merge_to_svn.py
    merge_to_svn.py /path/to/repository
    merge_to_svn.py C:\\Users\\user\\projects\\my-repo
"""

import subprocess
import sys
import os
import time
import argparse
from pathlib import Path

class Colors:
    """Colors for terminal output"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_step(message):
    """Print a step message"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}➜ {message}{Colors.END}")

def print_success(message):
    """Print a success message"""
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")

def print_error(message):
    """Print an error message"""
    print(f"{Colors.RED}✗ {message}{Colors.END}")

def print_warning(message):
    """Print a warning message"""
    print(f"{Colors.YELLOW}⚠ {message}{Colors.END}")

def print_info(message):
    """Print an informational message"""
    print(f"{Colors.CYAN}ℹ {message}{Colors.END}")

def run_command(command, error_message="Error executing command", check=True):
    """Execute a command and handle errors"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=check,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        return result.stdout, result.returncode, result.stderr
    except subprocess.CalledProcessError as e:
        if check:
            print_error(f"{error_message}")
            print(f"Command: {command}")
            print(f"Output: {e.stdout}")
            print(f"Error: {e.stderr}")
        return e.stdout, e.returncode, e.stderr

def check_git_repo():
    """Verify we are in a Git repository"""
    print_step("Verifying we are in a Git repository...")
    output, code, _ = run_command("git rev-parse --is-inside-work-tree")
    if code != 0 or output is None:
        print_error("Not in a Git repository!")
        return False
    print_success("Git repository found")
    return True

def get_current_branch():
    """Get the name of the current branch"""
    output, code, _ = run_command("git branch --show-current")
    if code == 0 and output:
        return output.strip()
    return None

def check_uncommitted_changes():
    """Check if there are uncommitted changes"""
    print_step("Checking for uncommitted changes...")
    output, code, _ = run_command("git status --porcelain")
    if output and output.strip():
        print_error("There are uncommitted changes!")
        print("Commit or stash your changes before continuing.")
        return False
    print_success("No uncommitted changes")
    return True

def get_conflicted_files():
    """Get the list of conflicted files"""
    output, code, _ = run_command("git diff --name-only --diff-filter=U", check=False)
    if code == 0 and output:
        files = [f.strip() for f in output.strip().split('\n') if f.strip()]
        return files
    return []

def check_merge_in_progress():
    """Check if there is a merge in progress"""
    git_dir = Path(".git")
    return (git_dir / "MERGE_HEAD").exists()

def check_rebase_in_progress():
    """Check if there is a rebase in progress"""
    git_dir = Path(".git")
    return (git_dir / "rebase-merge").exists() or (git_dir / "rebase-apply").exists()

def show_conflict_details(file_path):
    """Show details of a conflict"""
    print(f"\n{Colors.MAGENTA}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}Conflicted file: {file_path}{Colors.END}")
    print(f"{Colors.MAGENTA}{'='*60}{Colors.END}")
    
    # Show conflict status
    output, _, _ = run_command(f"git diff {file_path}", check=False)
    if output:
        print(output)
    
def open_merge_tool(file_path):
    """Open merge tool to resolve conflict"""
    print_info(f"Opening merge tool for {file_path}...")
    
    # Try to open TortoiseMerge if available
    tortoise_merge = r"C:\Program Files\TortoiseGit\bin\TortoiseGitMerge.exe"
    if os.path.exists(tortoise_merge):
        # TortoiseMerge with parameters for git
        _, code, _ = run_command(
            f'"{tortoise_merge}" -base:"%cd%\\{file_path}" -mine:"%cd%\\{file_path}" -theirs:"%cd%\\{file_path}"',
            check=False
        )
    else:
        # Use the merge tool configured in git
        _, code, _ = run_command(f"git mergetool {file_path}", check=False)
    
    return code == 0

def resolve_conflicts_interactively():
    """Handle interactive conflict resolution"""
    conflicted_files = get_conflicted_files()
    
    if not conflicted_files:
        return True
    
    print_warning(f"\n⚠ Found {len(conflicted_files)} conflicted files!")
    print("\nConflicted files:")
    for i, file in enumerate(conflicted_files, 1):
        print(f"  {i}. {file}")
    
    print(f"\n{Colors.BOLD}Available options:{Colors.END}")
    print("  1. Resolve conflicts one by one (interactive)")
    print("  2. Open all conflicted files with merge tool")
    print("  3. Resolve manually and resume later")
    print("  4. Cancel operation")
    
    choice = input(f"\n{Colors.YELLOW}Choose an option (1-4): {Colors.END}").strip()
    
    if choice == "1":
        return resolve_conflicts_one_by_one(conflicted_files)
    elif choice == "2":
        return resolve_all_conflicts_with_tool(conflicted_files)
    elif choice == "3":
        return manual_conflict_resolution(conflicted_files)
    elif choice == "4":
        print_warning("\nCanceling operation...")
        if check_merge_in_progress():
            run_command("git merge --abort", check=False)
        if check_rebase_in_progress():
            run_command("git rebase --abort", check=False)
        return False
    else:
        print_error("Invalid option!")
        return resolve_conflicts_interactively()

def resolve_conflicts_one_by_one(conflicted_files):
    """Resolve conflicts one at a time"""
    for i, file in enumerate(conflicted_files, 1):
        print(f"\n{Colors.CYAN}{'='*60}{Colors.END}")
        print(f"{Colors.BOLD}Conflict {i}/{len(conflicted_files)}: {file}{Colors.END}")
        print(f"{Colors.CYAN}{'='*60}{Colors.END}")
        
        show_conflict_details(file)
        
        print(f"\n{Colors.BOLD}Options:{Colors.END}")
        print("  1. Open with merge tool")
        print("  2. Use current version (ours)")
        print("  3. Use incoming version (theirs)")
        print("  4. Resolve manually and continue")
        print("  5. Skip this file (resolve later)")
        
        choice = input(f"\n{Colors.YELLOW}What do you want to do? (1-5): {Colors.END}").strip()
        
        if choice == "1":
            open_merge_tool(file)
            if confirm(f"Have you resolved the conflict in {file}?"):
                run_command(f"git add {file}")
                print_success(f"File {file} marked as resolved")
            else:
                print_warning(f"File {file} left in conflict")
        
        elif choice == "2":
            run_command(f"git checkout --ours {file}")
            run_command(f"git add {file}")
            print_success(f"Used 'ours' version for {file}")
        
        elif choice == "3":
            run_command(f"git checkout --theirs {file}")
            run_command(f"git add {file}")
            print_success(f"Used 'theirs' version for {file}")
        
        elif choice == "4":
            print_info(f"Manually resolve file {file}")
            input(f"{Colors.YELLOW}Press ENTER when finished...{Colors.END}")
            if confirm(f"Have you resolved the conflict in {file}?"):
                run_command(f"git add {file}")
                print_success(f"File {file} marked as resolved")
        
        elif choice == "5":
            print_warning(f"File {file} skipped")
            continue
    
    # Check if there are still conflicts
    remaining_conflicts = get_conflicted_files()
    if remaining_conflicts:
        print_warning(f"\nThere are still {len(remaining_conflicts)} conflicted files:")
        for file in remaining_conflicts:
            print(f"  - {file}")
        
        if confirm("\nDo you want to continue resolving them?"):
            return resolve_conflicts_one_by_one(remaining_conflicts)
        else:
            return manual_conflict_resolution(remaining_conflicts)
    
    return True

def resolve_all_conflicts_with_tool(conflicted_files):
    """Open all conflicted files with merge tool"""
    print_info("Opening merge tool for all conflicted files...")
    
    for file in conflicted_files:
        print(f"\nOpening {file}...")
        open_merge_tool(file)
        if confirm(f"Have you resolved the conflict in {file}?"):
            run_command(f"git add {file}")
            print_success(f"File {file} marked as resolved")
    
    # Check if there are still conflicts
    remaining_conflicts = get_conflicted_files()
    if remaining_conflicts:
        print_warning(f"\nThere are still {len(remaining_conflicts)} conflicted files")
        return resolve_conflicts_interactively()
    
    return True

def manual_conflict_resolution(conflicted_files):
    """Allow manual resolution and pause the script"""
    print(f"\n{Colors.YELLOW}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}MANUAL CONFLICT RESOLUTION{Colors.END}")
    print(f"{Colors.YELLOW}{'='*60}{Colors.END}")
    
    print("\nConflicted files to resolve:")
    for file in conflicted_files:
        print(f"  - {file}")
    
    print(f"\n{Colors.BOLD}Instructions:{Colors.END}")
    print("  1. Manually resolve conflicts in the listed files")
    print("  2. After resolving, run: git add <resolved-file>")
    print("  3. Verify with: git status")
    print("  4. Return here and press ENTER to continue")
    
    print(f"\n{Colors.CYAN}Useful commands:{Colors.END}")
    print("  git diff --name-only --diff-filter=U    # List conflicted files")
    print("  git checkout --ours <file>              # Use current version")
    print("  git checkout --theirs <file>            # Use incoming version")
    print("  git add <file>                          # Mark as resolved")
    
    input(f"\n{Colors.YELLOW}Press ENTER when you have resolved all conflicts...{Colors.END}")
    
    # Check if there are still conflicts
    remaining_conflicts = get_conflicted_files()
    if remaining_conflicts:
        print_error(f"\nThere are still {len(remaining_conflicts)} conflicted files:")
        for file in remaining_conflicts:
            print(f"  - {file}")
        
        if confirm("\nDo you want to resolve them interactively?"):
            return resolve_conflicts_interactively()
        else:
            print_error("Cannot continue with unresolved conflicts")
            return False
    
    print_success("All conflicts have been resolved!")
    return True

def complete_merge_or_rebase():
    """Complete a merge or rebase after conflict resolution"""
    if check_merge_in_progress():
        print_step("Completing merge...")
        output, code, _ = run_command("git commit --no-edit", check=False)
        if code != 0:
            # Try with a commit message
            output, code, _ = run_command('git commit -m "Merge completed after conflict resolution"', check=False)
        
        if code == 0:
            print_success("Merge completed")
            return True
        else:
            print_error("Error completing merge")
            return False
    
    elif check_rebase_in_progress():
        print_step("Completing rebase...")
        output, code, stderr = run_command("git rebase --continue", check=False)
        if code == 0:
            print_success("Rebase completed")
            return True
        else:
            # May need more steps
            if "conflict" in stderr.lower() or "conflict" in output.lower():
                print_warning("There are more conflicts to resolve in the rebase")
                return resolve_conflicts_interactively() and complete_merge_or_rebase()
            else:
                print_error("Error completing rebase")
                return False
    
    return True

def list_branches():
    """List all local branches"""
    output, code, _ = run_command("git branch")
    if code == 0 and output:
        branches = [b.strip().replace('* ', '') for b in output.strip().split('\n')]
        return branches
    return []

def switch_to_branch(branch_name):
    """Switch branch"""
    print_step(f"Switching to branch {branch_name}...")
    output, code, _ = run_command(
        f"git checkout {branch_name}",
        f"Error switching to branch {branch_name}"
    )
    if code != 0:
        return False
    print_success(f"Switched to branch {branch_name}")
    return True

def svn_rebase():
    """Perform SVN rebase with conflict handling"""
    print_step("Performing SVN Rebase to sync with SVN repository...")
    output, code, stderr = run_command("git svn rebase", check=False)
    
    if code != 0:
        # Check if there are conflicts
        conflicted_files = get_conflicted_files()
        if conflicted_files:
            print_warning("SVN Rebase generated conflicts!")
            if resolve_conflicts_interactively():
                # Complete the rebase
                return complete_merge_or_rebase()
            else:
                print_error("Cannot complete rebase")
                return False
        else:
            print_error("SVN Rebase failed!")
            print(f"Output: {output}")
            print(f"Error: {stderr}")
            return False
    
    print_success("SVN Rebase completed successfully")
    return True

def merge_branch(branch_name, no_ff=True):
    """Merge a branch into the current branch with conflict handling"""
    print_step(f"Merging branch {branch_name}...")
    no_ff_flag = "--no-ff" if no_ff else ""
    output, code, stderr = run_command(
        f"git merge {no_ff_flag} {branch_name} -m \"Merge branch '{branch_name}' into trunk\"",
        check=False
    )
    
    if code != 0:
        # Check if there are conflicts
        conflicted_files = get_conflicted_files()
        if conflicted_files:
            print_warning("Merge generated conflicts!")
            if resolve_conflicts_interactively():
                # Complete the merge
                return complete_merge_or_rebase()
            else:
                print_error("Cannot complete merge")
                run_command("git merge --abort", check=False)
                return False
        else:
            print_error(f"Merge failed!")
            print(f"Output: {output}")
            print(f"Error: {stderr}")
            return False
    
    print_success(f"Branch {branch_name} merged successfully")
    return True

def svn_dcommit():
    """Perform SVN dcommit to send changes to SVN"""
    print_step("Sending changes to SVN repository (SVN DCommit)...")
    print_warning("This operation may take several minutes...")
    output, code, _ = run_command(
        "git svn dcommit",
        "Error during SVN DCommit"
    )
    if code != 0:
        print_error("SVN DCommit failed!")
        return False
    print_success("Changes successfully sent to SVN repository!")
    return True

def confirm(message):
    """Ask for user confirmation"""
    response = input(f"{Colors.YELLOW}{message} (y/n): {Colors.END}").lower()
    return response in ['y', 'yes']

def main():
    """Main function"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Automate Git branch merge into SVN trunk with interactive conflict resolution',
        epilog='Example: merge_to_svn.py /path/to/repository'
    )
    parser.add_argument(
        'repository_path',
        nargs='?',
        default='.',
        help='Path to the git-svn repository (default: current directory)'
    )
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )
    
    args = parser.parse_args()
    
    # Convert to absolute path
    repo_path = Path(args.repository_path).resolve()
    
    # Check if path exists
    if not repo_path.exists():
        print_error(f"Path does not exist: {repo_path}")
        sys.exit(1)
    
    # Check if it's a directory
    if not repo_path.is_dir():
        print_error(f"Path is not a directory: {repo_path}")
        sys.exit(1)
    
    # Change to repository directory
    try:
        os.chdir(repo_path)
        print_info(f"Working in repository: {repo_path}")
    except Exception as e:
        print_error(f"Cannot change to directory {repo_path}: {e}")
        sys.exit(1)
    
    print(f"\n{Colors.BOLD}=== Git Branch → SVN Trunk Merge Script ==={Colors.END}")
    print(f"{Colors.BOLD}=== With interactive conflict management ==={Colors.END}\n")
    
    # Verify Git repository
    if not check_git_repo():
        sys.exit(1)
    
    # Get current branch
    current_branch = get_current_branch()
    print(f"Current branch: {Colors.BOLD}{current_branch}{Colors.END}")
    
    # Check for uncommitted changes
    if not check_uncommitted_changes():
        sys.exit(1)
    
    # Get branch list
    branches = list_branches()
    if not branches:
        print_error("No branches found!")
        sys.exit(1)
    
    # Ask which branch to merge
    print(f"\n{Colors.BOLD}Available branches:{Colors.END}")
    for i, branch in enumerate(branches, 1):
        marker = " (current)" if branch == current_branch else ""
        print(f"  {i}. {branch}{marker}")
    
    # Input branch to merge
    branch_to_merge = None
    while not branch_to_merge:
        try:
            choice = input(f"\n{Colors.YELLOW}Which branch do you want to merge into trunk? (number or name): {Colors.END}").strip()
            
            # Check if it's a number
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(branches):
                    branch_to_merge = branches[idx]
                else:
                    print_error("Invalid number!")
            # Check if it's a branch name
            elif choice in branches:
                branch_to_merge = choice
            else:
                print_error("Branch not found!")
        except (ValueError, KeyError):
            print_error("Invalid input!")
    
    # Ask for trunk name
    trunk_branch = input(f"\n{Colors.YELLOW}Trunk branch name (default: master): {Colors.END}").strip() or "master"
    
    # Verify trunk exists
    if trunk_branch not in branches:
        print_error(f"Branch {trunk_branch} does not exist!")
        sys.exit(1)
    
    # If we're already on the branch to merge, switch to trunk first
    if current_branch == branch_to_merge:
        print_warning(f"You are currently on branch {branch_to_merge}")
        if not switch_to_branch(trunk_branch):
            sys.exit(1)
    # If we're not on trunk, switch to trunk
    elif current_branch != trunk_branch:
        if not switch_to_branch(trunk_branch):
            sys.exit(1)
    
    # Summary
    print(f"\n{Colors.BOLD}Operation summary:{Colors.END}")
    print(f"  1. SVN Rebase on {trunk_branch}")
    print(f"  2. Merge {branch_to_merge} into {trunk_branch}")
    print(f"  3. Final SVN Rebase")
    print(f"  4. SVN DCommit to SVN repository")
    print(f"\n{Colors.CYAN}ℹ  The script will automatically handle any conflicts{Colors.END}")
    
    if not confirm("\nDo you want to proceed?"):
        print("\nOperation canceled.")
        sys.exit(0)
    
    # Step 1: SVN Rebase on trunk
    if not svn_rebase():
        sys.exit(1)
    
    # Step 2: Merge branch
    if not merge_branch(branch_to_merge):
        sys.exit(1)
    
    # Step 3: Final SVN Rebase
    if not svn_rebase():
        sys.exit(1)
    
    # Step 4: SVN DCommit
    if not svn_dcommit():
        sys.exit(1)
    
    # Option to delete branch
    print()
    if confirm(f"Do you want to delete the local branch {branch_to_merge}?"):
        print_step(f"Deleting branch {branch_to_merge}...")
        output, code, _ = run_command(f"git branch -d {branch_to_merge}", check=False)
        if code == 0:
            print_success(f"Branch {branch_to_merge} deleted")
        else:
            print_warning(f"Cannot delete branch (may have unmerged changes)")
            if confirm("Do you want to force deletion?"):
                run_command(f"git branch -D {branch_to_merge}")
                print_success(f"Branch {branch_to_merge} forcefully deleted")
    
    print(f"\n{Colors.GREEN}{Colors.BOLD}✓ Operation completed successfully!{Colors.END}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Operation interrupted by user.{Colors.END}")
        
        # Cleanup if necessary
        if check_merge_in_progress():
            if confirm("\nDo you want to abort the merge in progress?"):
                run_command("git merge --abort", check=False)
                print_success("Merge aborted")
        
        if check_rebase_in_progress():
            if confirm("\nDo you want to abort the rebase in progress?"):
                run_command("git rebase --abort", check=False)
                print_success("Rebase aborted")
        
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
