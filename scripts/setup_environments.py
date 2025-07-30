#!/usr/bin/env python3
"""
Setup script for GitHub Environments and CI/CD configuration.
This script helps users configure staging and production environments.
"""

import os
import sys
from pathlib import Path

def print_header():
    """Print setup header."""
    print("🚀 GitHub Environments Setup")
    print("=" * 50)
    print()

def check_github_repo():
    """Check if we're in a GitHub repository."""
    git_dir = Path('.git')
    if not git_dir.exists():
        print("❌ Not in a Git repository")
        print("Please run this script from your project root directory")
        return False
    
    # Check for remote origin
    try:
        import subprocess
        result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            remote_url = result.stdout.strip()
            if 'github.com' in remote_url:
                print(f"✅ GitHub repository detected: {remote_url}")
                return True
            else:
                print("⚠️  Repository is not on GitHub")
                return False
        else:
            print("⚠️  No remote origin found")
            return False
    except Exception as e:
        print(f"⚠️  Could not check repository: {e}")
        return False

def setup_environments():
    """Guide users through environment setup."""
    print("📋 Environment Setup Guide")
    print()
    print("This will help you set up staging and production environments.")
    print()
    
    # Check if environments already exist
    env_files = [
        Path('.github/environments/staging.yml'),
        Path('.github/environments/production.yml')
    ]
    
    existing_envs = [f for f in env_files if f.exists()]
    if existing_envs:
        print("✅ Environment files already exist:")
        for env_file in existing_envs:
            print(f"   - {env_file}")
        print()
        
        response = input("Do you want to recreate them? (y/n): ").lower().strip()
        if response != 'y':
            print("Setup cancelled.")
            return
    
    print("🔧 Setting up environments...")
    
    # Create .github/environments directory
    env_dir = Path('.github/environments')
    env_dir.mkdir(parents=True, exist_ok=True)
    
    # Create staging environment
    staging_content = '''name: staging
url: https://${{ github.repository_owner }}.github.io/${{ github.repository }}/staging/
protection_rules:
  - required_reviewers:
      users: []
      teams: []
    required_status_checks:
      strict: false
      contexts: []
    enforce_admins: false
    allow_force_pushes: false
    allow_deletions: false
    block_creations: false
    required_conversation_resolution: false
'''
    
    with open(env_dir / 'staging.yml', 'w') as f:
        f.write(staging_content)
    
    # Create production environment
    production_content = '''name: production
url: https://${{ github.repository_owner }}.github.io/${{ github.repository }}/
protection_rules:
  - required_reviewers:
      users: []
      teams: []
    required_status_checks:
      strict: true
      contexts:
        - "Staging Environment"
    enforce_admins: false
    allow_force_pushes: false
    allow_deletions: false
    block_creations: false
    required_conversation_resolution: true
'''
    
    with open(env_dir / 'production.yml', 'w') as f:
        f.write(production_content)
    
    print("✅ Environment files created:")
    print("   - .github/environments/staging.yml")
    print("   - .github/environments/production.yml")

def setup_secrets():
    """Guide users through secrets setup."""
    print()
    print("🔐 Secrets Configuration")
    print()
    print("You'll need to configure these secrets in your GitHub repository:")
    print()
    print("1. Go to: https://github.com/[username]/[repo]/settings/secrets/actions")
    print()
    print("2. Add these secrets:")
    print("   - TMDB_API_KEY (optional): For real movie posters")
    print("   - GITHUB_TOKEN (automatic): Provided by GitHub")
    print()
    print("3. To get TMDB API key:")
    print("   - Visit: https://www.themoviedb.org/settings/api")
    print("   - Create account and request API key")
    print("   - Add as repository secret")
    print()

def setup_branch_protection():
    """Guide users through branch protection setup."""
    print()
    print("🛡️ Branch Protection Setup")
    print()
    print("For production safety, set up branch protection:")
    print()
    print("1. Go to: https://github.com/[username]/[repo]/settings/branches")
    print()
    print("2. Add rule for 'main' branch:")
    print("   - Require pull request reviews before merging")
    print("   - Require status checks to pass before merging")
    print("   - Include administrators")
    print("   - Require conversation resolution")
    print()
    print("3. Add rule for 'staging-pages' branch:")
    print("   - Basic protection (optional)")
    print()

def print_next_steps():
    """Print next steps for users."""
    print()
    print("🎉 Setup Complete!")
    print()
    print("Next Steps:")
    print("1. Push your changes to GitHub")
    print("2. Configure secrets in repository settings")
    print("3. Set up branch protection rules")
    print("4. Create a test PR to trigger staging deployment")
    print()
    print("📚 Documentation:")
    print("   - See docs/CI_CD_SETUP.md for detailed guide")
    print("   - Check GitHub Actions tab for workflow status")
    print()

def main():
    """Main setup function."""
    print_header()
    
    # Check if we're in a GitHub repo
    if not check_github_repo():
        return
    
    # Setup environments
    setup_environments()
    
    # Setup secrets guide
    setup_secrets()
    
    # Setup branch protection guide
    setup_branch_protection()
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main() 