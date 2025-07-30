#!/usr/bin/env python3
"""
Clean up movies.json file to remove duplicates, ensure proper episode references,
and sort from oldest to newest.
"""

import json
import re
from typing import List, Dict, Any
from datetime import datetime

def clean_episode_data(episodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Clean and deduplicate episode data."""
    # Track seen episodes to avoid duplicates
    seen_episodes = set()
    cleaned_episodes = []
    
    for episode in episodes:
        # Create a unique key for deduplication
        episode_key = f"{episode['episode_number']}_{episode['title']}"
        
        if episode_key not in seen_episodes:
            seen_episodes.add(episode_key)
            
            # Clean up the episode data
            cleaned_episode = {
                "episode_number": episode["episode_number"],
                "title": clean_episode_title(episode["title"]),
                "air_date": episode["air_date"],
                "description": clean_description(episode["description"]),
                "movies": clean_movies_list(episode["movies"], episode["episode_number"])
            }
            
            cleaned_episodes.append(cleaned_episode)
    
    return cleaned_episodes

def clean_episode_title(title: str) -> str:
    """Clean up episode titles."""
    # Remove extra whitespace
    title = title.strip()
    
    # Remove redundant prefixes/suffixes
    title = re.sub(r'\s*\(LIVE!\)\s*', '', title)
    title = re.sub(r'\s*\(Vault Release\)\s*', '', title)
    title = re.sub(r'\s*\(Watch-Along\)\s*', '', title)
    
    return title

def clean_description(description: str) -> str:
    """Clean up episode descriptions."""
    # Remove redundant descriptions
    if description.startswith("Episode discussing"):
        return description
    
    # Extract movie title from description if possible
    movie_match = re.search(r'discussing\s+(.+)', description)
    if movie_match:
        movie_title = movie_match.group(1)
        return f"Episode discussing {movie_title}"
    
    return description

def clean_movies_list(movies: List[Dict[str, Any]], episode_number: int) -> List[Dict[str, Any]]:
    """Clean up movies list and ensure proper episode references."""
    cleaned_movies = []
    
    for movie in movies:
        # Clean movie title
        movie_title = clean_movie_title(movie["title"])
        
        # Ensure we have a valid year
        year = movie.get("year", 2024)
        if not isinstance(year, int) or year < 1900 or year > 2030:
            year = 2024
        
        cleaned_movie = {
            "title": movie_title,
            "year": year,
            "imdb_id": movie.get("imdb_id", ""),
            "notes": f"Main movie discussed in Episode {episode_number}",
            "episode_reference": episode_number
        }
        
        cleaned_movies.append(cleaned_movie)
    
    return cleaned_movies

def clean_movie_title(title: str) -> str:
    """Clean up movie titles."""
    # Remove extra whitespace
    title = title.strip()
    
    # Fix common title issues
    title_mapping = {
        "It's What's Inside": "It's What's Inside",
        "I Saw the TV Glow": "I Saw the TV Glow",
        "A Quiet Place: Day One": "A Quiet Place: Day One",
        "The Twilight Saga: Breaking Dawn - Part 1": "The Twilight Saga: Breaking Dawn - Part 1",
        "The Twilight Saga: Breaking Dawn - Part 2": "The Twilight Saga: Breaking Dawn - Part 2",
        "The Twilight Saga: New Moon": "The Twilight Saga: New Moon",
        "Speak No Evil (US Remake)": "Speak No Evil",
        "Halloween (2018)": "Halloween",
        "Evil Dead (2013)": "Evil Dead",
        "Inside (2007)": "Inside",
        "What Ever Happened to Baby Jane?": "What Ever Happened to Baby Jane?"
    }
    
    return title_mapping.get(title, title)

def sort_episodes_by_date(episodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Sort episodes from oldest to newest by air date."""
    def parse_date(date_str: str) -> datetime:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            # If date parsing fails, use a default date
            return datetime(2024, 1, 1)
    
    return sorted(episodes, key=lambda x: parse_date(x["air_date"]))

def update_episode_numbers(episodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Update episode numbers to be sequential from 1."""
    for i, episode in enumerate(episodes, 1):
        episode["episode_number"] = i
        # Update movie notes to reflect new episode number
        for movie in episode["movies"]:
            movie["notes"] = f"Main movie discussed in Episode {i}"
            movie["episode_reference"] = i
    
    return episodes

def main():
    """Main function to clean up movies.json."""
    # Read current movies.json
    with open('data/movies.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Original episodes: {len(data['episodes'])}")
    
    # Clean up episodes
    cleaned_episodes = clean_episode_data(data['episodes'])
    print(f"After deduplication: {len(cleaned_episodes)}")
    
    # Sort from oldest to newest
    sorted_episodes = sort_episodes_by_date(cleaned_episodes)
    print(f"Sorted episodes: {len(sorted_episodes)}")
    
    # Update episode numbers to be sequential
    final_episodes = update_episode_numbers(sorted_episodes)
    
    # Update metadata
    data['episodes'] = final_episodes
    data['metadata']['total_episodes'] = len(final_episodes)
    data['metadata']['last_updated'] = datetime.now().strftime("%Y-%m-%d")
    data['metadata']['sort_order'] = "oldest_to_newest"
    
    # Write cleaned data
    with open('data/movies.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Final episodes: {len(final_episodes)}")
    print("Movies.json cleaned and sorted!")
    
    # Show sample of cleaned data
    print("\nSample episodes (first 5):")
    for episode in final_episodes[:5]:
        print(f"Episode {episode['episode_number']}: {episode['title']}")
        print(f"  Date: {episode['air_date']}")
        print(f"  Movie: {episode['movies'][0]['title']} ({episode['movies'][0]['year']})")
        print()
    
    print("\nSample episodes (last 5):")
    for episode in final_episodes[-5:]:
        print(f"Episode {episode['episode_number']}: {episode['title']}")
        print(f"  Date: {episode['air_date']}")
        print(f"  Movie: {episode['movies'][0]['title']} ({episode['movies'][0]['year']})")
        print()

if __name__ == "__main__":
    main() 