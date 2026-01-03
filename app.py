import streamlit as st
from article_generator import ArticleGenerator
from config import config

st.set_page_config(page_title="AI Article Generator", layout="wide")

st.title("📝 AI Article Generator")
st.write("Powered by DeepSeek-R1 + Ollama")

# Initialize generator only once
@st.cache_resource
def load_generator():
    return ArticleGenerator()

generator = load_generator()

# Sidebar controls
st.sidebar.header("Article Settings")

topic = st.sidebar.text_input("Topic")
tone = st.sidebar.selectbox(
    "Tone",
    ["professional", "conversational", "persuasive", "educational", "entertaining"]
)

length = st.sidebar.slider("Target length (words)", 300, 2000, 800, step=100)
keywords = st.sidebar.text_input("Keywords (comma separated)")
style = st.sidebar.selectbox(
    "Style",
    ["informative", "persuasive", "narrative", "descriptive"]
)

# Main area
if st.button("Generate Article"):
    if not topic:
        st.error("Please enter a topic.")
    else:
        with st.spinner("Generating article..."):
            article = generator.create_article_from_scratch(
                topic=topic,
                tone=tone,
                length=length,
                keywords=keywords,
                style=style
            )

        st.subheader("Generated Article")
        st.write(article)

        st.download_button(
            "Download as TXT",
            article,
            file_name="article.txt",
            mime="text/plain"
        )
