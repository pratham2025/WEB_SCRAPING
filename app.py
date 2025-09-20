# streamlit_app.py
import streamlit as st
import requests
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(
    page_title="Education Announcements Hub",
    page_icon="📢",
    layout="wide",
)

# --- API URL ---
API_BASE_URL = "http://127.0.0.1:8000"

# --- Caching Functions ---
@st.cache_data(ttl=600)  # Cache data for 10 minutes
def fetch_api_data(endpoint):
    """Fetches data from a generic API endpoint."""
    try:
        url = f"{API_BASE_URL}/{endpoint}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API endpoint '{endpoint}': {e}. Is your scraper_api.py running?")
        return None

# --- UI Rendering Functions ---
def render_announcements_tab(source_name):
    """Renders the content for a single announcement source tab."""
    st.header(f"{source_name} Announcements")
    
    endpoint = f"announcements/{source_name}"
    
    with st.spinner(f"Fetching latest {source_name} data from database..."):
        response_data = fetch_api_data(endpoint)
        # We add the timestamp here so it reflects the frontend fetch time
        last_updated = datetime.now()

    if response_data and "data" in response_data:
        announcements = response_data["data"]

        col1, col2 = st.columns(2)
        search_term = col1.text_input("Search announcements", key=f"search_{source_name}").lower()
        sort_option = col2.selectbox("Sort by", ("Default (Newest First)", "Alphabetical (A-Z)"), key=f"sort_{source_name}")
        
        st.caption(f"Last updated: {last_updated.strftime('%Y-%m-%d %H:%M:%S')}")
        st.markdown("---")

        if sort_option == "Alphabetical (A-Z)":
            announcements.sort(key=lambda x: x['text'])
        
        if search_term:
            announcements = [item for item in announcements if search_term in item['text'].lower()]

        if announcements:
            for item in announcements:
                st.markdown(f"**{item['text']}** - [Read More]({item['link']})")
        else:
            st.info("No announcements found matching your criteria.")
    else:
        st.warning(f"Could not retrieve announcements for {source_name}.")

# --- Main App ---
def main():
    """Main function to run the Streamlit app."""
    st.title("📢 Education Announcements Hub")
    st.markdown("Your dynamic dashboard for the latest news from various educational websites.")

    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.success("Cache cleared! Fetching fresh data from the server.")
        st.rerun()

    # Dynamically fetch the list of sources from the API
    sources_data = fetch_api_data("sources")
    
    if sources_data and "sources" in sources_data and sources_data["sources"]:
        source_list = sources_data["sources"]
        
        # Dynamically create tabs
        created_tabs = st.tabs([f"🎓 {source}" for source in source_list])
        
        # Populate each tab
        for tab, source_name in zip(created_tabs, source_list):
            with tab:
                render_announcements_tab(source_name)
    else:
        st.warning("No data sources found. Please run the worker.py script to populate the database.")

if __name__ == "__main__":
    main()

