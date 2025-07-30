#!/usr/bin/env python3
"""
Generate PR summary and change documentation.
This script helps create comprehensive PR summaries with staging/production links.
"""

import json
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

class PRSummaryGenerator:
    def __init__(self):
        self.repo_owner = "serialforbreakfast"
        self.repo_name = "TooScaryDidntStream"
        self.production_url = f"https://{self.repo_owner}.github.io/{self.repo_name}/output/index.html"
        # Get PR number from environment or default to 'latest'
        self.pr_number = os.environ.get('GITHUB_EVENT_PULL_REQUEST_NUMBER', 'latest')
        self.staging_url = f"https://{self.repo_owner}.github.io/{self.repo_name}/staging/pr-{self.pr_number}/"

    def get_git_changes(self) -> Dict[str, List[str]]:
        """Get list of changed files from git."""
        try:
            # Get staged and unstaged changes
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True)
            
            if result.returncode != 0:
                return {}
            
            changes = {
                'modified': [],
                'added': [],
                'deleted': [],
                'renamed': []
            }
            
            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue
                    
                status = line[:2].strip()
                file_path = line[3:]
                
                if status == 'M':
                    changes['modified'].append(file_path)
                elif status == 'A':
                    changes['added'].append(file_path)
                elif status == 'D':
                    changes['deleted'].append(file_path)
                elif status == 'R':
                    changes['renamed'].append(file_path)
            
            return changes
            
        except Exception as e:
            print(f"Error getting git changes: {e}")
            return {}

    def analyze_data_changes(self) -> Dict[str, Any]:
        """Analyze changes to data files."""
        changes = self.get_git_changes()
        data_analysis = {
            'episodes_added': 0,
            'episodes_modified': 0,
            'movies_added': 0,
            'movies_modified': 0,
            'streaming_sources_updated': False
        }
        
        # Check if movies.json was modified
        if 'data/movies.json' in changes.get('modified', []):
            try:
                # Get the diff for movies.json
                result = subprocess.run(['git', 'diff', 'HEAD', 'data/movies.json'], 
                                      capture_output=True, text=True)
                
                if result.returncode == 0:
                    diff_output = result.stdout
                    
                    # Count episode and movie changes
                    lines = diff_output.split('\n')
                    for line in lines:
                        if line.startswith('+') and '"episode_number"' in line:
                            data_analysis['episodes_added'] += 1
                        elif line.startswith('+') and '"title"' in line and '"year"' in line:
                            data_analysis['movies_added'] += 1
                        elif line.startswith('-') and '"episode_number"' in line:
                            data_analysis['episodes_modified'] += 1
                        elif line.startswith('-') and '"title"' in line and '"year"' in line:
                            data_analysis['movies_modified'] += 1
                            
            except Exception as e:
                print(f"Error analyzing data changes: {e}")
        
        # Check if streaming data was updated
        if 'data/streaming_data.json' in changes.get('modified', []):
            data_analysis['streaming_sources_updated'] = True
        
        return data_analysis

    def analyze_script_changes(self) -> Dict[str, Any]:
        """Analyze changes to script files."""
        changes = self.get_git_changes()
        script_analysis = {
            'html_generation_changed': False,
            'streaming_fetch_changed': False,
            'new_scripts': [],
            'modified_scripts': []
        }
        
        for file_path in changes.get('modified', []):
            if file_path.startswith('scripts/'):
                script_analysis['modified_scripts'].append(file_path)
                
                if 'generate_html.py' in file_path:
                    script_analysis['html_generation_changed'] = True
                elif 'fetch_streaming_info.py' in file_path:
                    script_analysis['streaming_fetch_changed'] = True
        
        for file_path in changes.get('added', []):
            if file_path.startswith('scripts/'):
                script_analysis['new_scripts'].append(file_path)
        
        return script_analysis

    def analyze_workflow_changes(self) -> Dict[str, Any]:
        """Analyze changes to GitHub workflows."""
        changes = self.get_git_changes()
        workflow_analysis = {
            'staging_workflow_changed': False,
            'production_workflow_changed': False,
            'new_workflows': [],
            'modified_workflows': []
        }
        
        for file_path in changes.get('modified', []):
            if file_path.startswith('.github/workflows/'):
                workflow_analysis['modified_workflows'].append(file_path)
                
                if 'staging.yml' in file_path:
                    workflow_analysis['staging_workflow_changed'] = True
                elif 'update-streaming-data.yml' in file_path:
                    workflow_analysis['production_workflow_changed'] = True
        
        for file_path in changes.get('added', []):
            if file_path.startswith('.github/workflows/'):
                workflow_analysis['new_workflows'].append(file_path)
        
        return workflow_analysis

    def generate_change_summary(self) -> str:
        """Generate a comprehensive change summary."""
        data_analysis = self.analyze_data_changes()
        script_analysis = self.analyze_script_changes()
        workflow_analysis = self.analyze_workflow_changes()
        changes = self.get_git_changes()
        
        summary = f"""# 📊 Change Summary

## 🔗 Site Links
- **Production:** {self.production_url}
- **Staging:** {self.staging_url}

## 📈 Data Changes
"""
        
        if data_analysis['episodes_added'] > 0:
            summary += f"- ✅ Added {data_analysis['episodes_added']} new episodes\n"
        if data_analysis['episodes_modified'] > 0:
            summary += f"- 🔄 Modified {data_analysis['episodes_modified']} episodes\n"
        if data_analysis['movies_added'] > 0:
            summary += f"- 🎬 Added {data_analysis['movies_added']} new movies\n"
        if data_analysis['movies_modified'] > 0:
            summary += f"- 📝 Modified {data_analysis['movies_modified']} movies\n"
        if data_analysis['streaming_sources_updated']:
            summary += "- 🔄 Updated streaming sources\n"
        
        summary += "\n## 🔧 Script Changes\n"
        
        if script_analysis['html_generation_changed']:
            summary += "- 🎨 HTML generation updated\n"
        if script_analysis['streaming_fetch_changed']:
            summary += "- 🔍 Streaming data fetching updated\n"
        if script_analysis['new_scripts']:
            summary += f"- ➕ New scripts: {', '.join(script_analysis['new_scripts'])}\n"
        if script_analysis['modified_scripts']:
            summary += f"- 🔄 Modified scripts: {', '.join(script_analysis['modified_scripts'])}\n"
        
        summary += "\n## 🚀 Workflow Changes\n"
        
        if workflow_analysis['staging_workflow_changed']:
            summary += "- 🧪 Staging workflow updated\n"
        if workflow_analysis['production_workflow_changed']:
            summary += "- 🚀 Production workflow updated\n"
        if workflow_analysis['new_workflows']:
            summary += f"- ➕ New workflows: {', '.join(workflow_analysis['new_workflows'])}\n"
        if workflow_analysis['modified_workflows']:
            summary += f"- 🔄 Modified workflows: {', '.join(workflow_analysis['modified_workflows'])}\n"
        
        summary += "\n## 📁 Files Changed\n"
        
        total_changes = sum(len(files) for files in changes.values())
        summary += f"- **Total files changed:** {total_changes}\n"
        
        for change_type, files in changes.items():
            if files:
                summary += f"- **{change_type.title()}:** {len(files)} files\n"
                for file_path in files[:5]:  # Show first 5 files
                    summary += f"  - `{file_path}`\n"
                if len(files) > 5:
                    summary += f"  - ... and {len(files) - 5} more\n"
        
        summary += f"\n## 🧪 Testing Instructions\n"
        summary += f"1. **Compare Staging vs Production:**\n"
        summary += f"   - Production: {self.production_url}\n"
        summary += f"   - Staging: {self.staging_url}\n"
        summary += f"2. **Test Responsive Design:** Check on desktop, tablet, mobile\n"
        summary += f"3. **Verify Functionality:** Test all interactive features\n"
        summary += f"4. **Check Performance:** Ensure no significant regressions\n"
        
        return summary

    def generate_pr_template(self) -> str:
        """Generate a PR template with current information."""
        template = f"""# Pull Request Template

## 📋 Overview

**Type of Change:** [Feature/Bugfix/Documentation/Refactor]
**Related Issue:** [Link to issue if applicable]

## 🔗 Site Links

### Production Site
- **Current Production:** {self.production_url}
- **Production Branch:** `gh-pages`

### Staging Site
- **Staging Preview:** {self.staging_url}
- **Staging Branch:** `staging-pages`

## 📊 Before & After Comparison

### Before (Production)
- **URL:** {self.production_url}
- **Key Features:** [List current production features]

### After (Staging)
- **URL:** {self.staging_url}
- **New Features:** [List new features in this PR]

## 🎯 Changes Summary

[Use the generated summary below or describe your changes]

### What Changed
- [ ] **Data Updates:** [Describe any changes to `data/movies.json`]
- [ ] **Script Updates:** [Describe any changes to `scripts/` files]
- [ ] **UI/UX Changes:** [Describe visual or interaction changes]
- [ ] **Documentation:** [Describe any documentation updates]
- [ ] **CI/CD Changes:** [Describe any workflow or deployment changes]

### Files Modified
[Use the file list generated by the script]

## 🧪 Testing Checklist

### Staging Environment Testing
- [ ] **Site Loads:** Staging site loads without errors
- [ ] **Responsive Design:** Works on desktop, tablet, and mobile
- [ ] **Movie Posters:** Posters display correctly (with/without TMDB API)
- [ ] **Streaming Links:** All streaming links work properly
- [ ] **Search Functionality:** Episode search works correctly
- [ ] **Filter Functionality:** Streaming filters work as expected
- [ ] **Sidebar Toggle:** Show/hide sidebar works smoothly
- [ ] **Episode Navigation:** Clicking episodes scrolls to correct section
- [ ] **Performance:** Page loads quickly and smoothly

### Visual Testing
- [ ] **Desktop (1920x1080):** All elements properly positioned
- [ ] **Tablet (768px):** Responsive layout works correctly
- [ ] **Mobile (375px):** Mobile layout is functional
- [ ] **Poster Images:** Movie posters display with proper sizing
- [ ] **Typography:** All text is readable and properly sized
- [ ] **Colors:** Color scheme is consistent and accessible

### Functionality Testing
- [ ] **Data Validation:** All episodes and movies display correctly
- [ ] **Streaming Data:** Streaming sources are accurate and up-to-date
- [ ] **API Integration:** TMDB API calls work (if applicable)
- [ ] **Error Handling:** Graceful fallbacks for missing data
- [ ] **Cross-browser:** Works in Chrome, Firefox, Safari, Edge

## 📈 Impact Assessment

### User Experience Impact
- **Positive Changes:** [List improvements to user experience]
- **Potential Issues:** [List any potential concerns or breaking changes]
- **Migration Notes:** [Any steps users need to take]

### Performance Impact
- **Page Load Time:** [Estimated impact on load times]
- **File Size Changes:** [Changes to HTML/CSS/JS file sizes]
- **API Calls:** [Impact on external API usage]

## 🔍 Review Guidelines

### For Reviewers
1. **Compare Staging vs Production:** Use the provided links to compare
2. **Test Responsive Design:** Check on different screen sizes
3. **Verify Functionality:** Test all interactive features
4. **Check Performance:** Ensure no significant performance regressions
5. **Review Code Quality:** Ensure clean, maintainable code

### Review Checklist
- [ ] **Code Review:** Code follows project standards
- [ ] **Functionality:** All features work as expected
- [ ] **Responsive Design:** Works on all target devices
- [ ] **Accessibility:** Meets accessibility standards
- [ ] **Performance:** No significant performance impact
- [ ] **Documentation:** Changes are properly documented
- [ ] **Testing:** Appropriate tests are included/updated

## 🚀 Deployment Notes

### Staging Deployment
- **Status:** [Pending/In Progress/Complete]
- **URL:** {self.staging_url}
- **Branch:** `staging-pages`

### Production Deployment
- **Status:** [Pending/In Progress/Complete]
- **URL:** {self.production_url}
- **Branch:** `gh-pages`
- **Trigger:** Automatic on merge to `main`

---

**PR Author:** [Your Name]
**Reviewers:** [Tag relevant reviewers]
**Labels:** [Add appropriate labels]

---

*This template ensures comprehensive review and testing of all changes before production deployment.*
"""
        return template

def main():
    """Main function to generate PR summary."""
    generator = PRSummaryGenerator()
    
    print("📋 PR Summary Generator")
    print("=" * 50)
    print()
    
    # Generate change summary
    summary = generator.generate_change_summary()
    print(summary)
    
    print("\n" + "=" * 50)
    print("💡 Usage Instructions:")
    print("1. Copy the summary above into your PR description")
    print("2. Use the staging and production links for comparison")
    print("3. Complete the testing checklist")
    print("4. Tag appropriate reviewers")
    
    # Save summary to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary_file = f"pr_summary_{timestamp}.md"
    
    with open(summary_file, 'w') as f:
        f.write(summary)
    
    print(f"\n📄 Summary saved to: {summary_file}")

if __name__ == "__main__":
    main() 