import streamlit as st
from research_agent import research_agent, ecommerce_agent
from notetaker import save_note

st.set_page_config(page_title="Unified AI Research & Business Assistant", layout="wide")

st.title("Unified AI Research & Business Assistant")

tab1, tab2 = st.tabs(["🔍 Research", "🛒 Shopify Analyzer"])

with tab1:
    st.subheader("Research Agent")
    query = st.text_input("Enter your research query", "Generative AI in healthcare")
    if st.button("Run Research"):
        with st.spinner("Running research..."):
            result = research_agent(query)

            st.markdown("### 📑 Summary")
            st.write(result["summary"])

            st.markdown("### 🔗 Sources")
            st.json(result["sources"])

            path = save_note(f"Research_{query}", result, {})
            st.success(f"✅ Saved to {path}")

with tab2:
    st.subheader("Shopify Analyzer")
    col1, col2 = st.columns([2, 1])
    with col1:
        public_store_url = st.text_input("Public Shopify store URL (for product scraping)", "")
    with col2:
        limit = st.number_input("Items limit", min_value=1, max_value=50, value=10, step=1)

    c1, c2 = st.columns(2)

    # Public store mode
    with c1:
        if st.button("Analyze Public Store"):
            if not public_store_url.strip():
                st.error("⚠️ Please enter a public Shopify store URL")
            else:
                with st.spinner("Fetching public products..."):
                    data = ecommerce_agent(store_url=public_store_url.strip(), limit=limit, public_mode=True)
                    st.json(data)
                    path = save_note("Public Store Report",
                                     {"summary": f"Public scrape for {public_store_url}"},
                                     data)
                    st.success(f"✅ Saved to {path}")

    # Private store mode
    with c2:
        if st.button("Fetch My Private Store Data"):
            with st.spinner("Fetching private store data..."):
                data = ecommerce_agent(store_url=None, limit=limit, public_mode=False)
                st.json(data)
                path = save_note("Private Shopify Report",
                                 {"summary": "Private Shopify stats"},
                                 data)
                st.success(f"✅ Saved to {path}")
