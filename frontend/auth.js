// Google Login

async function loginWithGoogle() {
  if (!window.supabase) {
    console.error("Supabase client not initialized. Make sure secrets.js loads before auth.js");
    alert("Authentication system not ready. Please refresh the page.");
    return;
  }

  // Get the full URL of the current page for redirect after OAuth
  // This should match the Site URL configured in Supabase Dashboard
  const protocol = window.location.protocol;
  const host = window.location.host;
  const pathname = window.location.pathname;
  const redirectTo = `${protocol}//${host}${pathname}`;

  console.log("=== OAuth Debug Info ===");
  console.log("Current URL:", window.location.href);
  console.log("Protocol:", protocol);
  console.log("Host:", host);
  console.log("Pathname:", pathname);
  console.log("Redirect URL:", redirectTo);
  console.log("Supabase URL:", window.SUPABASE?.url);
  console.log("========================");

  // Show user-friendly message about redirect URL
  const redirectInfo = `Redirect URL: ${redirectTo}\n\nMake sure this URL is configured in:\n1. Supabase Dashboard → Authentication → URL Configuration\n2. Google Cloud Console → OAuth 2.0 Client → Authorized redirect URIs`;
  console.log(redirectInfo);

  // Clear manual login if exists (user is switching to Google login)
  if (localStorage.getItem('manual_user')) {
    localStorage.removeItem('manual_user');
  }
  
  try {
    const { data, error } = await window.supabase.auth.signInWithOAuth({
      provider: "google",
      options: {
        redirectTo: redirectTo,
        queryParams: {
          access_type: 'offline',
          prompt: 'consent',
        }
      }
    });
    
    if (error) {
      console.error("Login error:", error);
      const errorMsg = `Google Login Failed: ${error.message}\n\nCurrent redirect URL: ${redirectTo}\n\nPlease check:\n1. This redirect URL is added in Supabase Dashboard → Authentication → URL Configuration\n2. This redirect URL is added in Google Cloud Console → OAuth 2.0 Client → Authorized redirect URIs\n3. Google OAuth is enabled in Supabase Dashboard\n4. Your IP address (${host}) is accessible from your network`;
      alert(errorMsg);
    } else {
      console.log("OAuth redirect initiated successfully:", data);
      console.log("You will be redirected to Google for authentication...");
    }
  } catch (err) {
    console.error("Unexpected error during OAuth:", err);
    alert(`Unexpected error: ${err.message}\n\nRedirect URL: ${redirectTo}\n\nPlease check browser console for more details.`);
  }
  // Note: If successful, user will be redirected to Google, then back to redirectTo URL
}

// Manual Login (no password, no verification)
// Expose globally for inline onclick handler
window.handleManualLogin = function(event) {
  event.preventDefault();
  
  const nameInput = document.getElementById('manualLoginName');
  const emailInput = document.getElementById('manualLoginEmail');
  
  if (!nameInput || !emailInput) {
    alert('Form fields not found. Please refresh the page.');
    return;
  }
  
  const name = nameInput.value.trim();
  const email = emailInput.value.trim();
  
  if (!name || !email) {
    alert('Please enter both name and email.');
    return;
  }
  
  // Basic email validation
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    alert('Please enter a valid email address.');
    return;
  }
  
  // Clear any existing Supabase session (user is switching to manual login)
  if (window.supabase) {
    window.supabase.auth.signOut().catch(() => {
      // Ignore errors, just try to clear
    });
  }
  
  // Store user info in localStorage
  const userData = {
    id: `manual_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
    email: email,
    user_metadata: {
      full_name: name,
      name: name,
      manual_login: true
    },
    created_at: new Date().toISOString()
  };
  
  localStorage.setItem('manual_user', JSON.stringify(userData));
  
  // Close modal
  const modal = document.getElementById('loginModal');
  if (modal) {
    modal.setAttribute('aria-hidden', 'true');
  }
  
  // Show success message
  if (typeof notify === 'function') {
    notify('Logged in successfully!', 'success');
  } else {
    alert('Logged in successfully!');
  }
  
  // Reload to update UI
  setTimeout(() => {
    window.location.reload();
  }, 500);
}

// Fetch User (on every page load) - checks both Supabase and manual login
async function getLoggedInUser() {
  // First check for manual login user
  const manualUserStr = localStorage.getItem('manual_user');
  if (manualUserStr) {
    try {
      const manualUser = JSON.parse(manualUserStr);
      // Return in Supabase user format for compatibility
      return {
        id: manualUser.id,
        email: manualUser.email,
        user_metadata: manualUser.user_metadata || {},
        created_at: manualUser.created_at
      };
    } catch (e) {
      console.warn('Error parsing manual user:', e);
      localStorage.removeItem('manual_user');
    }
  }
  
  // Then check Supabase (Google OAuth)
  if (!window.supabase) {
    console.warn("Supabase client not initialized");
    return null;
  }
  const { data: { user }, error } = await window.supabase.auth.getUser();
  if (error) {
    console.error("Error fetching user:", error);
    return null;
  }
  return user;
}

// Logout
async function logoutUser() {
  // Check if it's a manual login user
  const manualUserStr = localStorage.getItem('manual_user');
  if (manualUserStr) {
    // Remove manual user
    localStorage.removeItem('manual_user');
    // Reload to update UI
    window.location.reload();
    return;
  }
  
  // Otherwise, logout from Supabase
  if (!window.supabase) {
    console.error("Supabase client not initialized");
    return;
  }
  const { error } = await window.supabase.auth.signOut();
  if (error) {
    console.error("Logout error:", error);
    alert("Logout failed: " + error.message);
  } else {
    // Reload current page to update UI
    window.location.reload();
  }
}

// Handle OAuth callback on page load
async function handleAuthCallback() {
  if (!window.supabase) {
    console.warn("Supabase not initialized, skipping auth callback");
    return;
  }
  
  // Check if this is a callback from OAuth
  const hashParams = new URLSearchParams(window.location.hash.substring(1));
  const accessToken = hashParams.get('access_token');
  const error = hashParams.get('error');
  const errorDescription = hashParams.get('error_description');
  
  console.log("=== OAuth Callback Debug ===");
  console.log("Current URL:", window.location.href);
  console.log("Hash:", window.location.hash);
  console.log("Access token present:", !!accessToken);
  console.log("Error:", error);
  console.log("Error description:", errorDescription);
  console.log("===========================");
  
  if (error) {
    console.error("OAuth error:", error);
    console.error("Error description:", errorDescription);
    const errorMsg = errorDescription 
      ? `Authentication failed: ${error}\n\nDetails: ${decodeURIComponent(errorDescription)}`
      : `Authentication failed: ${error}`;
    alert(errorMsg);
    // Clean up URL
    window.history.replaceState({}, document.title, window.location.pathname);
    return;
  }
  
  if (accessToken) {
    // Exchange the code for a session
    try {
      const { data, error: sessionError } = await window.supabase.auth.getSession();
      if (sessionError) {
        console.error("Session error:", sessionError);
        alert(`Session error: ${sessionError.message}`);
      } else if (data.session) {
        console.log("✅ Successfully authenticated!");
        console.log("User:", data.session.user?.email);
        // Clear manual login if exists (user switched to Google login)
        if (localStorage.getItem('manual_user')) {
          localStorage.removeItem('manual_user');
        }
        // Clean up URL hash
        window.history.replaceState({}, document.title, window.location.pathname);
        // Reload to update UI
        window.location.reload();
      } else {
        console.warn("No session found after OAuth callback");
      }
    } catch (err) {
      console.error("Error processing session:", err);
      alert(`Error processing authentication: ${err.message}`);
    }
  }
}

// Run callback handler on page load
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', handleAuthCallback);
} else {
  handleAuthCallback();
}

