#!/usr/bin/env python3
"""
Test version of the streaming fetcher with mock data.
This script tests the incremental update logic without requiring API keys.
"""

import json
import os
import sys
import time
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TestStreamingInfoFetcher:
    """Test version with mock data to validate incremental update logic."""
    
    def __init__(self):
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
    
    def create_mock_streaming_data(self, movie_title: str, year: int) -> Dict[str, Any]:
        """Create mock streaming data for testing."""
        self._rate_limit()
        
        # Simulate API delay
        time.sleep(0.1)
        
        # Create mock streaming sources
        streaming_sources = []
        
        # Add some mock providers based on movie type
        if "horror" in movie_title.lower() or year < 2000:
            streaming_sources.extend([
                {
                    'name': 'Shudder',
                    'type': 'subscription',
                    'region': 'US',
                    'web_url': 'https://www.shudder.com',
                    'logo_url': 'https://logo.clearbit.com/shudder.com'
                },
                {
                    'name': 'Tubi',
                    'type': 'free',
                    'region': 'US',
                    'web_url': 'https://www.tubi.tv',
                    'logo_url': 'https://logo.clearbit.com/tubi.tv'
                }
            ])
        else:
            streaming_sources.extend([
                {
                    'name': 'Netflix',
                    'type': 'subscription',
                    'region': 'US',
                    'web_url': 'https://www.netflix.com',
                    'logo_url': 'https://logo.clearbit.com/netflix.com'
                },
                {
                    'name': 'Amazon Prime',
                    'type': 'subscription',
                    'region': 'US',
                    'web_url': 'https://www.amazon.com',
                    'logo_url': 'https://logo.clearbit.com/amazon.com'
                }
            ])
        
        return {
            "title": movie_title,
            "year": year,
            "imdb_id": "",
            "streaming_sources": streaming_sources,
            "data_sources": ["mock"],
            "last_updated": datetime.now().strftime("%Y-%m-%d"),
            "tmdb_id": f"mock_{hash(movie_title) % 10000}"
        }
    
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
            
            # Create mock streaming data
            updated_movie = self.create_mock_streaming_data(movie["title"], movie["year"])
            
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
            "apis_used": ["mock"],
            "update_strategy": "incremental_with_caching"
        }
        
        # Save updated data
        self.save_streaming_data(self.streaming_data)
    
    def run(self):
        """Main execution function."""
        logger.info("Starting streaming data fetch with smart updates (TEST MODE)...")
        
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
        logger.info(f"Mock API calls made: {total_api_calls}")
        logger.info(f"Remaining daily TMDB calls: {1000 - total_api_calls}")


def main():
    """Main entry point."""
    fetcher = TestStreamingInfoFetcher()
    fetcher.run()


if __name__ == "__main__":
    main() 