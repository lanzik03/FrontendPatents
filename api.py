import streamlit as st
import requests
import math

st.set_page_config(page_title="Patent Validation", layout="wide")

st.title("Patent Search via PatentsView API")

# Initialize session state for pagination
if 'current_page' not in st.session_state:
    st.session_state.current_page = 1
if 'patents_data' not in st.session_state:
    st.session_state.patents_data = []
if 'total_patents' not in st.session_state:
    st.session_state.total_patents = 0
if 'last_searched_year' not in st.session_state:
    st.session_state.last_searched_year = None

search_year = st.text_input("Enter a year (explore from 1976 to 2025):", key="search_year")

if search_year:
    try:
        year = int(search_year)
    except ValueError:
        st.error("Please enter a valid year (like 2023)")
        st.stop()
    
    # Only search if year has changed
    if st.session_state.last_searched_year != year:
        st.session_state.last_searched_year = year
        st.session_state.current_page = 1
        
        url = "https://search.patentsview.org/api/v1/patent/"
        headers = {
            "X-Api-Key": st.secrets["PATENTSVIEW_API"],
            "Content-Type": "application/json"
        }
        payload = {
            "q": {"patent_year": year},
            "f": ["patent_id", "patent_title", "patent_abstract"],
            "o": {"size": 100}
        }
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            resp = response.json()
            pats = resp.get("patents", [])
            
            if pats:
                st.session_state.patents_data = pats
                st.session_state.total_patents = len(pats)
                st.success(f"Found {len(pats)} patents for year {year}")
            else:
                st.warning("No patents found for that year.")
                st.session_state.patents_data = []
                st.session_state.total_patents = 0
        else:
            st.error(f"Error {response.status_code}")
            st.text(response.text)
            st.session_state.patents_data = []
            st.session_state.total_patents = 0

# Display results with pagination
if st.session_state.patents_data:
    patents_per_page = 10
    total_pages = math.ceil(st.session_state.total_patents / patents_per_page)
    
    # Pagination controls
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("← Previous", disabled=st.session_state.current_page <= 1):
            st.session_state.current_page -= 1
            st.rerun()
    
    with col2:
        st.write(f"Page {st.session_state.current_page} of {total_pages}")
        st.write(f"Showing patents {(st.session_state.current_page-1)*patents_per_page + 1}-{min(st.session_state.current_page*patents_per_page, st.session_state.total_patents)} of {st.session_state.total_patents}")
    
    with col3:
        if st.button("Next →", disabled=st.session_state.current_page >= total_pages):
            st.session_state.current_page += 1
            st.rerun()
    
    st.markdown("---")
    
    # Calculate start and end indices for current page
    start_idx = (st.session_state.current_page - 1) * patents_per_page
    end_idx = min(start_idx + patents_per_page, st.session_state.total_patents)
    
    # Display patents for current page
    for i in range(start_idx, end_idx):
        p = st.session_state.patents_data[i]
        patent_id = p.get('patent_id')
        google_patent_url = f"https://patents.google.com/patent/US{patent_id}"
        
        st.markdown(f"### [{p.get('patent_title','N/A')}]({google_patent_url})")
        st.write(f"**Patent ID:** {patent_id}")
        st.write(f"**Abstract:** {p.get('patent_abstract','N/A')}")
        st.markdown("---")
    
    # Page navigation at bottom
    st.markdown("### Go to page:")
    page_cols = st.columns(min(total_pages, 10))
    
    for i in range(min(total_pages, 10)):
        page_num = i + 1
        with page_cols[i]:
            if st.button(f"{page_num}", key=f"page_{page_num}", 
                        type="primary" if page_num == st.session_state.current_page else "secondary"):
                st.session_state.current_page = page_num
                st.rerun()
    
    if total_pages > 10:
        st.write(f"... and {total_pages - 10} more pages")
