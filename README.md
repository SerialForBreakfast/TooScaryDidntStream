
# TooScaryDidntStream

A tool to help find where to stream movies mentioned in the *Too Scary; Didn't Watch* podcast.

## Github
https://github.com/SerialForBreakfast/TooScaryDidntStream

## What it does

- Tracks episodes and the movies they mention.
- Queries the JustWatch API to find current streaming availability.
- Outputs a clean HTML page with posters, streaming providers, and episode groupings.
- Auto-updates via GitHub Actions and deploys with GitHub Pages.

## Project Structure

```
.
├── data/
│   └── movies.json         # Source of truth for episodes and movies
├── output/
│   └── index.html          # Auto-generated HTML page
├── scripts/
│   ├── fetch_streaming_info.py  # Gets movie metadata from JustWatch
│   └── generate_html.py         # Builds HTML view from data
├── .github/
│   └── workflows/
│       └── update.yaml     # GitHub Actions workflow
└── README.md
```

## Getting Started

1. Clone this repository.
2. Add your own `data/movies.json` file with podcast movie mentions.
3. Run:

   ```bash
   python scripts/fetch_streaming_info.py
   python scripts/generate_html.py
   ```

4. Commit and push changes to trigger the GitHub Actions deployment.

## Hosting

This project is deployed via GitHub Pages. Output lives in the `output/` directory and updates automatically via GitHub Actions.

---
Created with ❤️ for movie nerds.
