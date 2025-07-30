# API Considerations and Rate Limits

## Current Data Scale

- **Total Episodes**: 343 episodes
- **Total Movies**: 343 movies (1 per episode)
- **Daily API Calls**: ~686 calls per full refresh (343 movies × 2 APIs)

## API Sources and Limits

### 1. Watchmode API (Primary)

**Free Tier Limits:**
- **1,000 requests per month**
- Rate limit: 10 requests per second
- No daily limits specified

**API Calls Per Movie:**
- 1 search call to find movie ID
- 1 sources call to get streaming data
- **Total: 2 calls per movie**

**Monthly Usage Analysis:**
- Full refresh (343 movies): 686 calls
- Daily refresh (30 days): 20,580 calls
- **❌ EXCEEDS FREE LIMIT** by ~20x

### 2. TMDB API (Fallback)

**Free Tier Limits:**
- **1,000 requests per day**
- Rate limit: 50 requests per second
- No monthly limits

**API Calls Per Movie:**
- 1 search call to find movie ID
- 1 watch providers call to get streaming data
- **Total: 2 calls per movie**

**Daily Usage Analysis:**
- Full refresh (343 movies): 686 calls
- **✅ WITHIN FREE LIMIT** (686 < 1,000)

## Recommended Strategy

### Option A: TMDB-Only Approach (Recommended)
```yaml
Primary: TMDB API
- Daily limit: 1,000 requests
- Our usage: 686 requests per full refresh
- Safety margin: 314 requests remaining
- Cost: Free
- Coverage: Good (powered by JustWatch partnership)
```

### Option B: Hybrid Approach
```yaml
Primary: TMDB API (daily refresh)
Fallback: Watchmode API (weekly refresh)
- TMDB: 686 calls daily
- Watchmode: 686 calls weekly
- Total monthly: 20,580 + 2,744 = 23,324 calls
- Cost: Free tier exceeded
```

### Option C: Incremental Updates
```yaml
Strategy: Only update new/changed movies
- Daily: Check for new episodes (5-10 movies)
- Weekly: Full refresh of recent episodes
- Monthly: Full refresh of all episodes
- Estimated daily calls: 10-20
- Estimated monthly calls: 600-1,200
- Cost: Well within free limits
```

## Implementation Recommendations

### 1. Immediate Changes Needed

**Update GitHub Actions Workflow:**
```yaml
# Current: Daily full refresh
schedule:
  - cron: '0 6 * * *'  # Daily at 6 AM

# Recommended: Incremental updates
schedule:
  - cron: '0 6 * * *'  # Daily incremental
  - cron: '0 6 * * 0'  # Weekly full refresh
```

### 2. Smart Update Logic

**Add to fetch_streaming_info.py:**
```python
def get_movies_to_update(self) -> List[Dict[str, Any]]:
    """Only fetch data for movies that need updating."""
    # Check last update time
    # Only update movies older than 7 days
    # Only update new episodes
    # Skip movies with recent streaming data
```

### 3. Caching Strategy

**Implement Local Caching:**
```python
# Cache streaming data for 7 days
# Skip API calls for recently updated movies
# Store last update timestamp per movie
```

## Rate Limiting Improvements

### Current Implementation:
```python
self.min_request_interval = 0.1  # 100ms between requests
```

### Recommended Implementation:
```python
# TMDB: 50 requests/second = 20ms interval
# Watchmode: 10 requests/second = 100ms interval
# Add exponential backoff for failures
# Add request queuing for high-volume updates
```

## Cost Analysis

### Free Tier Usage:
- **TMDB**: 686 calls daily = 20,580 monthly
- **Watchmode**: 686 calls daily = 20,580 monthly
- **Total**: 41,160 calls monthly

### Paid Tier Costs (if needed):
- **Watchmode Pro**: $99/month for 10,000 requests
- **TMDB**: Free tier sufficient
- **Alternative**: JustWatch API (partner access required)

## Recommended Action Plan

### Phase 1: Immediate (This Week)
1. **Switch to TMDB-only** for daily updates
2. **Implement incremental updates** (only new movies)
3. **Add caching** to avoid redundant API calls
4. **Update GitHub Actions** to run weekly full refresh

### Phase 2: Optimization (Next Week)
1. **Add smart update detection**
2. **Implement request queuing**
3. **Add failure retry logic**
4. **Monitor API usage** with logging

### Phase 3: Scale (Future)
1. **Consider paid API tiers** if needed
2. **Add multiple region support**
3. **Implement advanced caching**
4. **Add streaming data validation**

## Monitoring and Alerts

### Add to GitHub Actions:
```yaml
- name: Check API Usage
  run: |
    # Log API call counts
    # Alert if approaching limits
    # Track success/failure rates
```

### Metrics to Track:
- API calls per day/week/month
- Success rate per API
- Response times
- Error rates
- Cache hit rates

## Conclusion

**Current daily cron job will exceed free limits** by ~20x. 

**Recommended approach:**
1. Use TMDB-only for daily updates (within limits)
2. Implement incremental updates (only new movies)
3. Add 7-day caching to reduce API calls
4. Monitor usage and adjust as needed

This will keep us well within free tier limits while maintaining fresh streaming data. 