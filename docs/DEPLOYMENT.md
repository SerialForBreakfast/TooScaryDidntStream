# Deployment Guide

This guide explains how to securely deploy TooScaryDidntStream with automated updates using GitHub Actions and GitHub Secrets.

## Security Strategy

### API Key Management Options

| Method | Use Case | Security Level | Complexity |
|--------|----------|---------------|------------|
| **GitHub Secrets** | CI/CD automation | Excellent | Low |
| **Environment Variables** | Local development | Good | Very Low |
| **Encrypted .env** | Team sharing | Very Good | Medium |
| **External Key Management** | Enterprise | Excellent | High |

## Recommended Setup: GitHub Secrets + Actions

### Step 1: Set Up GitHub Secrets

1. **Navigate to your repository on GitHub**
2. **Go to Settings > Secrets and variables > Actions**
3. **Click "New repository secret"**
4. **Add these secrets:**

| Secret Name | Value | Where to Get |
|-------------|-------|--------------|
| `WATCHMODE_API_KEY` | Your Watchmode API key | [https://api.watchmode.com/](https://api.watchmode.com/) |
| `TMDB_API_KEY` | Your TMDB API key | [https://www.themoviedb.org/settings/api](https://www.themoviedb.org/settings/api) |

### Step 2: Enable GitHub Pages

1. **Go to Settings > Pages**
2. **Source: Deploy from a branch**
3. **Branch: `gh-pages` / `/ (root)`**
4. **Save the settings**

### Step 3: Enable Actions (if not already enabled)

1. **Go to Settings > Actions > General**
2. **Allow all actions and reusable workflows**
3. **Workflow permissions: Read and write permissions**
4. **Save**

### Step 4: Test the Workflow

1. **Make a small change to `data/movies.json`**
2. **Commit and push to main branch**
3. **Go to Actions tab to watch the workflow run**
4. **Check your GitHub Pages URL for the updated site**

## Workflow Features

### Automatic Triggers
- **Data Updates**: Runs when `data/movies.json` is modified
- **Daily Refresh**: Updates streaming data at 6 AM UTC daily
- **Manual Trigger**: Can be run manually from Actions tab

### Security Features
- **API keys never exposed** in logs or code
- **Encrypted secrets** at rest and in transit
- **Limited scope** - only accessible to authorized workflows
- **Audit trail** - all access is logged

### Auto-deployment Pipeline
1. **Fetch latest streaming data** using secure API keys
2. **Generate updated HTML** with new information
3. **Commit changes** back to repository
4. **Deploy to GitHub Pages** automatically

## Advanced Security Options

### Option A: Organization Secrets (for multiple repos)
- Set secrets at organization level
- Share across multiple repositories
- Centralized key management

### Option B: Environment-Specific Secrets
```yaml
# In your workflow
environment: production
env:
  WATCHMODE_API_KEY: ${{ secrets.PROD_WATCHMODE_API_KEY }}
  TMDB_API_KEY: ${{ secrets.PROD_TMDB_API_KEY }}
```

### Option C: External Secret Management
For enterprise use, consider:
- **Azure Key Vault**
- **AWS Secrets Manager** 
- **HashiCorp Vault**
- **Google Secret Manager**

## Monitoring and Maintenance

### Check Workflow Health
1. **Monitor Actions tab** for failed runs
2. **Set up notifications** for workflow failures
3. **Review logs** for API rate limit warnings

### API Key Rotation
1. **Generate new API keys** from providers
2. **Update GitHub Secrets** with new values
3. **Old keys remain active** until you disable them
4. **Test workflow** with new keys

### Troubleshooting Common Issues

| Issue | Solution |
|-------|----------|
| Workflow fails with "API key not found" | Check secret names match exactly |
| Rate limit exceeded | Add delays or reduce frequency |
| Pages not updating | Check gh-pages branch deployment |
| Commits not pushed | Check repository permissions |

## Alternative Deployment Options

### Option 1: Vercel with Environment Variables
```bash
# Deploy to Vercel
npm install -g vercel
vercel --env WATCHMODE_API_KEY=your_key
```

### Option 2: Netlify with Build Hooks
```yaml
# netlify.toml
[build.environment]
  WATCHMODE_API_KEY = "secured_in_netlify_ui"
```

### Option 3: Self-Hosted with Docker
```dockerfile
# Dockerfile
FROM python:3.11-slim
# API keys passed as build args (use build secrets)
ARG WATCHMODE_API_KEY
ARG TMDB_API_KEY
```

## Security Checklist

- [ ] API keys stored in GitHub Secrets (never in code)
- [ ] `.env` files added to `.gitignore`
- [ ] Workflow permissions set to minimum required
- [ ] Repository visibility set appropriately (public/private)
- [ ] Branch protection rules enabled for main branch
- [ ] Two-factor authentication enabled on GitHub account
- [ ] Regular API key rotation scheduled
- [ ] Monitoring set up for workflow failures

## Emergency Procedures

### If API Keys Are Compromised
1. **Immediately revoke** the compromised keys at provider
2. **Generate new keys** with different names if possible
3. **Update GitHub Secrets** with new keys
4. **Review access logs** for unauthorized usage
5. **Consider changing** repository visibility temporarily

### If Workflow Starts Failing
1. **Check Actions tab** for error details
2. **Verify API key validity** with providers
3. **Test locally** with same environment
4. **Check rate limits** and usage quotas
5. **Review recent changes** to workflow or dependencies

---

## Quick Start Summary

For immediate deployment:

1. **Get API keys** from Watchmode and TMDB
2. **Add them to GitHub Secrets** as `WATCHMODE_API_KEY` and `TMDB_API_KEY`
3. **Enable GitHub Pages** with `gh-pages` branch
4. **Push changes** to trigger the workflow
5. **Visit your GitHub Pages URL** to see the result

Your site will automatically update daily and whenever you modify the movie data! 