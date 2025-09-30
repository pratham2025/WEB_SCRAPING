# frontend/app.py (Updated with Summaries)

import streamlit as st
import requests
from datetime import datetime
import logging
import time # Added for the refresh button delay

# --- Page Configuration ---
st.set_page_config(
    page_title="ExamDoor Announcements Hub",
    page_icon="🔔",
    layout="wide",
)

# --- API URL ---
API_BASE_URL = "http://127.0.0.1:8000"

# --- Setup Logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Data Fetching Functions ---
@st.cache_data(ttl=600)  # Cache data for 10 minutes
def fetch_api_data(endpoint):
    """Fetches data from a specified API endpoint."""
    try:
        url = f"{API_BASE_URL}/{endpoint}"
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API endpoint '/{endpoint}': {e}")
        return None

def render_announcements_tab(source_name):
    """Renders the content for a single announcement source tab."""
    st.header(f"Latest Announcements from {source_name}")

    endpoint = f"announcements/{source_name}"
    
    with st.spinner(f"Fetching latest {source_name} data..."):
        response_data = fetch_api_data(endpoint)
        last_updated = datetime.now()

    if response_data and "data" in response_data:
        announcements = response_data["data"]

        col1, col2 = st.columns([3, 1])
        with col1:
            search_term = st.text_input(
                "Search announcements",
                key=f"search_{source_name}",
                placeholder=f"Search in {source_name} summaries..."
            ).lower()
        with col2:
            sort_option = st.selectbox(
                "Sort by",
                ("Default (Newest First)", "Alphabetical (A-Z)"),
                key=f"sort_{source_name}"
            )

        st.caption(f"Last updated: {last_updated.strftime('%Y-%m-%d %H:%M:%S')}")
        st.markdown("---")

        if sort_option == "Alphabetical (A-Z)":
            announcements.sort(key=lambda x: x.get('summary', x['text'])) # Sort by summary
        
        # --- MODIFIED: Search in both summary and original text ---
        if search_term:
            announcements = [
                item for item in announcements
                if search_term in item.get('summary', '').lower() or search_term in item['text'].lower()
            ]

        if announcements:
            # --- MODIFIED: Display the summary first, with original text in an expander ---
            for item in announcements:
                # Use item.get('summary', item['text']) as a fallback if summary doesn't exist for old entries
                summary = item.get('summary', item['text'])
                
                st.markdown(f"#### {summary}") # Display the summary as a subheader
                
                with st.expander("View Original Announcement Text"):
                    st.markdown(f"> _{item['text']}_") # Blockquote for original text

                st.markdown(
                    f"<a href='{item['link']}' target='_blank' style='color: #ff4b4b; text-decoration: none; font-weight: bold;'>Read on Official Site →</a>",
                    unsafe_allow_html=True
                )
                st.divider() # Use st.divider for a clean separator
        else:
            st.info("No announcements found matching your criteria.")
    else:
        st.warning(f"Could not retrieve announcements for {source_name}. Ensure the API is running and data has been scraped.")

def main():
    """Main function to run the dynamic Streamlit app."""
    st.title("🔔 ExamDoor Announcements Hub")
    st.markdown("Your central dashboard for summarized, easy-to-read news from various educational authorities.")

    if st.button("🔄 Refresh All Data"):
        st.cache_data.clear()
        st.success("Cache cleared! Re-fetching fresh data from the server...")
        time.sleep(1)
        st.rerun()

    # --- DYNAMIC TAB CREATION (No changes needed here) ---
    sources_data = fetch_api_data("sources")
    
    if sources_data and "sources" in sources_data and sources_data["sources"]:
        available_sources = sorted(sources_data["sources"])
        
        tab_titles = [f" {source} " for source in available_sources]
        tabs = st.tabs(tab_titles)
        
        for i, source_name in enumerate(available_sources):
            with tabs[i]:
                render_announcements_tab(source_name)
    else:
        st.error("Could not fetch the list of sources from the API. Please ensure the `scraper_api.py` server is running.")
        st.info("Once the API is running, data sources that have been successfully scraped will appear here.")

if __name__ == "__main__":
    main()