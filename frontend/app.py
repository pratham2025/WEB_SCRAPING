import streamlit as st
import requests
from datetime import datetime
import logging

# --- Page Configuration ---
st.set_page_config(
    page_title="Education Announcements Hub",
    page_icon="📢",
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
        # We add a timestamp here after the data is fetched.
        last_updated = datetime.now()

    if response_data and "data" in response_data:
        announcements = response_data["data"]

        col1, col2 = st.columns([3, 1])
        with col1:
            search_term = st.text_input(
                "Search announcements",
                key=f"search_{source_name}",
                placeholder=f"Search in {source_name}..."
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
            announcements.sort(key=lambda x: x['text'])
        
        if search_term:
            announcements = [
                item for item in announcements
                if search_term in item['text'].lower()
            ]

        if announcements:
            for item in announcements:
                with st.expander(f"📄 {item['text']}"):
                    st.markdown(f"**Source:** {item['source']}")
                    st.markdown(
                        f"<a href='{item['link']}' target='_blank' style='color: #ff4b4b; text-decoration: none; font-weight: bold;'>Read More on Official Site ↗</a>",
                        unsafe_allow_html=True
                    )
        else:
            st.info("No announcements found matching your criteria.")
    else:
        st.warning(f"Could not retrieve announcements for {source_name}. Ensure the API is running and data has been scraped.")

def main():
    """Main function to run the dynamic Streamlit app."""
    st.title("📢 Education Announcements Hub")
    st.markdown("Your central dashboard for the latest news from various educational authorities.")

    if st.button("🔄 Refresh All Data"):
        st.cache_data.clear()
        st.success("Cache cleared! Data will be re-fetched from the server.")
        time.sleep(1) # Give user time to see the message
        st.rerun()

    # --- DYNAMIC TAB CREATION ---
    sources_data = fetch_api_data("sources")
    
    if sources_data and "sources" in sources_data and sources_data["sources"]:
        # Sort sources alphabetically for consistent tab order
        available_sources = sorted(sources_data["sources"])
        
        # Create tabs dynamically based on the API response
        tabs = st.tabs([f"🎓 {source}" for source in available_sources])
        
        for i, source_name in enumerate(available_sources):
            with tabs[i]:
                render_announcements_tab(source_name)
    else:
        st.error("Could not fetch the list of sources from the API. Please ensure the `scraper_api.py` server is running.")
        st.info("Once the API is running, data sources that have been successfully scraped will appear here.")

if __name__ == "__main__":
    main()

