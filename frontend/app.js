// Update API_BASE to match your running API
// Auto-detect hostname: works on localhost and mobile devices via IP
const hostname = window.location.hostname || '127.0.0.1';
const API_BASE = `http://${hostname}:8000`;

const state = {
  sources: [],
  activeSource: null,
  items: [],
  filtered: [],
  page: 1,
  perPage: 10
};

// Metadata: full forms and short descriptions for sources
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
  "RRBMumbai": { full: "Railway Recruitment Board Mumbai", desc: "RRB Mumbai recruitment and results" },
  "RRBAhmedabad": { full: "Railway Recruitment Board Ahmedabad", desc: "RRB Ahmedabad recruitment and results" }
};

// Logo file mapping for known sources
const LOGO_MAP = {
  CBSE: "src/logos/CBSE.png",
  JEE: "src/logos/JEE.jpg",
  GATE: "src/logos/GATE.webp",
  ISRO: "src/logos/ISRO.png",
  NEET: "src/logos/NEET.jpg",
  NTA: "src/logos/NTA.png",
  KEA: "src/logos/KEA.jpg",
  KSEAB: "src/logos/KSEAB.jpg",
  MAHACET: "src/logos/MAHACET.png",
  MPSC: "src/logos/MPSC.png",
  RRBKolkata: "src/logos/RRBKOLKATA.png",
  RRBMumbai: "src/logos/RRBMUMBAI.avif",
  RRBAhmedabad: "src/logos/RRBAHMEDABAD.jpg",
  UPSC: "src/logos/UPSC.webp"
};

// Add new element selectors
const els = {
  tabs: document.getElementById("examTabs"),
  list: document.getElementById("examList"),
  count: document.getElementById("resultCount"),
  pagination: document.getElementById("pagination"),
  detail: document.getElementById("examDetail"),
  status: document.getElementById("connStatus"),
  sourceSelector: document.getElementById("sourceSelector"),
  sourceCardGrid: document.getElementById("sourceCardGrid"),
  resultsContainer: document.getElementById("resultsContainer"),
};

function setStatus(msg, warn=false){
  if (els.status){
    els.status.textContent = msg;
    els.status.style.background = warn ? "#FFF6F6" : "#F7FFF9";
    els.status.style.borderColor = warn ? "#ffd0d0" : "var(--green-100)";
    els.status.style.color = warn ? "#a82b2b" : "var(--green-700)";
  }
  console.log("[GETNOTIFY]", msg);
}

function showNotification(message, isError = false) {
  const notification = document.createElement('div');
  notification.className = `notification ${isError ? 'error' : 'success'}`;
  notification.textContent = message;
  document.body.appendChild(notification);
  setTimeout(() => { notification.remove(); }, 5000);
}

async function fetchJSON(url, options = {}){
  try{
    const res = await fetch(url, {
      headers: { accept: "application/json", ...(options.headers || {}) },
      ...options
    });
    if(!res.ok){
      const errorData = await res.json().catch(() => ({}));
      showNotification(`Error: HTTP ${res.status} for ${url}`, true);
      return {ok:false, status:res.status, error: errorData.message || `HTTP ${res.status}`};
    }
    const data = await res.json();
    return {ok:true, data};
  }catch(e){
    showNotification(`Failed to fetch ${url}. Check if API is running.`, true);
    console.warn(e);
    return {ok:false, error:String(e)};
  }
}

async function loadSources(){
  setStatus("Fetching sources …");
  const {ok, data} = await fetchJSON(`${API_BASE}/sources`);
  if (!ok || !data){
    setStatus("Couldn’t read /sources. Using sample data for preview.", true);
    state.sources = ["CBSE","JEE","MHT-CET","NEET","NTA"];
    buildSourceCards();
    return;
  }
  const sources = Array.isArray(data.sources) ? data.sources : (Array.isArray(data) ? data : []);
  state.sources = sources.map(String).sort((a,b)=>a.localeCompare(b));
  buildSourceCards();
}

// Build source cards
async function buildSourceCards() {
  if (!els.sourceCardGrid) return;
  
  // Get user's current subscriptions
  const subscriptions = await getUserSubscriptions();
  
  els.sourceCardGrid.innerHTML = state.sources.map(s => {
      const initials = s.split(/\s+/).map(w=>w[0]).slice(0,2).join("").toUpperCase();
      const meta = SOURCE_INFO[s] || { full: s, desc: "Latest announcements and updates" };
      const logo = LOGO_MAP[s];
      const isSubscribed = subscriptions.includes(s);
      return `
      <div class="source-card-wrapper">
        <a class="source-card" onclick="selectSource('${escapeAttr(s)}')">
            <div class="source-card-logo">${logo ? `<img src="${escapeAttr(logo)}" alt="${escapeAttr(meta.full)}"/>` : escapeHtml(initials)}</div>
            <h3>${escapeHtml(s)}</h3>
            <div class="source-full">${escapeHtml(meta.full)}</div>
            <p class="source-desc">${escapeHtml(meta.desc)}</p>
        </a>
        <button class="subscribe-btn ${isSubscribed ? 'subscribed' : ''}" 
                onclick="event.stopPropagation(); toggleSubscription('${escapeAttr(s)}', this)"
                data-source="${escapeAttr(s)}">
            ${isSubscribed ? '✓ Subscribed' : 'Subscribe'}
        </button>
      </div>`;
  }).join("");
}

// Handle selecting a source
async function selectSource(source) {
  els.sourceSelector.style.display = 'none';
  els.resultsContainer.style.display = 'block';
  
  els.tabs.innerHTML = `
      <button class="back-btn" onclick="showSourceSelector()">← All Sources</button>
      <button class="exam-tab active">${escapeHtml(source)}</button>
  `;

  await loadAnnouncements(source);
}

function showSourceSelector() {
  els.resultsContainer.style.display = 'none';
  els.sourceSelector.style.display = 'block';
}

// ✅ FINAL FIX: always show latest first
async function loadAnnouncements(source){
  state.activeSource = source;

  els.list.innerHTML = '';
  els.pagination.innerHTML = '';
  els.count.textContent = '0';
  if (els.status) els.status.style.display = 'block';

  setStatus(`Fetching announcements for ${source} …`);
  const {ok, data} = await fetchJSON(`${API_BASE}/announcements/${encodeURIComponent(source)}`);

  if (!ok || !data) {
    setStatus(`Couldn’t read announcements for ${source}. Showing empty list.`, true);
    state.items = [];
    if (els.status) els.status.style.display = 'block';
  } else {
    const arr = Array.isArray(data.data) ? data.data : (Array.isArray(data) ? data : []);

    // ✅ Reverse order to make sure latest is on top
    state.items = arr.map(normaAnn).reverse();

    console.log(`[loadAnnouncements] ${source}: ${state.items.length} items (latest first)`);

    if (els.status) els.status.style.display = 'none';
  }

  state.page = 1;
  applyFilters();
}

// Normalize announcements
function normaAnn(x){
  const rawDate = x.scraped_at ?? x.date ?? x.postedAt ?? x.published_at ?? null;
  return {
    id: String(x.id ?? cryptoId()),
    text: String(x.text ?? x.title ?? "Untitled"),
    source: String(x.source ?? state.activeSource ?? "Source"),
    link: String(x.link ?? x.url ?? "#"),
    date: rawDate
  };
}

function cryptoId(){ 
  try{ 
    return crypto.getRandomValues(new Uint32Array(1))[0].toString(16);
  }catch(_){
    return Math.random().toString(16).slice(2);
  } 
}

function applyFilters(){
  state.filtered = state.items.slice();
  renderList();
}

function renderList(){
  const start = (state.page-1)*state.perPage;
  const pageItems = state.filtered.slice(start, start+state.perPage);
  if (els.count) els.count.textContent = String(state.filtered.length);

  if (state.filtered.length > 0) {
      if (els.status) els.status.style.display = 'none';
      els.list.innerHTML = pageItems.map(renderCard).join("");
  } else {
      if (els.status && els.status.textContent.startsWith("Fetching")) {
        setStatus(`No announcements found for ${state.activeSource}.`, true);
        els.status.style.display = 'block';
      }
      els.list.innerHTML = '';
  }
  
  renderPagination();
}

function renderCard(x){
  const logoUrl = LOGO_MAP[x.source];
  let logoHtml = '';
  if (logoUrl) {
    logoHtml = `<img src="${escapeAttr(logoUrl)}" alt="${escapeAttr(x.source)} logo" />`;
  } else {
    const initials = (x.source || "??").split(/\s+/).map(w=>w[0]).slice(0,2).join("").toUpperCase();
    logoHtml = escapeHtml(initials);
  }

  return `<li class="card" data-id="${escapeAttr(x.id)}">
    <a href="${escapeAttr(x.link)}" target="_blank" rel="noopener" class="card-link">
      <div class="logo" aria-hidden="true">${logoHtml}</div>
      <div class="meta">
        <div class="title">${escapeHtml(x.text)}</div>
        <div class="org">${escapeHtml(x.source)}</div>
        <div class="row">${x.date ? escapeHtml(fmtDate(x.date)) : "Latest"}</div>
      </div>
    </a>
  </li>`;
}

function renderPagination(){
  const pages = Math.ceil(state.filtered.length / state.perPage) || 1;
  if (pages <= 1) {
    els.pagination.innerHTML = "";
    return;
  }
  
  let html = "";
  for(let i=1;i<=pages;i++){
    html += `<button class="page-btn ${i===state.page?'active':''}" onclick="gotoPage(${i})">${i}</button>`;
  }
  els.pagination.innerHTML = html;
}

function gotoPage(n){ 
  state.page = n; 
  renderList(); 
}

/* helpers */
function escapeHtml(s){return String(s??"").replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]))}
function escapeAttr(s){return escapeHtml(s).replace(/"/g,"&quot;")}
function fmtDate(dt){ 
  const d = new Date(dt); 
  return isNaN(d)? String(dt) : d.toLocaleDateString(undefined,{year:'numeric',month:'short',day:'numeric'}); 
}

// Subscription functions
async function getUserSubscriptions() {
  try {
    const user = await getLoggedInUser();
    if (!user || !user.email) return [];
    
    const {ok, data} = await fetchJSON(`${API_BASE}/subscriptions?email=${encodeURIComponent(user.email)}`);
    if (ok && data && Array.isArray(data.subscriptions)) {
      return data.subscriptions.map(s => s.source);
    }
    return [];
  } catch (e) {
    console.warn('Failed to fetch subscriptions:', e);
    return [];
  }
}

async function toggleSubscription(source, buttonEl) {
  try {
    const user = await getLoggedInUser();
    if (!user) {
      showNotification('Please log in to subscribe to sources', true);
      // Optionally open login modal
      const loginBtn = document.getElementById('loginBtn');
      if (loginBtn) loginBtn.click();
      return;
    }
    
    const isSubscribed = buttonEl.classList.contains('subscribed');
    const action = isSubscribed ? 'unsubscribe' : 'subscribe';
    
    buttonEl.disabled = true;
    buttonEl.textContent = isSubscribed ? 'Unsubscribing...' : 'Subscribing...';
    
    const result = await fetchJSON(`${API_BASE}/${action}`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({source, email: user.email})
    });
    const {ok, data, error} = result;
    
    if (ok) {
      if (isSubscribed) {
        buttonEl.classList.remove('subscribed');
        buttonEl.textContent = 'Subscribe';
        showNotification(`Unsubscribed from ${source}`);
      } else {
        buttonEl.classList.add('subscribed');
        buttonEl.textContent = '✓ Subscribed';
        showNotification(`Subscribed to ${source}! You'll receive email notifications for new announcements.`);
      }
    } else {
      showNotification(error || `Failed to ${action}`, true);
      buttonEl.textContent = isSubscribed ? '✓ Subscribed' : 'Subscribe';
    }
  } catch (e) {
    console.error('Subscription error:', e);
    showNotification('An error occurred. Please try again.', true);
    buttonEl.textContent = buttonEl.classList.contains('subscribed') ? '✓ Subscribed' : 'Subscribe';
  } finally {
    buttonEl.disabled = false;
  }
}

// Helper function to get logged in user (from auth.js)
async function getLoggedInUser() {
  if (!window.supabase) return null;
  try {
    const { data: { user } } = await window.supabase.auth.getUser();
    return user;
  } catch (e) {
    return null;
  }
}


/* expose */
window.gotoPage = gotoPage;
window.selectSource = selectSource;
window.showSourceSelector = showSourceSelector;
window.toggleSubscription = toggleSubscription;

/* init */
(async function init(){
  if (document.getElementById('sourceSelector')) {
    await loadSources();
  }
})();
