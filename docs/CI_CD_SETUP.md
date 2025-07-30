# CI/CD Staging Environment Setup

This document describes the staging environment and CI/CD pipeline for the TooScaryDidntStream project.

## 🏗️ Environment Overview

### Development → Staging → Production

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Development   │───▶│     Staging     │───▶│   Production    │
│                 │    │                 │    │                 │
│ • Feature       │    │ • PR Preview    │    │ • Live Site     │
│ • Bugfix        │    │ • Testing       │    │ • Main Branch   │
│ • Testing       │    │ • Validation    │    │ • Auto Deploy   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🔄 Workflow Pipeline

### 1. Development Environment
- **Trigger**: Pushes to `develop`, `feature/*`, `bugfix/*` branches
- **Purpose**: Validate changes, test functionality
- **Actions**:
  - Data format validation
  - HTML generation testing
  - Responsive design verification
  - Artifact creation

### 2. Staging Environment
- **Trigger**: Pull requests to `main` branch
- **Purpose**: Preview changes before production
- **Actions**:
  - Build and test changes
  - Deploy to staging URL
  - Create deployment status
  - Comment on PR with preview link

### 3. Production Environment
- **Trigger**: Merges to `main` branch or scheduled updates
- **Purpose**: Live production deployment
- **Actions**:
  - Fetch latest streaming data
  - Generate production HTML
  - Deploy to GitHub Pages
  - Create production deployment

## 🚀 Quick Start

### For Contributors

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes:**
   - Edit `data/movies.json` for new episodes
   - Modify `scripts/` for functionality changes
   - Update documentation as needed

3. **Push and create PR:**
   ```bash
   git add .
   git commit -m "Add your feature description"
   git push origin feature/your-feature-name
   ```
   Then create a Pull Request to `main`

4. **Review staging deployment:**
   - GitHub Actions will automatically deploy to staging
   - Check the PR comments for the staging URL
   - Test functionality on staging before merging

### For Maintainers

1. **Review staging deployments:**
   - Check staging URL in PR comments
   - Verify responsive design works
   - Test poster functionality
   - Validate streaming data

2. **Approve and merge:**
   - Once satisfied with staging, approve PR
   - Merge to trigger production deployment

3. **Monitor production:**
   - Check production deployment status
   - Verify live site functionality

## 📋 Environment URLs

### Staging
- **URL**: `https://[username].github.io/[repo]/staging/`
- **Branch**: `staging-pages`
- **Purpose**: Preview changes before production

### Production
- **URL**: `https://[username].github.io/[repo]/`
- **Branch**: `gh-pages`
- **Purpose**: Live production site

## 🔧 Configuration

### Required Secrets

Set these in your GitHub repository settings:

1. **TMDB_API_KEY** (Optional)
   - Used for real movie posters
   - Get from: https://www.themoviedb.org/settings/api

2. **GITHUB_TOKEN** (Automatic)
   - Provided by GitHub Actions
   - Used for deployments and API calls

### Environment Protection

#### Staging Environment
- **Protection**: Basic validation
- **Required Checks**: None (for quick testing)
- **Reviewers**: Optional

#### Production Environment
- **Protection**: Strict validation
- **Required Checks**: Staging Environment must pass
- **Reviewers**: Required for deployment
- **Conversation Resolution**: Required

## 🧪 Testing Strategy

### Automated Tests

1. **Data Validation**
   - JSON format validation
   - Required field checks
   - Episode structure validation

2. **HTML Generation**
   - Successful HTML creation
   - File size verification
   - Responsive CSS detection

3. **Poster Integration**
   - Poster count verification
   - Responsive image sources
   - Fallback handling

### Manual Testing Checklist

#### Staging Review
- [ ] Site loads correctly
- [ ] Responsive design works on mobile/tablet/desktop
- [ ] Movie posters display properly
- [ ] Streaming links work
- [ ] Search and filter functionality
- [ ] Episode navigation works
- [ ] No console errors

#### Production Verification
- [ ] Live site is accessible
- [ ] All functionality preserved
- [ ] Performance is acceptable
- [ ] No broken links or images

## 🔍 Troubleshooting

### Common Issues

1. **Staging deployment fails**
   - Check GitHub Actions logs
   - Verify branch permissions
   - Ensure secrets are configured

2. **Posters not loading**
   - Verify TMDB API key is set
   - Check network connectivity
   - Review API rate limits

3. **Responsive design issues**
   - Test on different devices
   - Check CSS media queries
   - Verify viewport meta tag

### Debug Commands

```bash
# Test local generation
python scripts/generate_html.py

# Validate data format
python -c "import json; json.load(open('data/movies.json'))"

# Check file sizes
ls -la output/

# Test responsive CSS
grep -A 5 "@media" output/index.html
```

## 📊 Monitoring

### GitHub Actions Dashboard
- **URL**: `https://github.com/[username]/[repo]/actions`
- **Purpose**: Monitor workflow runs and deployments

### Deployment History
- **URL**: `https://github.com/[username]/[repo]/deployments`
- **Purpose**: Track deployment status and history

### Environment Status
- **URL**: `https://github.com/[username]/[repo]/environments`
- **Purpose**: View environment protection and status

## 🔄 Workflow Files

### `.github/workflows/development.yml`
- Development testing and validation
- Runs on feature branches

### `.github/workflows/staging.yml`
- Staging deployment and preview
- Runs on pull requests

### `.github/workflows/update-streaming-data.yml`
- Production deployment
- Runs on main branch and schedules

## 📝 Best Practices

1. **Always test in staging first**
2. **Use descriptive commit messages**
3. **Review staging deployments thoroughly**
4. **Monitor production after deployment**
5. **Keep environments in sync**
6. **Document breaking changes**

## 🆘 Support

For issues with the CI/CD pipeline:
1. Check GitHub Actions logs
2. Review environment configurations
3. Verify secrets and permissions
4. Test locally if possible
5. Create an issue with detailed error information 