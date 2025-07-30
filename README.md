
# TooScaryDidntStream

A tool to help find where to stream movies mentioned in the *Too Scary; Didn't Watch* podcast.

### Official TSDW Links
- 🎙️ [Official Website](https://2scarydidntwatch.com)
- 🍎 [Apple Podcasts](https://podcasts.apple.com/us/podcast/too-scary-didnt-watch/id1476552025)
- 💚 [Spotify](https://open.spotify.com/show/0m7qJtF2wqJXqEHwkZzNK7)
- 🎥 [YouTube](https://www.youtube.com/@TooScaryDidntWatch)
- 🐦 [Twitter/X](https://twitter.com/2scarypodcast)
- 📸 [Instagram](https://www.instagram.com/tooscarydidntwatch)
- 💜 [Twitch](https://www.twitch.tv/tooscarydidntwatch)
- ⭐ [Patreon](https://www.patreon.com/tooscarydidntwatch)


## Live Site
**[https://serialforbreakfast.github.io/TooScaryDidntStream/output/index.html](https://serialforbreakfast.github.io/TooScaryDidntStream/output/index.html)** - Live site automatically updated via GitHub Actions

## Github
https://github.com/SerialForBreakfast/TooScaryDidntStream

## What it does

- Tracks episodes and the movies they mention.
- Queries streaming APIs (Watchmode + TMDB) to find current streaming availability.
- Outputs a clean HTML page with posters, streaming providers, and episode groupings.
- Features responsive design that works on desktop, tablet, and mobile devices.
- Auto-updates via GitHub Actions and deploys with GitHub Pages.

## Features

- **Episode Organization**: Movies grouped by podcast episode
- **Streaming Sources**: Shows where each movie is available to stream
- **Movie Posters**: Real movie posters from TMDB (with fallback placeholders)
- **Responsive Design**: Works on desktop, tablet, and mobile with adaptive poster sizes
- **Search & Filter**: Find episodes and filter by streaming service
- **Auto-updates**: Fresh streaming data via GitHub Actions
- **CI/CD Pipeline**: Staging environment for preview, production deployment

## Project Structure

```
.
├── data/
│   ├── movies.json         # Source of truth for episodes and movies
│   └── streaming_data.json # Generated streaming availability data
├── output/
│   └── index.html          # Auto-generated HTML page
├── scripts/
│   ├── fetch_streaming_info.py  # Gets streaming data from APIs
│   └── generate_html.py         # Builds HTML view from data
├── .github/
│   └── workflows/
│       └── update.yaml     # GitHub Actions workflow
├── venv/                   # Python virtual environment
├── requirements.txt        # Python dependencies
└── README.md
```

## Getting Started

### 1. Clone and Setup

```bash
git clone https://github.com/SerialForBreakfast/TooScaryDidntStream.git
cd TooScaryDidntStream

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Get API Keys (Free)

You'll need at least one of these free API keys:

#### Watchmode API (Recommended - Primary source)
1. Visit https://api.watchmode.com/
2. Sign up for a free account
3. Get your API key from the dashboard

#### TMDB API (Fallback source)
1. Visit https://www.themoviedb.org/settings/api
2. Create an account and request an API key
3. Use the v3 API key

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Copy the example and edit with your keys
cp .env.example .env
```

Edit `.env` with your API keys:
```
WATCHMODE_API_KEY=your_watchmode_api_key_here
TMDB_API_KEY=your_tmdb_api_key_here
```

Or set them in your shell:
```bash
export WATCHMODE_API_KEY="your_key_here"
export TMDB_API_KEY="your_key_here"
```

### 4. Setup Movie Posters (Optional)

To enable real movie posters in the HTML output:

```bash
# Run the TMDB setup script
python scripts/setup_tmdb.py
```

This will guide you through getting a free TMDB API key and configuring it for poster fetching.

### 5. Setup CI/CD Environments (Optional)

To enable staging and production deployments:

```bash
# Setup GitHub environments and CI/CD
python scripts/setup_environments.py
```

This will guide you through setting up staging and production environments with proper CI/CD pipelines.

### 6. Run the Scripts

```bash
# Activate virtual environment
source venv/bin/activate

# Fetch streaming data for all movies
python scripts/fetch_streaming_info.py

# Generate HTML output with posters
python scripts/generate_html.py
```

### 7. Create Pull Requests

```bash
# Generate PR summary with change analysis
python scripts/generate_pr_summary.py
```

This will create a comprehensive PR summary with:
- Links to production and staging sites
- Before/after comparison
- Detailed change analysis
- Testing instructions

### 5. View Results

- Streaming data will be saved to `data/streaming_data.json`
- HTML output will be generated in `output/index.html`

## Data Format

### Input (`data/movies.json`)
```json
{
  "episodes": [
    {
      "episode_number": 234,
      "title": "The Strangers: Prey at Night",
      "air_date": "2024-01-15",
      "description": "Episode description",
      "movies": [
        {
          "title": "The Strangers: Prey at Night",
          "year": 2018,
          "imdb_id": "tt1285009",
          "notes": "Main movie discussed in episode"
        }
      ]
    }
  ]
}
```

### Output (`data/streaming_data.json`)
```json
{
  "episodes": [
    {
      "episode_number": 234,
      "movies": [
        {
          "title": "The Strangers: Prey at Night",
          "year": 2018,
          "streaming_sources": [
            {
              "name": "Netflix",
              "type": "subscription",
              "region": "US",
              "web_url": "https://netflix.com/title/..."
            }
          ],
          "data_sources": ["watchmode", "tmdb"]
        }
      ]
    }
  ]
}
```

## API Data Sources

### Primary: Watchmode API
- **Comprehensive streaming data** for movies and TV shows
- **Multiple regions** supported (US, UK, Canada, etc.)
- **Real-time availability** across subscription, rental, and purchase services
- **Free tier available** with generous limits

### Fallback: TMDB API
- **Movie metadata** (posters, descriptions, cast)
- **Watch providers** (powered by JustWatch partnership)
- **Completely free** with high rate limits
- **Rich movie database** with extensive coverage

## Development

### Adding New Episodes

1. Edit `data/movies.json` to add new episodes and movies
2. Run `python scripts/fetch_streaming_info.py` to update streaming data
3. Run `python scripts/generate_html.py` to rebuild the site
4. Commit and push to trigger automatic deployment

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Hosting

This project is deployed via GitHub Pages with automated updates using GitHub Actions and secure API key management.

### Quick Deployment
1. **Add API keys to GitHub Secrets** (see [Deployment Guide](docs/DEPLOYMENT.md))
2. **Enable GitHub Pages** in repository settings
3. **Push changes** to trigger automatic deployment

### Automated Features
- **Auto-updates** when movie data changes
- **Daily refresh** of streaming availability
- **Secure API key handling** via GitHub Secrets
- **Zero-downtime deployments** 

For detailed setup instructions, see: **[Deployment Guide](docs/DEPLOYMENT.md)**

## License

MIT License - see LICENSE file for details.

## Non-Commercial Statu
- No monetization
- No ads
- No tracking
- Pure fan resource

**Project Creator**: 
- Email: [j<!-- -->oe<!-- -->@sh<!-- -->owblen<!-- -->der.com](mailto:joe@showblender.com)
- GitHub: [@SerialForBreakfast](https://github.com/SerialForBreakfast)

## TS;DW Creators
 - This was just for fun to learn some new code and to share with your other fans.  If you want ownership or changes just let me know and It'll be done.  Love the show.
---
