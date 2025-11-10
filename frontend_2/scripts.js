// ===========================
// GETNOTIFY Frontend JS Logic
// ===========================

const API_BASE = 'http://127.0.0.1:8000'; // Replace with backend URL when deployed

// Scroll to notices
function scrollToNotices() {
  document.getElementById('notice-board').scrollIntoView({ behavior: 'smooth' });
}

// Fetch news from latest_news table
// Table schema: id (int4, PK), headline (text), article_link (text), 
// article_date (text), scraped_at (timestamptz, nullable)
async function fetchLatestNews() {
  try {
    const response = await fetch(`${API_BASE}/latest-news`);
    if (!response.ok) throw new Error('Network response was not ok');

    const data = await response.json();
    return data.news || [];
  } catch (error) {
    console.error('Error fetching news:', error);
    return [];
  }
}

// Helper function to parse date from article_date or scraped_at
function parseDate(item) {
  // Try article_date first (text field) - format like "November 5, 2025 09:49 IST"
  if (item.article_date) {
    // Try multiple date parsing strategies
    let date = new Date(item.article_date);
    
    // If first attempt fails, try cleaning the string
    if (isNaN(date.getTime())) {
      // Remove IST and other timezone abbreviations, try again
      const cleaned = item.article_date.replace(/\s*(IST|GMT|UTC|EST|PST)\s*/gi, '').trim();
      date = new Date(cleaned);
    }
    
    // If still fails, try parsing common formats manually
    if (isNaN(date.getTime())) {
      // Try format: "November 5, 2025 09:49"
      const match = item.article_date.match(/(\w+)\s+(\d+),\s+(\d+)\s+(\d+):(\d+)/);
      if (match) {
        const [, month, day, year, hour, minute] = match;
        const monthMap = {
          'january': 0, 'february': 1, 'march': 2, 'april': 3, 'may': 4, 'june': 5,
          'july': 6, 'august': 7, 'september': 8, 'october': 9, 'november': 10, 'december': 11
        };
        const monthIndex = monthMap[month.toLowerCase()];
        if (monthIndex !== undefined) {
          date = new Date(parseInt(year), monthIndex, parseInt(day), parseInt(hour), parseInt(minute));
        }
      }
    }
    
    if (!isNaN(date.getTime())) {
      return date;
    }
  }
  
  // Fallback to scraped_at (timestamptz)
  if (item.scraped_at) {
    const date = new Date(item.scraped_at);
    if (!isNaN(date.getTime())) {
      return date;
    }
  }
  
  // Return very old date if no valid date found (will sort to bottom)
  return new Date(0);
}

// Sort news by date (latest first)
function sortNewsByDate(news) {
  return [...news].sort((a, b) => {
    const dateA = parseDate(a);
    const dateB = parseDate(b);
    // Sort descending (newest first) - compare timestamps
    const diff = dateB.getTime() - dateA.getTime();
    return diff;
  });
}

// Render notices to UI
async function renderNotices() {
  const container = document.getElementById('notices');
  if (!container) {
    console.error('News container not found');
    return;
  }
  
  container.innerHTML = '<p class="loading">Loading news bulletin...</p>';

  const news = await fetchLatestNews();
  container.innerHTML = '';

  if (!news || news.length === 0) {
    container.innerHTML = '<p class="no-data">No news available at the moment. Please check back later.</p>';
    return;
  }

  // Sort news by article_date (latest first)
  const sortedNews = sortNewsByDate(news);
  
  // Debug: Log sorted dates to verify sorting
  console.log('Sorted news dates:', sortedNews.map(item => ({
    headline: item.headline?.substring(0, 50),
    article_date: item.article_date,
    parsed: parseDate(item).toISOString()
  })));

  sortedNews.forEach((item, index) => {
    const card = document.createElement('div');
    card.classList.add('news-card');
    card.style.animationDelay = `${index * 0.05}s`;

    // Format date - prioritize article_date (text type), fallback to scraped_at (timestamptz)
    let dateStr = 'Date not available';
    
    // First try article_date (text field from table)
    if (item.article_date) {
      // If article_date already includes time (like "November 5, 2025 09:49 IST"), use it as-is
      if (item.article_date.includes(':') || item.article_date.match(/\d{1,2}:\d{2}/)) {
        dateStr = item.article_date;
      } else {
        // Try to parse and format
        try {
          const date = parseDate(item);
          if (date.getTime() !== 0) {
            // Format with time: "November 5, 2025 09:49 IST"
            const month = date.toLocaleDateString('en-US', { month: 'long' });
            const day = date.getDate();
            const year = date.getFullYear();
            const hours = date.getHours().toString().padStart(2, '0');
            const minutes = date.getMinutes().toString().padStart(2, '0');
            dateStr = `${month} ${day}, ${year} ${hours}:${minutes} IST`;
          } else {
            // Use as-is if parsing failed
            dateStr = item.article_date;
          }
        } catch (e) {
          dateStr = item.article_date;
        }
      }
    } 
    // Fallback to scraped_at (timestamptz field)
    else if (item.scraped_at) {
      try {
        const date = new Date(item.scraped_at);
        const month = date.toLocaleDateString('en-US', { month: 'long' });
        const day = date.getDate();
        const year = date.getFullYear();
        const hours = date.getHours().toString().padStart(2, '0');
        const minutes = date.getMinutes().toString().padStart(2, '0');
        dateStr = `${month} ${day}, ${year} ${hours}:${minutes} IST`;
      } catch (e) {
        dateStr = 'Date not available';
      }
    }

    // Use exact field names from latest_news table
    const headline = item.headline || 'Untitled Notice';
    const link = item.article_link || '#';

    card.innerHTML = `
      <svg class="news-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M4 22h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v16a2 2 0 0 1-2 2Zm0 0a2 2 0 0 1-2-2v-9c0-1.1.9-2 2-2h2"></path>
        <path d="M18 14h-8"></path>
        <path d="M15 18h-5"></path>
        <path d="M10 6h8v4h-8V6Z"></path>
      </svg>
      <div class="news-content">
        <h3>${headline}</h3>
        <div class="news-date">${dateStr}</div>
        ${link && link !== '#' ? `<a href="${link}" target="_blank" rel="noopener noreferrer" class="news-link">Read More →</a>` : ''}
      </div>
    `;

    container.appendChild(card);
  });
}

// Theme toggle functionality
function toggleTheme() {
  document.body.classList.toggle('light-mode');
  const isLight = document.body.classList.contains('light-mode');
  localStorage.setItem('theme', isLight ? 'light' : 'dark');
}

// Hero Carousel Functionality
let currentSlide = 0;
const totalSlides = 5;
const SLIDE_DURATION_MS = 5000;
let carouselInterval = null;

function initHeroCarousel() {
  const carouselTrack = document.getElementById('heroCarousel');
  const dots = document.querySelectorAll('.carousel-dot');
  const heroSection = document.getElementById('heroSection');
  
  if (!carouselTrack) return;

  function goToSlide(slideIndex) {
    currentSlide = slideIndex;
    const translateX = -currentSlide * 20; // Each slide is 20% width
    carouselTrack.style.transform = `translateX(${translateX}%)`;

    const boxes = document.querySelectorAll('.hero-box');
    boxes.forEach((box, index) => {
      box.classList.toggle('active', index === currentSlide);
    });

    dots.forEach((dot, index) => {
      dot.classList.toggle('active', index === currentSlide);
    });
  }

  function nextSlide() {
    currentSlide = (currentSlide + 1) % totalSlides;
    goToSlide(currentSlide);
  }

  function startCarousel() {
    stopCarousel();
    carouselInterval = setInterval(nextSlide, SLIDE_DURATION_MS);
  }

  function stopCarousel() {
    if (carouselInterval) {
      clearInterval(carouselInterval);
      carouselInterval = null;
    }
  }

  function resetCarousel() {
    startCarousel();
  }

  dots.forEach((dot, index) => {
    dot.addEventListener('click', () => {
      goToSlide(index);
      resetCarousel();
    });
  });

  const hoverTarget = heroSection || document.querySelector('.hero-carousel-container');
  if (hoverTarget) {
    hoverTarget.addEventListener('mouseenter', stopCarousel);
    hoverTarget.addEventListener('mouseleave', startCarousel);
  }

  goToSlide(0);
  startCarousel();
}

// Create Network Pattern Connections
function createNetworkPattern() {
  const heroSection = document.getElementById('heroSection');
  if (!heroSection) return;

  // Create SVG for network connections
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('class', 'network-svg');
  svg.setAttribute('width', '100%');
  svg.setAttribute('height', '100%');
  svg.style.position = 'absolute';
  svg.style.top = '0';
  svg.style.left = '0';
  svg.style.width = '100%';
  svg.style.height = '100%';
  svg.style.pointerEvents = 'none';
  svg.style.zIndex = '0';
  svg.style.opacity = '0.4';

  heroSection.appendChild(svg);

  // Node positions
  const nodes = [
    { x: 10, y: 15 }, { x: 25, y: 30 }, { x: 40, y: 20 }, { x: 60, y: 25 },
    { x: 75, y: 35 }, { x: 85, y: 50 }, { x: 70, y: 60 }, { x: 50, y: 65 },
    { x: 30, y: 70 }, { x: 15, y: 55 }, { x: 35, y: 45 }, { x: 55, y: 45 },
    { x: 80, y: 15 }, { x: 20, y: 80 }, { x: 90, y: 75 }, { x: 45, y: 35 }
  ];

  // Draw connections between nearby nodes
  nodes.forEach((node1, i) => {
    nodes.forEach((node2, j) => {
      if (i < j) {
        const dx = node2.x - node1.x;
        const dy = node2.y - node1.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        // Connect nodes that are close to each other
        if (distance < 35 && Math.random() > 0.3) {
          const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
          line.setAttribute('x1', node1.x + '%');
          line.setAttribute('y1', node1.y + '%');
          line.setAttribute('x2', node2.x + '%');
          line.setAttribute('y2', node2.y + '%');
          line.setAttribute('stroke', '#FFD60A');
          line.setAttribute('stroke-width', '1');
          line.setAttribute('opacity', '0.3');
          line.style.filter = 'blur(0.5px)';
          svg.appendChild(line);
        }
      }
    });

    // Draw glowing nodes
    const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    circle.setAttribute('cx', node1.x + '%');
    circle.setAttribute('cy', node1.y + '%');
    circle.setAttribute('r', '3');
    const colors = ['#FFD60A', '#8A2BE2', '#00BFFF'];
    circle.setAttribute('fill', colors[i % 3]);
    circle.setAttribute('opacity', '0.6');
    circle.style.filter = 'blur(1px) drop-shadow(0 0 4px currentColor)';
    circle.style.animation = `nodePulse ${2 + Math.random() * 2}s ease-in-out infinite`;
    svg.appendChild(circle);
  });
}

// Add node pulse animation
const style = document.createElement('style');
style.textContent = `
  @keyframes nodePulse {
    0%, 100% {
      opacity: 0.4;
      transform: scale(1);
    }
    50% {
      opacity: 0.8;
      transform: scale(1.3);
    }
  }
`;
document.head.appendChild(style);

// Apply saved theme
window.onload = function () {
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme === 'light') {
    document.body.classList.add('light-mode');
  }
  renderNotices();
  initHeroCarousel();
  createNetworkPattern();
};

// Theme toggle functionality removed as per user request