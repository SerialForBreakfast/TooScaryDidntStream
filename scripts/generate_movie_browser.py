#!/usr/bin/env python3
"""
Generate a new movie-focused UI for the streaming tracker.
"""

import json
import logging
from typing import Dict, List, Any, Set
from collections import defaultdict

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MovieBrowserGenerator:
    def __init__(self):
        self.movies_data = None
        self.streaming_data = None

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

    def get_all_movies_with_streaming(self) -> List[Dict[str, Any]]:
        """Extract all movies with their streaming information."""
        movies_with_streaming = []
        
        # Create a lookup for streaming data by episode and movie title
        streaming_lookup = {}
        for episode_data in self.streaming_data.get("episodes", []):
            episode_num = episode_data["episode_number"]
            for movie in episode_data.get("movies", []):
                key = (episode_num, movie["title"].lower(), movie.get("year"))
                streaming_lookup[key] = movie.get("streaming_sources", [])
        
        # Process each episode and movie
        for episode in self.movies_data.get("episodes", []):
            episode_num = episode["episode_number"]
            episode_title = episode["title"]
            
            for movie in episode.get("movies", []):
                movie_title = movie["title"]
                movie_year = movie.get("year")
                
                # Look up streaming sources
                key = (episode_num, movie_title.lower(), movie_year)
                streaming_sources = streaming_lookup.get(key, [])
                
                movie_info = {
                    "title": movie_title,
                    "year": movie_year,
                    "episode": episode_num,
                    "episode_title": episode_title,
                    "notes": movie.get("notes", ""),
                    "streaming_sources": streaming_sources
                }
                
                movies_with_streaming.append(movie_info)
        
        # Remove duplicates (same movie might appear in multiple episodes)
        seen = set()
        unique_movies = []
        for movie in movies_with_streaming:
            key = (movie["title"].lower(), movie["year"])
            if key not in seen:
                seen.add(key)
                unique_movies.append(movie)
        
        return unique_movies

    def get_streaming_services(self, movies: List[Dict[str, Any]]) -> Set[str]:
        """Get all unique streaming service names."""
        services = set()
        for movie in movies:
            for source in movie.get("streaming_sources", []):
                services.add(source.get("name", ""))
        return services

    def generate_css(self) -> str:
        """Generate CSS for the movie browser."""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f8fafc;
            color: #1a202c;
            line-height: 1.6;
        }

        .header {
            background: #2d3748;
            color: white;
            padding: 1.5rem 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .header-content {
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
        }

        .header h1 {
            font-size: 1.8rem;
            font-weight: 700;
        }

        .header p {
            font-size: 0.9rem;
            color: #a0aec0;
            margin-top: 0.25rem;
        }

        .stats {
            display: flex;
            gap: 2rem;
            font-size: 0.9rem;
        }

        .stat {
            text-align: center;
        }

        .stat-number {
            font-size: 1.5rem;
            font-weight: bold;
            color: #4fd1c7;
        }

        .filters {
            background: white;
            border-bottom: 1px solid #e2e8f0;
            padding: 1.5rem 0;
            position: sticky;
            top: 88px;
            z-index: 90;
        }

        .filters-content {
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 2rem;
        }

        .filter-section {
            display: flex;
            flex-wrap: wrap;
            gap: 2rem;
            align-items: center;
            margin-bottom: 1rem;
        }

        .filter-group {
            display: flex;
            flex-wrap: wrap;
            gap: 0.75rem;
            align-items: center;
        }

        .filter-group label {
            font-weight: 600;
            color: #4a5568;
            font-size: 0.9rem;
            min-width: 80px;
        }

        .filter-btn {
            padding: 0.5rem 1rem;
            border: 2px solid #e2e8f0;
            background: white;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s;
            font-size: 0.85rem;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .filter-btn:hover {
            border-color: #4299e1;
            background: #ebf8ff;
        }

        .filter-btn.active {
            background: #4299e1;
            border-color: #4299e1;
            color: white;
        }

        .search-section {
            display: flex;
            gap: 1rem;
            align-items: center;
            flex-wrap: wrap;
        }

        .search-input {
            padding: 0.75rem 1rem;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            font-size: 0.9rem;
            min-width: 300px;
            transition: border-color 0.2s;
        }

        .search-input:focus {
            outline: none;
            border-color: #4299e1;
        }

        .clear-filters {
            padding: 0.75rem 1.5rem;
            background: #f7fafc;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 500;
            transition: all 0.2s;
        }

        .clear-filters:hover {
            background: #edf2f7;
            border-color: #cbd5e0;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
        }

        .movies-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 2rem;
            margin-top: 2rem;
        }

        .movie-card {
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            overflow: hidden;
            transition: all 0.3s;
            border: 1px solid #e2e8f0;
        }

        .movie-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
        }

        .movie-poster {
            width: 100%;
            height: 200px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            border-bottom: 1px solid #e2e8f0;
            position: relative;
            color: white;
        }

        .movie-poster .placeholder {
            font-size: 3rem;
            opacity: 0.7;
        }

        .episode-badge {
            position: absolute;
            top: 0.75rem;
            left: 0.75rem;
            background: rgba(45, 55, 72, 0.9);
            color: white;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
        }

        .movie-info {
            padding: 1.5rem;
        }

        .movie-title {
            font-size: 1.1rem;
            font-weight: 700;
            color: #2d3748;
            margin-bottom: 0.5rem;
        }

        .movie-year {
            color: #718096;
            font-size: 0.9rem;
            margin-bottom: 1rem;
        }

        .streaming-services {
            margin-bottom: 1rem;
        }

        .service-type {
            margin-bottom: 0.75rem;
        }

        .service-type:last-child {
            margin-bottom: 0;
        }

        .service-type-label {
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            color: #718096;
            margin-bottom: 0.5rem;
            letter-spacing: 0.5px;
        }

        .services-list {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
        }

        .service-tag {
            padding: 0.25rem 0.75rem;
            background: #edf2f7;
            border: 1px solid #e2e8f0;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 500;
            color: #4a5568;
            text-decoration: none;
            transition: all 0.2s;
        }

        .service-tag:hover {
            background: #e2e8f0;
            transform: translateY(-1px);
        }

        .service-tag.subscription {
            background: #c6f6d5;
            border-color: #9ae6b4;
            color: #22543d;
        }

        .service-tag.rent {
            background: #fed7d7;
            border-color: #fbb6ce;
            color: #742a2a;
        }

        .service-tag.buy {
            background: #bee3f8;
            border-color: #90cdf4;
            color: #2a4365;
        }

        .service-tag.free {
            background: #d9f7be;
            border-color: #b7eb8f;
            color: #237804;
        }

        .episode-link {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            color: #4299e1;
            text-decoration: none;
            font-size: 0.9rem;
            font-weight: 500;
            padding: 0.5rem 0;
            transition: color 0.2s;
        }

        .episode-link:hover {
            color: #2b6cb0;
        }

        .no-results {
            text-align: center;
            padding: 4rem 2rem;
            color: #718096;
        }

        .no-results h3 {
            font-size: 1.5rem;
            margin-bottom: 1rem;
            color: #4a5568;
        }

        .loading {
            text-align: center;
            padding: 2rem;
            color: #718096;
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            .header-content {
                flex-direction: column;
                text-align: center;
            }

            .filters-content {
                padding: 0 1rem;
            }

            .filter-section {
                flex-direction: column;
                align-items: stretch;
                gap: 1rem;
            }

            .filter-group {
                flex-direction: column;
                align-items: stretch;
            }

            .filter-group label {
                min-width: unset;
                margin-bottom: 0.5rem;
            }

            .search-input {
                min-width: unset;
                width: 100%;
            }

            .container {
                padding: 1rem;
            }

            .movies-grid {
                grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
                gap: 1.5rem;
            }

            .stats {
                gap: 1rem;
            }
        }

        @media (max-width: 480px) {
            .movies-grid {
                grid-template-columns: 1fr;
            }
        }
        """

    def generate_javascript(self, movies: List[Dict[str, Any]]) -> str:
        """Generate JavaScript for the movie browser."""
        # Convert Python data to JavaScript
        movies_json = json.dumps(movies, indent=2)
        
        return f"""
        let allMovies = {movies_json};
        let filteredMovies = [];
        let currentFilters = {{
            type: 'all',
            service: 'all',
            search: ''
        }};

        // Initialize the app
        function init() {{
            applyFilters();
            setupEventListeners();
        }}

        // Setup event listeners
        function setupEventListeners() {{
            // Type filters
            document.querySelectorAll('[data-type]').forEach(btn => {{
                btn.addEventListener('click', () => {{
                    document.querySelectorAll('[data-type]').forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    currentFilters.type = btn.dataset.type;
                    applyFilters();
                }});
            }});

            // Service filters
            document.querySelectorAll('[data-service]').forEach(btn => {{
                btn.addEventListener('click', () => {{
                    document.querySelectorAll('[data-service]').forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    currentFilters.service = btn.dataset.service;
                    applyFilters();
                }});
            }});

            // Search
            document.getElementById('search-input').addEventListener('input', (e) => {{
                currentFilters.search = e.target.value.toLowerCase();
                applyFilters();
            }});

            // Clear filters
            document.getElementById('clear-filters').addEventListener('click', () => {{
                currentFilters = {{ type: 'all', service: 'all', search: '' }};
                document.getElementById('search-input').value = '';
                document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
                document.querySelector('[data-type="all"]').classList.add('active');
                document.querySelector('[data-service="all"]').classList.add('active');
                applyFilters();
            }});
        }}

        // Apply current filters
        function applyFilters() {{
            filteredMovies = allMovies.filter(movie => {{
                // Search filter
                if (currentFilters.search) {{
                    const searchTerm = currentFilters.search;
                    if (!movie.title.toLowerCase().includes(searchTerm) &&
                        !movie.episode_title.toLowerCase().includes(searchTerm)) {{
                        return false;
                    }}
                }}

                // Type filter
                if (currentFilters.type !== 'all') {{
                    const hasType = movie.streaming_sources.some(source => {{
                        if (currentFilters.type === 'subscription') return source.type === 'subscription';
                        if (currentFilters.type === 'rent') return source.type === 'rent' || source.type === 'buy';
                        if (currentFilters.type === 'free') return source.type === 'free' || source.name.toLowerCase().includes('free');
                        return true;
                    }});
                    if (!hasType) return false;
                }}

                // Service filter
                if (currentFilters.service !== 'all') {{
                    const hasService = movie.streaming_sources.some(source => 
                        source.name.toLowerCase().includes(currentFilters.service.toLowerCase())
                    );
                    if (!hasService) return false;
                }}

                return true;
            }});

            renderMovies();
            updateStats();
        }}

        // Render movies
        function renderMovies() {{
            const grid = document.getElementById('movies-grid');
            const noResults = document.getElementById('no-results');

            if (filteredMovies.length === 0) {{
                grid.style.display = 'none';
                noResults.style.display = 'block';
                return;
            }}

            noResults.style.display = 'none';
            grid.style.display = 'grid';

            grid.innerHTML = filteredMovies.map(movie => `
                <div class="movie-card">
                    <div class="movie-poster">
                        <div class="placeholder">🎬</div>
                        <div class="episode-badge">Episode ${{movie.episode}}</div>
                    </div>
                    <div class="movie-info">
                        <div class="movie-title">${{movie.title}}</div>
                        <div class="movie-year">${{movie.year}}</div>
                        
                        <div class="streaming-services">
                            ${{renderStreamingServices(movie.streaming_sources)}}
                        </div>
                        
                        <a href="#episode-${{movie.episode}}" class="episode-link">
                            ▶ ${{movie.episode_title}}
                        </a>
                    </div>
                </div>
            `).join('');
        }}

        // Render streaming services for a movie
        function renderStreamingServices(sources) {{
            if (!sources || sources.length === 0) {{
                return '<div class="service-type"><div class="service-type-label">No streaming info</div></div>';
            }}

            const grouped = sources.reduce((acc, source) => {{
                const type = source.type || 'unknown';
                if (!acc[type]) acc[type] = [];
                acc[type].push(source);
                return acc;
            }}, {{}});

            return Object.entries(grouped).map(([type, services]) => `
                <div class="service-type">
                    <div class="service-type-label">${{type}}</div>
                    <div class="services-list">
                        ${{services.map(service => `
                            <span class="service-tag ${{type}}">${{service.name}}</span>
                        `).join('')}}
                    </div>
                </div>
            `).join('');
        }}

        // Update statistics
        function updateStats() {{
            document.getElementById('total-movies').textContent = allMovies.length;
            document.getElementById('visible-movies').textContent = filteredMovies.length;
        }}

        // Start the app when DOM is loaded
        document.addEventListener('DOMContentLoaded', init);
        """

    def generate_service_filters(self, movies: List[Dict[str, Any]]) -> str:
        """Generate filter buttons for streaming services."""
        services = set()
        for movie in movies:
            for source in movie.get("streaming_sources", []):
                service_name = source.get("name", "").lower()
                # Map to common service names
                if "netflix" in service_name:
                    services.add("netflix")
                elif "amazon" in service_name:
                    services.add("amazon")
                elif "apple" in service_name:
                    services.add("apple")
                elif "google" in service_name:
                    services.add("google")
                elif "youtube" in service_name:
                    services.add("youtube")
                elif "tubi" in service_name:
                    services.add("tubi")
                elif "pluto" in service_name:
                    services.add("pluto")
                elif "hbo" in service_name:
                    services.add("hbo")
                elif "hulu" in service_name:
                    services.add("hulu")
        
        service_buttons = []
        for service in sorted(services):
            service_label = service.title()
            if service == "apple":
                service_label = "Apple TV"
            elif service == "google":
                service_label = "Google Play"
            elif service == "youtube":
                service_label = "YouTube"
            elif service == "hbo":
                service_label = "HBO Max"
            
            service_buttons.append(f'<button class="filter-btn" data-service="{service}">{service_label}</button>')
        
        return '\n                    '.join(service_buttons)

    def generate_html(self) -> str:
        """Generate the complete HTML page."""
        movies = self.get_all_movies_with_streaming()
        service_filters = self.generate_service_filters(movies)
        
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Too Scary; Didn't Watch - Movie Browser</title>
    <style>{self.generate_css()}</style>
</head>
<body>
    <header class="header">
        <div class="header-content">
            <div>
                <h1>Too Scary; Didn't Watch</h1>
                <p>Browse movies mentioned in the podcast</p>
            </div>
            <div class="stats">
                <div class="stat">
                    <div class="stat-number" id="total-movies">0</div>
                    <div>Movies</div>
                </div>
                <div class="stat">
                    <div class="stat-number" id="visible-movies">0</div>
                    <div>Showing</div>
                </div>
            </div>
        </div>
    </header>

    <div class="filters">
        <div class="filters-content">
            <div class="filter-section">
                <div class="filter-group">
                    <label>Streaming Type:</label>
                    <button class="filter-btn active" data-type="all">All</button>
                    <button class="filter-btn" data-type="subscription">📺 Subscription</button>
                    <button class="filter-btn" data-type="rent">💰 Rent/Buy</button>
                    <button class="filter-btn" data-type="free">🆓 Free</button>
                </div>
                
                <div class="filter-group">
                    <label>Service:</label>
                    <button class="filter-btn active" data-service="all">All Services</button>
                    {service_filters}
                </div>
            </div>
            
            <div class="search-section">
                <input type="text" class="search-input" placeholder="Search movies..." id="search-input">
                <button class="clear-filters" id="clear-filters">Clear All Filters</button>
            </div>
        </div>
    </div>

    <div class="container">
        <div class="movies-grid" id="movies-grid"></div>
        <div class="no-results" id="no-results" style="display: none;">
            <h3>No movies found</h3>
            <p>Try adjusting your filters or search terms</p>
        </div>
    </div>

    <script>{self.generate_javascript(movies)}</script>
</body>
</html>'''
        
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
    logger.info("Starting movie browser generation...")
    
    generator = MovieBrowserGenerator()
    generator.load_data()
    
    html_content = generator.generate_html()
    generator.save_html(html_content)
    
    logger.info("Movie browser generation completed successfully!")

if __name__ == "__main__":
    main()