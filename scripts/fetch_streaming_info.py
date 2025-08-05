#!/usr/bin/env python3
"""
Fetch streaming information for movies mentioned in podcast episodes.

This script reads from data/movies.json and fetches streaming availability
using TMDB API with smart incremental updates and caching. Results are saved to
data/streaming_data.json.

Required environment variables:
- TMDB_API_KEY: API key from https://www.themoviedb.org/settings/api

Usage:
    python scripts/fetch_streaming_info.py
"""

import json
import os
import sys
import time
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class StreamingInfoFetcher:
    """Fetches streaming availability data for movies with smart caching."""
    
    def __init__(self):
        # Load API keys
        self.tmdb_api_key = os.getenv('TMDB_API_KEY')
        self.watchmode_api_key = os.getenv('WATCHMODE_API_KEY')

        # Validate at least one provider key is available
        if not self.tmdb_api_key and not self.watchmode_api_key:
            logger.error("Neither WATCHMODE_API_KEY nor TMDB_API_KEY found. Please set at least one of them.")
            sys.exit(1)

        if self.watchmode_api_key:
            logger.info("Watchmode API key loaded – direct streaming links enabled")
        if self.tmdb_api_key:
            logger.info("TMDB API key loaded – fallback streaming data & posters enabled")
            
        self.tmdb_base_url = "https://api.themoviedb.org/3"
        
        # Rate limiting for TMDB (50 requests/second)
        self.last_request_time = 0
        self.min_request_interval = 0.02  # 20ms between requests (50 req/sec)
        
        # Caching settings
        self.cache_duration_days = 7
        self.movies_data = None
        self.streaming_data = None
        
    def _rate_limit(self):
        """Ensure we don't exceed API rate limits."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            time.sleep(sleep_time)
            
        self.last_request_time = time.time()
    
    def search_movie_tmdb(self, title: str, year: int) -> Optional[Dict[str, Any]]:
        """Search for a movie using TMDB API."""
        self._rate_limit()
        
        try:
            params = {
                'api_key': self.tmdb_api_key,
                'query': title,
                'year': year
            }
            
            url = f"{self.tmdb_base_url}/search/movie"
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            results = data.get('results', [])
            
            if results:
                # Return the first (best) match
                movie = results[0]
                logger.info(f"Found {title} ({year}) on TMDB: ID {movie['id']}")
                return movie
            else:
                logger.warning(f"No results found for {title} ({year}) on TMDB")
                return None
                
        except requests.RequestException as e:
            logger.error(f"TMDB search failed for {title}: {e}")
            return None
    
    def get_watch_providers_tmdb(self, tmdb_id: int) -> List[Dict[str, Any]]:
        """Get watch providers for a movie from TMDB."""
        self._rate_limit()
        
        try:
            params = {
                'api_key': self.tmdb_api_key,
                'watch_region': 'US'
            }
            
            url = f"{self.tmdb_base_url}/movie/{tmdb_id}/watch/providers"
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            results = data.get('results', {})
            us_providers = results.get('US', {})
            
            # Extract streaming sources
            streaming_sources = []
            
            # Free sources
            for provider in us_providers.get('free', []):
                streaming_sources.append({
                    'name': provider.get('provider_name', 'Unknown'),
                    'type': 'free',
                    'region': 'US',
                    'web_url': f"https://www.themoviedb.org/movie/{tmdb_id}/watch",
                    'logo_url': f"https://image.tmdb.org/t/p/original{provider.get('logo_path', '')}"
                })
            
            # Subscription sources
            for provider in us_providers.get('flatrate', []):
                streaming_sources.append({
                    'name': provider.get('provider_name', 'Unknown'),
                    'type': 'subscription',
                    'region': 'US',
                    'web_url': f"https://www.themoviedb.org/movie/{tmdb_id}/watch",
                    'logo_url': f"https://image.tmdb.org/t/p/original{provider.get('logo_path', '')}"
                })
            
            # Rent sources
            for provider in us_providers.get('rent', []):
                streaming_sources.append({
                    'name': provider.get('provider_name', 'Unknown'),
                    'type': 'rent',
                    'region': 'US',
                    'web_url': f"https://www.themoviedb.org/movie/{tmdb_id}/watch",
                    'logo_url': f"https://image.tmdb.org/t/p/original{provider.get('logo_path', '')}"
                })
            
            # Buy sources
            for provider in us_providers.get('buy', []):
                streaming_sources.append({
                    'name': provider.get('provider_name', 'Unknown'),
                    'type': 'buy',
                    'region': 'US',
                    'web_url': f"https://www.themoviedb.org/movie/{tmdb_id}/watch",
                    'logo_url': f"https://image.tmdb.org/t/p/original{provider.get('logo_path', '')}"
                })
            
            logger.info(f"Found {len(streaming_sources)} streaming sources for TMDB ID {tmdb_id}")
            return streaming_sources
            
        except requests.RequestException as e:
            logger.error(f"Failed to get watch providers for TMDB ID {tmdb_id}: {e}")
            return []
    
    # --------------------------- Watchmode integration ---------------------------
    def search_movie_watchmode(self, title: str, year: int) -> Optional[Dict[str, Any]]:
        """Search for a movie on Watchmode API and return the first matching result."""
        if not self.watchmode_api_key:
            return None
        try:
            params = {
                'apiKey': self.watchmode_api_key,
                'search_field': 'name',
                'search_value': title,
                'types': 'movie'
            }
            url = "https://api.watchmode.com/v1/search/"
            self._rate_limit()
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            for result in data.get('title_results', []):
                if year and result.get('year') and result['year'] != year:
                    continue
                logger.info(f"Found {title} ({year}) on Watchmode: ID {result['id']}")
                return result
        except Exception as e:
            logger.error(f"Watchmode search failed for {title}: {e}")
        return None

    def get_watch_providers_watchmode(self, watchmode_id: int) -> List[Dict[str, Any]]:
        """Get streaming sources for a title from Watchmode API (region = US)."""
        if not self.watchmode_api_key:
            return []
        try:
            params = {
                'apiKey': self.watchmode_api_key,
                'regions': 'US'
            }
            url = f"https://api.watchmode.com/v1/title/{watchmode_id}/sources/"
            self._rate_limit()
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            streaming_sources = []
            # Map Watchmode's type codes to our canonical names
            type_map = {
                'sub': 'subscription',
                'buy': 'buy',
                'rent': 'rent',
                'free': 'free'
            }
            for src in data:
                src_type = type_map.get(src.get('type'), src.get('type', 'unknown'))
                streaming_sources.append({
                    'name': src.get('name', 'Unknown'),
                    'type': src_type,
                    'region': src.get('region', 'US'),
                    'web_url': src.get('web_url') or src.get('ios_appstore_url') or src.get('android_playstore_url') or '',
                    'logo_url': src.get('logo_100px', '')
                })
            logger.info(f"Found {len(streaming_sources)} streaming sources for Watchmode ID {watchmode_id}")
            return streaming_sources
        except Exception as e:
            logger.error(f"Failed to get Watchmode sources for ID {watchmode_id}: {e}")
            return []

    def is_movie_recently_updated(self, movie_title: str, episode_number: int) -> bool:
        """Check if a movie was recently updated (within cache duration)."""
        if not self.streaming_data:
            return False
        
        for episode in self.streaming_data.get("episodes", []):
            if episode.get("episode_number") == episode_number:
                for movie in episode.get("movies", []):
                    if movie.get("title") == movie_title:
                        last_updated = movie.get("last_updated")
                        if last_updated:
                            try:
                                update_date = datetime.strptime(last_updated, "%Y-%m-%d")
                                days_since_update = (datetime.now() - update_date).days
                                return days_since_update < self.cache_duration_days
                            except ValueError:
                                return False
        return False
    
    def get_movies_to_update(self) -> List[Dict[str, Any]]:
        """Get list of movies that need updating (new or recently changed)."""
        movies_to_update = []
        
        for episode in self.movies_data.get("episodes", []):
            episode_number = episode["episode_number"]
            
            for movie in episode.get("movies", []):
                movie_title = movie["title"]
                
                # Check if movie needs updating
                if not self.is_movie_recently_updated(movie_title, episode_number):
                    movies_to_update.append({
                        "episode_number": episode_number,
                        "movie": movie
                    })
                    logger.info(f"Will update: {movie_title} (Episode {episode_number})")
                else:
                    logger.debug(f"Skipping (recently updated): {movie_title} (Episode {episode_number})")
        
        logger.info(f"Found {len(movies_to_update)} movies to update")
        return movies_to_update
    
    def fetch_movie_streaming_info(self, movie: Dict[str, Any], episode_number: int) -> Dict[str, Any]:
        """Fetch streaming availability for a single movie.
        Priority order:
        1. Watchmode (direct provider URLs)
        2. TMDB watch/providers (JustWatch aggregated page)
        This keeps TMDB as a fallback for completeness while giving users proper deep links when available.
        """
        title = movie.get("title", "Unknown")
        year = movie.get("year", "")

        watchmode_sources: List[Dict[str, Any]] = []
        tmdb_sources: List[Dict[str, Any]] = []
        watchmode_id = None
        tmdb_id = None

        # ---- Watchmode (preferred) ----
        if self.watchmode_api_key:
            wm_movie = self.search_movie_watchmode(title, year)
            if wm_movie:
                watchmode_id = wm_movie["id"]
                watchmode_sources = self.get_watch_providers_watchmode(watchmode_id)
                # Re-use TMDB ID if Watchmode returns it
                if wm_movie.get("tmdb_id") and not tmdb_id:
                    tmdb_id = wm_movie["tmdb_id"]

        # ---- TMDB fallback / supplement ----
        if self.tmdb_api_key and not tmdb_id:
            tmdb_movie = self.search_movie_tmdb(title, year)
            if tmdb_movie:
                tmdb_id = tmdb_movie["id"]

        if self.tmdb_api_key and tmdb_id:
            tmdb_sources = self.get_watch_providers_tmdb(tmdb_id)

        # Merge sources, preferring Watchmode versions where available
        streaming_sources = watchmode_sources or []
        if tmdb_sources:
            existing_keys = {(s.get("name"), s.get("type")) for s in streaming_sources}
            for src in tmdb_sources:
                key = (src.get("name"), src.get("type"))
                if key not in existing_keys:
                    streaming_sources.append(src)

        data_sources = []
        if watchmode_sources:
            data_sources.append("watchmode")
        if tmdb_sources:
            data_sources.append("tmdb")

        if not streaming_sources:
            logger.warning(f"No streaming data found for {title} ({year})")

        return {
            "title": title,
            "year": year,
            "imdb_id": movie.get("imdb_id", ""),
            "streaming_sources": streaming_sources,
            "data_sources": data_sources,
            "last_updated": datetime.now().strftime("%Y-%m-%d"),
            "tmdb_id": tmdb_id,
            "watchmode_id": watchmode_id
        }
    
    def load_movies_data(self) -> Dict[str, Any]:
        """Load movies data from JSON file."""
        try:
            with open('data/movies.json', 'r', encoding='utf-8') as f:
                self.movies_data = json.load(f)
            logger.info(f"Loaded {len(self.movies_data.get('episodes', []))} episodes")
            return self.movies_data
        except FileNotFoundError:
            logger.error("data/movies.json not found")
            sys.exit(1)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in movies.json: {e}")
            sys.exit(1)
    
    def load_streaming_data(self) -> Dict[str, Any]:
        """Load existing streaming data if available."""
        try:
            with open('data/streaming_data.json', 'r', encoding='utf-8') as f:
                self.streaming_data = json.load(f)
            logger.info("Loaded existing streaming data")
            return self.streaming_data
        except FileNotFoundError:
            logger.info("No existing streaming data found, will create new")
            self.streaming_data = {"episodes": [], "metadata": {}}
            return self.streaming_data
    
    def save_streaming_data(self, data: Dict[str, Any]):
        """Save streaming data to JSON file."""
        try:
            with open('data/streaming_data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info("Streaming data saved successfully")
        except Exception as e:
            logger.error(f"Error saving streaming data: {e}")
            raise
    
    def update_streaming_data(self, movies_to_update: List[Dict[str, Any]]):
        """Update streaming data for specific movies."""
        # Load existing data
        self.load_streaming_data()
        
        # Create episode lookup for existing data
        existing_episodes = {}
        for episode in self.streaming_data.get("episodes", []):
            existing_episodes[episode["episode_number"]] = episode
        
        # Update movies
        for item in movies_to_update:
            episode_number = item["episode_number"]
            movie = item["movie"]
            
            # Fetch new streaming data
            updated_movie = self.fetch_movie_streaming_info(movie, episode_number)
            
            # Update or create episode entry
            if episode_number in existing_episodes:
                # Update existing episode
                episode = existing_episodes[episode_number]
                # Find and update the specific movie
                for i, existing_movie in enumerate(episode.get("movies", [])):
                    if existing_movie.get("title") == movie["title"]:
                        episode["movies"][i] = updated_movie
                        break
                else:
                    # Movie not found, add it
                    episode["movies"].append(updated_movie)
            else:
                # Create new episode entry
                new_episode = {
                    "episode_number": episode_number,
                    "movies": [updated_movie]
                }
                existing_episodes[episode_number] = new_episode
        
        # Convert back to list and sort by episode number
        updated_episodes = list(existing_episodes.values())
        updated_episodes.sort(key=lambda x: x["episode_number"])
        
        # Update metadata
        self.streaming_data["episodes"] = updated_episodes
        self.streaming_data["metadata"] = {
            "podcast_name": "Too Scary; Didn't Watch",
            "last_updated": datetime.now().strftime("%Y-%m-%d"),
            "total_episodes": len(updated_episodes),
            "apis_used": ["tmdb"],
            "update_strategy": "incremental_with_caching"
        }
        
        # Save updated data
        self.save_streaming_data(self.streaming_data)
    
    def run(self):
        """Main execution function."""
        logger.info("Starting streaming data fetch with smart updates...")
        
        # Load movies data
        self.load_movies_data()
        
        # Get movies that need updating
        movies_to_update = self.get_movies_to_update()
        
        if not movies_to_update:
            logger.info("No movies need updating. All data is current.")
            return
        
        # Update streaming data
        self.update_streaming_data(movies_to_update)
        
        logger.info(f"Updated streaming data for {len(movies_to_update)} movies")
        
        # Log API usage statistics
        total_api_calls = len(movies_to_update) * 2  # 2 calls per movie (search + providers)
        logger.info(f"API calls made: {total_api_calls}")
        logger.info(f"Remaining daily TMDB calls: {1000 - total_api_calls}")


def main():
    """Main entry point."""
    fetcher = StreamingInfoFetcher()
    fetcher.run()


if __name__ == "__main__":
    main() 