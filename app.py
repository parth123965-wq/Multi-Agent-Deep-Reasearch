import streamlit as st
from pipline import run_deep_research_tool

st.set_page_config(
    page_title="Deep Research AI",
    page_icon="🔎",
    layout="wide"
)

st.title("🔎 Multi-Agent Deep Research System")
st.markdown(
    """
    Enter a research topic and let the AI agents:
    - Search the web
    - Scrape relevant content
    - Generate a research report
    - Critically review the report
    """
)

topic = st.text_input(
    "Enter Research Topic",
    placeholder="e.g. Future of AI Agents in Software Engineering"
)

if st.button("Start Research"):
    
    if not topic.strip():
        st.warning("Please enter a research topic.")
    
    else:
        with st.spinner("Running Deep Research Pipeline..."):
            
            try:
                result = run_deep_research_tool(topic)

                st.success("Research Completed Successfully!")

                # Search Results
                with st.expander("🔍 Search Results", expanded=False):
                    st.write(result.get("search_result", "No search result found."))

                # Scraper Results
                with st.expander("🌐 Scraper Results", expanded=False):
                    st.write(result.get("scraper_result", "No scraper result found."))

                # Final Report
                st.subheader("📝 Research Report")
                st.markdown(result.get("report", "No report generated."))

                # Critic Feedback
                st.subheader("📊 Critic Review")
                st.markdown(result.get("feedback", "No feedback generated."))

            except Exception as e:
                st.error(f"Error: {str(e)}")