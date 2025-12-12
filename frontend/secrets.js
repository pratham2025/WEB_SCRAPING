// secrets.js — Supabase credentials (use anon key only!)
window.SUPABASE = {
  url: "https://hfsazlirxtjbarftyoqh.supabase.co",
  anonKey: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imhmc2F6bGlyeHRqYmFyZnR5b3FoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjIyNTgwNTMsImV4cCI6MjA3NzgzNDA1M30.edUhPzkhHMbadGtvLpZPryX0f4u4FRX9blSkWXmCYGI" // get from Supabase project settings → API → anon key
};

// Initialize Supabase client
// The @supabase/supabase-js@2 CDN from jsdelivr exposes it as a global
// We need to wait for the script to fully load
(function initSupabase() {
  let retryCount = 0;
  const maxRetries = 50; // 5 seconds max (50 * 100ms)
  
  function tryInit() {
    // The CDN script should be loaded before this, but we check multiple possibilities
    const createClient = (function() {
      // Try different possible global names
      if (typeof supabase !== 'undefined' && typeof supabase.createClient === 'function') {
        return supabase.createClient;
      }
      if (typeof window.supabase !== 'undefined' && typeof window.supabase.createClient === 'function') {
        return window.supabase.createClient;
      }
      // Check for the actual library from CDN
      if (typeof window.supabase !== 'undefined' && typeof window.supabase.createClient === 'function') {
        return window.supabase.createClient;
      }
      return null;
    })();

    if (createClient && window.SUPABASE && window.SUPABASE.url && window.SUPABASE.anonKey) {
      try {
        window.supabase = createClient(window.SUPABASE.url, window.SUPABASE.anonKey);
        console.log('✅ Supabase client initialized');
        console.log('Supabase URL:', window.SUPABASE.url);
        console.log('Current page URL:', window.location.href);
        return true;
      } catch (err) {
        console.error('❌ Error initializing Supabase client:', err);
        return false;
      }
    } else {
      retryCount++;
      if (retryCount < maxRetries) {
        // Retry after a short delay if script hasn't loaded yet
        if (retryCount === 1) {
          console.warn('⚠️ Supabase library not found, retrying...');
        }
        setTimeout(tryInit, 100);
      } else {
        console.error('❌ Failed to initialize Supabase after', maxRetries, 'retries');
        console.error('Make sure the Supabase CDN script is loaded before secrets.js');
        alert('Authentication system failed to load. Please refresh the page. If the problem persists, check your internet connection.');
      }
      return false;
    }
  }
  
  tryInit();
})();
