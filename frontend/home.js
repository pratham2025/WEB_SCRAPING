// home.js

// API Base URL (copied from app.js)
const API_BASE = "http://127.0.0.1:8000";

// --- NEW: Load Latest News ---
document.addEventListener('DOMContentLoaded', () => {
    // We already have a DOMContentLoaded listener in common.js,
    // but this is specific to home.js logic.
    loadLatestNews();
});

async function loadLatestNews() {
    const listEl = document.getElementById('latestNewsList');
    if (!listEl) return;

    try {
        // You'll need to create this /latest-news endpoint in your FastAPI
        const res = await fetch(`${API_BASE}/latest-news`);
        if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
        }
        const data = await res.json(); // Assuming { "news": [...] }
        
        let newsItems = [];
        
        // --- MODIFIED THIS BLOCK ---
        if (data && Array.isArray(data.news)) {
            // Handle the new API structure { "news": [...] }
            newsItems = data.news;
        } else if (data && data.data) {
            // Fallback for old structure { "data": [...] }
            newsItems = data.data;
        } else if (Array.isArray(data)) {
            // Fallback if the API just returns an array
            newsItems = data;
        }
        // --- END MODIFICATION ---

        // Limit to 3 news items for the homepage grid
        const limitedNews = newsItems.slice(0, 3);

        if (limitedNews.length > 0) {
            listEl.innerHTML = limitedNews.map(renderNewsCard).join('');
        } else {
            listEl.innerHTML = '<p>No news updates at this time.</p>';
        }

    } catch (error) {
        console.error("Failed to load latest news:", error);
        if (listEl) {
            listEl.innerHTML = '<p>Could not load news. Please try again later.</p>';
        }
    }
}

function renderNewsCard(news) {
    const { headline, article_link, article_date } = news;
    return `
        <div class="news-card">
            <span class="news-card-date">${article_date ? escapeHtml(fmtDate(article_date)) : 'Latest Update'}</span>
            <h3 class="news-card-headline">${escapeHtml(headline)}</h3>
            <div class="news-card-footer">
                <a href="${escapeAttr(article_link)}" class="btn secondary" target="_blank" rel="noopener">
                    Read More
                </a>
            </div>
        </div>
    `;
}
// --- END: Load Latest News ---


// Handle subscription form
document.getElementById('subscribeForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = e.target.querySelector('input[type="email"]').value;
    
    // Show success message (in production, this would connect to a backend)
    alert(`Subscription successful! We'll send updates to ${email}`);
    e.target.reset();
});

// Smooth scroll for anchor links
document.querySelectorAll('a.smooth-scroll').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});

// --- NEW: Helper functions (copied from app.js) ---
function escapeHtml(s){return String(s??"").replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]))}
function escapeAttr(s){return escapeHtml(s).replace(/"/g,"&quot;")}
function fmtDate(dt){ const d = new Date(dt); return isNaN(d)? String(dt) : d.toLocaleDateString(undefined,{year:'numeric',month:'short',day:'numeric'}); }