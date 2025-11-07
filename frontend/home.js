// home.js — Notice Board Edition
// Base API URL (avoid redeclaration if app.js already defines it)
if (typeof API_BASE === 'undefined') {
    window.API_BASE = "http://127.0.0.1:8000";
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
            loadLatestNews({ limit: 3 });
        } else {
            btn.textContent = 'Show Top 20';
            btn.dataset.state = 'all';
            loadLatestNews({ limit: 20 });
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

    const limit = opts.limit ?? 3;

    // Show loading state
    listEl.innerHTML = `<div class="notice-empty">Loading news...</div>`;

    try {
        console.log(`Fetching latest news from ${API_BASE}/latest-news`);
        const res = await fetch(`${API_BASE}/latest-news?limit=${limit * 2}`, {
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

        // Sort by date descending if possible (using scraped_at as fallback)
        newsItems.sort((a, b) => {
            const da = new Date(a.article_date || a.scraped_at || a.date || a.published_at || a.postedAt || 0);
            const db = new Date(b.article_date || b.scraped_at || b.date || b.published_at || b.postedAt || 0);
            return db - da;
        });

        // Limit for homepage
        const limited = newsItems.slice(0, limit);

        // If no news found
        if (limited.length === 0) {
            listEl.innerHTML = `<div class="notice-empty">No news updates at this time. Check back later!</div>`;
            return;
        }

        console.log(`Rendering ${limited.length} news items`);

        // Build and inject HTML
        listEl.innerHTML = limited.map((n, idx) => renderNoticeCard(n, idx)).join('');

        // Apply staggered animation
        requestAnimationFrame(() => {
            const cards = listEl.querySelectorAll('.notice');
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
// Render a single notice card
// ----------------------
function renderNoticeCard(news, idx) {
    // Support different field names
    const headline = news.headline ?? news.title ?? news.text ?? news.name ?? 'Untitled';
    const link = news.article_link ?? news.link ?? news.url ?? '#';
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

    // Tilt variation for notice board style
    const tiltClass = `tilt-${(idx % 4) + 1}`;

    // Escape for safety
    const safeHeadline = escapeHtml(headline);
    const safeLink = escapeAttr(link);

    // Return HTML card - improved layout
    return `
    <article class="notice" data-idx="${idx}">
        ${isNew ? `<span class="badge">NEW</span>` : ''}
        <div class="notice-header">
            <div class="date">
                <svg class="date-icon" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                    <line x1="16" y1="2" x2="16" y2="6"></line>
                    <line x1="8" y1="2" x2="8" y2="6"></line>
                    <line x1="3" y1="10" x2="21" y2="10"></line>
                </svg>
                ${escapeHtml(dateStr)}
            </div>
        </div>
        <h3 class="headline">${safeHeadline}</h3>
        <div class="note-actions">
            <a href="${safeLink}" target="_blank" rel="noopener" class="btn secondary read-link">
                Read More
                <svg class="link-icon" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                    <polyline points="15 3 21 3 21 9"></polyline>
                    <line x1="10" y1="14" x2="21" y2="3"></line>
                </svg>
            </a>
        </div>
    </article>
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

