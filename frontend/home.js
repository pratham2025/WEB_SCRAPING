// home.js — Notice Board Edition
// Base API URL
const API_BASE = "http://127.0.0.1:8000";

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
    if (!listEl) return;

    const limit = opts.limit ?? 3;

    try {
        const res = await fetch(`${API_BASE}/latest-news`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();

        // Normalize data: {news: []}, {data: []}, or array
        let newsItems = [];
        if (data && Array.isArray(data.news)) newsItems = data.news;
        else if (data && Array.isArray(data.data)) newsItems = data.data;
        else if (Array.isArray(data)) newsItems = data;
        else newsItems = [];

        // Sort by date descending if possible
        newsItems.sort((a, b) => {
            const da = new Date(a.article_date || a.date || a.published_at || a.postedAt || 0);
            const db = new Date(b.article_date || b.date || b.published_at || b.postedAt || 0);
            return db - da;
        });

        // Limit for homepage
        const limited = newsItems.slice(0, limit);

        // If no news found
        if (limited.length === 0) {
            listEl.innerHTML = `<div class="notice-empty">No news updates at this time.</div>`;
            return;
        }

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

        // Wire up "Read" buttons
        listEl.querySelectorAll('.notice .open-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const url = btn.dataset.url;
                if (url) window.open(url, '_blank', 'noopener');
            });
        });

    } catch (err) {
        console.error('Failed to load latest news:', err);
        listEl.innerHTML = `<div class="notice-empty">Could not load news. Please try again later.</div>`;
    }
}

// ----------------------
// Render a single notice card
// ----------------------
function renderNoticeCard(news, idx) {
    // Support different field names
    const headline = news.headline ?? news.title ?? news.text ?? news.name ?? 'Untitled';
    const link = news.article_link ?? news.link ?? news.url ?? '#';
    const dateRaw = news.article_date ?? news.date ?? news.published_at ?? news.postedAt ?? null;

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

    // Return HTML card
    return `
    <article class="notice ${tiltClass}" data-idx="${idx}">
        ${isNew ? `<span class="badge">NEW</span>` : ''}
        <div class="date">${escapeHtml(dateStr)}</div>
        <h3 class="headline">${safeHeadline}</h3>
        <div class="note-actions">
            <button class="btn secondary open-btn" data-url="${safeLink}">Read</button>
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
    const d = new Date(dt);
    return isNaN(d)
        ? String(dt)
        : d.toLocaleDateString(undefined, {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
}
