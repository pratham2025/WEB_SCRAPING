// secrets.js — Supabase credentials (use anon key only!)
window.SUPABASE = {
  url: "https://hfsazlirxtjbarftyoqh.supabase.co",
  anonKey: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imhmc2F6bGlyeHRqYmFyZnR5b3FoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjIyNTgwNTMsImV4cCI6MjA3NzgzNDA1M30.edUhPzkhHMbadGtvLpZPryX0f4u4FRX9blSkWXmCYGI" // get from Supabase project settings → API → anon key
};

// Initialize Supabase client
// The @supabase/supabase-js@2 CDN from jsdelivr exposes it as a global
// We need to wait for the script to fully load
(function initSupabase() {
  // The CDN script should be loaded before this, but we check multiple possibilities
  const createClient = (function() {
    // Try different possible global names
    if (typeof supabase !== 'undefined' && typeof supabase.createClient === 'function') {
      return supabase.createClient;
    }
    if (typeof window.supabase !== 'undefined' && typeof window.supabase.createClient === 'function') {
      return window.supabase.createClient;
    }
    if (typeof supabasejs !== 'undefined' && typeof supabasejs.createClient === 'function') {
      return supabasejs.createClient;
    }
    if (typeof window.supabasejs !== 'undefined' && typeof window.supabasejs.createClient === 'function') {
      return window.supabasejs.createClient;
    }
    return null;
  })();

  if (createClient) {
    window.supabase = createClient(window.SUPABASE.url, window.SUPABASE.anonKey);
    console.log('✅ Supabase client initialized');
  } else {
    // Retry after a short delay if script hasn't loaded yet
    console.warn('⚠️ Supabase library not found, retrying...');
    setTimeout(initSupabase, 100);
  }
})();
