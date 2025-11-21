#!/usr/bin/env python3
"""
Script to prepare and create all 73 commits for BitSight MDQA QA project
Following the specified dates and requirements from 2023
"""

import os
import subprocess
import random
from datetime import datetime

# Complete list of commit dates for 2023
COMMIT_DATES = [
    # January
    ("2023-01-03", 1),
    ("2023-01-06", 1),
    ("2023-01-17", 3),
    ("2023-01-18", 1),
    ("2023-01-31", 1),
    # February
    ("2023-02-01", 1),
    ("2023-02-25", 3),
    ("2023-02-28", 3),
    # March
    ("2023-03-05", 1),
    ("2023-03-10", 1),
    ("2023-03-11", 4),
    ("2023-03-12", 1),
    ("2023-03-15", 1),
    ("2023-03-18", 1),
    ("2023-03-31", 1),
    # April
    ("2023-04-05", 1),
    ("2023-04-10", 1),
    ("2023-04-15", 1),
    ("2023-04-21", 1),
    # May
    ("2023-05-06", 1),
    ("2023-05-07", 1),
    ("2023-05-08", 1),
    ("2023-05-09", 1),
    ("2023-05-21", 1),
    ("2023-05-25", 1),
    ("2023-05-26", 3),
    # June
    ("2023-06-01", 1),
    ("2023-06-02", 1),
    ("2023-06-07", 1),
    ("2023-06-13", 1),
    ("2023-06-25", 1),
    ("2023-06-26", 1),
    # July
    ("2023-07-08", 1),
    ("2023-07-12", 1),
    ("2023-07-13", 1),
    ("2023-07-21", 1),
    # August
    ("2023-08-03", 1),
    ("2023-08-05", 1),
    ("2023-08-13", 1),
    ("2023-08-17", 1),
    ("2023-08-20", 1),
    ("2023-08-28", 1),
    # September
    ("2023-09-05", 1),
    ("2023-09-10", 1),
    ("2023-09-11", 1),
    ("2023-09-22", 1),
    ("2023-09-24", 1),
    ("2023-09-25", 1),
    ("2023-09-30", 1),
    # October
    ("2023-10-01", 1),
    ("2023-10-02", 1),
    ("2023-10-07", 1),
    ("2023-10-15", 1),
    ("2023-10-20", 1),
    # November
    ("2023-11-05", 1),
    ("2023-11-13", 1),
    ("2023-11-18", 1),
    ("2023-11-19", 1),
    # December
    ("2023-12-02", 1),
    ("2023-12-10", 1),
    ("2023-12-11", 1),
    ("2023-12-15", 1),
]

# Commit messages (73 unique messages starting with capital letter)
COMMIT_MESSAGES = [
    # January (7 commits)
    "Initial project setup with Playwright and Python",
    "Add requirements and project configuration",
    "Create base page object model structure",
    "Implement homepage page object class",
    "Add products page object implementation",
    "Setup pytest configuration and fixtures",
    "Configure test markers and browser settings",
    # February (7 commits)
    "Implement smoke test suite for homepage",
    "Add critical path smoke tests",
    "Create navigation testing framework",
    "Develop link validation tests",
    "Add dropdown menu test implementation",
    "Enhance navigation test coverage",
    "Update navigation selectors and methods",
    # March (11 commits)
    "Build comprehensive regression test suite",
    "Add full functionality regression tests",
    "Implement security vulnerability tests",
    "Create XSS prevention test cases",
    "Add SQL injection test scenarios",
    "Develop secure headers validation",
    "Implement clickjacking protection tests",
    "Create UI element test suite",
    "Add button interaction tests",
    "Develop form element validation",
    "Implement modal and accordion tests",
    # April (4 commits)
    "Create usability and accessibility tests",
    "Add WCAG compliance test cases",
    "Implement keyboard navigation tests",
    "Develop ARIA label validation tests",
    # May (10 commits)
    "Build page structure validation tests",
    "Add HTML structure test cases",
    "Create semantic HTML validation",
    "Implement meta tag verification tests",
    "Add structured data testing",
    "Develop content hierarchy validation",
    "Create form validation test suite",
    "Add email field validation tests",
    "Implement phone number validation",
    "Create character limit test cases",
    # June (6 commits)
    "Develop performance metrics testing",
    "Add page load time measurements",
    "Implement Core Web Vitals tests",
    "Create resource loading tests",
    "Add memory usage monitoring",
    "Develop cache header validation",
    # July (4 commits)
    "Build cross-browser compatibility tests",
    "Add Chromium specific test cases",
    "Implement Firefox compatibility tests",
    "Create WebKit/Safari test scenarios",
    # August (6 commits)
    "Develop error handling test suite",
    "Add 404 page validation tests",
    "Implement JavaScript error handling",
    "Create form submission error tests",
    "Add network timeout handling",
    "Develop error recovery scenarios",
    # September (7 commits)
    "Create search functionality tests",
    "Add search input validation",
    "Implement search results testing",
    "Develop autocomplete test cases",
    "Add search filter validation",
    "Create pagination testing",
    "Implement search history tests",
    # October (5 commits)
    "Build content validation test suite",
    "Add text content verification",
    "Implement copyright validation",
    "Create social media link tests",
    "Develop testimonial content tests",
    # November (4 commits)
    "Create mobile responsiveness tests",
    "Add touch interaction testing",
    "Implement viewport rendering tests",
    "Develop mobile navigation tests",
    # December (4 commits)
    "Build integration E2E test suite",
    "Add complete user journey tests",
    "Implement data validation tests",
    "Final test suite optimizations"
]

# All project files
PROJECT_FILES = [
    "requirements.txt",
    "pytest.ini",
    "conftest.py",
    "pages/base_page.py",
    "pages/home_page.py",
    "pages/products_page.py",
    "pages/home_page_real.py",
    "tests/test_smoke_homepage.py",
    "tests/test_navigation_links.py",
    "tests/test_regression_full.py",
    "tests/test_security_vulnerability.py",
    "tests/test_ui_elements.py",
    "tests/test_usability_accessibility.py",
    "tests/test_page_structure.py",
    "tests/test_dropdown_menus.py",
    "tests/test_forms_validation.py",
    "tests/test_with_real_selectors.py",
    "tests/test_performance_metrics.py",
    "tests/test_cross_browser.py",
    "tests/test_error_handling.py",
    "tests/test_search_functionality.py",
    "tests/test_content_validation.py",
    "tests/test_mobile_responsiveness.py",
    "tests/test_integration_e2e.py",
    "tests/test_data_validation.py",
    "inspect_dom.py",
    "extract_selectors.py",
    "actual_selectors.json",
    "DOM_INSPECTION_FINDINGS.md",
    "README.md"
]

def get_file_lines(filepath):
    """Get specific lines from a file"""
    try:
        with open(filepath, 'r') as f:
            return f.readlines()
    except:
        return []

def create_partial_file(filepath, start_line, num_lines):
    """Create a partial version of a file with specific lines"""
    lines = get_file_lines(filepath)
    if not lines:
        return ""
    
    end_line = min(start_line + num_lines, len(lines))
    return ''.join(lines[start_line:end_line])

def prepare_commits():
    """Prepare all commits with proper distribution"""
    
    commits = []
    commit_index = 0
    
    # Expand dates based on commit count
    all_dates = []
    for date, count in COMMIT_DATES:
        for _ in range(count):
            all_dates.append(date)
    
    # Map files to commits
    lines_per_file = {}
    for filepath in PROJECT_FILES:
        lines = get_file_lines(filepath)
        lines_per_file[filepath] = len(lines)
    
    # Create commits
    for i, date in enumerate(all_dates):
        if i >= len(COMMIT_MESSAGES):
            message = f"Update test implementation #{i-len(COMMIT_MESSAGES)+1}"
        else:
            message = COMMIT_MESSAGES[i]
            
        # Random lines between 40 and 100
        num_lines = random.randint(40, 100)
        
        commits.append({
            'date': date,
            'message': message,
            'lines': num_lines,
            'files': []
        })
    
    # Distribute files across commits
    file_assignments = {}
    files_per_commit = len(PROJECT_FILES) // len(commits) + 1
    
    for i, filepath in enumerate(PROJECT_FILES):
        commit_idx = i // files_per_commit
        if commit_idx >= len(commits):
            commit_idx = len(commits) - 1
        
        if filepath not in file_assignments:
            file_assignments[filepath] = []
        
        file_assignments[filepath].append(commit_idx)
        
    # Assign files to commits
    for filepath, commit_indices in file_assignments.items():
        total_lines = lines_per_file.get(filepath, 100)
        lines_per_commit = total_lines // len(commit_indices)
        
        for idx, commit_idx in enumerate(commit_indices):
            start_line = idx * lines_per_commit
            commits[commit_idx]['files'].append({
                'path': filepath,
                'start': start_line,
                'lines': min(commits[commit_idx]['lines'], lines_per_commit)
            })
    
    return commits

def main():
    """Main function to prepare commits"""
    
    print("="*80)
    print("PREPARING 73 COMMITS FOR BITSIGHT MDQA QA PROJECT")
    print("="*80)
    
    commits = prepare_commits()
    
    print(f"\nTotal commits to create: {len(commits)}")
    print("\nCommit distribution by month:")
    
    month_counts = {}
    for commit in commits:
        month = commit['date'][:7]
        month_counts[month] = month_counts.get(month, 0) + 1
    
    for month, count in sorted(month_counts.items()):
        print(f"  {month}: {count} commits")
    
    print("\n" + "="*80)
    print("COMMITS PREPARED SUCCESSFULLY!")
    print("="*80)
    print("\nTo create and push these commits:")
    print("1. Run: python3 create_commits.py")
    print("2. Review the commits locally")
    print("3. Get permission to push")
    print("4. Run: git push origin main")
    
    # Save commit plan
    with open('commit_plan.txt', 'w') as f:
        for i, commit in enumerate(commits, 1):
            f.write(f"Commit {i}:\n")
            f.write(f"  Date: {commit['date']}\n")
            f.write(f"  Message: {commit['message']}\n")
            f.write(f"  Lines: {commit['lines']}\n")
            f.write(f"  Files: {len(commit['files'])}\n")
            f.write("\n")
    
    print("\nCommit plan saved to commit_plan.txt")
    
    return commits

if __name__ == "__main__":
    commits = main()
