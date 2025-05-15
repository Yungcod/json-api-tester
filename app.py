import streamlit as st
import json
import base64
from io import BytesIO
from utils import (
    fetch_json_from_url,
    validate_json_string,
    analyze_json_structure
)

def get_download_link(json_data):
    """Generate a download link for JSON data"""
    json_str = json.dumps(json_data, indent=2)
    b64 = base64.b64encode(json_str.encode()).decode()
    href = f'<a href="data:file/json;base64,{b64}" download="data.json" class="download-button">Download JSON file</a>'
    return href

def main():
    st.set_page_config(
        page_title="JSON API Tester", 
        page_icon=None,
        layout="wide"
    )
    
    # Custom CSS for better styling
    st.markdown("""
        <style>
        .download-button {
            background-color: #4CAF50;
            color: white;
            padding: 8px 16px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            border-radius: 4px;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 24px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: #f0f2f6;
            border-radius: 4px 4px 0px 0px;
            gap: 1px;
            padding-top: 10px;
            padding-bottom: 10px;
        }
        .main-header {
            text-align: center;
            margin-bottom: 20px;
        }
        .subheader {
            color: #4d4d4d;
            margin-bottom: 30px;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="main-header"><h1>JSON API Tester</h1></div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader">Validate and analyze JSON data from API endpoints or pasted content.</div>', unsafe_allow_html=True)
    
    # Create tabs for the two input methods
    tab1, tab2 = st.tabs(["API URL", "Manual JSON"])
    
    with tab1:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            api_url = st.text_input("Enter API URL (must return JSON):", 
                                   placeholder="https://api.example.com/data")
        
        with col2:
            st.write("")
            st.write("")
            fetch_button = st.button("Fetch and Validate", key="fetch_button", use_container_width=True)
        
        # Example APIs
        with st.expander("Example APIs to try"):
            st.markdown("""
            - [Random User API](https://randomuser.me/api/) - Random user data
            - [JSON Placeholder](https://jsonplaceholder.typicode.com/todos/1) - Todo item
            - [JSON Placeholder Users](https://jsonplaceholder.typicode.com/users) - List of users
            - [Open Library](https://openlibrary.org/api/books?bibkeys=ISBN:0385472579&format=json) - Book data
            - [JSON Tester](https://jsonplaceholder.typicode.com/comments) - Comments (larger dataset)
            """)
            
        if fetch_button:
            if not api_url:
                st.warning("Please enter an API URL")
            else:
                with st.spinner("Fetching data..."):
                    success, result = fetch_json_from_url(api_url)
                    
                    if not success:
                        st.error(result)
                    else:
                        st.success("Successfully fetched and parsed JSON!")
                        process_valid_json(result)
    
    with tab2:
        example_json = '''{
  "name": "John Doe",
  "age": 30,
  "isEmployed": true,
  "address": {
    "street": "123 Main St",
    "city": "Anytown",
    "zipCode": "12345"
  },
  "phoneNumbers": [
    {
      "type": "home",
      "number": "555-1234"
    },
    {
      "type": "work",
      "number": "555-5678"
    }
  ]
}'''
        
        json_input = st.text_area("Paste JSON data:", height=300, 
                                placeholder=example_json)
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            validate_button = st.button("Validate", key="validate_button", use_container_width=True)
            
        with col2:
            clear_button = st.button("Clear", key="clear_button", use_container_width=True)
            if clear_button:
                st.session_state["json_input"] = ""
                st.experimental_rerun()
                
        with col3:
            load_example = st.button("Load Example", key="load_example", use_container_width=True)
            if load_example:
                # Store the example in session state so it persists
                st.session_state["json_input"] = example_json
                st.experimental_rerun()
        
        if validate_button:
            if not json_input:
                st.warning("Please paste some JSON data")
            else:
                success, result = validate_json_string(json_input)
                
                if not success:
                    st.error(result)
                else:
                    st.success("Valid JSON!")
                    process_valid_json(result)

def process_valid_json(data):
    """Process valid JSON data and display results"""
    # Display a preview of the JSON
    with st.expander("JSON Preview", expanded=True):
        st.json(data)
    
    # Analyze the structure
    analysis = analyze_json_structure(data)
    
    # Display the analysis in a more attractive format
    st.subheader("JSON Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Structure Summary")
        metrics_col1, metrics_col2 = st.columns(2)
        
        with metrics_col1:
            st.metric(label="Root Type", value=analysis['root_type'])
            st.metric(label="Top-level Items", value=analysis['top_level_count'])
        
        with metrics_col2:
            st.metric(label="Nesting Depth", value=analysis['nesting_depth'])
            st.metric(label="Total Items", value=analysis['total_items'])
    
    with col2:
        st.markdown("### Top-level Keys and Types")
        
        if analysis['top_level_keys']:
            keys_table = []
            for key, type_name in analysis['top_level_keys'].items():
                keys_table.append({"Key": key, "Type": type_name})
            
            st.table(keys_table)
        else:
            st.info("No keys found (empty structure)")
    
    # Add download button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(get_download_link(data), unsafe_allow_html=True)

if __name__ == "__main__":
    main() 