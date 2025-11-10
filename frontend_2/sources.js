// ===========================
// GETNOTIFY Sources Page JS
// ===========================

const API_BASE = 'http://127.0.0.1:8000'; // Replace with backend URL when deployed

// Source metadata
const SOURCE_INFO = {
  "CBSE": { full: "Central Board of Secondary Education", desc: "National school board for India" },
  "JEE": { full: "Joint Entrance Examination", desc: "Engineering admissions (Main/Advanced)" },
  "GATE": { full: "Graduate Aptitude Test in Engineering", desc: "Post-grad and PSU recruitment exam" },
  "ISRO": { full: "Indian Space Research Organisation", desc: "Recruitment and exam updates" },
  "NEET": { full: "National Eligibility cum Entrance Test", desc: "Medical and dental admissions" },
  "NTA": { full: "National Testing Agency", desc: "Agency notifications and test schedules" },
  "KEA": { full: "Karnataka Examinations Authority", desc: "State entrance and recruitment notices" },
  "KSEAB": { full: "Karnataka School Examination and Assessment Board", desc: "School exam notifications" },
  "MAHACET": { full: "Maharashtra State CET Cell", desc: "State common entrance test updates" },
  "MPSC": { full: "Maharashtra Public Service Commission", desc: "State civil services recruitment" },
  "UPSC": { full: "Union Public Service Commission", desc: "Civil services and national-level recruitment exams" },
  "RRBKolkata": { full: "Railway Recruitment Board Kolkata", desc: "RRB Kolkata recruitment and results" },
  "RRBMumbai": { full: "Railway Recruitment Board Mumbai", desc: "RRB Mumbai recruitment and results" }
};

// Logo file mapping (if you have logos, update paths accordingly)
const LOGO_MAP = {
  CBSE: "../frontend/src/logos/CBSE.png",
  JEE: "../frontend/src/logos/JEE.jpg",
  GATE: "../frontend/src/logos/GATE.webp",
  ISRO: "../frontend/src/logos/ISRO.png",
  NEET: "../frontend/src/logos/NEET.jpg",
  NTA: "../frontend/src/logos/NTA.png",
  KEA: "../frontend/src/logos/KEA.jpg",
  KSEAB: "../frontend/src/logos/KSEAB.jpg",
  MAHACET: "../frontend/src/logos/MAHACET.png",
  MPSC: "../frontend/src/logos/MPSC.png",
  RRBKolkata: "../frontend/src/logos/RRBKOLKATA.png",
  RRBMumbai: "../frontend/src/logos/RRBMUMBAI.avif",
  UPSC: "../frontend/src/logos/UPSC.webp"
};

// Fetch available sources from API
async function fetchSources() {
  try {
    const response = await fetch(`${API_BASE}/sources`);
    if (!response.ok) throw new Error('Network response was not ok');
    const data = await response.json();
    return Array.isArray(data.sources) ? data.sources : (Array.isArray(data) ? data : []);
  } catch (error) {
    console.error('Error fetching sources:', error);
    // Return default sources if API fails
    return ["CBSE", "JEE", "GATE", "ISRO", "NEET", "NTA", "KEA", "KSEAB", "MAHACET", "MPSC", "UPSC"];
  }
}

// Build source cards
function buildSourceCards(sources) {
  const grid = document.getElementById('sourcesGrid');
  if (!grid) return;

  grid.innerHTML = sources.map(source => {
    const meta = SOURCE_INFO[source] || { full: source, desc: "Latest announcements and updates" };
    const logo = LOGO_MAP[source];
    const initials = source.split(/\s+/).map(w => w[0]).slice(0, 2).join("").toUpperCase();
    
    return `
      <div class="source-card" onclick="handleSourceClick('${source.replace(/'/g, "\\'")}')">
        <div class="source-card-logo">
          ${logo ? `<img src="${logo}" alt="${meta.full}" onerror="this.parentElement.textContent='${initials}'">` : initials}
        </div>
        <h3>${source}</h3>
        <div class="source-full">${meta.full}</div>
        <p class="source-desc">${meta.desc}</p>
      </div>
    `;
  }).join('');
}

// Handle source card click
function handleSourceClick(source) {
  const encoded = encodeURIComponent(source);
  window.location.href = `source-announcements.html?source=${encoded}`;
}

// Create Network Pattern for Sources Page
function createNetworkPattern() {
  const body = document.body;
  if (!body) return;

  // Create SVG for network connections
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('class', 'network-svg');
  svg.setAttribute('width', '100%');
  svg.setAttribute('height', '100%');
  svg.style.position = 'fixed';
  svg.style.top = '0';
  svg.style.left = '0';
  svg.style.width = '100%';
  svg.style.height = '100%';
  svg.style.pointerEvents = 'none';
  svg.style.zIndex = '0';
  svg.style.opacity = '0.3';

  body.appendChild(svg);

  // Node positions
  const nodes = [
    { x: 15, y: 20 }, { x: 30, y: 35 }, { x: 45, y: 25 }, { x: 65, y: 30 },
    { x: 80, y: 40 }, { x: 90, y: 55 }, { x: 75, y: 65 }, { x: 55, y: 70 },
    { x: 35, y: 75 }, { x: 20, y: 60 }, { x: 40, y: 50 }, { x: 60, y: 50 },
    { x: 85, y: 20 }, { x: 25, y: 85 }, { x: 95, y: 80 }, { x: 50, y: 40 },
    { x: 10, y: 45 }, { x: 70, y: 15 }, { x: 30, y: 10 }
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
          line.setAttribute('opacity', '0.25');
          line.style.filter = 'blur(0.5px)';
          svg.appendChild(line);
        }
      }
    });

    // Draw glowing nodes
    const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    circle.setAttribute('cx', node1.x + '%');
    circle.setAttribute('cy', node1.y + '%');
    circle.setAttribute('r', '2.5');
    const colors = ['#FFD60A', '#8A2BE2', '#00BFFF'];
    circle.setAttribute('fill', colors[i % 3]);
    circle.setAttribute('opacity', '0.5');
    circle.style.filter = 'blur(0.8px) drop-shadow(0 0 3px currentColor)';
    circle.style.animation = `nodePulse ${2 + Math.random() * 2}s ease-in-out infinite`;
    svg.appendChild(circle);
  });
}

// Add node pulse animation style if not exists
if (!document.getElementById('network-animation-style')) {
  const style = document.createElement('style');
  style.id = 'network-animation-style';
  style.textContent = `
    @keyframes nodePulse {
      0%, 100% {
        opacity: 0.3;
        transform: scale(1);
      }
      50% {
        opacity: 0.7;
        transform: scale(1.2);
      }
    }
  `;
  document.head.appendChild(style);
}

// Initialize page
async function init() {
  const sources = await fetchSources();
  buildSourceCards(sources);
  createNetworkPattern();
}

// Load on page ready
window.onload = init;

