// common.js
document.addEventListener("DOMContentLoaded", async function() {
  const headerPlaceholder = document.querySelector("header.topbar");
  const footerPlaceholder = document.querySelector("footer.footer");

  // Fetch and inject header and footer
  try {
      const [headerRes, footerRes] = await Promise.all([
          fetch('_header.html'),
          fetch('_footer.html')
      ]);

      if (headerRes.ok && headerPlaceholder) {
          headerPlaceholder.innerHTML = await headerRes.text();
          // Move modal out of sticky header to body so position:fixed centers to viewport
          const injectedModal = document.getElementById('loginModal');
          if (injectedModal && injectedModal.parentElement !== document.body) {
              document.body.appendChild(injectedModal);
          }
      }
      
      if (footerRes.ok && footerPlaceholder) {
          footerPlaceholder.innerHTML = await footerRes.text();
          // Set copyright year after footer is loaded
          const yearEl = document.getElementById('year');
          if(yearEl) yearEl.textContent = new Date().getFullYear();
      }
      
      // After loading header, manage active links and search bar visibility
      setActiveNavLink();
      handleSearchBar();

      // Auth modal wiring
      setupLoginModal();

      // Ensure Google script is loaded and GIS is initialized for dynamically injected header
      try {
          await ensureGoogleScriptLoaded();
          await initGoogleSignIn();
      } catch (e) {
          console.warn('Google script init failed (will retry on open):', e);
      }

  } catch (error) {
      console.error("Error loading header/footer:", error);
  }
});

function setActiveNavLink() {
  // Use 'home.html' as the default for root paths
  const currentPage = window.location.pathname.split('/').pop() || 'home.html';
  const navLinks = document.querySelectorAll('.actions .link');
  
  navLinks.forEach(link => {
      const linkPage = link.getAttribute('href').split('/').pop();
      if (linkPage === currentPage) {
          link.classList.add('active');
      } else {
          link.classList.remove('active');
      }
  });
}

function handleSearchBar() {
  const searchBar = document.getElementById('globalSearch');
  if (!searchBar) return;

  // Hide search bar on pages that don't need it
  const nonSearchPages = ['home.html', 'syllabus.html'];
  const currentPage = window.location.pathname.split('/').pop() || 'home.html';

  if (nonSearchPages.includes(currentPage)) {
      searchBar.style.display = 'none';
  }
}

// --- Auth modal and Google Sign-In ---
function setupLoginModal(){
  const loginBtn = document.getElementById('loginBtn');
  const modal = document.getElementById('loginModal');
  if(!loginBtn || !modal) return;

  const closeSelectors = ['[data-close="true"]'];
  const open = () => { modal.setAttribute('aria-hidden','false'); };
  const close = () => { modal.setAttribute('aria-hidden','true'); };

  loginBtn.addEventListener('click', async () => {
      open();
      try {
          await ensureGoogleScriptLoaded();
          await initGoogleSignIn();
      } catch(e){
          console.error('Failed to initialize Google Sign-In:', e);
      }
  });
  closeSelectors.forEach(sel => {
      modal.querySelectorAll(sel).forEach(el => el.addEventListener('click', close));
  });

  // Close on Escape
  document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && modal.getAttribute('aria-hidden') === 'false') close();
  });

  // Google callback to receive credential
  window.handleGoogleCredentialResponse = (response) => {
      try {
          // You will need to verify this token on your server
          const idToken = response.credential;
          notify('Logged in with Google', 'success');
          close();
          // Optionally store token temporarily
          sessionStorage.setItem('google_id_token', idToken);
      } catch(err){
          notify('Google login failed', 'error');
          console.error(err);
      }
  };
}

function notify(message, type='success'){
  const node = document.createElement('div');
  node.className = `notification ${type}`;
  node.textContent = message;
  document.body.appendChild(node);
  setTimeout(() => node.remove(), 2500);
}

// --- Utilities to load and init Google Identity Services when header is injected dynamically ---
function ensureGoogleScriptLoaded(){
  return new Promise((resolve, reject) => {
      if (window.google && window.google.accounts && window.google.accounts.id) return resolve();
      // Avoid adding duplicate script
      if (document.querySelector('script[data-gis="true"]')) {
          document.querySelector('script[data-gis="true"]').addEventListener('load', () => resolve());
          document.querySelector('script[data-gis="true"]').addEventListener('error', (e) => reject(e));
          return;
      }
      const s = document.createElement('script');
      s.src = 'https://accounts.google.com/gsi/client';
      s.async = true; s.defer = true; s.setAttribute('data-gis','true');
      s.onload = () => resolve();
      s.onerror = (e) => reject(e);
      document.head.appendChild(s);
  });
}

async function initGoogleSignIn(){
  const onloadEl = document.getElementById('g_id_onload');
  const signInContainer = document.querySelector('.g_id_signin');
  if (!onloadEl || !signInContainer || !(window.google && window.google.accounts && window.google.accounts.id)) return;

  const clientId = onloadEl.dataset.client_id;
  if (!clientId) return;

  // Initialize only once
  if (!initGoogleSignIn._initialized) {
      window.google.accounts.id.initialize({
          client_id: clientId,
          callback: window.handleGoogleCredentialResponse,
          auto_select: false,
      });
      initGoogleSignIn._initialized = true;
  }

  // Render button fresh each time the modal opens
  signInContainer.innerHTML = '';
  window.google.accounts.id.renderButton(signInContainer, {
      type: 'standard',
      shape: 'rect',
      size: 'large',
      theme: 'outline',
      text: 'signin_with',
      logo_alignment: 'left',
      width: 320
  });
}