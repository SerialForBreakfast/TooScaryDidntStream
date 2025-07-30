#!/usr/bin/env python3
"""
Generate HTML output for the movie streaming tracker.
"""

import json
import logging
import requests
from datetime import datetime
from typing import Dict, List, Any

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class HTMLGenerator:
    def __init__(self):
        self.movies_data = None
        self.streaming_data = None
        # TMDB API configuration - you can set this as an environment variable
        self.tmdb_api_key = None  # Set your TMDB API key here or use environment variable
        self.tmdb_base_url = "https://api.themoviedb.org/3"
        self.tmdb_poster_base_url = "https://image.tmdb.org/t/p"

    def configure_tmdb_api(self, api_key: str = None):
        """Configure TMDB API key for poster fetching."""
        if api_key:
            self.tmdb_api_key = api_key
            logger.info("TMDB API key configured")
        else:
            # Try to load from .env file first
            self._load_env_file()
            
            # Try to get from environment variable
            import os
            env_api_key = os.getenv('TMDB_API_KEY')
            if env_api_key:
                self.tmdb_api_key = env_api_key
                logger.info("TMDB API key loaded from environment variable")
            else:
                logger.warning("No TMDB API key provided. Posters will use placeholder images.")
                logger.info("To enable real movie posters, run: python scripts/setup_tmdb.py")

    def _load_env_file(self):
        """Load environment variables from .env file."""
        try:
            import os
            from pathlib import Path
            
            env_file = Path('.env')
            if env_file.exists():
                with open(env_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            os.environ[key] = value
                logger.info("Loaded environment variables from .env file")
        except Exception as e:
            logger.debug(f"Could not load .env file: {e}")

    def load_data(self):
        """Load movies and streaming data."""
        try:
            # Load movies data
            with open('data/movies.json', 'r', encoding='utf-8') as f:
                self.movies_data = json.load(f)
            
            # Load streaming data (optional)
            try:
                with open('data/streaming_data.json', 'r', encoding='utf-8') as f:
                    self.streaming_data = json.load(f)
                logger.info("Loaded streaming data successfully")
            except FileNotFoundError:
                logger.warning("streaming_data.json not found, using mock data")
                self.streaming_data = self.create_mock_streaming_data()
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise

    def create_mock_streaming_data(self) -> Dict[str, Any]:
        """Create mock streaming data for development."""
        mock_data = {"episodes": []}
        
        for episode in self.movies_data.get("episodes", []):
            episode_data = {
                "episode_number": episode["episode_number"],
                "movies": []
            }
            
            for movie in episode.get("movies", []):
                # Create varied mock streaming sources based on movie characteristics
                streaming_sources = []
                
                # Add different types of sources based on movie year/genre
                movie_year = movie.get("year", 2024)
                movie_title = movie.get("title", "").lower()
                
                # Free sources (more common for older movies)
                if movie_year < 2010 or "horror" in movie_title:
                    streaming_sources.append({
                        "name": "Tubi",
                        "type": "free",
                        "region": "US",
                        "web_url": "https://tubi.tv",
                        "logo_url": "https://logo.clearbit.com/tubi.tv"
                    })
                    streaming_sources.append({
                        "name": "Pluto TV",
                        "type": "free",
                        "region": "US",
                        "web_url": "https://pluto.tv",
                        "logo_url": "https://logo.clearbit.com/pluto.tv"
                    })
                
                # Subscription sources
                streaming_sources.append({
                    "name": "Netflix",
                    "type": "subscription",
                    "region": "US",
                    "web_url": "https://netflix.com",
                    "logo_url": "https://logo.clearbit.com/netflix.com"
                })
                
                if movie_year >= 2020:
                    streaming_sources.append({
                        "name": "HBO Max",
                        "type": "subscription",
                        "region": "US",
                        "web_url": "https://hbomax.com",
                        "logo_url": "https://logo.clearbit.com/hbomax.com"
                    })
                
                # Rent sources (for newer movies)
                if movie_year >= 2022:
                    streaming_sources.append({
                        "name": "iTunes",
                        "type": "rent",
                        "region": "US",
                        "web_url": "https://itunes.apple.com",
                        "logo_url": "https://logo.clearbit.com/itunes.apple.com"
                    })
                    streaming_sources.append({
                        "name": "Google Play",
                        "type": "rent",
                        "region": "US",
                        "web_url": "https://play.google.com",
                        "logo_url": "https://logo.clearbit.com/play.google.com"
                    })
                
                # Buy sources
                streaming_sources.append({
                    "name": "Amazon",
                    "type": "buy",
                    "region": "US",
                    "web_url": "https://amazon.com",
                    "logo_url": "https://logo.clearbit.com/amazon.com"
                })
                
                movie_data = {
                    "title": movie["title"],
                    "year": movie["year"],
                    "streaming_sources": streaming_sources,
                    "data_sources": ["mock"]
                }
                episode_data["movies"].append(movie_data)
            
            mock_data["episodes"].append(episode_data)
        
        return mock_data

    def find_streaming_data(self, episode_number: int, movie_title: str) -> List[Dict[str, Any]]:
        """Find streaming data for a specific movie."""
        if not self.streaming_data:
            return []
        
        for episode in self.streaming_data.get("episodes", []):
            if episode.get("episode_number") == episode_number:
                for movie in episode.get("movies", []):
                    if movie.get("title") == movie_title:
                        return movie.get("streaming_sources", [])
        
        return []

    def sort_streaming_sources(self, sources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Sort streaming sources by priority: Free > Subscription > Rent > Buy."""
        priority_order = {"free": 0, "subscription": 1, "rent": 2, "buy": 3}
        
        return sorted(sources, key=lambda x: priority_order.get(x.get("type", "").lower(), 4))

    def format_source_type(self, source_type: str) -> str:
        """Format source type for display."""
        return source_type.lower()

    def search_movie_on_tmdb(self, title: str, year: int) -> Dict[str, Any]:
        """Search for a movie on TMDB API."""
        if not self.tmdb_api_key:
            return None
        
        try:
            url = f"{self.tmdb_base_url}/search/movie"
            params = {
                'api_key': self.tmdb_api_key,
                'query': title,
                'year': year,
                'language': 'en-US'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data.get('results'):
                return data['results'][0]  # Return the first (most relevant) result
            
        except Exception as e:
            logger.warning(f"Error searching TMDB for '{title}': {e}")
        
        return None

    def get_movie_poster_url(self, movie_title: str, year: int) -> str:
        """Get movie poster URL from TMDB or return a placeholder."""
        # Try to get poster from TMDB
        movie_data = self.search_movie_on_tmdb(movie_title, year)
        
        if movie_data and movie_data.get('poster_path'):
            poster_path = movie_data['poster_path']
            # Use w500 size for good quality and reasonable file size
            return f"{self.tmdb_poster_base_url}/w500{poster_path}"
        
        # Fallback to a better placeholder with movie info
        encoded_title = movie_title.replace(' ', '+')
        return f"https://via.placeholder.com/500x750/2c3e50/ffffff?text={encoded_title}+({year})"

    def get_movie_poster_urls(self, movie_title: str, year: int) -> Dict[str, str]:
        """Get multiple poster sizes for responsive design."""
        movie_data = self.search_movie_on_tmdb(movie_title, year)
        
        poster_urls = {}
        
        if movie_data and movie_data.get('poster_path'):
            poster_path = movie_data['poster_path']
            # Multiple sizes for responsive design
            poster_urls = {
                'small': f"{self.tmdb_poster_base_url}/w185{poster_path}",
                'medium': f"{self.tmdb_poster_base_url}/w342{poster_path}",
                'large': f"{self.tmdb_poster_base_url}/w500{poster_path}",
                'original': f"{self.tmdb_poster_base_url}/original{poster_path}"
            }
        else:
            # Fallback placeholder
            encoded_title = movie_title.replace(' ', '+')
            placeholder_url = f"https://via.placeholder.com/500x750/2c3e50/ffffff?text={encoded_title}+({year})"
            poster_urls = {
                'small': placeholder_url,
                'medium': placeholder_url,
                'large': placeholder_url,
                'original': placeholder_url
            }
        
        return poster_urls

    def get_podcast_episode_url(self, episode_number: int) -> str:
        """Generate podcast episode URL based on episode number."""
        # Actual Apple Podcasts ID for "Too Scary; Didn't Watch"
        podcast_id = "1476552025"
        return f"https://podcasts.apple.com/us/podcast/too-scary-didnt-watch/id{podcast_id}?i=1000{episode_number:04d}"

    def generate_episode_sidebar(self) -> str:
        """Generate the episode sidebar with filtering."""
        episodes = self.movies_data.get("episodes", [])
        
        html = '''
        <div class="sidebar" id="sidebar">
            <div class="sidebar-header">
                <h3>Episodes</h3>
                <button id="toggle-sidebar" class="toggle-sidebar-btn">
                    <span class="toggle-icon">◀</span>
                    <span class="toggle-text">Hide Sidebar</span>
                </button>
            </div>
            
            <div class="filter-section">
                <h4>Streaming Filters</h4>
                <div class="streaming-filter">
                    <label>Show movies available on:</label>
                    <div class="service-checkboxes">
                        <label class="checkbox-item">
                            <input type="checkbox" value="netflix" checked> Netflix
                        </label>
                        <label class="checkbox-item">
                            <input type="checkbox" value="hbo" checked> HBO Max
                        </label>
                        <label class="checkbox-item">
                            <input type="checkbox" value="tubi" checked> Tubi
                        </label>
                        <label class="checkbox-item">
                            <input type="checkbox" value="amazon" checked> Amazon
                        </label>
                        <label class="checkbox-item">
                            <input type="checkbox" value="itunes" checked> iTunes
                        </label>
                        <label class="checkbox-item">
                            <input type="checkbox" value="google" checked> Google Play
                        </label>
                        <label class="checkbox-item">
                            <input type="checkbox" value="pluto" checked> Pluto TV
                        </label>
                    </div>
                    <div class="free-filter">
                        <label class="checkbox-item">
                            <input type="checkbox" id="free-only" value="free"> Free only
                        </label>
                    </div>
                    <button id="apply-filter" class="filter-button">Apply Filter</button>
                    <button id="clear-filter" class="filter-button secondary">Clear All</button>
                </div>
            </div>
            
            <div class="search-section">
                <div class="search-container">
                    <input type="text" id="episode-filter" placeholder="Search episodes..." class="episode-search">
                    <div class="search-icon">🔍</div>
                </div>
            </div>
            
            <div class="episode-list" id="episode-list">
        '''
        
        # Group episodes by first letter
        episodes_by_letter = {}
        for episode in episodes:
            title = episode["title"]
            first_letter = title[0].upper() if title else "Other"
            if first_letter not in episodes_by_letter:
                episodes_by_letter[first_letter] = []
            episodes_by_letter[first_letter].append(episode)
        
        # Sort letters alphabetically
        sorted_letters = sorted(episodes_by_letter.keys())
        
        for letter in sorted_letters:
            html += f'<div class="letter-section" data-letter="{letter}">'
            html += f'<div class="letter-header">{letter}</div>'
            
            # Get episodes for this letter
            letter_episodes = episodes_by_letter[letter]
            letter_episodes.sort(key=lambda x: x["title"])
            
            for episode in letter_episodes:
                episode_number = episode["episode_number"]
                title = episode["title"]
                air_date = episode["air_date"]
                
                html += f'''
                <div class="episode-item" data-episode="{episode_number}" data-title="{title.lower()}" data-date="{air_date}">
                    <div class="episode-number">#{episode_number}</div>
                    <div class="episode-info">
                        <div class="episode-title">{title}</div>
                        <div class="episode-date">{air_date}</div>
                    </div>
                </div>
                '''
            
            html += '</div>'
        
        html += '''
            </div>
        </div>
        '''
        
        return html

    def generate_movie_html(self, movie: Dict[str, Any], episode_number: int) -> str:
        """Generate HTML for a single movie."""
        title = movie.get("title", "Unknown")
        year = movie.get("year", "")
        imdb_id = movie.get("imdb_id", "")
        notes = movie.get("notes", "")
        
        # Get movie poster URLs for responsive design
        poster_urls = self.get_movie_poster_urls(title, year)
        
        # Find streaming data
        streaming_sources = self.find_streaming_data(episode_number, title)
        
        html = f'''
        <div class="movie">
            <div class="movie-content">
                <div class="movie-poster">
                    <picture class="poster-container">
                        <source media="(min-width: 768px)" srcset="{poster_urls['large']}">
                        <source media="(min-width: 480px)" srcset="{poster_urls['medium']}">
                        <img src="{poster_urls['small']}" alt="{title} poster" class="poster-image" 
                             loading="lazy" onerror="this.style.display='none'">
                    </picture>
                </div>
                <div class="movie-details">
                    <div class="movie-header">
                        <h4>{title} ({year})</h4>
                        {f'<div class="imdb-link"><a href="https://www.imdb.com/title/{imdb_id}" target="_blank">IMDB</a></div>' if imdb_id else ''}
                    </div>
                    <div class="movie-notes">{notes}</div>
        '''
        
        # Streaming sources organized by type
        if streaming_sources:
            # Sort sources by priority
            sorted_sources = self.sort_streaming_sources(streaming_sources)

            # Group sources by type
            sources_by_type = {}
            for source in sorted_sources:
                source_type = self.format_source_type(source.get('type', ''))
                if source_type not in sources_by_type:
                    sources_by_type[source_type] = []
                sources_by_type[source_type].append(source)

            html += '<div class="streaming-sources">'

            # Display sections in priority order
            priority_order = ['free', 'subscription', 'rent', 'buy']

            for source_type in priority_order:
                if source_type in sources_by_type:
                    # Add section header
                    section_label = source_type.upper()
                    html += f'<div class="streaming-section">'
                    html += f'<div class="section-label">{section_label}</div>'
                    html += f'<div class="section-sources">'

                    # Add sources for this type
                    for source in sources_by_type[source_type]:
                        source_name = source.get('name', 'Unknown Service')
                        web_url = source.get('web_url')
                        logo_url = source.get('logo_url')

                        # Create source link
                        if web_url:
                            source_html = f'<a href="{web_url}" class="source" target="_blank" rel="noopener">'
                        else:
                            source_html = f'<span class="source">'

                        # Add logo if available
                        if logo_url:
                            source_html += f'<img src="{logo_url}" alt="{source_name}" class="source-logo" onerror="this.style.display=\'none\'">'

                        source_html += source_name

                        if web_url:
                            source_html += '</a>'
                        else:
                            source_html += '</span>'

                        html += source_html

                    html += '</div></div>'

                    html += '</div>'

                html += '</div>'
            html += '</div>'

        html += '</div>'
        return html

    def generate_episode_html(self, episode: Dict[str, Any]) -> str:
        """Generate HTML for a single episode."""
        episode_number = episode.get("episode_number", 0)
        title = episode.get("title", "Unknown Episode")
        air_date = episode.get("air_date", "")
        description = episode.get("description", "")
        movies = episode.get("movies", [])
        
        # Get podcast episode URL
        podcast_url = self.get_podcast_episode_url(episode_number)
        
        html = f'''
        <div class="episode" id="episode-{episode_number}">
            <div class="episode-header">
                <div class="episode-title-section">
                    <h3>Episode {episode_number}: {title}</h3>
                    <div class="episode-meta">
                        <span class="air-date">{air_date}</span>
                        <a href="{podcast_url}" class="podcast-link" target="_blank" rel="noopener">
                            <span class="podcast-icon">🎧</span>
                            Listen to Episode
                        </a>
                    </div>
                </div>
            </div>
            <div class="episode-description">{description}</div>
            <div class="movies">
        '''
        
        for movie in movies:
            html += self.generate_movie_html(movie, episode_number)
        
        html += '''
            </div>
        </div>
        '''
        
        return html

    def generate_stats_dashboard(self) -> str:
        """Generate statistics dashboard."""
        episodes = self.movies_data.get("episodes", [])
        total_episodes = len(episodes)
        total_movies = sum(len(episode.get("movies", [])) for episode in episodes)
        
        # Count streaming sources
        total_streaming_sources = 0
        for episode in episodes:
            for movie in episode.get("movies", []):
                streaming_sources = self.find_streaming_data(episode["episode_number"], movie["title"])
                total_streaming_sources += len(streaming_sources)
        
        return f'''
        <div class="stats-dashboard">
            <div class="stat-card">
                <div class="stat-number">{total_episodes}</div>
                <div class="stat-label">Episodes</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{total_movies}</div>
                <div class="stat-label">Movies</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{total_streaming_sources}</div>
                <div class="stat-label">Streaming Sources</div>
            </div>
        </div>
        '''

    def generate_css(self) -> str:
        """Generate CSS styles."""
        return '''
        <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f8f9fa;
        }

        .container {
            display: flex;
            min-height: 100vh;
            flex-wrap: wrap;
            max-width: 100%;
            box-sizing: border-box;
        }

        .sidebar {
            width: 350px;
            background: white;
            border-right: 1px solid #e9ecef;
            overflow-y: auto;
            height: 100vh;
            position: fixed;
            left: 0;
            top: 0;
            box-sizing: border-box;
            transition: transform 0.3s ease;
            z-index: 1000;
        }

        .sidebar.hidden {
            transform: translateX(-100%);
        }

        .sidebar-header {
            padding: 20px;
            border-bottom: 1px solid #e9ecef;
            background: #f8f9fa;
        }

        .sidebar-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
        }

        .sidebar-header h3 {
            margin-bottom: 0;
            color: #495057;
            font-size: 1.2rem;
            flex: 1;
        }

        .toggle-sidebar-btn {
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 8px 12px;
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 6px;
            font-size: 0.85rem;
            color: #495057;
            cursor: pointer;
            transition: all 0.2s ease;
            white-space: nowrap;
        }

        .toggle-sidebar-btn:hover {
            background: #e9ecef;
            border-color: #adb5bd;
        }

        .toggle-sidebar-btn.active {
            background: #007bff;
            color: white;
            border-color: #007bff;
        }

        .toggle-icon {
            font-size: 1rem;
        }

        .toggle-text {
            font-weight: 500;
        }

        .sidebar-toggle-float {
            position: fixed;
            top: 20px;
            left: 20px;
            z-index: 1001;
            display: none;
        }

        .sidebar-toggle-float.show {
            display: block;
        }

        .toggle-sidebar-btn.float {
            background: #007bff;
            color: white;
            border-color: #007bff;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        }

        .toggle-sidebar-btn.float:hover {
            background: #0056b3;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }

        .search-container {
            position: relative;
        }

        .episode-search {
            width: 100%;
            padding: 10px 35px 10px 12px;
            border: 1px solid #dee2e6;
            border-radius: 6px;
            font-size: 14px;
            background: white;
        }

        .episode-search:focus {
            outline: none;
            border-color: #007bff;
            box-shadow: 0 0 0 2px rgba(0,123,255,0.25);
        }

        .search-icon {
            position: absolute;
            right: 10px;
            top: 50%;
            transform: translateY(-50%);
            color: #6c757d;
            font-size: 14px;
        }

        .episode-list {
            padding: 0;
        }

        .filter-section {
            padding: 20px;
            border-bottom: 1px solid #e9ecef;
            background: #f8f9fa;
        }

        .filter-section h4 {
            margin-bottom: 15px;
            color: #495057;
            font-size: 1rem;
        }

        .streaming-filter {
            margin-bottom: 15px;
        }

        .streaming-filter label {
            display: block;
            margin-bottom: 10px;
            color: #495057;
            font-size: 0.9rem;
            font-weight: 500;
        }

        .service-checkboxes {
            display: flex;
            flex-direction: column;
            gap: 8px;
            margin-bottom: 15px;
        }

        .checkbox-item {
            display: flex;
            align-items: center;
            font-size: 0.85rem;
            color: #495057;
            cursor: pointer;
        }

        .checkbox-item input[type="checkbox"] {
            margin-right: 8px;
            cursor: pointer;
        }

        .filter-button {
            background: #007bff;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-size: 0.85rem;
            cursor: pointer;
            margin-right: 8px;
            transition: background-color 0.2s ease;
        }

        .filter-button:hover {
            background: #0056b3;
        }

        .filter-button.secondary {
            background: #6c757d;
        }

        .filter-button.secondary:hover {
            background: #545b62;
        }

        .search-section {
            padding: 20px;
            border-bottom: 1px solid #e9ecef;
            background: white;
        }

        .free-filter {
            margin: 15px 0;
            padding: 10px;
            background: #e8f4fd;
            border-radius: 4px;
            border-left: 3px solid #007bff;
        }

        .free-filter .checkbox-item {
            font-weight: 500;
            color: #007bff;
        }

        .letter-section {
            margin-bottom: 20px;
        }

        .letter-header {
            padding: 10px 20px;
            background: #f8f9fa;
            font-weight: 600;
            color: #495057;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .episode-item {
            display: flex;
            padding: 12px 20px;
            border-bottom: 1px solid #f1f3f4;
            cursor: pointer;
            transition: background-color 0.2s ease;
        }

        .episode-item:hover {
            background: #f8f9fa;
        }

        .episode-item.hidden {
            display: none;
        }

        .episode-number {
            font-weight: 600;
            color: #007bff;
            margin-right: 12px;
            font-size: 0.9rem;
            min-width: 40px;
        }

        .episode-info {
            flex: 1;
        }

        .episode-title {
            font-weight: 500;
            color: #495057;
            margin-bottom: 2px;
            font-size: 0.9rem;
        }

        .episode-date {
            font-size: 0.8rem;
            color: #6c757d;
        }

        .main-content {
            flex: 1;
            margin-left: 350px;
            padding: 30px;
            max-width: calc(100vw - 350px);
            box-sizing: border-box;
            flex-wrap: wrap;
            transition: margin-left 0.3s ease;
        }

        .main-content.sidebar-hidden {
            margin-left: 0;
            max-width: 100vw;
        }

        .header {
            margin-bottom: 40px;
        }

        .header-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
        }

        .header-text {
            text-align: left;
        }

        .header-text h1 {
            color: #2c3e50;
            font-size: 2.5rem;
            margin-bottom: 10px;
        }

        .header-text p {
            color: #6c757d;
            font-size: 1.1rem;
        }

        .header-controls {
            display: flex;
            gap: 15px;
        }

        .sort-button {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 12px 20px;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .sort-button:hover {
            background: #0056b3;
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }

        .sort-button:active {
            transform: translateY(0);
        }

        .sort-button #sort-icon {
            font-size: 16px;
            transition: transform 0.2s ease;
        }

        .episode {
            background: white;
            border-radius: 8px;
            padding: 25px;
            margin-bottom: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            max-width: 100%;
            box-sizing: border-box;
            flex-wrap: wrap;
        }

        .episode-header {
            margin-bottom: 15px;
        }

        .episode-title-section {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            flex-wrap: wrap;
            gap: 15px;
        }

        .episode-header h3 {
            color: #2c3e50;
            font-size: 1.4rem;
            margin-bottom: 5px;
            flex: 1;
        }

        .episode-meta {
            color: #6c757d;
            font-size: 0.9rem;
            display: flex;
            align-items: center;
            gap: 15px;
            flex-wrap: wrap;
        }

        .podcast-link {
            display: flex;
            align-items: center;
            gap: 5px;
            color: #007bff;
            text-decoration: none;
            font-weight: 500;
            padding: 6px 12px;
            background: #e8f4fd;
            border-radius: 4px;
            transition: all 0.2s ease;
        }

        .podcast-link:hover {
            background: #d1ecf1;
            color: #0056b3;
            text-decoration: none;
        }

        .podcast-icon {
            font-size: 1rem;
        }

        .episode-description {
            color: #6c757d;
            margin-bottom: 20px;
            font-style: italic;
        }

        .movies {
            display: grid;
            gap: 20px;
        }

        .movie {
            border: 1px solid #e9ecef;
            border-radius: 6px;
            padding: 20px;
            background: #fafbfc;
            max-width: 100%;
            box-sizing: border-box;
        }

        .movie-content {
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
            max-width: 100%;
            box-sizing: border-box;
        }

        .movie-poster {
            flex-shrink: 0;
            display: flex;
            justify-content: center;
        }

        .poster-container {
            position: relative;
            display: block;
        }

        .poster-image {
            width: 120px;
            height: 180px;
            object-fit: cover;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            background: #f8f9fa;
        }

        .poster-image:hover {
            transform: scale(1.05);
            box-shadow: 0 8px 24px rgba(0,0,0,0.2);
        }

        /* Responsive poster sizes */
        @media screen and (max-width: 768px) {
            .poster-image {
                width: 100px;
                height: 150px;
            }
        }

        @media screen and (max-width: 480px) {
            .poster-image {
                width: 80px;
                height: 120px;
            }
        }

        .movie-details {
            flex: 1;
        }

        .movie-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }

        .movie-header h4 {
            color: #2c3e50;
            font-size: 1.2rem;
        }

        .imdb-link a {
            color: #f3ce13;
            text-decoration: none;
            font-size: 0.9rem;
        }

        .movie-notes {
            color: #6c757d;
            font-size: 0.9rem;
            margin-bottom: 15px;
        }

        .streaming-sources {
            margin-top: 15px;
        }

        .streaming-section {
            margin-bottom: 15px;
            display: flex;
            flex-direction: column;
        }

        .section-label {
            font-weight: 600;
            font-size: 0.8rem;
            text-transform: uppercase;
            color: #6c757d;
            margin-bottom: 8px;
            letter-spacing: 0.5px;
        }

        .section-sources {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            max-width: 100%;
            box-sizing: border-box;
        }

        .source {
            display: flex;
            align-items: center;
            padding: 8px 12px;
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 20px;
            text-decoration: none;
            color: #495057;
            font-size: 0.9rem;
            transition: all 0.2s ease;
        }

        .source:hover {
            background: #e9ecef;
            transform: translateY(-1px);
            text-decoration: none;
            color: #495057;
        }

        .source-logo {
            width: 16px;
            height: 16px;
            margin-right: 6px;
            border-radius: 2px;
        }

        .stats-dashboard {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }

        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .stat-number {
            font-size: 2rem;
            font-weight: bold;
            color: #007bff;
            margin-bottom: 5px;
        }

        .stat-label {
            color: #6c757d;
            font-size: 0.9rem;
        }

        /* Responsive styles for tablets */
        @media screen and (max-width: 1024px) {
            .main-content {
                padding: 20px;
            }

            .episode-header h3 {
                font-size: 1.2rem;
            }

            .movie-header h4 {
                font-size: 1rem;
            }
        }

        /* Responsive styles for mobile */
        @media screen and (max-width: 768px) {
            .container {
                flex-direction: column;
                flex-wrap: wrap;
                max-width: 100%;
            }

            .sidebar {
                width: 100%;
                height: auto;
                max-height: 500px;
                border-right: none;
                border-bottom: 1px solid #e9ecef;
                position: relative;
            }

            .sidebar-header {
                flex-direction: column;
                align-items: stretch;
                gap: 15px;
            }

            .toggle-sidebar-btn {
                align-self: flex-end;
                font-size: 0.8rem;
                padding: 6px 10px;
            }

            .sidebar-toggle-float {
                top: 10px;
                left: 10px;
            }

            .main-content {
                margin-left: 0;
                max-width: 100%;
                padding: 20px;
            }

            .header-content {
                flex-direction: column;
                align-items: flex-start;
            }

            .header-controls {
                margin-top: 15px;
            }

            .episode {
                padding: 15px;
            }

            .movie-content {
                flex-direction: column;
                align-items: center;
                text-align: center;
            }

            .movie-poster {
                margin-bottom: 15px;
            }

            .movie-header {
                flex-direction: column;
                align-items: center;
                gap: 10px;
            }

            .streaming-section {
                flex-direction: column;
            }

            .section-sources {
                flex-direction: column;
                align-items: center;
            }

            .source {
                justify-content: center;
                min-width: 120px;
            }
        }

        /* Extra small screens */
        @media screen and (max-width: 480px) {
            .main-content {
                padding: 15px;
            }

            .episode {
                padding: 10px;
            }

            .movie {
                padding: 15px;
            }

            .header-text h1 {
                font-size: 1.8rem;
            }

            .episode-header h3 {
                font-size: 1.1rem;
            }

            .movie-header h4 {
                font-size: 1rem;
            }
        }
        </style>
        '''

    def generate_javascript(self) -> str:
        """Generate JavaScript for filtering functionality."""
        return r'''
        <script>
        document.addEventListener('DOMContentLoaded', function() {
            const filterInput = document.getElementById('episode-filter');
            const episodeItems = document.querySelectorAll('.episode-item');
            const toggleSidebarBtn = document.getElementById('toggle-sidebar');
            const sidebar = document.getElementById('sidebar');
            const mainContent = document.getElementById('main-content');
            const sidebarToggleFloat = document.getElementById('sidebar-toggle-float');
            const toggleText = document.querySelector('#toggle-sidebar .toggle-text');
            const floatToggleText = document.querySelector('#sidebar-toggle-float .toggle-text');
            let debounceTimer;
            let sidebarVisible = true;

            function filterEpisodes() {
                const searchTerm = filterInput.value.toLowerCase().trim();
                
                episodeItems.forEach(item => {
                    const episodeNumber = item.querySelector('.episode-number').textContent;
                    const episodeTitle = item.querySelector('.episode-title').textContent.toLowerCase();
                    const episodeDate = item.querySelector('.episode-date').textContent;
                    
                    const matchesNumber = episodeNumber.includes(searchTerm);
                    const matchesTitle = episodeTitle.includes(searchTerm);
                    const matchesDate = episodeDate.includes(searchTerm);
                    
                    if (searchTerm === '' || matchesNumber || matchesTitle || matchesDate) {
                        item.classList.remove('hidden');
                    } else {
                        item.classList.add('hidden');
                    }
                });
                
                // Show/hide letter sections based on visible episodes
                const letterSections = document.querySelectorAll('.letter-section');
                letterSections.forEach(section => {
                    const visibleItems = section.querySelectorAll('.episode-item:not(.hidden)');
                    if (visibleItems.length === 0) {
                        section.style.display = 'none';
                    } else {
                        section.style.display = 'block';
                    }
                });
            }

            filterInput.addEventListener('input', function() {
                clearTimeout(debounceTimer);
                debounceTimer = setTimeout(filterEpisodes, 1000);
            });

            // Add click handlers for episode navigation
            episodeItems.forEach(item => {
                item.addEventListener('click', function() {
                    const episodeNumber = this.getAttribute('data-episode');
                    const targetEpisode = document.getElementById(`episode-${episodeNumber}`);
                    
                    if (targetEpisode) {
                        targetEpisode.scrollIntoView({ 
                            behavior: 'smooth',
                            block: 'start'
                        });
                        
                        // Highlight the episode briefly
                        targetEpisode.style.backgroundColor = '#fff3cd';
                        setTimeout(() => {
                            targetEpisode.style.backgroundColor = '';
                        }, 2000);
                    }
                });
            });

            // Sorting functionality
            let currentSortOrder = 'asc'; // 'asc' for A-Z, 'desc' for Z-A
            
            window.toggleSort = function() {
                const episodesContainer = document.querySelector('.episodes-container');
                const episodes = Array.from(episodesContainer.children);
                const sortButton = document.getElementById('sort-button');
                const sortIcon = document.getElementById('sort-icon');
                const sortText = document.getElementById('sort-text');
                
                // Toggle sort order
                currentSortOrder = currentSortOrder === 'asc' ? 'desc' : 'asc';
                
                // Update button appearance
                if (currentSortOrder === 'asc') {
                    sortIcon.textContent = '↓';
                    sortText.textContent = 'A-Z';
                } else {
                    sortIcon.textContent = '↑';
                    sortText.textContent = 'Z-A';
                }
                
                // Sort episodes
                episodes.sort((a, b) => {
                    const aTitle = a.querySelector('h3').textContent.toLowerCase();
                    const bTitle = b.querySelector('h3').textContent.toLowerCase();
                    
                    // Extract episode numbers for proper numeric sorting
                    const aEpisodeMatch = aTitle.match(/episode (\d+)/i);
                    const bEpisodeMatch = bTitle.match(/episode (\d+)/i);
                    
                    if (aEpisodeMatch && bEpisodeMatch) {
                        const aEpisodeNum = parseInt(aEpisodeMatch[1]);
                        const bEpisodeNum = parseInt(bEpisodeMatch[1]);
                        
                        if (currentSortOrder === 'asc') {
                            return aEpisodeNum - bEpisodeNum;
                        } else {
                            return bEpisodeNum - aEpisodeNum;
                        }
                    } else {
                        // Fallback to alphabetical sorting
                        if (currentSortOrder === 'asc') {
                            return aTitle.localeCompare(bTitle);
                        } else {
                            return bTitle.localeCompare(aTitle);
                        }
                    }
                });
                
                // Re-append episodes in sorted order
                episodes.forEach(episode => {
                    episodesContainer.appendChild(episode);
                });
                
                // Add smooth transition effect
                episodes.forEach(episode => {
                    episode.style.transition = 'all 0.3s ease';
                });
            };

            // Streaming filter functionality
            const applyFilterBtn = document.getElementById('apply-filter');
            const clearFilterBtn = document.getElementById('clear-filter');
            const serviceCheckboxes = document.querySelectorAll('.service-checkboxes input[type="checkbox"]');

            function filterByStreamingServices() {
                const selectedServices = Array.from(serviceCheckboxes)
                    .filter(checkbox => checkbox.checked)
                    .map(checkbox => checkbox.value.toLowerCase());
                
                const freeOnly = document.getElementById('free-only').checked;

                const episodes = document.querySelectorAll('.episode');
                
                episodes.forEach(episode => {
                    const movies = episode.querySelectorAll('.movie');
                    let hasVisibleMovies = false;

                    movies.forEach(movie => {
                        const streamingSources = movie.querySelectorAll('.source');
                        let hasSelectedService = false;
                        let hasFreeSource = false;

                        streamingSources.forEach(source => {
                            const sourceText = source.textContent.toLowerCase();
                            const sourceType = source.closest('.streaming-section');
                            
                            // Check if this is a free source
                            if (sourceType && sourceType.querySelector('.section-label').textContent.toLowerCase().includes('free')) {
                                hasFreeSource = true;
                            }
                            
                            const hasService = selectedServices.some(service => {
                                const serviceMap = {
                                    'netflix': 'netflix',
                                    'hbo': 'hbo',
                                    'tubi': 'tubi',
                                    'amazon': 'amazon',
                                    'itunes': 'itunes',
                                    'google': 'google play',
                                    'pluto': 'pluto'
                                };
                                return sourceText.includes(serviceMap[service] || service);
                            });

                            if (hasService) {
                                hasSelectedService = true;
                            }
                        });

                        // Apply free-only filter if enabled
                        let shouldShow = hasSelectedService;
                        if (freeOnly && !hasFreeSource) {
                            shouldShow = false;
                        }

                        if (shouldShow) {
                            movie.style.display = 'block';
                            hasVisibleMovies = true;
                        } else {
                            movie.style.display = 'none';
                        }
                    });

                    // Show/hide episode based on whether it has visible movies
                    if (hasVisibleMovies) {
                        episode.style.display = 'block';
                    } else {
                        episode.style.display = 'none';
                    }
                });
            }

            function clearStreamingFilter() {
                // Reset all checkboxes to checked
                serviceCheckboxes.forEach(checkbox => {
                    checkbox.checked = true;
                });
                
                // Reset free-only checkbox to unchecked
                document.getElementById('free-only').checked = false;

                // Show all episodes and movies
                const episodes = document.querySelectorAll('.episode');
                const movies = document.querySelectorAll('.movie');
                
                episodes.forEach(episode => {
                    episode.style.display = 'block';
                });
                
                movies.forEach(movie => {
                    movie.style.display = 'block';
                });
            }

            // Event listeners
            applyFilterBtn.addEventListener('click', filterByStreamingServices);
            clearFilterBtn.addEventListener('click', clearStreamingFilter);

            // Toggle sidebar functionality
            function toggleSidebar() {
                sidebarVisible = !sidebarVisible;
                
                if (sidebarVisible) {
                    sidebar.classList.remove('hidden');
                    mainContent.classList.remove('sidebar-hidden');
                    sidebarToggleFloat.classList.remove('show');
                    toggleText.textContent = 'Hide Sidebar';
                    floatToggleText.textContent = 'Show Sidebar';
                } else {
                    sidebar.classList.add('hidden');
                    mainContent.classList.add('sidebar-hidden');
                    sidebarToggleFloat.classList.add('show');
                    toggleText.textContent = 'Show Sidebar';
                    floatToggleText.textContent = 'Hide Sidebar';
                }
            }

            toggleSidebarBtn.addEventListener('click', toggleSidebar);
            
            // Floating toggle button
            const floatToggleBtn = document.querySelector('#sidebar-toggle-float .toggle-sidebar-btn');
            floatToggleBtn.addEventListener('click', toggleSidebar);
        });
        </script>
        '''

    def generate_html(self) -> str:
        """Generate the complete HTML page."""
        episodes = self.movies_data.get("episodes", [])
        
        html = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Too Scary; Didn't Watch - Movie Streaming Tracker</title>
            {self.generate_css()}
        </head>
        <body>
            <div class="container">
                {self.generate_episode_sidebar()}
                
                <div class="main-content" id="main-content">
                    <div class="sidebar-toggle-float" id="sidebar-toggle-float">
                        <button class="toggle-sidebar-btn float">
                            <span class="toggle-icon">▶</span>
                            <span class="toggle-text">Show Sidebar</span>
                        </button>
                    </div>
                    <div class="header">
                        <div class="header-content">
                            <div class="header-text">
                                <h1>Too Scary; Didn't Watch</h1>
                                <p>Find where to stream movies mentioned in the podcast</p>
                            </div>
                            <div class="header-controls">
                                <button id="sort-button" class="sort-button" onclick="toggleSort()">
                                    <span id="sort-icon">↓</span>
                                    <span id="sort-text">A-Z</span>
                                </button>
                            </div>
                        </div>
                    </div>
                    
                    {self.generate_stats_dashboard()}
                    
                    <div class="episodes-container">
        '''
        
        for episode in episodes:
            html += self.generate_episode_html(episode)
        
        html += '''
                    </div>
                </div>
            </div>
            
            ''' + self.generate_javascript() + '''
        </body>
        </html>
        '''
        
        return html

    def save_html(self, html_content: str, output_file: str = 'output/index.html'):
        """Save HTML content to file."""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            logger.info(f"HTML output saved to {output_file}")
        except Exception as e:
            logger.error(f"Error saving HTML: {e}")
            raise

def main():
    """Main function."""
    logger.info("Starting HTML generation...")
    
    generator = HTMLGenerator()
    
    # Configure TMDB API for poster fetching
    generator.configure_tmdb_api()
    
    generator.load_data()
    
    html_content = generator.generate_html()
    generator.save_html(html_content)
    
    logger.info("HTML generation completed successfully!")

if __name__ == "__main__":
    main() 