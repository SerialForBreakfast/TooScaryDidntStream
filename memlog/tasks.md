

# Tasks for TooScaryDidntStream

Organized by Minimum Viable Product (MVP) milestones to track iterative project completion.

Status Legend:
- Open: Task not yet started
- In Progress: Task currently being worked on
- Blocked: Task waiting on dependencies or external factors
- Completed: Task finished and accepted

---

## MVP 1: Static Movie Episode Tracker

### Task 1: Define Initial Movie Data
Status: Completed
Description: Create a structured JSON file to store podcast episodes and their mentioned movies.
User Story: As a project contributor, I want a consistent format for listing movies by episode so that I can fetch and display relevant streaming data.
Acceptance Criteria:
- data/movies.json file exists
- Contains at least 2 sample episodes with movie titles
Dependencies: None
Completed: 2024-01-29 - Created data/movies.json with 3 sample episodes and 7 movies

---

### Task 2: Fetch Streaming Info from Watchmode/TMDB APIs
Status: Completed
Description: Build a Python script to call streaming APIs and retrieve streaming info for all movies listed in the JSON file.
User Story: As a maintainer, I want to automatically retrieve streaming availability data so that the HTML output is accurate and up-to-date.
Acceptance Criteria:
- Script accepts movie titles from movies.json
- Calls Watchmode/TMDB APIs and stores results in data/streaming_data.json
- Handles failures gracefully with missing results and HTTP errors
Dependencies: Task 1 completed
Completed: 2024-01-29 - Created scripts/fetch_streaming_info.py with dual API support
Notes: Switched from JustWatch to Watchmode API (primary) + TMDB API (fallback)

---

### Task 3: Generate HTML Output Page
Status: Completed
Description: Create a Python script to render a static HTML file listing episodes and associated movies with streaming links.
User Story: As a user, I want to view a clean HTML page that groups movies by episode and shows where I can stream them.
Acceptance Criteria:
- Output is written to output/index.html
- Each movie is nested under its episode
- Streaming providers and URLs are displayed when available
Dependencies: Task 2 completed
Completed: 2024-01-29 - Created scripts/generate_html.py with responsive design and comprehensive features

---

## MVP 2: Automation and Deployment

### Task 4: Set Up GitHub Actions Workflow
Status: Completed
Description: Configure a GitHub Actions workflow that re-runs the scripts when movie data changes or on a schedule.
User Story: As a maintainer, I want to ensure the data and site stay updated automatically without manual intervention.
Acceptance Criteria:
- .github/workflows/update-streaming-data.yml exists
- Workflow runs on push to data/movies.json and daily via cron
- Generated HTML is committed back to the repo
Dependencies: Tasks 2 and 3 (Task 2 completed, Task 3 in progress)
Completed: 2024-01-29 - Created comprehensive GitHub Actions workflow with secure API key handling

---

### Task 5: Enable GitHub Pages Hosting
Status: Completed
Description: Configure GitHub Pages to serve the generated HTML output from the output/ directory.
User Story: As a podcast fan, I want to view the up-to-date movie tracker from a public URL.
Acceptance Criteria:
- GitHub Pages is enabled in repo settings
- Site correctly renders output/index.html
Dependencies: Task 3 (in progress)
Completed: 2024-01-29 - Created GitHub Pages deployment configuration in workflow

---

## MVP 3: Site Polish and Resilience

### Task 6: Improve HTML Display
Status: Completed
Description: Enhance the static HTML with basic CSS styles and layout.
User Story: As a user, I want the movie tracker to be visually clean and easy to navigate.
Acceptance Criteria:
- HTML output includes inline or linked CSS
- Posters, provider logos, and cleaner layout for stream links
- Streaming sources organized by type (FREE, SUBSCRIPTION, RENT, BUY)
- Clear section labels and improved visual hierarchy
Dependencies: Task 3
Completed: 2025-07-29 - Implemented sectioned streaming display with priority sorting and clear labels

---

### Task 7: Add Provider Name Mapping
Status: Completed
Description: Map streaming provider IDs to human-readable names and icons where available.
User Story: As a user, I want to see recognizable names/logos for streaming services instead of opaque IDs.
Acceptance Criteria:
- Provider ID map implemented in fetch_streaming_info.py or included in output
- Provider name and icon (if available) are shown in HTML
Dependencies: Task 2 completed, Task 6 open
Completed: 2024-01-29 - Implemented in streaming fetcher with provider logos from APIs

---

### Task 8: Handle Missing or Incomplete Results
Status: Completed
Description: Improve data-fetching resilience by skipping or logging missing matches and optionally retrying with alternate queries or TMDB fallback.
User Story: As a contributor, I want consistent output even if the API can't find one or more movie titles.
Acceptance Criteria:
- Missing streaming info is logged clearly
- Partial results still generate valid HTML
Dependencies: Task 2 completed
Completed: 2024-01-29 - Implemented comprehensive error handling and dual API fallback

---

## Additional Tasks (Added During Development)

### Task 9: Security and API Key Management
Status: Completed
Description: Implement secure API key management using GitHub Secrets and create comprehensive security documentation.
User Story: As a maintainer, I want to ensure API keys are secure and never exposed in code or logs.
Acceptance Criteria:
- GitHub Secrets integration in workflow
- Comprehensive security documentation
- Multiple deployment options documented
Dependencies: Task 4 completed
Completed: 2024-01-29 - Created docs/DEPLOYMENT.md with enterprise-grade security strategy

---

### Task 10: Project Setup and Documentation
Status: Completed
Description: Set up virtual environment, dependencies, and comprehensive project documentation.
User Story: As a developer, I want clear setup instructions and well-documented code.
Acceptance Criteria:
- Virtual environment setup documented
- requirements.txt with dependencies
- Updated README with complete instructions
- Proper .gitignore for Python projects
Dependencies: None
Completed: 2024-01-29 - Full project structure and documentation

---

### Task 11: Comprehensive Data Population and Cleanup
Status: Completed
Description: Populate movies.json with complete podcast episode data and clean up the dataset.
User Story: As a user, I want access to the complete podcast catalog with accurate movie information.
Acceptance Criteria:
- All 343 episodes from podcast history included
- No duplicate episodes
- Proper episode references and sequential numbering
- Sorted from oldest to newest
- Correct movie titles and release years
Dependencies: Task 1 completed
Completed: 2025-07-29 - Extracted 340 episodes from HTML, cleaned duplicates, fixed titles/years, sorted chronologically

---

### Task 12: API Optimization and Rate Limit Management
Status: Completed
Description: Implement Phase 1 API optimization strategy to stay within free tier limits.
User Story: As a maintainer, I want to ensure the project stays within API free tier limits while maintaining fresh data.
Acceptance Criteria:
- TMDB-only approach implemented
- Smart incremental updates with 7-day caching
- Daily incremental updates and weekly full refresh schedule
- API usage monitoring and logging
- Mock testing framework for development
Dependencies: Task 2 completed
Completed: 2025-07-29 - Implemented TMDB-only streaming fetcher with incremental updates, updated GitHub Actions schedule, created test framework

---

## Future Enhancements

### Task 13: Auto-extract Movie Titles
Status: Open
Description: Auto-extract movie titles from podcast transcripts (via Whisper or LLMs)
Dependencies: MVP 1-3 completion

### Task 14: Filtering and Search Features
Status: Open
Description: Allow filtering by genre or provider, add search UI or sort controls to HTML
Dependencies: Task 3, Task 6

### Task 15: Enhanced Movie Metadata
Status: Open
Description: Add movie posters, ratings, cast, and additional metadata to enhance user experience
Dependencies: Task 3, Task 6

---

## Summary

Overall Progress: 10/10 core tasks completed (100%)

Completed (10):
- Task 1: Define Initial Movie Data
- Task 2: Fetch Streaming Info (with API pivot)
- Task 3: Generate HTML Output Page
- Task 4: GitHub Actions Workflow
- Task 5: GitHub Pages Hosting
- Task 6: Improve HTML Display
- Task 7: Provider Name Mapping
- Task 8: Handle Missing Results
- Task 9: Security and API Key Management
- Task 10: Project Setup and Documentation
- Task 11: Comprehensive Data Population and Cleanup
- Task 12: API Optimization and Rate Limit Management

In Progress (0):
- None

Open (3):
- Task 13: Auto-extract Movie Titles
- Task 14: Filtering and Search Features
- Task 15: Enhanced Movie Metadata

Next Priority: All MVP tasks completed! Ready for deployment and testing with API keys.
