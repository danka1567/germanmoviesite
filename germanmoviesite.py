import streamlit as st
import cloudscraper
from urllib.parse import urljoin, urlparse
import re

# Set page title and configuration
st.set_page_config(
    page_title="URL Redirect Finder",
    page_icon="🔗",
    layout="centered"
)

# App title and description
st.title("🔗 URL Redirect Finder")
st.markdown("Enter a URL to find redirect links from the page content.")

# Input box for URL
url = st.text_input(
    "Enter URL:",
    value="https://s.to/serie/stream/naruto-shippuden/staffel-1/episode-1",
    placeholder="https://example.com/path/to/page"
)

def find_redirect_url(input_url):
    """Find redirect URL from the given page"""
    try:
        # Validate URL format
        if not input_url.startswith(('http://', 'https://')):
            return "❌ Error: Please enter a valid URL starting with http:// or https://"
        
        BASE = "{uri.scheme}://{uri.netloc}".format(uri=urlparse(input_url))
        
        # Create scraper and get page content
        scraper = cloudscraper.create_scraper()
        response = scraper.get(input_url)
        html = response.text
        
        # Search for redirect pattern
        redirect_match = re.search(r'(/redirect/\d+)', html)
        
        if redirect_match:
            redirect_url = urljoin(BASE, redirect_match.group(1))
            return f"✅ Found redirect URL: {redirect_url}"
        else:
            return "❌ No redirect URL found in the page content"
            
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Process button
if st.button("Find Redirect URL"):
    if url:
        with st.spinner("Searching for redirect URL..."):
            result = find_redirect_url(url)
        
        # Output box (using st.text_area for better display)
        st.subheader("Result:")
        st.text_area("", value=result, height=100, key="output")
    else:
        st.warning("⚠️ Please enter a URL first")

# Additional information
st.markdown("---")
st.markdown("""
**How it works:**
1. Enter a URL in the input box above
2. Click the "Find Redirect URL" button
3. The app will scan the page for redirect patterns and display the result

**Note:** This app looks for patterns matching `/redirect/` followed by numbers in the page HTML.
""")
