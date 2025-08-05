#!/usr/bin/env python3
"""
Cache movie posters from TMDB during build time to avoid runtime API calls.
This downloads posters once during CI/CD and serves them from GitHub Pages.
"""

import json
import logging
import os
import requests
import time
from pathlib import Path
from typing import Dict, List, Any
from urllib.parse import urlparse
import hashlib

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PosterCacheManager:
    def __init__(self):
        self.tmdb_api_key = None
        self.tmdb_base_url = "https://api.themoviedb.org/3"
        self.tmdb_poster_base_url = "https://image.tmdb.org/t/p"
        self.cache_dir = Path("output/posters")
        self.cache_manifest = "output/poster_manifest.json"
        self.movies_data = None
        self.streaming_data = None
        self._load_tmdb_config()
        
    def _load_tmdb_config(self):
        """Load TMDB API configuration."""
        # Try to load from .env file first
        env_file = Path('.env')
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key] = value
        
        # Get API key from environment
        self.tmdb_api_key = os.getenv('TMDB_API_KEY')
        
        if self.tmdb_api_key:
            logger.info("TMDB API key loaded - poster caching enabled")
        else:
            logger.warning("No TMDB API key found - skipping poster caching")
            
    def load_data(self):
        """Load movie and streaming data."""
        try:
            with open('data/movies.json', 'r', encoding='utf-8') as f:
                self.movies_data = json.load(f)
            logger.info("Loaded movie data successfully")
            
            with open('data/streaming_data.json', 'r', encoding='utf-8') as f:
                self.streaming_data = json.load(f)
            logger.info("Loaded streaming data successfully")
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
            
    def get_all_movies_with_tmdb_ids(self) -> List[Dict[str, Any]]:
        """Extract all movies with their TMDB IDs."""
        movies_with_ids = []
        
        # Create a lookup for TMDB IDs from streaming data
        tmdb_lookup = {}
        for episode_data in self.streaming_data.get("episodes", []):
            episode_num = episode_data["episode_number"]
            for movie in episode_data.get("movies", []):
                tmdb_id = movie.get("tmdb_id")
                if tmdb_id:
                    key = (episode_num, movie["title"].lower(), movie.get("year"))
                    tmdb_lookup[key] = tmdb_id
        
        # Process each episode and movie
        for episode in self.movies_data.get("episodes", []):
            episode_num = episode["episode_number"]
            
            for movie in episode.get("movies", []):
                movie_title = movie["title"]
                movie_year = movie.get("year")
                
                # Look up TMDB ID
                key = (episode_num, movie_title.lower(), movie_year)
                tmdb_id = tmdb_lookup.get(key)
                
                if tmdb_id:
                    movie_info = {
                        "title": movie_title,
                        "year": movie_year,
                        "episode": episode_num,
                        "tmdb_id": tmdb_id
                    }
                    movies_with_ids.append(movie_info)
        
        # Remove duplicates based on TMDB ID
        seen_ids = set()
        unique_movies = []
        for movie in movies_with_ids:
            if movie["tmdb_id"] not in seen_ids:
                seen_ids.add(movie["tmdb_id"])
                unique_movies.append(movie)
        
        logger.info(f"Found {len(unique_movies)} unique movies with TMDB IDs")
        return unique_movies
        
    def create_cache_directory(self):
        """Create poster cache directory."""
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Cache directory created: {self.cache_dir}")
        
    def get_poster_filename(self, tmdb_id: int, size: str = "w500") -> str:
        """Generate a safe filename for cached poster."""
        return f"{tmdb_id}_{size}.jpg"
        
    def download_poster(self, tmdb_id: int, title: str, sizes: List[str] = ["w342", "w500", "w780"]) -> Dict[str, str]:
        """Download movie poster in multiple sizes."""
        if not self.tmdb_api_key:
            return {}
            
        try:
            # Get movie details from TMDB
            url = f"{self.tmdb_base_url}/movie/{tmdb_id}"
            response = requests.get(url, params={'api_key': self.tmdb_api_key}, timeout=10)
            
            if response.status_code == 200:
                movie_data = response.json()
                poster_path = movie_data.get('poster_path')
                
                if not poster_path:
                    logger.warning(f"No poster path for {title} (TMDB ID: {tmdb_id})")
                    return {}
                
                cached_posters = {}
                
                for size in sizes:
                    poster_url = f"{self.tmdb_poster_base_url}/{size}{poster_path}"
                    filename = self.get_poster_filename(tmdb_id, size)
                    file_path = self.cache_dir / filename
                    
                    # Skip if already cached
                    if file_path.exists():
                        cached_posters[size] = f"posters/{filename}"
                        continue
                    
                    # Download poster
                    try:
                        poster_response = requests.get(poster_url, timeout=15)
                        if poster_response.status_code == 200:
                            with open(file_path, 'wb') as f:
                                f.write(poster_response.content)
                            cached_posters[size] = f"posters/{filename}"
                            logger.info(f"Cached {size} poster for {title}")
                        else:
                            logger.warning(f"Failed to download {size} poster for {title}: {poster_response.status_code}")
                    except Exception as e:
                        logger.error(f"Error downloading {size} poster for {title}: {e}")
                
                # Rate limiting - be respectful to TMDB
                time.sleep(0.1)  # 100ms delay between requests
                
                return cached_posters
            else:
                logger.warning(f"Failed to get movie data for {title} (TMDB ID: {tmdb_id}): {response.status_code}")
                return {}
                
        except Exception as e:
            logger.error(f"Error fetching poster for {title}: {e}")
            return {}
            
    def cache_all_posters(self):
        """Cache all movie posters."""
        if not self.tmdb_api_key:
            logger.warning("No TMDB API key - skipping poster caching")
            return {}
            
        movies = self.get_all_movies_with_tmdb_ids()
        poster_manifest = {}
        
        self.create_cache_directory()
        
        logger.info(f"Starting to cache posters for {len(movies)} movies...")
        
        for i, movie in enumerate(movies):
            title = movie["title"]
            tmdb_id = movie["tmdb_id"]
            year = movie["year"]
            
            logger.info(f"Processing {i+1}/{len(movies)}: {title} ({year})")
            
            cached_posters = self.download_poster(tmdb_id, title)
            
            if cached_posters:
                poster_manifest[tmdb_id] = {
                    "title": title,
                    "year": year,
                    "posters": cached_posters,
                    "cache_date": time.strftime("%Y-%m-%d %H:%M:%S")
                }
            
            # Progress logging
            if (i + 1) % 10 == 0:
                logger.info(f"Progress: {i+1}/{len(movies)} movies processed")
        
        # Save manifest
        self.save_poster_manifest(poster_manifest)
        
        logger.info(f"Poster caching complete! Cached {len(poster_manifest)} movie posters")
        return poster_manifest
        
    def save_poster_manifest(self, manifest: Dict[str, Any]):
        """Save poster manifest file."""
        try:
            with open(self.cache_manifest, 'w', encoding='utf-8') as f:
                json.dump(manifest, f, indent=2, ensure_ascii=False)
            logger.info(f"Poster manifest saved: {self.cache_manifest}")
        except Exception as e:
            logger.error(f"Error saving poster manifest: {e}")
            
    def load_poster_manifest(self) -> Dict[str, Any]:
        """Load existing poster manifest."""
        try:
            if Path(self.cache_manifest).exists():
                with open(self.cache_manifest, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"Could not load poster manifest: {e}")
        return {}
        
    def cleanup_old_posters(self, days: int = 30):
        """Remove cached posters older than specified days."""
        if not self.cache_dir.exists():
            return
            
        cutoff_time = time.time() - (days * 24 * 60 * 60)
        cleaned_count = 0
        
        for poster_file in self.cache_dir.glob("*.jpg"):
            if poster_file.stat().st_mtime < cutoff_time:
                poster_file.unlink()
                cleaned_count += 1
                
        if cleaned_count > 0:
            logger.info(f"Cleaned up {cleaned_count} old poster files")

def main():
    """Main function."""
    logger.info("Starting poster caching process...")
    
    cache_manager = PosterCacheManager()
    cache_manager.load_data()
    
    # Clean up old posters (older than 30 days)
    cache_manager.cleanup_old_posters(30)
    
    # Cache all posters
    manifest = cache_manager.cache_all_posters()
    
    logger.info(f"Poster caching completed! Total cached: {len(manifest)} movies")

if __name__ == "__main__":
    main()