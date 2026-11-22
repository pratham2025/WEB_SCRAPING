// secrets.example.js — Template for frontend Supabase credentials (use anon key only!)
// Copy this file to secrets.js and fill in your Supabase project details.

window.SUPABASE = {
  url: "https://your-project.supabase.co",
  anonKey: "your-supabase-anon-key"
};

(function initSupabase() {
  let retryCount = 0;
  const maxRetries = 50;
  
  function tryInit() {
    const createClient = (function() {
      if (typeof supabase !== 'undefined' && typeof supabase.createClient === 'function') {
        return supabase.createClient;
      }
      if (typeof window.supabase !== 'undefined' && typeof window.supabase.createClient === 'function') {
        return window.supabase.createClient;
      }
      return null;
    })();

    if (createClient && window.SUPABASE && window.SUPABASE.url && window.SUPABASE.anonKey) {
      try {
        window.supabase = createClient(window.SUPABASE.url, window.SUPABASE.anonKey);
        console.log('✅ Supabase client initialized');
        return true;
      } catch (err) {
        console.error('❌ Error initializing Supabase client:', err);
        return false;
      }
    } else {
      retryCount++;
      if (retryCount < maxRetries) {
        setTimeout(tryInit, 100);
      } else {
        console.error('❌ Failed to initialize Supabase client');
      }
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', tryInit);
  } else {
    tryInit();
  }
})();
