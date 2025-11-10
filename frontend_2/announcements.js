// ===========================
// GETNOTIFY - Source Announcements Logic
// ===========================

const API_BASE = 'http://127.0.0.1:8000'; // align with other pages

const LOGO_MAP = {
  CBSE: '../frontend/src/logos/CBSE.png',
  JEE: '../frontend/src/logos/JEE.jpg',
  GATE: '../frontend/src/logos/GATE.webp',
  ISRO: '../frontend/src/logos/ISRO.png',
  NEET: '../frontend/src/logos/NEET.jpg',
  NTA: '../frontend/src/logos/NTA.png',
  KEA: '../frontend/src/logos/KEA.jpg',
  KSEAB: '../frontend/src/logos/KSEAB.jpg',
  MAHACET: '../frontend/src/logos/MAHACET.png',
  MPSC: '../frontend/src/logos/MPSC.png',
  UPSC: '../frontend/src/logos/UPSC.webp',
  RRBKolkata: '../frontend/src/logos/RRBKOLKATA.png',
  RRBMumbai: '../frontend/src/logos/RRBMUMBAI.avif'
};

// reuse metadata from sources page (duplicated for standalone loading)
const SOURCE_INFO = {
  CBSE: { full: 'Central Board of Secondary Education', desc: 'National school board for India' },
  JEE: { full: 'Joint Entrance Examination', desc: 'Engineering admissions (Main/Advanced)' },
  GATE: { full: 'Graduate Aptitude Test in Engineering', desc: 'Post-grad and PSU recruitment exam' },
  ISRO: { full: 'Indian Space Research Organisation', desc: 'Recruitment and exam updates' },
  NEET: { full: 'National Eligibility cum Entrance Test', desc: 'Medical and dental admissions' },
  NTA: { full: 'National Testing Agency', desc: 'Agency notifications and test schedules' },
  KEA: { full: 'Karnataka Examinations Authority', desc: 'State entrance and recruitment notices' },
  KSEAB: { full: 'Karnataka School Examination and Assessment Board', desc: 'School exam notifications' },
  MAHACET: { full: 'Maharashtra State CET Cell', desc: 'State common entrance test updates' },
  MPSC: { full: 'Maharashtra Public Service Commission', desc: 'State civil services recruitment' },
  UPSC: { full: 'Union Public Service Commission', desc: 'Civil services and national-level recruitment exams' },
  RRBKolkata: { full: 'Railway Recruitment Board Kolkata', desc: 'RRB Kolkata recruitment and results' },
  RRBMumbai: { full: 'Railway Recruitment Board Mumbai', desc: 'RRB Mumbai recruitment and results' }
};

const announcementsList = document.getElementById('announcementsList');
const sourceTitleEl = document.getElementById('sourceTitle');
const sourceFullEl = document.getElementById('sourceFull');
const sourceDescEl = document.getElementById('sourceDesc');
const subscribeSourceEl = document.getElementById('subscribeSource');
const subscribeForm = document.getElementById('subscribeForm');
const subscribeStatus = document.getElementById('subscribeStatus');
const refreshBtn = document.getElementById('refreshBtn');
const sourceHeroIconEl = document.getElementById('sourceHeroIcon');
const sourceHeroIconFallbackEl = document.getElementById('sourceHeroIconFallback');
const sourceHeroIconWrapper = document.getElementById('sourceHeroIconWrapper');

const queryParams = new URLSearchParams(window.location.search);
const sourceParam = queryParams.get('source');
const sourceKey = sourceParam ? decodeURIComponent(sourceParam) : null;

function setUnknownSource() {
  sourceTitleEl.textContent = 'Source Not Found';
  sourceFullEl.textContent = '';
  sourceDescEl.textContent = 'The requested source could not be identified. Please return to the sources list.';
  subscribeSourceEl.textContent = 'this source';
  updateSourceIcon(null);
  if (announcementsList) {
    announcementsList.innerHTML = '<div class="empty-state">Select a valid source from the sources page to view announcements.</div>';
  }
}

function updateSourceIcon(sourceKey) {
  if (!sourceHeroIconEl || !sourceHeroIconFallbackEl) return;
  const logoSrc = sourceKey ? LOGO_MAP[sourceKey] : null;
  const initials = sourceKey ? sourceKey.slice(0, 3).toUpperCase() : 'SRC';
  if (logoSrc) {
    sourceHeroIconEl.onload = () => {
      sourceHeroIconEl.style.display = 'block';
      sourceHeroIconFallbackEl.style.display = 'none';
    };
    sourceHeroIconEl.onerror = () => {
      sourceHeroIconEl.style.display = 'none';
      sourceHeroIconFallbackEl.textContent = initials;
      sourceHeroIconFallbackEl.style.display = 'block';
    };
    sourceHeroIconEl.src = logoSrc;
    sourceHeroIconEl.alt = `${sourceKey} logo`;
  } else {
    sourceHeroIconEl.removeAttribute('src');
    sourceHeroIconEl.style.display = 'none';
    sourceHeroIconFallbackEl.textContent = initials;
    sourceHeroIconFallbackEl.style.display = 'block';
  }
}

function populateSourceMeta() {
  if (!sourceKey) {
    setUnknownSource();
    return;
  }
  const meta = SOURCE_INFO[sourceKey] || { full: sourceKey, desc: 'Latest announcements and updates' };
  sourceTitleEl.textContent = `${sourceKey} Announcements`;
  sourceFullEl.textContent = meta.full;
  sourceDescEl.textContent = meta.desc;
  subscribeSourceEl.textContent = meta.full || sourceKey;
  updateSourceIcon(sourceKey);
}

async function fetchAnnouncements() {
  if (!announcementsList) return;

  announcementsList.innerHTML = '<div class="empty-state">Loading announcements...</div>';

  if (!sourceKey) {
    setUnknownSource();
    return;
  }

  try {
    const response = await fetch(`${API_BASE}/announcements/${encodeURIComponent(sourceKey)}`);
    if (!response.ok) throw new Error('Failed to load announcements');

    const data = await response.json();
    const announcementsRaw = Array.isArray(data.announcements)
      ? data.announcements
      : Array.isArray(data)
        ? data
        : Array.isArray(data.data)
          ? data.data
          : [];

    const announcements = announcementsRaw
      .map((item, index) => {
        const timestamp = parseAnnouncementDate(item);
        return { item, index, timestamp };
      })
      .sort((a, b) => {
        if (b.timestamp !== a.timestamp) {
          return b.timestamp - a.timestamp;
        }
        // fall back to original ordering (which is already newest-first from API)
        return a.index - b.index;
      })
      .map(wrapper => wrapper.item)
      .reverse();

    if (!announcements.length) {
      announcementsList.innerHTML = '<div class="empty-state">No announcements available yet. Check back soon!</div>';
      return;
    }

    announcementsList.innerHTML = announcements.map((item, index) => {
      const title = item.title || item.headline || item.text || `Announcement ${index + 1}`;
      const summary = item.summary || item.description || item.text || 'Details available in the linked notice.';
      const link = item.link || item.url || item.article_link;
      const rawDate = item.date || item.published_at || item.article_date || item.scraped_at;
      const formattedDate = formatAnnouncementDate(rawDate);

      return `
        <article class="announcement-card" style="animation-delay:${index * 0.05}s">
          <header class="announcement-header">
            <h3 class="announcement-title">${title}</h3>
            <div class="announcement-date">${formattedDate}</div>
          </header>
          <p class="announcement-summary">${summary}</p>
          <div class="announcement-actions">
            ${link ? `<a class="announcement-link" href="${link}" target="_blank" rel="noopener noreferrer">Read Official Notice →</a>` : ''}
          </div>
        </article>
      `;
    }).join('');
  } catch (error) {
    console.error('Error fetching announcements:', error);
    announcementsList.innerHTML = '<div class="empty-state">Unable to load announcements right now. Please try again later.</div>';
  }
}

function formatAnnouncementDate(raw) {
  if (!raw) return 'Date unavailable';
  const date = new Date(raw);
  if (!Number.isNaN(date.getTime())) {
    return date.toLocaleDateString('en-IN', {
      day: 'numeric',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  }
  return raw;
}

function parseAnnouncementDate(item) {
  const raw = item.date || item.published_at || item.article_date || item.scraped_at;
  if (!raw) return 0;
  const date = new Date(raw);
  if (!Number.isNaN(date.getTime())) {
    return date.getTime();
  }
  return 0;
}

async function handleSubscribe(event) {
  event.preventDefault();
  if (!sourceKey) {
    subscribeStatus.textContent = 'Select a valid source before subscribing.';
    subscribeStatus.className = 'subscribe-status error';
    return;
  }

  const emailInput = document.getElementById('emailInput');
  const email = emailInput.value.trim();
  if (!email) return;

  subscribeStatus.textContent = 'Subscribing...';
  subscribeStatus.className = 'subscribe-status';

  try {
    const response = await fetch(`${API_BASE}/subscribe`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, source: sourceKey })
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.message || 'Subscription failed');
    }

    subscribeStatus.textContent = 'Subscribed! Check your inbox for a confirmation.';
    subscribeStatus.className = 'subscribe-status success';
    emailInput.value = '';
  } catch (error) {
    console.error('Subscription error:', error);
    subscribeStatus.textContent = error.message || 'Unable to subscribe right now.';
    subscribeStatus.className = 'subscribe-status error';
  }
}

function init() {
  populateSourceMeta();
  fetchAnnouncements();
  if (refreshBtn) {
    refreshBtn.addEventListener('click', fetchAnnouncements);
  }
  if (subscribeForm) {
    subscribeForm.addEventListener('submit', handleSubscribe);
  }
}

document.addEventListener('DOMContentLoaded', init);

