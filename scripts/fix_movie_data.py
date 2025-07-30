#!/usr/bin/env python3
"""
Fix movie titles and years in the cleaned movies.json file.
"""

import json
from typing import Dict, Any

def fix_movie_titles_and_years() -> Dict[str, Any]:
    """Fix movie titles and years with correct data."""
    # Correct movie data mapping
    movie_corrections = {
        "MIDSOMMAR": {"title": "Midsommar", "year": 2019},
        "THE WITCH": {"title": "The Witch", "year": 2015},
        "THE EVIL DEAD": {"title": "The Evil Dead", "year": 1981},
        "IT": {"title": "It", "year": 2017},
        "IT CHAPTER TWO": {"title": "It Chapter Two", "year": 2019},
        "FINAL DESTINATION: BLOODLINES": {"title": "Final Destination: Bloodlines", "year": 2024},
        "M3GAN 2.0": {"title": "M3GAN 2.0", "year": 2025},
        "28 YEARS LATER": {"title": "28 Years Later", "year": 2025},
        "Titan: The OceanGate Disaster": {"title": "Titan: The OceanGate Disaster", "year": 2024},
        "The Ritual": {"title": "The Ritual", "year": 2017},
        "American Psycho": {"title": "American Psycho", "year": 2000},
        "Oddity": {"title": "Oddity", "year": 2024},
        "They Live": {"title": "They Live", "year": 1988},
        "28 Weeks Later": {"title": "28 Weeks Later", "year": 2007},
        "The Loved Ones": {"title": "The Loved Ones", "year": 2009},
        "The Hole": {"title": "The Hole", "year": 2009},
        "Sinners": {"title": "Sinners", "year": 2024},
        "Dogtooth": {"title": "Dogtooth", "year": 2009},
        "Drop": {"title": "Drop", "year": 2024},
        "Beetlejuice": {"title": "Beetlejuice", "year": 1988},
        "The Blackening": {"title": "The Blackening", "year": 2022},
        "Hell of a Summer": {"title": "Hell of a Summer", "year": 2024},
        "Mads": {"title": "Mads", "year": 2024},
        "The Love Witch": {"title": "The Love Witch", "year": 2016},
        "Leprechaun 2": {"title": "Leprechaun 2", "year": 1994},
        "The Monkey": {"title": "The Monkey", "year": 2024},
        "Sunshine": {"title": "Sunshine", "year": 2007},
        "What Ever Happened to Baby Jane?": {"title": "What Ever Happened to Baby Jane?", "year": 1962},
        "Evil Dead": {"title": "Evil Dead", "year": 2013},
        "Death Becomes Her": {"title": "Death Becomes Her", "year": 1992},
        "Ganja & Hess": {"title": "Ganja & Hess", "year": 1973},
        "The Haunting in Connecticut": {"title": "The Haunting in Connecticut", "year": 2009},
        "The Innocents": {"title": "The Innocents", "year": 1961},
        "The Slumber Party Massacre": {"title": "The Slumber Party Massacre", "year": 1982},
        "It's What's Inside": {"title": "It's What's Inside", "year": 2024},
        "Nosferatu": {"title": "Nosferatu", "year": 1922},
        "The Neon Demon": {"title": "The Neon Demon", "year": 2016},
        "Immaculate": {"title": "Immaculate", "year": 2024},
        "Inside": {"title": "Inside", "year": 2007},
        "The Nightmare Before Christmas": {"title": "The Nightmare Before Christmas", "year": 1993},
        "Single White Female": {"title": "Single White Female", "year": 1992},
        "Red Eye": {"title": "Red Eye", "year": 2005},
        "Heretic": {"title": "Heretic", "year": 2024},
        "Smile 2": {"title": "Smile 2", "year": 2024},
        "Your Monster": {"title": "Your Monster", "year": 2024},
        "Terrifier 3": {"title": "Terrifier 3", "year": 2024},
        "The Substance": {"title": "The Substance", "year": 2024},
        "Speak No Evil": {"title": "Speak No Evil", "year": 2024},
        "Halloween": {"title": "Halloween", "year": 2018},
        "Titanic": {"title": "Titanic", "year": 1997},
        "Bone Tomahawk": {"title": "Bone Tomahawk", "year": 2015},
        "Sleepy Hollow": {"title": "Sleepy Hollow", "year": 1999},
        "Cam": {"title": "Cam", "year": 2018},
        "The Reef": {"title": "The Reef", "year": 2010},
        "Alien: Romulus": {"title": "Alien: Romulus", "year": 2024},
        "Cuckoo": {"title": "Cuckoo", "year": 2024},
        "Twisters": {"title": "Twisters", "year": 2024},
        "Trap": {"title": "Trap", "year": 2024},
        "Longlegs": {"title": "Longlegs", "year": 2024},
        "A Quiet Place: Day One": {"title": "A Quiet Place: Day One", "year": 2024},
        "MaXXXine": {"title": "MaXXXine", "year": 2024},
        "The Devil's Bath": {"title": "The Devil's Bath", "year": 2024},
        "The First Omen": {"title": "The First Omen", "year": 2024},
        "Abigail": {"title": "Abigail", "year": 2024},
        "In a Violent Nature": {"title": "In a Violent Nature", "year": 2024},
        "I Saw the TV Glow": {"title": "I Saw the TV Glow", "year": 2024},
        "Night Swim": {"title": "Night Swim", "year": 2024},
        "The Twilight Saga: Breaking Dawn - Part 2": {"title": "The Twilight Saga: Breaking Dawn - Part 2", "year": 2012},
        "The Twilight Saga: New Moon": {"title": "The Twilight Saga: New Moon", "year": 2009},
        "Rear Window": {"title": "Rear Window", "year": 1954},
        "Splice": {"title": "Splice", "year": 2009},
        "Alone": {"title": "Alone", "year": 2020},
        "Ex Machina": {"title": "Ex Machina", "year": 2014},
        "The Fog": {"title": "The Fog", "year": 1980},
        "The Twilight Saga: Breaking Dawn - Part 1": {"title": "The Twilight Saga: Breaking Dawn - Part 1", "year": 2011},
        "Late Night with the Devil": {"title": "Late Night with the Devil", "year": 2023},
        "Revenge": {"title": "Revenge", "year": 2017},
        "Donnie Darko": {"title": "Donnie Darko", "year": 2001},
        "Joy Ride": {"title": "Joy Ride", "year": 2023}
    }
    
    return movie_corrections

def main():
    """Main function to fix movie data."""
    # Read current movies.json
    with open('data/movies.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Get corrections
    corrections = fix_movie_titles_and_years()
    
    # Fix each episode
    for episode in data['episodes']:
        for movie in episode['movies']:
            current_title = movie['title']
            
            # Check if we have a correction for this movie
            if current_title in corrections:
                correction = corrections[current_title]
                movie['title'] = correction['title']
                movie['year'] = correction['year']
                print(f"Fixed: {current_title} -> {correction['title']} ({correction['year']})")
            elif current_title.upper() in corrections:
                correction = corrections[current_title.upper()]
                movie['title'] = correction['title']
                movie['year'] = correction['year']
                print(f"Fixed: {current_title} -> {correction['title']} ({correction['year']})")
    
    # Write corrected data
    with open('data/movies.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\nFixed {len(data['episodes'])} episodes")
    print("Movies.json corrected!")

if __name__ == "__main__":
    main() 