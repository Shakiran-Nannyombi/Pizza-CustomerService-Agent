import streamlit as st
from pathlib import Path

def main():
    st.set_page_config(page_title="Restaurant Guide - Pizza AI", page_icon="📖")
    
    # Get the project root
    project_root = Path(__file__).parent.parent.parent
    doc_path = project_root / "docs" / "RESTAURANT-GUIDE.md"
    
    if doc_path.exists():
        with open(doc_path, "r") as f:
            st.markdown(f.read())
    else:
        st.error("Restaurant Guide documentation not found.")

if __name__ == "__main__":
    main()
