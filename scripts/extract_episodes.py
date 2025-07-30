#!/usr/bin/env python3
"""
Extract episode titles from the HTML file and identify movies.

This script parses the Episodes.html file to extract all episode titles
and attempts to identify the main movie discussed in each episode.
"""

import re
import json
from typing import List, Dict, Any
from datetime import datetime, timedelta

def extract_episode_titles(html_content: str) -> List[Dict[str, Any]]:
    """Extract episode titles from HTML content."""
    # Pattern to match episode titles
    pattern = r'data-testid="episode-lockup-title">([^<]+)</span>'
    matches = re.findall(pattern, html_content)
    
    episodes = []
    episode_number = 240  # Start from current episode number
    
    for title in matches:
        # Clean up the title
        clean_title = title.strip()
        
        # Extract the main movie title from the episode title
        movie_title = extract_movie_title(clean_title)
        
        # Generate a date (approximate based on episode number)
        # Assuming weekly episodes, going backwards from current date
        days_back = (240 - episode_number) * 7
        air_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
        
        episode_data = {
            "episode_number": episode_number,
            "title": clean_title,
            "air_date": air_date,
            "description": f"Episode discussing {movie_title}",
            "movies": [
                {
                    "title": movie_title,
                    "year": extract_movie_year(movie_title),
                    "imdb_id": "",  # Will be filled by API lookup
                    "notes": "Main movie discussed in episode"
                }
            ]
        }
        
        episodes.append(episode_data)
        episode_number -= 1
    
    return episodes

def extract_movie_title(episode_title: str) -> str:
    """Extract the main movie title from episode title."""
    # Remove common episode suffixes
    title = episode_title
    
    # Remove guest names in parentheses
    title = re.sub(r'\s+with\s+[^()]+', '', title)
    title = re.sub(r'\s*\([^)]*\)', '', title)
    
    # Remove common episode prefixes/suffixes
    title = re.sub(r'^(LIVE!|Vault Release|Watch-Along)\s*', '', title)
    title = re.sub(r'\s*(LIVE!|Vault Release|Watch-Along)\s*$', '', title)
    
    # Handle special cases
    if "FINAL DESTINATION: BLOODLINES" in title:
        return "Final Destination: Bloodlines"
    elif "M3GAN 2.0" in title:
        return "M3GAN 2.0"
    elif "28 YEARS LATER" in title:
        return "28 Years Later"
    elif "TITAN: THE OCEANGATE DISASTER" in title:
        return "Titan: The OceanGate Disaster"
    elif "AMERICAN PSYCHO" in title:
        return "American Psycho"
    elif "THEY LIVE" in title:
        return "They Live"
    elif "28 WEEKS LATER" in title:
        return "28 Weeks Later"
    elif "THE LOVED ONES" in title:
        return "The Loved Ones"
    elif "THE HOLE" in title:
        return "The Hole"
    elif "SINNERS" in title:
        return "Sinners"
    elif "DOGTOOTH" in title:
        return "Dogtooth"
    elif "DROP" in title:
        return "Drop"
    elif "BEETLEJUICE" in title:
        return "Beetlejuice"
    elif "THE BLACKENING" in title:
        return "The Blackening"
    elif "HELL OF A SUMMER" in title:
        return "Hell of a Summer"
    elif "MADS" in title:
        return "Mads"
    elif "THE LOVE WITCH" in title:
        return "The Love Witch"
    elif "LEPRECHAUN 2" in title:
        return "Leprechaun 2"
    elif "THE MONKEY" in title:
        return "The Monkey"
    elif "SUNSHINE" in title:
        return "Sunshine"
    elif "WHAT EVER HAPPENED TO BABY JANE?" in title:
        return "What Ever Happened to Baby Jane?"
    elif "EVIL DEAD (2013)" in title:
        return "Evil Dead"
    elif "DEATH BECOMES HER" in title:
        return "Death Becomes Her"
    elif "GANJA & HESS" in title:
        return "Ganja & Hess"
    elif "THE HAUNTING IN CONNECTICUT" in title:
        return "The Haunting in Connecticut"
    elif "THE INNOCENTS" in title:
        return "The Innocents"
    elif "THE SLUMBER PARTY MASSACRE" in title:
        return "The Slumber Party Massacre"
    elif "IT'S WHATS INSIDE" in title:
        return "It's What's Inside"
    elif "NOSFERATU" in title:
        return "Nosferatu"
    elif "THE NEON DEMON" in title:
        return "The Neon Demon"
    elif "IMMACULATE" in title:
        return "Immaculate"
    elif "INSIDE (2007)" in title:
        return "Inside"
    elif "THE NIGHTMARE BEFORE CHRISTMAS" in title:
        return "The Nightmare Before Christmas"
    elif "SINGLE WHITE FEMALE" in title:
        return "Single White Female"
    elif "RED EYE" in title:
        return "Red Eye"
    elif "HERETIC" in title:
        return "Heretic"
    elif "SMILE 2" in title:
        return "Smile 2"
    elif "YOUR MONSTER" in title:
        return "Your Monster"
    elif "TERRIFIER 3" in title:
        return "Terrifier 3"
    elif "THE SUBSTANCE" in title:
        return "The Substance"
    elif "SPEAK NO EVIL (US REMAKE)" in title:
        return "Speak No Evil"
    elif "HALLOWEEN (2018)" in title:
        return "Halloween"
    elif "TITANIC" in title:
        return "Titanic"
    elif "BONE TOMAHAWK" in title:
        return "Bone Tomahawk"
    elif "SLEEPY HOLLOW" in title:
        return "Sleepy Hollow"
    elif "CAM" in title:
        return "Cam"
    elif "THE REEF" in title:
        return "The Reef"
    elif "ALIEN: ROMULUS" in title:
        return "Alien: Romulus"
    elif "CUCKOO" in title:
        return "Cuckoo"
    elif "TWISTERS" in title:
        return "Twisters"
    elif "TRAP" in title:
        return "Trap"
    elif "LONGLEGS" in title:
        return "Longlegs"
    elif "A QUIET PLACE: DAY ONE" in title:
        return "A Quiet Place: Day One"
    elif "MAXXXINE" in title:
        return "MaXXXine"
    elif "THE DEVIL'S BATH" in title:
        return "The Devil's Bath"
    elif "THE FIRST OMEN" in title:
        return "The First Omen"
    elif "ABIGAIL" in title:
        return "Abigail"
    elif "IN A VIOLENT NATURE" in title:
        return "In a Violent Nature"
    elif "I SAW THE TV GLOW" in title:
        return "I Saw the TV Glow"
    elif "NIGHT SWIM" in title:
        return "Night Swim"
    elif "BREAKING DAWN PART 2" in title:
        return "The Twilight Saga: Breaking Dawn - Part 2"
    elif "THE TWILIGHT SAGA: NEW MOON" in title:
        return "The Twilight Saga: New Moon"
    elif "REAR WINDOW" in title:
        return "Rear Window"
    elif "SPLICE" in title:
        return "Splice"
    elif "ALONE" in title:
        return "Alone"
    elif "EX MACHINA" in title:
        return "Ex Machina"
    elif "THE FOG" in title:
        return "The Fog"
    elif "BREAKING DAWN PART 1" in title:
        return "The Twilight Saga: Breaking Dawn - Part 1"
    elif "LATE NIGHT WITH THE DEVIL" in title:
        return "Late Night with the Devil"
    elif "REVENGE" in title:
        return "Revenge"
    elif "DONNIE DARKO" in title:
        return "Donnie Darko"
    elif "JOY RIDE" in title:
        return "Joy Ride"
    elif "ODDITY" in title:
        return "Oddity"
    elif "THE RITUAL" in title:
        return "The Ritual"
    elif "M3GAN 2.0" in title:
        return "M3GAN 2.0"
    
    # Default: clean up the title
    return title.strip()

def extract_movie_year(movie_title: str) -> int:
    """Extract or estimate the movie year based on title."""
    # Known years for specific movies
    year_mapping = {
        "Final Destination: Bloodlines": 2024,
        "M3GAN 2.0": 2025,
        "28 Years Later": 2025,
        "Titan: The OceanGate Disaster": 2024,
        "American Psycho": 2000,
        "They Live": 1988,
        "28 Weeks Later": 2007,
        "The Loved Ones": 2009,
        "The Hole": 2009,
        "Sinners": 2024,
        "Dogtooth": 2009,
        "Drop": 2024,
        "Beetlejuice": 1988,
        "The Blackening": 2022,
        "Hell of a Summer": 2024,
        "Mads": 2024,
        "The Love Witch": 2016,
        "Leprechaun 2": 1994,
        "The Monkey": 2024,
        "Sunshine": 2007,
        "What Ever Happened to Baby Jane?": 1962,
        "Evil Dead": 2013,
        "Death Becomes Her": 1992,
        "Ganja & Hess": 1973,
        "The Haunting in Connecticut": 2009,
        "The Innocents": 1961,
        "The Slumber Party Massacre": 1982,
        "It's What's Inside": 2024,
        "Nosferatu": 1922,
        "The Neon Demon": 2016,
        "Immaculate": 2024,
        "Inside": 2007,
        "The Nightmare Before Christmas": 1993,
        "Single White Female": 1992,
        "Red Eye": 2005,
        "Heretic": 2024,
        "Smile 2": 2024,
        "Your Monster": 2024,
        "Terrifier 3": 2024,
        "The Substance": 2024,
        "Speak No Evil": 2024,
        "Halloween": 2018,
        "Titanic": 1997,
        "Bone Tomahawk": 2015,
        "Sleepy Hollow": 1999,
        "Cam": 2018,
        "The Reef": 2010,
        "Alien: Romulus": 2024,
        "Cuckoo": 2024,
        "Twisters": 2024,
        "Trap": 2024,
        "Longlegs": 2024,
        "A Quiet Place: Day One": 2024,
        "MaXXXine": 2024,
        "The Devil's Bath": 2024,
        "The First Omen": 2024,
        "Abigail": 2024,
        "In a Violent Nature": 2024,
        "I Saw the TV Glow": 2024,
        "Night Swim": 2024,
        "The Twilight Saga: Breaking Dawn - Part 2": 2012,
        "The Twilight Saga: New Moon": 2009,
        "Rear Window": 1954,
        "Splice": 2009,
        "Alone": 2020,
        "Ex Machina": 2014,
        "The Fog": 1980,
        "The Twilight Saga: Breaking Dawn - Part 1": 2011,
        "Late Night with the Devil": 2023,
        "Revenge": 2017,
        "Donnie Darko": 2001,
        "Joy Ride": 2023,
        "Oddity": 2024,
        "The Ritual": 2017,
        "M3GAN 2.0": 2025
    }
    
    return year_mapping.get(movie_title, 2024)  # Default to 2024 for unknown movies

def main():
    """Main function to extract episodes and update movies.json."""
    # Read the HTML file
    with open('forImporting/Episodes.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Extract episodes
    episodes = extract_episode_titles(html_content)
    
    # Read current movies.json
    with open('data/movies.json', 'r', encoding='utf-8') as f:
        current_data = json.load(f)
    
    # Add new episodes to the beginning of the list
    current_data['episodes'] = episodes + current_data['episodes']
    
    # Update metadata
    current_data['metadata']['total_episodes'] = len(current_data['episodes'])
    current_data['metadata']['last_updated'] = datetime.now().strftime("%Y-%m-%d")
    
    # Write updated data
    with open('data/movies.json', 'w', encoding='utf-8') as f:
        json.dump(current_data, f, indent=2, ensure_ascii=False)
    
    print(f"Extracted {len(episodes)} episodes from HTML file")
    print(f"Total episodes in movies.json: {len(current_data['episodes'])}")
    
    # Print first few episodes for verification
    print("\nFirst 5 episodes:")
    for episode in episodes[:5]:
        print(f"Episode {episode['episode_number']}: {episode['title']}")
        print(f"  Movie: {episode['movies'][0]['title']} ({episode['movies'][0]['year']})")

if __name__ == "__main__":
    main() 