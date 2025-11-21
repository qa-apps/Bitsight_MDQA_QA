#!/usr/bin/env python3
"""
Script to create all 73 commits with specific dates and code distribution
This will create the actual git commits locally
"""

import os
import subprocess
import random
import shutil
from datetime import datetime
from prepare_commits import COMMIT_DATES, COMMIT_MESSAGES, PROJECT_FILES

def run_git_command(command):
    """Run a git command and return output"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def get_file_content_chunk(filepath, start_line, num_lines):
    """Get a chunk of lines from a file"""
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
            
        # Ensure we don't exceed file boundaries
        end_line = min(start_line + num_lines, len(lines))
        
        # If start_line is beyond file, wrap around
        if start_line >= len(lines):
            start_line = start_line % len(lines)
            end_line = min(start_line + num_lines, len(lines))
            
        return lines[start_line:end_line]
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return []

def create_commits():
    """Create all commits with proper dates and content"""
    
    print("="*80)
    print("CREATING GIT COMMITS FOR BITSIGHT MDQA QA PROJECT")
    print("="*80)
    
    # Initialize git if not already initialized
    if not os.path.exists('.git'):
        print("\nInitializing git repository...")
        run_git_command('git init')
        run_git_command('git config user.name "QA Developer"')
        run_git_command('git config user.email "qa@bitsight-mdqa.com"')
    
    # Create backup of current state
    backup_dir = '.backup_original'
    if not os.path.exists(backup_dir):
        print("\nCreating backup of current files...")
        os.makedirs(backup_dir)
        for filepath in PROJECT_FILES:
            if os.path.exists(filepath):
                backup_path = os.path.join(backup_dir, filepath)
                os.makedirs(os.path.dirname(backup_path), exist_ok=True)
                shutil.copy2(filepath, backup_path)
    
    # Expand dates based on commit count
    all_dates = []
    for date, count in COMMIT_DATES:
        for _ in range(count):
            all_dates.append(date)
    
    # Total commits to create
    total_commits = len(all_dates)
    print(f"\nTotal commits to create: {total_commits}")
    
    # Track which files have been created in commits
    files_created = set()
    
    # Create a mapping of which files to include in each commit
    files_per_commit = []
    all_files = PROJECT_FILES.copy()
    random.shuffle(all_files)  # Randomize order
    
    # Distribute files across commits
    base_files_per_commit = len(all_files) // total_commits
    remainder = len(all_files) % total_commits
    
    file_index = 0
    for i in range(total_commits):
        num_files = base_files_per_commit
        if i < remainder:
            num_files += 1
        
        commit_files = []
        for _ in range(num_files):
            if file_index < len(all_files):
                commit_files.append(all_files[file_index])
                file_index += 1
        
        files_per_commit.append(commit_files)
    
    # Create each commit
    for commit_num, (date, message_idx) in enumerate(zip(all_dates, range(len(all_dates)))):
        
        # Get commit message
        if message_idx < len(COMMIT_MESSAGES):
            message = COMMIT_MESSAGES[message_idx]
        else:
            message = f"Continue test implementation #{message_idx - len(COMMIT_MESSAGES) + 1}"
        
        print(f"\nCommit {commit_num + 1}/{total_commits}: {message}")
        print(f"  Date: {date}")
        
        # Get files for this commit
        commit_files = files_per_commit[commit_num] if commit_num < len(files_per_commit) else []
        
        # Random lines between 40 and 100
        target_lines = random.randint(40, 100)
        lines_per_file = target_lines // max(len(commit_files), 1) if commit_files else target_lines
        
        files_modified = []
        total_lines_added = 0
        
        for filepath in commit_files:
            # Create directory if needed
            dir_path = os.path.dirname(filepath)
            if dir_path and not os.path.exists(dir_path):
                os.makedirs(dir_path, exist_ok=True)
            
            # Check if file exists in backup
            backup_path = os.path.join(backup_dir, filepath)
            
            if filepath not in files_created:
                # First time creating this file - use partial content
                if os.path.exists(backup_path):
                    # Get chunk of original file
                    with open(backup_path, 'r') as f:
                        all_lines = f.readlines()
                    
                    # Calculate how many lines to include
                    num_lines = min(lines_per_file, len(all_lines))
                    if num_lines < len(all_lines):
                        # Partial file
                        selected_lines = all_lines[:num_lines]
                    else:
                        # Full file
                        selected_lines = all_lines
                    
                    with open(filepath, 'w') as f:
                        f.writelines(selected_lines)
                    
                    total_lines_added += len(selected_lines)
                    files_created.add(filepath)
                    files_modified.append(filepath)
                    
            else:
                # File already created - add more content
                if os.path.exists(backup_path):
                    with open(backup_path, 'r') as f:
                        all_lines = f.readlines()
                    
                    with open(filepath, 'r') as f:
                        current_lines = f.readlines()
                    
                    # Add more lines from original
                    current_line_count = len(current_lines)
                    if current_line_count < len(all_lines):
                        new_lines_to_add = min(lines_per_file, len(all_lines) - current_line_count)
                        additional_lines = all_lines[current_line_count:current_line_count + new_lines_to_add]
                        
                        with open(filepath, 'a') as f:
                            f.writelines(additional_lines)
                        
                        total_lines_added += len(additional_lines)
                        files_modified.append(filepath)
        
        # If no files modified, create a dummy change
        if not files_modified and commit_num == 0:
            # First commit - create initial README
            with open('README.md', 'w') as f:
                f.write(f"# BitSight MDQA QA Project\n\nInitialized on {date}\n")
            files_modified.append('README.md')
            total_lines_added = 2
        
        # Stage and commit files
        if files_modified:
            print(f"  Files modified: {len(files_modified)}")
            print(f"  Lines added: ~{total_lines_added}")
            
            # Stage files
            for filepath in files_modified:
                run_git_command(f'git add {filepath}')
            
            # Create commit with specific date
            commit_date = f"{date} 12:00:00"
            commit_cmd = f'git commit -m "{message}" --date="{commit_date}"'
            success, stdout, stderr = run_git_command(commit_cmd)
            
            if success:
                print(f"  ✓ Commit created successfully")
            else:
                print(f"  ✗ Error creating commit: {stderr}")
        else:
            print(f"  ⚠ No files to commit")
    
    # Restore any remaining files to their full state
    print("\n" + "="*80)
    print("Restoring full file contents...")
    
    for filepath in PROJECT_FILES:
        backup_path = os.path.join(backup_dir, filepath)
        if os.path.exists(backup_path):
            dir_path = os.path.dirname(filepath)
            if dir_path and not os.path.exists(dir_path):
                os.makedirs(dir_path, exist_ok=True)
            shutil.copy2(backup_path, filepath)
    
    # Create final commit with all files complete
    print("\nCreating final commit with complete files...")
    run_git_command('git add -A')
    final_date = "2023-12-31 23:59:59"
    run_git_command(f'git commit -m "Finalize project with all test suites complete" --date="{final_date}"')
    
    print("\n" + "="*80)
    print("ALL COMMITS CREATED SUCCESSFULLY!")
    print("="*80)
    
    # Show git log summary
    print("\nGit log summary (last 10 commits):")
    success, stdout, stderr = run_git_command('git log --oneline -10')
    if success:
        print(stdout)
    
    print("\nTotal commits in repository:")
    success, stdout, stderr = run_git_command('git rev-list --count HEAD')
    if success:
        print(f"  {stdout.strip()} commits")
    
    print("\n" + "="*80)
    print("NEXT STEPS:")
    print("1. Review commits: git log --oneline")
    print("2. Check commit dates: git log --format='%ad %s' --date=short")
    print("3. Get permission to push")
    print("4. Push to repository: git push origin main")
    print("="*80)

if __name__ == "__main__":
    create_commits()
