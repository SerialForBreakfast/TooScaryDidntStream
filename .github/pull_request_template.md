# Pull Request Template

## 📋 Overview

**Type of Change:** [Feature/Bugfix/Documentation/Refactor]
**Related Issue:** [Link to issue if applicable]

## 🔗 Site Links

### Production Site
- **Current Production:** https://serialforbreakfast.github.io/TooScaryDidntStream/output/index.html
- **Production Branch:** `gh-pages`

### Staging Site
- **Staging Preview:** https://serialforbreakfast.github.io/TooScaryDidntStream/staging/
- **Staging Branch:** `staging-pages`

## 📊 Before & After Comparison

### Before (Production)
- **URL:** https://serialforbreakfast.github.io/TooScaryDidntStream/output/index.html
- **Key Features:** [List current production features]

### After (Staging)
- **URL:** https://serialforbreakfast.github.io/TooScaryDidntStream/staging/
- **New Features:** [List new features in this PR]

## 🎯 Changes Summary

### What Changed
- [ ] **Data Updates:** [Describe any changes to `data/movies.json`]
- [ ] **Script Updates:** [Describe any changes to `scripts/` files]
- [ ] **UI/UX Changes:** [Describe visual or interaction changes]
- [ ] **Documentation:** [Describe any documentation updates]
- [ ] **CI/CD Changes:** [Describe any workflow or deployment changes]

### Detailed Changes
```
[Provide a detailed list of all changes made in this PR]
```

### Files Modified
- [ ] `data/movies.json` - [Description of changes]
- [ ] `scripts/generate_html.py` - [Description of changes]
- [ ] `.github/workflows/` - [Description of changes]
- [ ] `docs/` - [Description of changes]
- [ ] `README.md` - [Description of changes]

## 🧪 Testing Checklist

### Staging Environment Testing
- [ ] **Site Loads:** Staging site loads without errors
- [ ] **Responsive Design:** Works on desktop, tablet, and mobile
- [ ] **Movie Posters:** Posters display correctly (with/without TMDB API)
- [ ] **Streaming Links:** All streaming links work properly
- [ ] **Search Functionality:** Episode search works correctly
- [ ] **Filter Functionality:** Streaming filters work as expected
- [ ] **Sidebar Toggle:** Show/hide sidebar works smoothly
- [ ] **Episode Navigation:** Clicking episodes scrolls to correct section
- [ ] **Performance:** Page loads quickly and smoothly

### Visual Testing
- [ ] **Desktop (1920x1080):** All elements properly positioned
- [ ] **Tablet (768px):** Responsive layout works correctly
- [ ] **Mobile (375px):** Mobile layout is functional
- [ ] **Poster Images:** Movie posters display with proper sizing
- [ ] **Typography:** All text is readable and properly sized
- [ ] **Colors:** Color scheme is consistent and accessible

### Functionality Testing
- [ ] **Data Validation:** All episodes and movies display correctly
- [ ] **Streaming Data:** Streaming sources are accurate and up-to-date
- [ ] **API Integration:** TMDB API calls work (if applicable)
- [ ] **Error Handling:** Graceful fallbacks for missing data
- [ ] **Cross-browser:** Works in Chrome, Firefox, Safari, Edge

## 📈 Impact Assessment

### User Experience Impact
- **Positive Changes:** [List improvements to user experience]
- **Potential Issues:** [List any potential concerns or breaking changes]
- **Migration Notes:** [Any steps users need to take]

### Performance Impact
- **Page Load Time:** [Estimated impact on load times]
- **File Size Changes:** [Changes to HTML/CSS/JS file sizes]
- **API Calls:** [Impact on external API usage]

### Technical Debt
- **Code Quality:** [Impact on code maintainability]
- **Documentation:** [Updates needed for documentation]
- **Testing:** [New tests needed or existing tests updated]

## 🔍 Review Guidelines

### For Reviewers
1. **Compare Staging vs Production:** Use the provided links to compare
2. **Test Responsive Design:** Check on different screen sizes
3. **Verify Functionality:** Test all interactive features
4. **Check Performance:** Ensure no significant performance regressions
5. **Review Code Quality:** Ensure clean, maintainable code

### Review Checklist
- [ ] **Code Review:** Code follows project standards
- [ ] **Functionality:** All features work as expected
- [ ] **Responsive Design:** Works on all target devices
- [ ] **Accessibility:** Meets accessibility standards
- [ ] **Performance:** No significant performance impact
- [ ] **Documentation:** Changes are properly documented
- [ ] **Testing:** Appropriate tests are included/updated

## 🚀 Deployment Notes

### Staging Deployment
- **Status:** [Pending/In Progress/Complete]
- **URL:** https://serialforbreakfast.github.io/TooScaryDidntStream/staging/
- **Branch:** `staging-pages`

### Production Deployment
- **Status:** [Pending/In Progress/Complete]
- **URL:** https://serialforbreakfast.github.io/TooScaryDidntStream/output/index.html
- **Branch:** `gh-pages`
- **Trigger:** Automatic on merge to `main`

## 📝 Additional Notes

### Breaking Changes
[Describe any breaking changes and migration steps]

### Dependencies
[List any new dependencies or requirements]

### Environment Variables
[Document any new environment variables needed]

### Future Considerations
[Note any follow-up work or future improvements]

---

**PR Author:** [Your Name]
**Reviewers:** [Tag relevant reviewers]
**Labels:** [Add appropriate labels]

---

*This template ensures comprehensive review and testing of all changes before production deployment.* 