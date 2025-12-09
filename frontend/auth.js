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

  console.log("Initiating Google OAuth with redirectTo:", redirectTo);

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
    alert("Google Login Failed: " + error.message + "\n\nPlease check:\n1. Google OAuth is enabled in Supabase Dashboard\n2. Site URL is configured correctly in Supabase\n3. Redirect URI is added in Google Cloud Console");
  } else {
    console.log("OAuth redirect initiated:", data);
  }
  // Note: If successful, user will be redirected to Google, then back to redirectTo URL
}

// Fetch User (on every page load)
async function getLoggedInUser() {
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
  if (!window.supabase) return;
  
  // Check if this is a callback from OAuth
  const hashParams = new URLSearchParams(window.location.hash.substring(1));
  const accessToken = hashParams.get('access_token');
  const error = hashParams.get('error');
  
  if (error) {
    console.error("OAuth error:", error);
    alert("Authentication failed: " + error);
    // Clean up URL
    window.history.replaceState({}, document.title, window.location.pathname);
    return;
  }
  
  if (accessToken) {
    // Exchange the code for a session
    const { data, error: sessionError } = await window.supabase.auth.getSession();
    if (sessionError) {
      console.error("Session error:", sessionError);
    } else if (data.session) {
      console.log("Successfully authenticated!");
      // Clean up URL hash
      window.history.replaceState({}, document.title, window.location.pathname);
    }
  }
}

// Run callback handler on page load
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', handleAuthCallback);
} else {
  handleAuthCallback();
}

