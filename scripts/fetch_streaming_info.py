#!/usr/bin/env python3
"""
Fetch streaming information for movies mentioned in podcast episodes.

This script reads from data/movies.json and fetches streaming availability
using Watchmode API (primary) with TMDB fallback. Results are saved to
data/streaming_data.json.

Required environment variables:
- WATCHMODE_API_KEY: API key from https://api.watchmode.com/
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
from urllib.parse import urlencode
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class StreamingInfoFetcher:
    """Fetches streaming availability data for movies."""
    
    def __init__(self):
        self.watchmode_api_key = os.getenv('WATCHMODE_API_KEY')
        self.tmdb_api_key = os.getenv('TMDB_API_KEY')
        
        if not self.watchmode_api_key:
            logger.warning("WATCHMODE_API_KEY not found. Watchmode features disabled.")
        if not self.tmdb_api_key:
            logger.warning("TMDB_API_KEY not found. TMDB features disabled.")
            
        self.watchmode_base_url = "https://api.watchmode.com/v1"
        self.tmdb_base_url = "https://api.themoviedb.org/3"
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 0.1  # 100ms between requests
        
    def _rate_limit(self):
        """Ensure we don't exceed API rate limits."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            time.sleep(sleep_time)
            
        self.last_request_time = time.time()
    
    def search_movie_watchmode(self, title: str, year: int) -> Optional[Dict[str, Any]]:
        """Search for a movie using Watchmode API."""
        if not self.watchmode_api_key:
            return None
            
        self._rate_limit()
        
        try:
            # Search by name
            params = {
                'apiKey': self.watchmode_api_key,
                'search_field': 'name',
                'search_value': title,
                'types': 'movie'
            }
            
            url = f"{self.watchmode_base_url}/search/"
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            title_results = data.get('title_results', [])
            
            # Find exact year match
            for movie in title_results:
                if movie.get('year') == year and movie.get('type') == 'movie':
                    logger.info(f"Found {title} ({year}) on Watchmode: ID {movie['id']}")
                    return movie
                    
            logger.warning(f"No exact year match for {title} ({year}) on Watchmode")
            return None
            
        except requests.RequestException as e:
            logger.error(f"Watchmode search failed for {title}: {e}")
            return None
    
    def get_streaming_sources_watchmode(self, movie_id: int) -> List[Dict[str, Any]]:
        """Get streaming sources for a movie from Watchmode."""
        if not self.watchmode_api_key:
            return []
            
        self._rate_limit()
        
        try:
            params = {
                'apiKey': self.watchmode_api_key,
                'regions': 'US'  # Focus on US for now
            }
            
            url = f"{self.watchmode_base_url}/title/{movie_id}/sources/"
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            sources = response.json()
            logger.info(f"Found {len(sources)} streaming sources for movie ID {movie_id}")
            return sources
            
        except requests.RequestException as e:
            logger.error(f"Failed to get streaming sources for movie ID {movie_id}: {e}")
            return []
    
    def search_movie_tmdb(self, title: str, year: int) -> Optional[Dict[str, Any]]:
        """Search for a movie using TMDB API as fallback."""
        if not self.tmdb_api_key:
            return None
            
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
                movie = results[0]  # Take first result
                logger.info(f"Found {title} ({year}) on TMDB: ID {movie['id']}")
                return movie
            else:
                logger.warning(f"No results for {title} ({year}) on TMDB")
                return None
                
        except requests.RequestException as e:
            logger.error(f"TMDB search failed for {title}: {e}")
            return None
    
    def get_watch_providers_tmdb(self, tmdb_id: int) -> List[Dict[str, Any]]:
        """Get watch providers from TMDB."""
        if not self.tmdb_api_key:
            return []
            
        self._rate_limit()
        
        try:
            params = {'api_key': self.tmdb_api_key}
            
            url = f"{self.tmdb_base_url}/movie/{tmdb_id}/watch/providers"
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            us_providers = data.get('results', {}).get('US', {})
            
            # Combine all provider types
            all_providers = []
            for provider_type in ['flatrate', 'rent', 'buy']:
                providers = us_providers.get(provider_type, [])
                for provider in providers:
                    provider['type'] = provider_type
                    all_providers.append(provider)
            
            logger.info(f"Found {len(all_providers)} watch providers for TMDB ID {tmdb_id}")
            return all_providers
            
        except requests.RequestException as e:
            logger.error(f"Failed to get watch providers for TMDB ID {tmdb_id}: {e}")
            return []
    
    def fetch_movie_streaming_info(self, movie: Dict[str, Any]) -> Dict[str, Any]:
        """Fetch streaming info for a single movie."""
        title = movie['title']
        year = movie['year']
        
        logger.info(f"Fetching streaming info for: {title} ({year})")
        
        result = {
            'title': title,
            'year': year,
            'imdb_id': movie.get('imdb_id'),
            'streaming_sources': [],
            'data_sources': [],
            'last_updated': time.strftime('%Y-%m-%d')
        }
        
        # Try Watchmode first
        watchmode_movie = self.search_movie_watchmode(title, year)
        if watchmode_movie:
            sources = self.get_streaming_sources_watchmode(watchmode_movie['id'])
            if sources:
                result['streaming_sources'].extend(sources)
                result['data_sources'].append('watchmode')
                result['watchmode_id'] = watchmode_movie['id']
        
        # Try TMDB as fallback or supplement
        tmdb_movie = self.search_movie_tmdb(title, year)
        if tmdb_movie:
            providers = self.get_watch_providers_tmdb(tmdb_movie['id'])
            if providers:
                # Convert TMDB format to match our schema
                tmdb_sources = []
                for provider in providers:
                    tmdb_source = {
                        'source_id': provider['provider_id'],
                        'name': provider['provider_name'],
                        'type': provider['type'],
                        'region': 'US',
                        'web_url': None,  # TMDB doesn't provide direct links
                        'logo_url': f"https://image.tmdb.org/t/p/original{provider['logo_path']}"
                    }
                    tmdb_sources.append(tmdb_source)
                
                result['streaming_sources'].extend(tmdb_sources)
                result['data_sources'].append('tmdb')
                result['tmdb_id'] = tmdb_movie['id']
        
        logger.info(f"Found {len(result['streaming_sources'])} total sources for {title}")
        return result
    
    def load_movies_data(self) -> Dict[str, Any]:
        """Load movies data from JSON file."""
        try:
            with open('data/movies.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error("data/movies.json not found. Please create this file first.")
            sys.exit(1)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in data/movies.json: {e}")
            sys.exit(1)
    
    def save_streaming_data(self, data: Dict[str, Any]):
        """Save streaming data to JSON file."""
        os.makedirs('data', exist_ok=True)
        
        with open('data/streaming_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info("Streaming data saved to data/streaming_data.json")
    
    def run(self):
        """Main execution function."""
        logger.info("Starting streaming info fetch process...")
        
        # Load input data
        movies_data = self.load_movies_data()
        episodes = movies_data.get('episodes', [])
        
        # Process all movies
        streaming_data = {
            'episodes': [],
            'metadata': {
                'podcast_name': movies_data.get('metadata', {}).get('podcast_name', 'Unknown'),
                'last_updated': time.strftime('%Y-%m-%d %H:%M:%S'),
                'total_movies_processed': 0,
                'apis_used': []
            }
        }
        
        total_movies = 0
        
        for episode in episodes:
            episode_streaming = {
                'episode_number': episode['episode_number'],
                'title': episode['title'],
                'air_date': episode['air_date'],
                'description': episode['description'],
                'movies': []
            }
            
            for movie in episode.get('movies', []):
                movie_streaming_info = self.fetch_movie_streaming_info(movie)
                episode_streaming['movies'].append(movie_streaming_info)
                total_movies += 1
                
                # Small delay between movies to be respectful
                time.sleep(0.5)
            
            streaming_data['episodes'].append(episode_streaming)
        
        # Update metadata
        streaming_data['metadata']['total_movies_processed'] = total_movies
        if self.watchmode_api_key:
            streaming_data['metadata']['apis_used'].append('watchmode')
        if self.tmdb_api_key:
            streaming_data['metadata']['apis_used'].append('tmdb')
        
        # Save results
        self.save_streaming_data(streaming_data)
        
        logger.info(f"Process complete! Processed {total_movies} movies across {len(episodes)} episodes.")


def main():
    """Main entry point."""
    fetcher = StreamingInfoFetcher()
    
    # Check for required API keys
    if not fetcher.watchmode_api_key and not fetcher.tmdb_api_key:
        logger.error("No API keys found. Please set WATCHMODE_API_KEY and/or TMDB_API_KEY environment variables.")
        logger.info("Get Watchmode API key: https://api.watchmode.com/")
        logger.info("Get TMDB API key: https://www.themoviedb.org/settings/api")
        sys.exit(1)
    
    fetcher.run()


if __name__ == "__main__":
    main() 