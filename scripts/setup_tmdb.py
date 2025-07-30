#!/usr/bin/env python3
"""
Setup script for TMDB API key configuration.
This script helps users configure their TMDB API key for movie poster fetching.
"""

import os
import sys
from pathlib import Path

def setup_tmdb_api():
    """Guide users through TMDB API key setup."""
    print("🎬 TMDB API Key Setup for Movie Posters")
    print("=" * 50)
    print()
    print("To enable real movie posters in your HTML output, you need a TMDB API key.")
    print()
    print("1. Visit https://www.themoviedb.org/settings/api")
    print("2. Create a free account if you don't have one")
    print("3. Request an API key (choose 'Developer' option)")
    print("4. Copy your API key")
    print()
    
    # Check if API key is already set
    current_key = os.getenv('TMDB_API_KEY')
    if current_key:
        print(f"✅ TMDB API key is already configured: {current_key[:8]}...")
        print()
        response = input("Do you want to update it? (y/n): ").lower().strip()
        if response != 'y':
            print("Setup cancelled.")
            return
    
    # Get API key from user
    api_key = input("Enter your TMDB API key: ").strip()
    
    if not api_key:
        print("❌ No API key provided. Setup cancelled.")
        return
    
    # Validate API key format (basic check)
    if len(api_key) < 20:
        print("❌ API key seems too short. Please check your key.")
        return
    
    # Test the API key
    print("\n🔍 Testing API key...")
    try:
        import requests
        test_url = "https://api.themoviedb.org/3/configuration"
        response = requests.get(test_url, params={'api_key': api_key}, timeout=10)
        
        if response.status_code == 200:
            print("✅ API key is valid!")
        else:
            print(f"❌ API key validation failed. Status code: {response.status_code}")
            return
            
    except Exception as e:
        print(f"❌ Error testing API key: {e}")
        return
    
    # Save to environment file
    env_file = Path('.env')
    env_content = f"TMDB_API_KEY={api_key}\n"
    
    try:
        if env_file.exists():
            # Read existing content and update/add TMDB_API_KEY
            with open(env_file, 'r') as f:
                lines = f.readlines()
            
            # Remove existing TMDB_API_KEY line if it exists
            lines = [line for line in lines if not line.startswith('TMDB_API_KEY=')]
            
            # Add new line
            lines.append(env_content)
            
            with open(env_file, 'w') as f:
                f.writelines(lines)
        else:
            # Create new .env file
            with open(env_file, 'w') as f:
                f.write(env_content)
        
        print(f"✅ API key saved to {env_file}")
        print()
        print("📝 To use this API key in your scripts, you can:")
        print("   1. Load the .env file in your Python scripts")
        print("   2. Set the environment variable manually")
        print("   3. Pass the key directly to the HTMLGenerator.configure_tmdb_api() method")
        print()
        print("🎉 Setup complete! Your movie posters will now use real images from TMDB.")
        
    except Exception as e:
        print(f"❌ Error saving API key: {e}")
        print("You can manually set the TMDB_API_KEY environment variable.")

def load_env_file():
    """Load environment variables from .env file."""
    env_file = Path('.env')
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value

if __name__ == "__main__":
    # Load existing .env file if it exists
    load_env_file()
    
    setup_tmdb_api() 