import streamlit as st
import pandas as pd
import openai
import os

# Set your OpenAI API key here
openai.api_key = os.getenv("OPENAI_API_KEY")

# Streamlit UI
st.title("AI-Powered Storage Management")

# Upload CSV file
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    # Read CSV file
    df = pd.read_csv(uploaded_file)
    st.write("Original Data:")
    st.dataframe(df)
    
    # Ask AI to optimize storage
    prompt = f"""Analyze this storage data and suggest ways to optimize it:
    {df.to_string()}
    """
    
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=500
    )
    
    st.write("AI Suggestions:")
    st.write(response.choices[0].text)
else:
    st.info("Please upload a CSV file to get started.")