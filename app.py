import streamlit as st
import asyncio
from coordinator import ResearchCoordinator
import time

# Page configuration
st.set_page_config(
    page_title="Deep Research Agent",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        color: #1f77b4;
    }
    .status-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .result-box {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        margin: 0.5rem 0;
    }
    .query-box {
        background-color: #e8f4fd;
        padding: 0.8rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border: 1px solid #b3d9ff;
        color: #1a1a1a;
        font-weight: 500;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .query-box:hover {
        background-color: #d1e7ff;
        border-color: #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🔍 Deep Research Agent</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("Settings")
        st.markdown("---")
        
        # Add any configuration options here
        st.subheader("About")
        st.markdown("""
        This AI-powered research agent will:
        1. Analyze your query
        2. Generate search queries
        3. Search the web
        4. Analyze results
        5. Synthesize findings
        6. Determine if more research is needed
        """)
    
    # Main content area
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Query input
        st.subheader("Enter Your Research Query")
        query = st.text_area(
            "What would you like to research?",
            height=100,
            placeholder="Enter a detailed research question or topic..."
        )
        
        # Research button
        if st.button("🚀 Start Research", type="primary", use_container_width=True):
            if query.strip():
                run_research(query)
            else:
                st.error("Please enter a research query.")

def run_research(query: str):
    """Run the research process with Streamlit UI updates"""
    
    # Initialize session state for tracking progress
    if 'research_progress' not in st.session_state:
        st.session_state.research_progress = {
            'current_step': '',
            'search_results': [],
            'queries': [],
            'iteration': 1,
            'final_report': None
        }
    
    # Create progress container
    progress_container = st.container()
    results_container = st.container()
    
    with progress_container:
        st.subheader("Research Progress")
        progress_bar = st.progress(0)
        status_text = st.empty()
        
    with results_container:
        # Create tabs for different sections
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Query Analysis", "🔍 Search Results", "📊 Follow-up Decisions", "📄 Final Report"])
        
        with tab1:
            query_analysis_placeholder = st.empty()
            
        with tab2:
            search_results_placeholder = st.empty()
            
        with tab3:
            followup_placeholder = st.empty()
            
        with tab4:
            final_report_placeholder = st.empty()
    
    # Run the async research process
    asyncio.run(research_process(
        query, 
        progress_bar, 
        status_text, 
        query_analysis_placeholder,
        search_results_placeholder,
        followup_placeholder,
        final_report_placeholder
    ))

async def research_process(query, progress_bar, status_text, query_analysis_placeholder, 
                          search_results_placeholder, followup_placeholder, final_report_placeholder):
    """Main research process with Streamlit UI updates"""
    
    try:
        # Initialize coordinator
        coordinator = ResearchCoordinator(query)
        
        # Step 1: Generate queries
        status_text.text("Analyzing query and generating search queries...")
        progress_bar.progress(10)
        
        query_response = await coordinator.generate_queries()
        
        # Update query analysis tab
        with query_analysis_placeholder.container():
            st.markdown("### Query Analysis")
            st.markdown(f"**Thoughts:** {query_response.thoughts}")
            st.markdown("**Generated Search Queries:**")
            for i, query in enumerate(query_response.queries, 1):
                st.markdown(f"<div class='query-box'>{i}. {query}</div>", unsafe_allow_html=True)
        
        progress_bar.progress(20)
        
        # Step 2: Perform initial research
        status_text.text("Performing initial research...")
        await coordinator.perform_research_for_queries(queries=query_response.queries)
        
        # Update search results tab
        with search_results_placeholder.container():
            st.markdown("### Search Results")
            for i, result in enumerate(coordinator.search_results, 1):
                with st.expander(f"{i}. {result.title}"):
                    st.markdown(f"**URL:** {result.url}")
                    st.markdown(f"**Summary:** {result.summary}")
        
        progress_bar.progress(60)
        
        # Step 3: Follow-up research loop
        iteration = 1
        while iteration < 3:
            status_text.text(f"Evaluating if more research is needed (iteration {iteration})...")
            
            decision_response = await coordinator.generate_followup()
            
            # Update follow-up decisions tab
            with followup_placeholder.container():
                st.markdown("### Follow-up Decisions")
                st.markdown(f"**Decision:** {'More research needed' if decision_response.should_follow_up else 'Research complete'}")
                st.markdown(f"**Reasoning:** {decision_response.reasoning}")
                
                if decision_response.should_follow_up:
                    st.markdown("**Follow-up Queries:**")
                    for i, query in enumerate(decision_response.queries, 1):
                        st.markdown(f"<div class='query-box'>{i}. {query}</div>", unsafe_allow_html=True)
            
            if not decision_response.should_follow_up:
                break
                
            iteration += 1
            status_text.text(f"Conducting follow-up research (iteration {iteration})...")
            await coordinator.perform_research_for_queries(queries=decision_response.queries)
            
            # Update search results with new findings
            with search_results_placeholder.container():
                st.markdown("### Search Results")
                for i, result in enumerate(coordinator.search_results, 1):
                    with st.expander(f"{i}. {result.title}"):
                        st.markdown(f"**URL:** {result.url}")
                        st.markdown(f"**Summary:** {result.summary}")
        
        progress_bar.progress(80)
        
        # Step 4: Generate final report
        status_text.text("Synthesizing research findings...")
        final_report = await coordinator.synthesis_report()
        
        progress_bar.progress(100)
        status_text.text("Research complete! ✅")
        
        # Update final report tab
        with final_report_placeholder.container():
            st.markdown("### Final Research Report")
            st.markdown(final_report)
            
            # Add download button for the report
            st.download_button(
                label="📥 Download Report",
                data=final_report,
                file_name=f"research_report_{int(time.time())}.md",
                mime="text/markdown"
            )
        
        # Success message
        st.success("🎉 Research completed successfully! Check the tabs above for detailed results.")
        
    except Exception as e:
        st.error(f"An error occurred during research: {str(e)}")
        st.exception(e)

if __name__ == "__main__":
    main()
