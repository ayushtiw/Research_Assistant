import streamlit as st
import requests
from datetime import datetime
import json
from typing import List, Dict, Any
import pandas as pd

class ResearchAssistantUI:
    def __init__(self):
        self.api_url = "http://localhost:8000"  # Base URL for FastAPI backend
        self.setup_session_state()
        self.setup_ui()

    def setup_session_state(self):
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        if 'current_papers' not in st.session_state:
            st.session_state.current_papers = []
        if 'current_topic' not in st.session_state:
            st.session_state.current_topic = ""

    def setup_ui(self):
        st.title("Academic Research Assistant")
        
        # Sidebar for topic search
        with st.sidebar:
            st.header("Search Papers")
            topic = st.text_input("Enter Research Topic")
            col1, col2 = st.columns(2)
            with col1:
                start_year = st.number_input("Start Year", 
                                           min_value=1900, 
                                           max_value=datetime.now().year,
                                           value=datetime.now().year - 5)
            with col2:
                end_year = st.number_input("End Year", 
                                         min_value=1900, 
                                         max_value=datetime.now().year,
                                         value=datetime.now().year)
            
            if st.button("Search"):
                self.search_papers(topic, start_year, end_year)

        # Main area with tabs
        tab1, tab2, tab3 = st.tabs(["Papers Timeline", "Chat Interface", "Review Generator"])
        
        with tab1:
            self.render_papers_timeline()
        
        with tab2:
            self.render_chat_interface()
        
        with tab3:
            self.render_review_generator()

    def search_papers(self, topic: str, start_year: int, end_year: int):
        try:
            response = requests.post(
                f"{self.api_url}/search_papers",
                json={"topic": topic, "start_year": start_year, "end_year": end_year}
            )
            if response.status_code == 200:
                st.session_state.current_papers = response.json()["papers"]
                st.session_state.current_topic = topic
                st.success(f"Found {len(st.session_state.current_papers)} papers")
            else:
                st.error("Failed to fetch papers")
        except Exception as e:
            st.error(f"Error: {str(e)}")

    def render_papers_timeline(self):
        if not st.session_state.current_papers:
            st.info("Search for a topic to see papers timeline")
            return

        # Convert papers to DataFrame for better visualization
        df = pd.DataFrame(st.session_state.current_papers)
        df['published_date'] = pd.to_datetime(df['published_date'])
        df = df.sort_values('published_date')

        # Create timeline visualization
        st.header("Papers Timeline")
        fig = self.create_timeline_chart(df)
        st.plotly_chart(fig)

        # Display papers in a table
        st.header("Papers List")
        for paper in st.session_state.current_papers:
            with st.expander(f"{paper['title']} ({paper['published_date'][:10]})"):
                st.write(f"**Authors:** {', '.join(paper['authors'])}")
                st.write(f"**Abstract:** {paper['abstract']}")
                st.write(f"**URL:** {paper['url']}")

    def render_chat_interface(self):
        st.header("Chat Interface")
        
        # Display chat history
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f"**User:** {msg['content']}")
            elif msg["role"] == "assistant":
                st.markdown(f"**Assistant:** {msg['content']}")

        # Chat input and button
        prompt = st.text_input("Ask a question about the papers...", key="chat_input")
        if st.button("Send"):
            if not st.session_state.current_papers:
                st.error("Please search for papers first")
                return

            # Add user message to chat
            if prompt:
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                
                # Get response from API
                try:
                    response = requests.post(
                        f"{self.api_url}/ask_question",
                        json={
                            "text": prompt,
                            "papers": [p["title"] for p in st.session_state.current_papers]
                        }
                    )
                    if response.status_code == 200:
                        answer = response.json()["answer"]
                        st.session_state.chat_history.append({"role": "assistant", "content": answer})
                    else:
                        st.error("Failed to get response")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

    def render_review_generator(self):
        st.header("Review Generator")
        
        if not st.session_state.current_topic:
            st.info("Search for a topic first to generate a review")
            return

        if st.button("Generate Review"):
            try:
                response = requests.post(
                    f"{self.api_url}/generate_review",
                    json={"topic": st.session_state.current_topic}
                )
                if response.status_code == 200:
                    review = response.json()["review"]
                    st.markdown(review)
                else:
                    st.error("Failed to generate review")
            except Exception as e:
                st.error(f"Error: {str(e)}")

    @staticmethod
    def create_timeline_chart(df: pd.DataFrame):
        import plotly.express as px
        
        fig = px.scatter(df, 
                        x='published_date', 
                        y=[1] * len(df),
                        hover_data=['title', 'authors'],
                        title='Papers Timeline')
        
        fig.update_traces(marker=dict(size=10))
        fig.update_layout(yaxis_visible=False)
        
        return fig

if __name__ == "__main__":
    app = ResearchAssistantUI()
