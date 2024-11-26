import streamlit as st
from textblob import TextBlob

# Custom CSS for Styling (Optional)
st.markdown(
    """
    <style>
        .main {
            background-color: #f7fce4;
        }
        div.stButton > button {
            background-color: #a8d5ba;
            color: white;
            border-radius: 8px;
            border: 1px solid #86c5a6;
        }
        div.stButton > button:hover {
            background-color: #86c5a6;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# App Title
st.title("🔍 Sentiment Analysis App")

# Input Text
user_input = st.text_area("Enter text to analyze sentiment:", placeholder="Type something...")

# Perform Sentiment Analysis
if st.button("Analyze"):
    if user_input.strip() == "":
        st.warning("Please enter some text before analyzing.")
    else:
        blob = TextBlob(user_input)
        sentiment_score = blob.sentiment.polarity
        
        # Determine sentiment
        if sentiment_score > 0:
            sentiment = "Positive 😊"
        elif sentiment_score < 0:
            sentiment = "Negative 😔"
        else:
            sentiment = "Neutral 😐"
        
        # Display Results
        st.write(f"### Sentiment: {sentiment}")
        st.write(f"**Sentiment Score:** {sentiment_score:.2f}")
