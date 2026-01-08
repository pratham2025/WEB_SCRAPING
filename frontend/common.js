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
              // Ensure all content is preserved when moving
              const modalContent = injectedModal.innerHTML;
              document.body.appendChild(injectedModal);
              // Double-check content is still there
              if (injectedModal.innerHTML !== modalContent) {
                  injectedModal.innerHTML = modalContent;
              }
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

      // Auth modal wiring - ensure it's set up after modal is moved to body
      setTimeout(() => {
        setupLoginModal();
      }, 50);
      
      // Ensure login button is visible initially (will be hidden if user is logged in)
      const loginBtn = document.getElementById('loginBtn');
      if (loginBtn) {
        loginBtn.style.display = 'inline-block';
        loginBtn.style.visibility = 'visible';
      }
      
      // Check and display user details if logged in
      updateUserDetails();
      
      // Setup user dropdown menu
      setupUserDropdown();
      
      // Listen for auth state changes
      setupAuthStateListener();
      
      // Mobile menu toggle - use setTimeout to ensure DOM is ready
      setTimeout(() => {
        setupMobileMenu();
      }, 100);

      // Google Sign-In is now handled by Supabase OAuth (auth.js)
      // No need to initialize the old Google Sign-In library

  } catch (error) {
      console.error("Error loading header/footer:", error);
  }
});

function setActiveNavLink() {
  // Use 'index.html' as the default for root paths
  const currentPage = window.location.pathname.split('/').pop() || 'index.html';
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
  const nonSearchPages = ['index.html'];
  const currentPage = window.location.pathname.split('/').pop() || 'index.html';

  if (nonSearchPages.includes(currentPage)) {
      searchBar.style.display = 'none';
  }
}

// --- Auth modal and Google Sign-In ---
function setupLoginModal(){
  const loginBtn = document.getElementById('loginBtn');
  const modal = document.getElementById('loginModal');
  if(!loginBtn || !modal) {
    console.warn('Login button or modal not found');
    return;
  }

  // Verify modal has content - if missing or partial, recreate it
  const buildModalTemplate = () => `
    <div class="modal-backdrop" data-close="true"></div>
    <div class="modal-content auth-modal" role="document">
      <button class="modal-close" type="button" aria-label="Close" data-close="true">×</button>
      <div class="auth-hero">
        <img src="src/images/bell_icon.png" alt="GETNOTIFY" class="bell-logo" width="44" height="44" style="flex-shrink: 0;"/>
        <h3 class="auth-title">GETNOTIFY</h3>
      </div>
      
      <!-- Manual Login Form -->
      <div id="manualLoginForm" style="margin-bottom: 1.5rem;">
        <p class="auth-desc" style="margin-bottom: 1rem;">Enter your details to get started (no password required)</p>
        <form id="manualLoginFormElement" onsubmit="handleManualLogin(event)" style="display: flex; flex-direction: column; gap: 0.75rem; max-width: 320px; margin: 0 auto;">
          <input 
            type="text" 
            id="manualLoginName" 
            placeholder="Your Name" 
            required 
            style="padding: 12px; border: 1px solid var(--ink-300); border-radius: 8px; font-size: 14px; font-family: inherit;"
          />
          <input 
            type="email" 
            id="manualLoginEmail" 
            placeholder="Your Email" 
            required 
            style="padding: 12px; border: 1px solid var(--ink-300); border-radius: 8px; font-size: 14px; font-family: inherit;"
          />
          <button type="submit" class="btn primary" style="width: 100%; margin-top: 0.5rem;">
            Continue
          </button>
        </form>
        <div style="text-align: center; margin: 1rem 0; position: relative;">
          <div style="position: absolute; top: 50%; left: 0; right: 0; height: 1px; background: var(--ink-300);"></div>
          <span style="background: white; padding: 0 12px; color: var(--ink-500); font-size: 14px; position: relative;">or</span>
        </div>
      </div>
      
      <p class="auth-desc" style="margin-bottom: 1rem;">Log in with Google to sync your preferences across devices</p>
      <button onclick="loginWithGoogle()" class="btn secondary google-signin-btn" style="width: 100%; max-width: 320px; margin: 0 auto;">
        <svg width="18" height="18" viewBox="0 0 18 18" xmlns="http://www.w3.org/2000/svg">
          <path fill="#4285F4" d="M17.64 9.2c0-.637-.057-1.251-.164-1.84H9v3.481h4.844c-.209 1.125-.843 2.078-1.796 2.717v2.258h2.908c1.702-1.567 2.684-3.874 2.684-6.615z"/>
          <path fill="#34A853" d="M9 18c2.43 0 4.467-.806 5.956-2.184l-2.908-2.258c-.806.54-1.837.86-3.048.86-2.344 0-4.328-1.584-5.036-3.711H.957v2.332C2.438 15.983 5.482 18 9 18z"/>
          <path fill="#FBBC05" d="M3.964 10.712c-.18-.54-.282-1.117-.282-1.712 0-.595.102-1.172.282-1.712V4.956H.957C.348 6.175 0 7.55 0 9c0 1.45.348 2.825.957 4.044l3.007-2.332z"/>
          <path fill="#EA4335" d="M9 3.58c1.321 0 2.508.454 3.44 1.345l2.582-2.58C13.463.891 11.426 0 9 0 5.482 0 2.438 2.017.957 4.956L3.964 7.288C4.672 5.163 6.656 3.58 9 3.58z"/>
        </svg>
        <span>Sign in with Google</span>
      </button>
      <p class="auth-privacy">By continuing, you agree to receive notifications from time to time. You can unsubscribe anytime.</p>
    </div>
  `;

  // Always render the latest modal template so deployments
  // don't depend on older inline HTML in `_header.html`
  modal.innerHTML = buildModalTemplate();
  const modalContent = modal.querySelector('.modal-content');

  const closeSelectors = ['[data-close="true"]'];
  const open = () => { 
    modal.setAttribute('aria-hidden','false');
    // Force visibility of all content
    const allContent = modal.querySelectorAll('*');
    allContent.forEach(el => {
      el.style.visibility = 'visible';
      el.style.opacity = '1';
    });
  };
  const close = () => { modal.setAttribute('aria-hidden','true'); };

  loginBtn.addEventListener('click', () => {
      open();
      // Reset form when opening
      const form = document.getElementById('manualLoginFormElement');
      if (form) {
        form.reset();
      }
      // Google Sign-In is now handled by Supabase OAuth (auth.js)
      // The button in the modal will call loginWithGoogle() directly
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

// --- Mobile menu toggle functionality ---
function setupMobileMenu() {
  const menuToggle = document.getElementById('menuToggle');
  const mainNav = document.getElementById('mainNav');
  if (!menuToggle || !mainNav) {
    console.warn('Mobile menu elements not found');
    return;
  }
  
  // Prevent duplicate event listeners
  if (menuToggle.dataset.initialized === 'true') {
    return;
  }
  menuToggle.dataset.initialized = 'true';

  // Create overlay element
  let overlay = document.querySelector('.menu-overlay');
  if (!overlay) {
    overlay = document.createElement('div');
    overlay.className = 'menu-overlay';
    document.body.appendChild(overlay);
  }

  const toggleMenu = () => {
    const isOpen = mainNav.classList.contains('menu-open');
    if (isOpen) {
      mainNav.classList.remove('menu-open');
      overlay.classList.remove('active');
      menuToggle.setAttribute('aria-expanded', 'false');
      document.body.style.overflow = '';
    } else {
      mainNav.classList.add('menu-open');
      overlay.classList.add('active');
      menuToggle.setAttribute('aria-expanded', 'true');
      document.body.style.overflow = 'hidden';
    }
  };

  menuToggle.addEventListener('click', toggleMenu);
  
  // Close menu when clicking overlay
  overlay.addEventListener('click', () => {
    if (mainNav.classList.contains('menu-open')) {
      toggleMenu();
    }
  });

  // Close menu when clicking a link (mobile)
  const navLinks = mainNav.querySelectorAll('.link, .btn');
  navLinks.forEach(link => {
    link.addEventListener('click', () => {
      if (window.innerWidth <= 900 && mainNav.classList.contains('menu-open')) {
        toggleMenu();
      }
    });
  });

  // Close menu on window resize if it goes back to desktop
  window.addEventListener('resize', () => {
    if (window.innerWidth > 900 && mainNav.classList.contains('menu-open')) {
      mainNav.classList.remove('menu-open');
      overlay.classList.remove('active');
      menuToggle.setAttribute('aria-expanded', 'false');
      document.body.style.overflow = '';
    }
  });
}

// Update user details in header
async function updateUserDetails() {
  const userDetails = document.getElementById('userDetails');
  const loginBtn = document.getElementById('loginBtn');
  const topbar = document.querySelector('.topbar');
  
  if (!userDetails) return;
  
  // Wait for Supabase to be ready
  if (!window.supabase) {
    // Retry after a short delay
    setTimeout(updateUserDetails, 200);
    return;
  }
  
  try {
    const user = await getLoggedInUser();
    
    if (user) {
      // User is logged in - show user details
      userDetails.style.display = 'flex';
      if (loginBtn) loginBtn.style.display = 'none';
      if (topbar) topbar.classList.add('user-logged-in');
      
      // Populate user info
      const userNameEl = document.getElementById('userName');
      const userEmailEl = document.getElementById('userEmail');
      const userAvatarEl = document.getElementById('userAvatar');
      
      // Get user metadata (from Google OAuth or manual login)
      const displayName = user.user_metadata?.full_name || 
                         user.user_metadata?.name || 
                         user.email?.split('@')[0] || 
                         'User';
      const email = user.email || '';
      const avatarUrl = user.user_metadata?.avatar_url || 
                       user.user_metadata?.picture || 
                       '';
      const isManualLogin = user.user_metadata?.manual_login || false;
      
      if (userNameEl) userNameEl.textContent = displayName;
      if (userEmailEl) userEmailEl.textContent = email;
      // Update main avatar (only if not manual login, otherwise use initials)
      if (userAvatarEl) {
        if (isManualLogin || !avatarUrl) {
          // For manual login, show initials
          const initials = displayName.split(' ').map(n => n[0]).join('').toUpperCase().substring(0, 2);
          userAvatarEl.style.display = 'none';
          // Create or update fallback
          let fallback = userAvatarEl.parentNode.querySelector('.avatar-fallback');
          if (!fallback) {
            fallback = document.createElement('div');
            fallback.className = 'avatar-fallback';
            fallback.style.cssText = 'width: 32px; height: 32px; border-radius: 50%; background: var(--green-500); color: white; display: flex; align-items: center; justify-content: center; font-weight: 600; font-size: 14px;';
            userAvatarEl.parentNode.insertBefore(fallback, userAvatarEl);
          }
          fallback.textContent = initials;
        } else {
          updateAvatar(userAvatarEl, avatarUrl, displayName);
        }
      }
      
      // Update dropdown avatar
      const userAvatarLarge = document.getElementById('userAvatarLarge');
      if (userAvatarLarge) {
        if (isManualLogin || !avatarUrl) {
          // For manual login, show initials
          const initials = displayName.split(' ').map(n => n[0]).join('').toUpperCase().substring(0, 2);
          userAvatarLarge.style.display = 'none';
          // Create or update fallback
          let fallback = userAvatarLarge.parentNode.querySelector('.avatar-fallback');
          if (!fallback) {
            fallback = document.createElement('div');
            fallback.className = 'avatar-fallback';
            fallback.style.cssText = 'width: 64px; height: 64px; border-radius: 50%; background: var(--green-500); color: white; display: flex; align-items: center; justify-content: center; font-weight: 600; font-size: 24px;';
            userAvatarLarge.parentNode.insertBefore(fallback, userAvatarLarge);
          }
          fallback.textContent = initials;
        } else {
          updateAvatar(userAvatarLarge, avatarUrl, displayName);
        }
      }
      
      // Update dropdown text
      const userNameLarge = document.getElementById('userNameLarge');
      const userEmailLarge = document.getElementById('userEmailLarge');
      if (userNameLarge) userNameLarge.textContent = displayName;
      if (userEmailLarge) userEmailLarge.textContent = email;
    } else {
      // User is not logged in - hide user details and show login button
      userDetails.style.display = 'none';
      if (loginBtn) {
        loginBtn.style.display = 'inline-block';
        loginBtn.style.visibility = 'visible';
      }
      if (topbar) topbar.classList.remove('user-logged-in');
    }
  } catch (error) {
    console.error('Error updating user details:', error);
    // On error, hide user details and show login button
    userDetails.style.display = 'none';
    if (loginBtn) {
      loginBtn.style.display = 'inline-block';
      loginBtn.style.visibility = 'visible';
    }
    if (topbar) topbar.classList.remove('user-logged-in');
  }
}

// Helper function to update avatar
function updateAvatar(avatarEl, avatarUrl, displayName) {
  if (!avatarEl) return;
  
  const parent = avatarEl.parentNode;
  if (!parent) return;
  
  // Remove any existing fallback
  const existingFallback = parent.querySelector('.avatar-fallback');
  if (existingFallback) {
    existingFallback.remove();
  }
  
  if (avatarUrl) {
    // Show avatar image
    avatarEl.src = avatarUrl;
    avatarEl.alt = displayName;
    avatarEl.style.display = 'block';
    avatarEl.onerror = function() {
      // If image fails to load, show fallback instead
      this.style.display = 'none';
      const initials = displayName.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
      const fallback = document.createElement('div');
      fallback.className = 'avatar-fallback';
      fallback.textContent = initials;
      parent.insertBefore(fallback, avatarEl);
    };
  } else {
    // Fallback: use initials as avatar
    const initials = displayName.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
    avatarEl.style.display = 'none';
    // Create a fallback div with initials
    const fallback = document.createElement('div');
    fallback.className = 'avatar-fallback';
    fallback.textContent = initials;
    parent.insertBefore(fallback, avatarEl);
  }
}

// Setup user dropdown menu
function setupUserDropdown() {
  const userInfoTrigger = document.getElementById('userInfoTrigger');
  const userDropdown = document.getElementById('userDropdown');
  
  if (!userInfoTrigger || !userDropdown) return;
  
  // Toggle dropdown on click
  userInfoTrigger.addEventListener('click', (e) => {
    e.stopPropagation();
    const isExpanded = userInfoTrigger.getAttribute('aria-expanded') === 'true';
    userInfoTrigger.setAttribute('aria-expanded', !isExpanded);
    userDropdown.setAttribute('aria-hidden', isExpanded);
  });
  
  // Close dropdown when clicking outside
  document.addEventListener('click', (e) => {
    if (!userInfoTrigger.contains(e.target) && !userDropdown.contains(e.target)) {
      userInfoTrigger.setAttribute('aria-expanded', 'false');
      userDropdown.setAttribute('aria-hidden', 'true');
    }
  });
  
  // Close dropdown on escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && userInfoTrigger.getAttribute('aria-expanded') === 'true') {
      userInfoTrigger.setAttribute('aria-expanded', 'false');
      userDropdown.setAttribute('aria-hidden', 'true');
    }
  });
}

// Setup auth state listener to automatically update UI on login/logout
function setupAuthStateListener() {
  if (!window.supabase) {
    // Retry after a short delay
    setTimeout(setupAuthStateListener, 200);
    return;
  }
  
  // Listen for auth state changes
  window.supabase.auth.onAuthStateChange((event, session) => {
    if (event === 'SIGNED_IN' || event === 'SIGNED_OUT' || event === 'TOKEN_REFRESHED') {
      updateUserDetails();
    }
  });
}