

# Tasks for TooScaryDidntStream

Organized by Minimum Viable Product (MVP) milestones to track iterative project completion.

---

## ✅ MVP 1: Static Movie Episode Tracker

### Task 1: Define Initial Movie Data
**Description**: Create a structured JSON file to store podcast episodes and their mentioned movies.
**User Story**: As a project contributor, I want a consistent format for listing movies by episode so that I can fetch and display relevant streaming data.
**Acceptance Criteria**:
- `data/movies.json` is present
- At least 2 sample episodes with movie titles
**Dependencies**: None

---

### Task 2: Fetch Streaming Info from JustWatch API
**Description**: Build a Python script to call the JustWatch API and retrieve streaming info for all movies listed in the JSON file.
**User Story**: As a maintainer, I want to automatically retrieve streaming availability data so that the HTML output is accurate and up-to-date.
**Acceptance Criteria**:
- Script accepts movie titles from `movies.json`
- Calls JustWatch API and stores results in `data/streaming_data.json`
- Handles failures gracefully (missing results, HTTP errors)
**Dependencies**: Task 1

---

### Task 3: Generate HTML Output Page
**Description**: Create a Python script to render a static HTML file listing episodes and associated movies with streaming links.
**User Story**: As a user, I want to view a clean HTML page that groups movies by episode and shows where I can stream them.
**Acceptance Criteria**:
- Output is written to `output/index.html`
- Each movie is nested under its episode
- Streaming providers and URLs are displayed when available
**Dependencies**: Task 2

---

## ✅ MVP 2: Automation and Deployment

### Task 4: Set Up GitHub Actions Workflow
**Description**: Configure a GitHub Actions workflow that re-runs the scripts when movie data changes or on a schedule.
**User Story**: As a maintainer, I want to ensure the data and site stay updated automatically without manual intervention.
**Acceptance Criteria**:
- `.github/workflows/update.yaml` exists
- Workflow runs on push to `data/movies.json` and daily via cron
- Generated HTML is committed back to the repo
**Dependencies**: Tasks 2, 3

---

### Task 5: Enable GitHub Pages Hosting
**Description**: Configure GitHub Pages to serve the generated HTML output from the `output/` directory.
**User Story**: As a podcast fan, I want to view the up-to-date movie tracker from a public URL.
**Acceptance Criteria**:
- GitHub Pages is enabled in repo settings
- Site correctly renders `output/index.html`
**Dependencies**: Task 3

---

## ✅ MVP 3: Site Polish and Resilience

### Task 6: Improve HTML Display
**Description**: Enhance the static HTML with basic CSS styles and layout.
**User Story**: As a user, I want the movie tracker to be visually clean and easy to navigate.
**Acceptance Criteria**:
- HTML output includes inline or linked CSS
- Posters, provider logos, and cleaner layout for stream links
**Dependencies**: Task 3

---

### Task 7: Add Provider Name Mapping
**Description**: Map JustWatch provider IDs to human-readable names and icons where available.
**User Story**: As a user, I want to see recognizable names/logos for streaming services instead of opaque IDs.
**Acceptance Criteria**:
- Provider ID map implemented in `fetch_streaming_info.py` or included in output
- Provider name and icon (if available) are shown in HTML
**Dependencies**: Task 2, Task 6

---

### Task 8: Handle Missing or Incomplete Results
**Description**: Improve data-fetching resilience by skipping or logging missing matches and optionally retrying with alternate queries or TMDB fallback.
**User Story**: As a contributor, I want consistent output even if the API can’t find one or more movie titles.
**Acceptance Criteria**:
- Missing streaming info is logged clearly
- Partial results still generate valid HTML
**Dependencies**: Task 2

---

## ✅ Future Enhancements

- Auto-extract movie titles from podcast transcripts (via Whisper or LLMs)
- Allow filtering by genre or provider
- Add search UI or sort controls to HTML
