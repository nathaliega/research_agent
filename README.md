# Deep Research Agent

An AI-powered research agent that performs comprehensive web research using multiple AI agents to analyze queries, search the web, and synthesize findings.

## Features

- **Query Analysis**: AI analyzes your research question and generates optimized search queries
- **Web Search**: Searches multiple sources using DuckDuckGo
- **Content Analysis**: AI analyzes each search result for relevance and extracts key information
- **Follow-up Research**: Automatically determines if more research is needed and generates follow-up queries
- **Report Synthesis**: Creates comprehensive research reports with findings and sources
- **Web Interface**: Beautiful Streamlit web app with real-time progress tracking


## Usage


### Direct Streamlit command
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## How to Use

1. **Enter Your Query**: Type a detailed research question in the text area
2. **Start Research**: Click the "🚀 Start Research" button
3. **Monitor Progress**: Watch the progress bar and status updates
4. **View Results**: Check the different tabs for:
   - **Query Analysis**: How the AI interpreted your question
   - **Search Results**: All sources found and analyzed
   - **Follow-up Decisions**: Whether more research was needed
   - **Final Report**: Complete synthesized findings
5. **Download Report**: Get your research report as a markdown file

## Architecture

The app uses multiple AI agents working together:

- **Query Agent**: Analyzes research questions and generates search queries
- **Search Agent**: Analyzes web content for relevance and extracts summaries
- **Follow-up Agent**: Decides if more research is needed
- **Synthesis Agent**: Creates comprehensive research reports
