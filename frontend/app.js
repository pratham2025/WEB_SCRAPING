// Update API_BASE to match your running API
const API_BASE = "http://127.0.0.1:8000";

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
  "GATE": { full: "Graduate Aptitude Test in Engineering", desc: "Post‑grad and PSU recruitment exam" },
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

// Logo file mapping for known sources
const LOGO_MAP = {
  CBSE: "src/logos/CBSE.png",
  JEE: "src/logos/JEE.jpg",
  GATE: "src/logos/GATE.webp",
  ISRO: "src/logos/ISRO.png",
  NEET: "src/logos/NEET.jpg",
  NTA: "src/logos/NTA.png",
  KEA: "src/logos/KEA.jpg", // optional, in case added later
  KSEAB: "src/logos/KSEAB.jpg", // optional
  MAHACET: "src/logos/MAHACET.png",
  MPSC: "src/logos/MPSC.png",
  RRBKolkata: "src/logos/RRBKOLKATA.png",
  RRBMumbai: "src/logos/RRBMUMBAI.avif",
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
  console.log("[ExamDoor]", msg);
}

function showNotification(message, isError = false) {
  const notification = document.createElement('div');
  notification.className = `notification ${isError ? 'error' : 'success'}`;
  notification.textContent = message;
  document.body.appendChild(notification);
  setTimeout(() => { notification.remove(); }, 5000);
}

async function fetchJSON(url){
  try{
    const res = await fetch(url, { headers:{accept:"application/json"} });
    if(!res.ok){
      showNotification(`Error: HTTP ${res.status} for ${url}`, true);
      return {ok:false, status:res.status, error:`HTTP ${res.status}`};
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

// NEW function to build the source cards
function buildSourceCards() {
    if (!els.sourceCardGrid) return;
    els.sourceCardGrid.innerHTML = state.sources.map(s => {
        const initials = s.split(/\s+/).map(w=>w[0]).slice(0,2).join("").toUpperCase();
        const meta = SOURCE_INFO[s] || { full: s, desc: "Latest announcements and updates" };
        const logo = LOGO_MAP[s];
        return `
        <a class="source-card" onclick="selectSource('${escapeAttr(s)}')">
            <div class="source-card-logo">${logo ? `<img src="${escapeAttr(logo)}" alt="${escapeAttr(meta.full)}"/>` : escapeHtml(initials)}</div>
            <h3>${escapeHtml(s)}</h3>
            <div class="source-full">${escapeHtml(meta.full)}</div>
            <p class="source-desc">${escapeHtml(meta.desc)}</p>
        </a>`;
    }).join("");
}

// NEW function to handle selecting a source
async function selectSource(source) {
    els.sourceSelector.style.display = 'none';
    els.resultsContainer.style.display = 'block';
    
    // Update tab bar to show selected source and a back button
    els.tabs.innerHTML = `
        <button class="back-btn" onclick="showSourceSelector()">← All Sources</button>
        <button class="exam-tab active">${escapeHtml(source)}</button>
    `;

    await loadAnnouncements(source);
}

// NEW function to go back to the source grid
function showSourceSelector() {
    els.resultsContainer.style.display = 'none';
    els.sourceSelector.style.display = 'block';
}

async function loadAnnouncements(source){
  state.activeSource = source;
  setStatus(`Fetching announcements for ${source} …`);
  const {ok, data} = await fetchJSON(`${API_BASE}/announcements/${encodeURIComponent(source)}`);
  if(!ok || !data){
    setStatus(`Couldn’t read announcements for ${source}. Showing empty list.`, true);
    state.items = [];
  }else{
    const arr = Array.isArray(data.data) ? data.data : (Array.isArray(data) ? data : []);
    state.items = arr.map(normaAnn);
  }
  state.page = 1;
  applyFilters();
}

function normaAnn(x){
  return {
    id: String(x.id ?? cryptoId()),
    text: String(x.text ?? x.title ?? "Untitled"),
    source: String(x.source ?? state.activeSource ?? "Source"),
    link: String(x.link ?? x.url ?? "#"),
    date: x.date ?? x.postedAt ?? x.published_at ?? null
  };
}

function cryptoId(){ try{ return crypto.getRandomValues(new Uint32Array(1))[0].toString(16);}catch(_){return Math.random().toString(16).slice(2);} }

function applyFilters(){
  const q = (document.getElementById("q")?.value || "").trim().toLowerCase();
  let arr = state.items.slice();
  if (q) arr = arr.filter(i => i.text.toLowerCase().includes(q));
  state.filtered = arr;
  renderList();
}

function renderList(){
  const start = (state.page-1)*state.perPage;
  const pageItems = state.filtered.slice(start, start+state.perPage);
  if (els.count) els.count.textContent = String(state.filtered.length);
  els.list.innerHTML = pageItems.map(renderCard).join("");
  renderPagination();
}

function renderCard(x){
  const initials = (x.source || "??").split(/\s+/).map(w=>w[0]).slice(0,2).join("").toUpperCase();
  return `<li class="card" data-id="${escapeAttr(x.id)}" onclick="selectItem('${escapeAttr(x.id)}')">
    <div class="logo" aria-hidden="true">${escapeHtml(initials)}</div>
    <div class="meta">
      <div class="title">${escapeHtml(x.text)}</div>
      <div class="org">${escapeHtml(x.source)}</div>
      <div class="row">${x.date ? escapeHtml(fmtDate(x.date)) : "Latest"}</div>
    </div>
    <div><a class="btn primary" href="${escapeAttr(x.link)}" target="_blank" rel="noopener">Read</a></div>
  </li>`;
}

function renderPagination(){
  const pages = Math.ceil(state.filtered.length / state.perPage) || 1;
  let html = "";
  for(let i=1;i<=pages;i++){
    html += `<button class="page-btn ${i===state.page?'active':''}" onclick="gotoPage(${i})">${i}</button>`;
  }
  els.pagination.innerHTML = html;
}

function gotoPage(n){ state.page = n; renderList(); }

function selectItem(id){
  const x = state.filtered.find(j => String(j.id) === String(id));
  if(!x || !els.detail) return;
  els.detail.classList.remove("empty");
  els.detail.innerHTML = `
    <div class="detail-header">
      <div>
        <h3 class="detail-title">${escapeHtml(x.text)}</h3>
        <div class="detail-org">${escapeHtml(x.source)}</div>
      </div>
      <div class="detail-actions">
        <a href="${escapeAttr(x.link)}" target="_blank" rel="noopener" class="btn primary apply">Open on official site</a>
        <button class="btn save" type="button" onclick="saveItem('${escapeAttr(x.id)}')">Save</button>
      </div>
    </div>
    <div class="detail-body">
      ${x.date ? `<p><b>Date:</b> ${escapeHtml(fmtDate(x.date))}</p>` : ""}
      <p>Announcement from <b>${escapeHtml(x.source)}</b>. Use the button to read it on the official website.</p>
    </div>`;
}

function saveItem(id){
  try{
    const set = new Set(JSON.parse(localStorage.getItem("savedAnnouncements")||"[]"));
    if (set.has(id)) set.delete(id); else set.add(id);
    localStorage.setItem("savedAnnouncements", JSON.stringify([...set]));
    alert("Saved list updated.");
  }catch(e){}
}

/* helpers */
function escapeHtml(s){return String(s??"").replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]))}
function escapeAttr(s){return escapeHtml(s).replace(/"/g,"&quot;")}
function fmtDate(dt){ const d = new Date(dt); return isNaN(d)? String(dt) : d.toLocaleDateString(undefined,{year:'numeric',month:'short',day:'numeric'}); }

/* events */
// Remove search binding: no global search or filters now
document.querySelectorAll(".chip[data-sort]")?.forEach(ch=>{
  ch.addEventListener("click", ()=>{
    document.querySelectorAll(".chip[data-sort]").forEach(c=>c.classList.remove("active"));
    ch.classList.add("active"); applyFilters();
  });
});

/* expose for inline handlers */
window.selectItem = selectItem;
window.gotoPage = gotoPage;
window.selectSource = selectSource; // Expose new functions
window.showSourceSelector = showSourceSelector;

/* init */
(async function init(){
  // This check ensures we only run this logic on the notifications page
  if (document.getElementById('sourceSelector')) {
    const def = document.querySelector('.chip[data-sort="default"]'); if(def) def.classList.add("active");
    await loadSources();
  }
})();
