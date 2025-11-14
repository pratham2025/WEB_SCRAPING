// home.js — Notice Board Edition
// Base API URL (avoid redeclaration if app.js already defines it)
if (typeof API_BASE === 'undefined') {
    // Auto-detect hostname: works on localhost and mobile devices via IP
    const hostname = window.location.hostname || '127.0.0.1';
    window.API_BASE = `http://${hostname}:8000`;
}

// Wait for the DOM to load
document.addEventListener('DOMContentLoaded', () => {
    bindButtons();
    loadLatestNews();
});

// ----------------------
// Bind UI Buttons
// ----------------------
function bindButtons() {
    // Toggle between showing top 3 and all notices
    document.getElementById('showAllBtn')?.addEventListener('click', (e) => {
        const btn = e.currentTarget;
        const board = document.getElementById('latestNewsList');
        if (btn.dataset.state === 'all') {
            btn.textContent = 'Show All';
            btn.dataset.state = '';
            loadLatestNews({ limit: 10 });
        } else {
            btn.textContent = 'Show Top 10';
            btn.dataset.state = 'all';
            loadLatestNews({ limit: 10 });
        }
    });

    // Manual refresh button
    document.getElementById('refreshNewsBtn')?.addEventListener('click', async () => {
        await loadLatestNews({ force: true });
        flashNotice('News refreshed');
    });
}

// ----------------------
// Visual feedback notification
// ----------------------
function flashNotice(msg) {
    const node = document.createElement('div');
    node.className = 'notification success';
    node.textContent = msg;
    document.body.appendChild(node);
    setTimeout(() => node.remove(), 2000);
}

// ----------------------
// Fetch and render latest news
// ----------------------
async function loadLatestNews(opts = {}) {
    const listEl = document.getElementById('latestNewsList');
    if (!listEl) {
        console.error('latestNewsList element not found');
        return;
    }

    const limit = opts.limit ?? 10; // Show top 10 news items

    // Show loading state
    listEl.innerHTML = `<div class="notice-empty">Loading news...</div>`;

    try {
        console.log(`Fetching latest news from ${API_BASE}/latest-news`);
        const res = await fetch(`${API_BASE}/latest-news?limit=${limit}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (!res.ok) {
            throw new Error(`HTTP ${res.status}: ${res.statusText}`);
        }

        const data = await res.json();
        console.log('API Response:', data);

        // Normalize data: {news: []}, {data: []}, or array
        let newsItems = [];
        if (data && Array.isArray(data.news)) {
            newsItems = data.news;
        } else if (data && Array.isArray(data.data)) {
            newsItems = data.data;
        } else if (Array.isArray(data)) {
            newsItems = data;
        } else {
            console.warn('Unexpected data format:', data);
            newsItems = [];
        }

        console.log(`Found ${newsItems.length} news items`);

        // Parse and sort by article_date (prioritize article_date over scraped_at)
        newsItems.forEach(item => {
            // Parse article_date properly
            const dateStr = item.article_date || item.date || item.published_at || item.postedAt;
            if (dateStr) {
                // Try to parse the date string (handles formats like "November 5, 2025 09:49 IST")
                let parsedDate = new Date(dateStr);
                
                // If parsing failed, try to extract date from string format
                if (isNaN(parsedDate.getTime()) && typeof dateStr === 'string') {
                    // Extract date from formats like "November 5, 2025 09:49 IST"
                    const dateMatch = dateStr.match(/(\w+)\s+(\d+),\s+(\d{4})/);
                    if (dateMatch) {
                        const [, monthName, day, year] = dateMatch;
                        parsedDate = new Date(`${monthName} ${day}, ${year}`);
                    }
                }
                
                // Store parsed timestamp for sorting
                item._sortDate = isNaN(parsedDate.getTime()) ? 0 : parsedDate.getTime();
            } else {
                // Fallback to scraped_at if article_date is not available
                const scrapedDate = new Date(item.scraped_at || 0);
                item._sortDate = isNaN(scrapedDate.getTime()) ? 0 : scrapedDate.getTime();
            }
        });

        // Sort by article_date descending (newest first), filter out items older than 90 days
        const now = Date.now();
        const ninetyDaysAgo = now - (90 * 24 * 60 * 60 * 1000);
        
        newsItems = newsItems
            .filter(item => item._sortDate > ninetyDaysAgo) // Filter out news older than 90 days
            .sort((a, b) => {
                // Sort by article_date (newest first)
                return b._sortDate - a._sortDate;
            });

        console.log(`After filtering and sorting: ${newsItems.length} news items`);

        // Limit for homepage (top 10)
        const limited = newsItems.slice(0, limit);

        // If no news found
        if (limited.length === 0) {
            listEl.innerHTML = `<div class="notice-empty">No news updates at this time. Check back later!</div>`;
            return;
        }

        console.log(`Rendering ${limited.length} news items`);

        // Build newspaper-style layout: featured card + grid
        listEl.innerHTML = renderNewspaperLayout(limited);

        // Apply staggered animation
        requestAnimationFrame(() => {
            const cards = listEl.querySelectorAll('.news-featured, .news-card-small');
            cards.forEach((card, i) => {
                card.style.animationDelay = `${i * 80}ms`;
                card.classList.add('animate');
            });
        });

        // Links are now direct <a> tags, no need to wire up

    } catch (err) {
        console.error('Failed to load latest news:', err);
        let errorMsg = 'Could not load news. ';
        if (err.message.includes('Failed to fetch') || err.message.includes('NetworkError')) {
            errorMsg += 'Please make sure the backend server is running at ' + API_BASE;
        } else {
            errorMsg += err.message;
        }
        listEl.innerHTML = `<div class="notice-empty">${errorMsg}</div>`;
    }
}

// ----------------------
// Render newspaper-style layout (featured + grid)
// ----------------------
function renderNewspaperLayout(newsItems) {
    if (newsItems.length === 0) return '';
    
    // SECTION 1: Large card 1, Small 1-3 (right), Small 4-5 (below)
    const section1Large = newsItems[0];
    const section1Right = newsItems.slice(1, 4); // Small 1, 2, 3
    const section1Bottom = newsItems.slice(4, 6); // Small 4, 5
    
    // SECTION 2: Small 6-7 (top), Large card 2, Small 8-10 (right)
    const section2Top = newsItems.slice(6, 8); // Small 6, 7
    const section2Large = newsItems[8]; // Large card 2
    const section2Right = newsItems.slice(9); // Small 8, 9, 10 (remaining items)
    
    return `
        <!-- SECTION 1 -->
        <div class="news-section">
            <div class="section-title">Latest Updates</div>
            <div class="newspaper-layout section-1">
                <!-- Large News Card 1 (Left) -->
                <article class="news-featured">
                    ${renderNewsCard(section1Large, 0, true)}
                </article>
                
                <!-- Small 1, 2, 3 (Right, Stacked) -->
                <div class="news-grid-right">
                    ${section1Right.map((news, idx) => `
                        <article class="news-card-small">
                            ${renderNewsCard(news, idx + 1, false)}
                        </article>
                    `).join('')}
                </div>
                
                <!-- Small 4, 5 (Below, Horizontal) -->
                <div class="news-grid-bottom">
                    ${section1Bottom.map((news, idx) => `
                        <article class="news-card-small">
                            ${renderNewsCard(news, idx + 4, false)}
                        </article>
                    `).join('')}
                </div>
            </div>
        </div>
        
        <!-- SECTION 2 -->
        ${newsItems.length > 6 ? `
            <div class="news-section">
                <div class="newspaper-layout section-2">
                    <!-- Small 6, 7 (Top, Horizontal) -->
                    <div class="news-grid-top">
                        ${section2Top.map((news, idx) => `
                            <article class="news-card-small">
                                ${renderNewsCard(news, idx + 6, false)}
                            </article>
                        `).join('')}
                    </div>
                    
                    <!-- Large News Card 2 (Left) -->
                    ${section2Large ? `
                        <article class="news-featured">
                            ${renderNewsCard(section2Large, 8, true)}
                        </article>
                    ` : ''}
                    
                    <!-- Small 8, 9, 10 (Right, Stacked) -->
                    <div class="news-grid-right">
                        ${section2Right.map((news, idx) => `
                            <article class="news-card-small">
                                ${renderNewsCard(news, idx + 9, false)}
                            </article>
                        `).join('')}
                    </div>
                </div>
            </div>
        ` : ''}
    `;
}

// ----------------------
// Render a single news card (with image support)
// ----------------------
function renderNewsCard(news, idx, isFeatured) {
    // Support different field names
    const headline = news.headline ?? news.title ?? news.text ?? news.name ?? 'Untitled';
    const link = news.article_link ?? news.link ?? news.url ?? '#';
    const imageUrl = news.image_url ?? news.imageUrl ?? news.image ?? null;
    // Try multiple date fields, including scraped_at as fallback
    const dateRaw = news.article_date ?? news.scraped_at ?? news.date ?? news.published_at ?? news.postedAt ?? null;

    // Format date
    const dateStr = dateRaw ? fmtDate(dateRaw) : 'Latest';

    // Check if new (within 48 hours)
    let isNew = false;
    if (dateRaw) {
        const dt = new Date(dateRaw);
        if (!isNaN(dt)) {
            const diffMs = Date.now() - dt.getTime();
            isNew = diffMs >= 0 && diffMs <= (48 * 60 * 60 * 1000);
        }
    }

    // Escape for safety
    const safeHeadline = escapeHtml(headline);
    const safeLink = escapeAttr(link);
    const safeImageUrl = imageUrl ? escapeAttr(imageUrl) : null;

    // Featured card has larger image and more content
    if (isFeatured) {
        return `
            ${safeImageUrl ? `
                <div class="news-image featured-image">
                    <img src="${safeImageUrl}" alt="${safeHeadline}" loading="lazy" onerror="this.style.display='none'; this.nextElementSibling.style.display='block';">
                    <div class="image-placeholder" style="display:none;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                            <circle cx="8.5" cy="8.5" r="1.5"></circle>
                            <polyline points="21 15 16 10 5 21"></polyline>
                        </svg>
                    </div>
                </div>
            ` : ''}
            <div class="news-content">
                ${isNew ? `<span class="news-badge">NEW</span>` : ''}
                <div class="news-date">
                    <svg class="date-icon" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                        <line x1="16" y1="2" x2="16" y2="6"></line>
                        <line x1="8" y1="2" x2="8" y2="6"></line>
                        <line x1="3" y1="10" x2="21" y2="10"></line>
                    </svg>
                    ${escapeHtml(dateStr)}
                </div>
                <h3 class="news-headline featured-headline">
                    <a href="${safeLink}" target="_blank" rel="noopener">${safeHeadline}</a>
                </h3>
                <a href="${safeLink}" target="_blank" rel="noopener" class="news-read-link">
                    Read More
                    <svg class="link-icon" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                        <polyline points="15 3 21 3 21 9"></polyline>
                        <line x1="10" y1="14" x2="21" y2="3"></line>
                    </svg>
                </a>
            </div>
        `;
    }
    
    // Small grid card
    return `
        ${safeImageUrl ? `
            <div class="news-image small-image">
                <img src="${safeImageUrl}" alt="${safeHeadline}" loading="lazy" onerror="this.style.display='none'; this.nextElementSibling.style.display='block';">
                <div class="image-placeholder" style="display:none;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                        <circle cx="8.5" cy="8.5" r="1.5"></circle>
                        <polyline points="21 15 16 10 5 21"></polyline>
                    </svg>
                </div>
            </div>
        ` : ''}
        <div class="news-content">
            ${isNew ? `<span class="news-badge">NEW</span>` : ''}
            <div class="news-date">
                <svg class="date-icon" xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                    <line x1="16" y1="2" x2="16" y2="6"></line>
                    <line x1="8" y1="2" x2="8" y2="6"></line>
                    <line x1="3" y1="10" x2="21" y2="10"></line>
                </svg>
                ${escapeHtml(dateStr)}
            </div>
            <h3 class="news-headline">
                <a href="${safeLink}" target="_blank" rel="noopener">${safeHeadline}</a>
            </h3>
            <a href="${safeLink}" target="_blank" rel="noopener" class="news-read-link small">
                Read More
                <svg class="link-icon" xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                    <polyline points="15 3 21 3 21 9"></polyline>
                    <line x1="10" y1="14" x2="21" y2="3"></line>
                </svg>
            </a>
        </div>
    `;
}

// ----------------------
// Helper functions
// ----------------------
function escapeHtml(s) {
    return String(s ?? "").replace(/[&<>"']/g, m => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
    }[m]));
}

function escapeAttr(s) {
    return escapeHtml(s).replace(/"/g, "&quot;");
}

function fmtDate(dt) {
    // Handle different date formats from database
    if (!dt) return 'Latest';
    
    // Try to parse the date string
    let d = new Date(dt);
    
    // If parsing failed, try to extract date from formats like "November 5, 2025 10:30 IST"
    if (isNaN(d.getTime())) {
        // Extract month, day, year from string like "November 5, 2025"
        const dateMatch = dt.match(/(\w+)\s+(\d+),\s+(\d{4})/);
        if (dateMatch) {
            const [, monthName, day, year] = dateMatch;
            // Create a date string that JavaScript can parse
            d = new Date(`${monthName} ${day}, ${year}`);
        }
    }
    
    // If still invalid, try ISO format or return a cleaned version
    if (isNaN(d.getTime())) {
        // Try ISO format
        d = new Date(dt.replace(/\s+IST$/, ''));
    }
    
    // If still invalid, return a cleaned version of the original string
    if (isNaN(d.getTime())) {
        // Return first part of date string (before time if present)
        const cleaned = dt.split(/\s+\d{1,2}:\d{2}/)[0] || dt;
        return cleaned.length > 25 ? cleaned.substring(0, 25) + '...' : cleaned;
    }
    
    // Format as "Nov 5, 2025"
    return d.toLocaleDateString(undefined, {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

