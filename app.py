import streamlit as st
import requests

# Set the FastAPI backend URL
API_URL = "http://127.0.0.1:8000/summarize/"

st.title("News Summarizer Chatbot")

# Get user input for news query
query = st.text_input("Enter a news topic:")

if query:
    # Send the query to the FastAPI backend
    response = requests.post(API_URL, json={"query": query})
    summaries = response.json().get("summaries", [])
    
    if summaries:
        st.write("### Summarized News Articles:")
        for idx, summary in enumerate(summaries, 1):
            st.write(f"#### Article {idx}:")
            st.write(summary)
    else:
        st.write("No articles found.")
