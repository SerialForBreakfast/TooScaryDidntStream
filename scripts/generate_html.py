#!/usr/bin/env python3
"""
Generate HTML output for TooScaryDidntStream podcast movie tracker.

This script reads streaming data from data/streaming_data.json and generates
a clean, responsive HTML page showing episodes, movies, and streaming availability.

Usage:
    python scripts/generate_html.py
"""

import json
import os
import sys
import time
from typing import Dict, List, Any, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class HTMLGenerator:
    """Generates static HTML for the movie streaming tracker."""
    
    def __init__(self):
        self.output_dir = 'output'
        self.streaming_data = None
        
    def load_streaming_data(self) -> Dict[str, Any]:
        """Load streaming data from JSON file."""
        try:
            with open('data/streaming_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                logger.info("Loaded streaming data successfully")
                return data
        except FileNotFoundError:
            logger.error("data/streaming_data.json not found. Please run fetch_streaming_info.py first.")
            # Create mock data for development
            return self._create_mock_data()
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in streaming data: {e}")
            sys.exit(1)
    
    def _create_mock_data(self) -> Dict[str, Any]:
        """Create mock data for development when streaming data doesn't exist."""
        logger.warning("Creating mock streaming data for development")
        return {
            "episodes": [
                {
                    "episode_number": 234,
                    "title": "The Strangers: Prey at Night",
                    "air_date": "2024-01-15",
                    "description": "The gang discusses this 2018 horror sequel and its streaming availability",
                    "movies": [
                        {
                            "title": "The Strangers: Prey at Night",
                            "year": 2018,
                            "imdb_id": "tt1285009",
                            "streaming_sources": [],
                            "data_sources": [],
                            "last_updated": "2024-01-29"
                        }
                    ]
                }
            ],
            "metadata": {
                "podcast_name": "Too Scary; Didn't Watch",
                "last_updated": "2024-01-29",
                "total_movies_processed": 1,
                "apis_used": ["mock"]
            }
        }
    
    def generate_css(self) -> str:
        """Generate CSS styles for the HTML page."""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f8f9fa;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 0;
            margin-bottom: 40px;
            border-radius: 10px;
        }
        
        h1 {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 10px;
            text-align: center;
        }
        
        .subtitle {
            font-size: 1.2rem;
            text-align: center;
            opacity: 0.9;
            margin-bottom: 20px;
        }
        
        .stats {
            display: flex;
            justify-content: center;
            gap: 30px;
            flex-wrap: wrap;
            margin-top: 20px;
        }
        
        .stat {
            text-align: center;
        }
        
        .stat-number {
            font-size: 2rem;
            font-weight: bold;
            display: block;
        }
        
        .stat-label {
            font-size: 0.9rem;
            opacity: 0.8;
        }
        
        .episode {
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 30px;
            overflow: hidden;
            transition: transform 0.2s ease;
        }
        
        .episode:hover {
            transform: translateY(-2px);
        }
        
        .episode-header {
            background: #f8f9fa;
            padding: 20px;
            border-bottom: 1px solid #e9ecef;
        }
        
        .episode-number {
            color: #6c757d;
            font-size: 0.9rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .episode-title {
            font-size: 1.5rem;
            font-weight: 600;
            color: #2c3e50;
            margin: 5px 0;
        }
        
        .episode-date {
            color: #6c757d;
            font-size: 0.9rem;
        }
        
        .episode-description {
            color: #495057;
            margin-top: 10px;
            line-height: 1.5;
        }
        
        .movies {
            padding: 0;
        }
        
        .movie {
            padding: 20px;
            border-bottom: 1px solid #f1f3f4;
        }
        
        .movie:last-child {
            border-bottom: none;
        }
        
        .movie-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 15px;
        }
        
        .movie-title {
            font-size: 1.2rem;
            font-weight: 600;
            color: #2c3e50;
        }
        
        .movie-year {
            color: #6c757d;
            font-size: 1rem;
            margin-left: 10px;
        }
        
        .movie-notes {
            color: #6c757d;
            font-size: 0.9rem;
            font-style: italic;
            margin-top: 5px;
        }
        
        .streaming-sources {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 15px;
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
        
        .source.subscription {
            background: #d4edda;
            border-color: #c3e6cb;
            color: #155724;
        }
        
        .source.rent {
            background: #fff3cd;
            border-color: #ffeaa7;
            color: #856404;
        }
        
        .source.buy {
            background: #f8d7da;
            border-color: #f5c6cb;
            color: #721c24;
        }
        
        .source.free {
            background: #cce5ff;
            border-color: #b3d9ff;
            color: #004085;
        }
        
        .source-logo {
            width: 20px;
            height: 20px;
            margin-right: 8px;
            border-radius: 4px;
        }
        
        .no-streaming {
            color: #6c757d;
            font-style: italic;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
            margin-top: 10px;
        }
        
        .data-sources {
            margin-top: 10px;
            font-size: 0.8rem;
            color: #6c757d;
        }
        
        .footer {
            text-align: center;
            margin-top: 60px;
            padding: 40px 0;
            color: #6c757d;
            border-top: 1px solid #e9ecef;
        }
        
        .last-updated {
            font-size: 0.9rem;
            margin-bottom: 10px;
        }
        
        .github-link {
            color: #667eea;
            text-decoration: none;
        }
        
        .github-link:hover {
            text-decoration: underline;
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .container {
                padding: 15px;
            }
            
            h1 {
                font-size: 2rem;
            }
            
            .stats {
                gap: 20px;
            }
            
            .movie-header {
                flex-direction: column;
                align-items: flex-start;
            }
            
            .streaming-sources {
                justify-content: flex-start;
            }
        }
        """
    
    def format_source_type(self, source_type: str) -> str:
        """Format source type for display."""
        type_mapping = {
            'flatrate': 'subscription',
            'sub': 'subscription',
            'rent': 'rent',
            'buy': 'buy',
            'free': 'free',
            'tve': 'subscription'
        }
        return type_mapping.get(source_type.lower(), source_type)
    
    def generate_movie_html(self, movie: Dict[str, Any]) -> str:
        """Generate HTML for a single movie."""
        title = movie.get('title', 'Unknown Movie')
        year = movie.get('year', '')
        notes = movie.get('notes', '')
        streaming_sources = movie.get('streaming_sources', [])
        data_sources = movie.get('data_sources', [])
        
        # Movie header
        html = f"""
        <div class="movie">
            <div class="movie-header">
                <div>
                    <span class="movie-title">{title}</span>
                    {f'<span class="movie-year">({year})</span>' if year else ''}
                    {f'<div class="movie-notes">{notes}</div>' if notes else ''}
                </div>
            </div>
        """
        
        # Streaming sources
        if streaming_sources:
            html += '<div class="streaming-sources">'
            
            for source in streaming_sources:
                source_name = source.get('name', 'Unknown Service')
                source_type = self.format_source_type(source.get('type', ''))
                web_url = source.get('web_url')
                logo_url = source.get('logo_url')
                
                # Create source link
                if web_url:
                    source_html = f'<a href="{web_url}" class="source {source_type}" target="_blank" rel="noopener">'
                else:
                    source_html = f'<span class="source {source_type}">'
                
                # Add logo if available
                if logo_url:
                    source_html += f'<img src="{logo_url}" alt="{source_name}" class="source-logo" onerror="this.style.display=\'none\'">'
                
                source_html += source_name
                
                if web_url:
                    source_html += '</a>'
                else:
                    source_html += '</span>'
                
                html += source_html
            
            html += '</div>'
        else:
            html += '<div class="no-streaming">No streaming sources found</div>'
        
        # Data sources attribution
        if data_sources:
            html += f'<div class="data-sources">Data from: {", ".join(data_sources)}</div>'
        
        html += '</div>'
        return html
    
    def generate_episode_html(self, episode: Dict[str, Any]) -> str:
        """Generate HTML for a single episode."""
        episode_number = episode.get('episode_number', '')
        title = episode.get('title', 'Unknown Episode')
        air_date = episode.get('air_date', '')
        description = episode.get('description', '')
        movies = episode.get('movies', [])
        
        html = f"""
        <div class="episode">
            <div class="episode-header">
                <div class="episode-number">Episode {episode_number}</div>
                <h2 class="episode-title">{title}</h2>
                {f'<div class="episode-date">{air_date}</div>' if air_date else ''}
                {f'<div class="episode-description">{description}</div>' if description else ''}
            </div>
            <div class="movies">
        """
        
        # Add movies
        for movie in movies:
            html += self.generate_movie_html(movie)
        
        html += """
            </div>
        </div>
        """
        
        return html
    
    def generate_html(self) -> str:
        """Generate the complete HTML page."""
        data = self.load_streaming_data()
        episodes = data.get('episodes', [])
        metadata = data.get('metadata', {})
        
        podcast_name = metadata.get('podcast_name', 'Podcast Movie Tracker')
        last_updated = metadata.get('last_updated', 'Unknown')
        total_movies = metadata.get('total_movies_processed', 0)
        apis_used = metadata.get('apis_used', [])
        
        # Calculate stats
        total_episodes = len(episodes)
        total_streaming_sources = 0
        
        for episode in episodes:
            for movie in episode.get('movies', []):
                total_streaming_sources += len(movie.get('streaming_sources', []))
        
        # Generate HTML
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{podcast_name} - Movie Streaming Tracker</title>
    <meta name="description" content="Find where to stream movies mentioned in the {podcast_name} podcast.">
    <style>
        {self.generate_css()}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{podcast_name}</h1>
            <p class="subtitle">Movie Streaming Tracker</p>
            <div class="stats">
                <div class="stat">
                    <span class="stat-number">{total_episodes}</span>
                    <span class="stat-label">Episodes</span>
                </div>
                <div class="stat">
                    <span class="stat-number">{total_movies}</span>
                    <span class="stat-label">Movies</span>
                </div>
                <div class="stat">
                    <span class="stat-number">{total_streaming_sources}</span>
                    <span class="stat-label">Streaming Options</span>
                </div>
            </div>
        </header>
        
        <main>
        """
        
        # Add episodes
        if episodes:
            # Sort episodes by episode number (descending - newest first)
            sorted_episodes = sorted(episodes, key=lambda x: x.get('episode_number', 0), reverse=True)
            
            for episode in sorted_episodes:
                html += self.generate_episode_html(episode)
        else:
            html += """
            <div class="episode">
                <div class="episode-header">
                    <h2 class="episode-title">No Episodes Available</h2>
                    <div class="episode-description">No episode data found. Please run the streaming info fetcher first.</div>
                </div>
            </div>
            """
        
        html += """
        </main>
        
        <footer class="footer">
        """
        
        if last_updated:
            html += f'<div class="last-updated">Last updated: {last_updated}</div>'
        
        if apis_used:
            html += f'<div class="data-attribution">Streaming data powered by: {", ".join(apis_used).title()}</div>'
        
        html += """
            <div>
                <a href="https://github.com/SerialForBreakfast/TooScaryDidntStream" class="github-link">
                    View on GitHub
                </a>
            </div>
        </footer>
    </div>
</body>
</html>"""
        
        return html
    
    def save_html(self, html_content: str):
        """Save HTML content to output file."""
        os.makedirs(self.output_dir, exist_ok=True)
        
        output_file = os.path.join(self.output_dir, 'index.html')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"HTML output saved to {output_file}")
    
    def run(self):
        """Main execution function."""
        logger.info("Starting HTML generation...")
        
        try:
            html_content = self.generate_html()
            self.save_html(html_content)
            logger.info("HTML generation completed successfully!")
            
            # Print file info
            output_file = os.path.join(self.output_dir, 'index.html')
            file_size = os.path.getsize(output_file)
            logger.info(f"Generated file: {output_file} ({file_size:,} bytes)")
            
        except Exception as e:
            logger.error(f"HTML generation failed: {e}")
            sys.exit(1)


def main():
    """Main entry point."""
    generator = HTMLGenerator()
    generator.run()


if __name__ == "__main__":
    main() 