import os
# Fix chromadb Pydantic "chroma_server_nofile" error before any imports
os.environ.setdefault("CHROMA_SERVER_NOFILE", "")
os.environ.setdefault("IS_PERSISTENT", "0")

import streamlit as st
import time
import re
from dotenv import load_dotenv

# Load environment variables from .env file if it exists (local dev)
load_dotenv()

# Also check Streamlit Cloud secrets
if "XAI_API_KEY" not in os.environ:
    try:
        if "XAI_API_KEY" in st.secrets:
            os.environ["XAI_API_KEY"] = st.secrets["XAI_API_KEY"]
    except Exception:
        pass

st.set_page_config(page_title="Content Marketing Pipeline", page_icon="✍️", layout="wide")

def parse_output(text):
    """
    Parses the final crew output to extract the blog post and social media posts.
    """
    blog_post = text
    linkedin_post = ""
    twitter_post = ""
    instagram_post = ""

    # Using regex to split. It handles case insensitivity and optional whitespace
    linkedin_match = re.search(r"##\s*LINKEDIN\s*POST", text, re.IGNORECASE)
    twitter_match = re.search(r"##\s*TWITTER\s*THREAD", text, re.IGNORECASE)
    instagram_match = re.search(r"##\s*INSTAGRAM\s*CAPTION", text, re.IGNORECASE)

    if linkedin_match:
        blog_post = text[:linkedin_match.start()].strip()
        
        if twitter_match:
            linkedin_post = text[linkedin_match.end():twitter_match.start()].strip()
            
            if instagram_match:
                twitter_post = text[twitter_match.end():instagram_match.start()].strip()
                instagram_post = text[instagram_match.end():].strip()
            else:
                twitter_post = text[twitter_match.end():].strip()
        else:
            linkedin_post = text[linkedin_match.end():].strip()
    else:
        # Fallback if the model didn't use the exact headers
        pass

    return blog_post, linkedin_post, twitter_post, instagram_post

# ─── Sidebar ───
st.sidebar.title("✍️ Content Pipeline")
st.sidebar.markdown("AI-powered multi-agent content generation using **CrewAI** and **xAI Grok**.")

st.sidebar.markdown("---")
st.sidebar.subheader("🤖 Agents in the Crew")
st.sidebar.info(
    "1. **Trend Researcher** — Finds compelling angles & target audience.\n"
    "2. **SEO Analyst** — Identifies high-value keywords & metadata.\n"
    "3. **Blog Writer** — Writes an engaging, SEO-optimized post.\n"
    "4. **Social Repurposer** — Adapts the post for LinkedIn, Twitter/X, and Instagram."
)

st.sidebar.markdown("---")
st.sidebar.caption("Built with [CrewAI](https://crewai.com) • Powered by [xAI Grok](https://x.ai)")

# ─── Main Area ───
st.title("✍️ Content Marketing Pipeline")
st.markdown("Enter a topic below to generate a full blog post and tailored social media content automatically.")

topic = st.text_input("Enter your content topic", placeholder="e.g. The future of AI in education")

if st.button("Generate Content", type="primary"):
    # Check for the API key from .env or Streamlit secrets
    api_key = os.environ.get("XAI_API_KEY")
    
    if not api_key:
        st.error("⚠️ Please set XAI_API_KEY in your .env file or Streamlit secrets.")
        st.stop()

    if not topic:
        st.error("Please enter a topic.")
        st.stop()

    with st.spinner("🚀 Running your content crew... this may take 1-2 mins"):
        start_time = time.time()
        
        try:
            from crew import build_crew
            
            crew_instance = build_crew()
            result = crew_instance.kickoff(inputs={"topic": topic})
            end_time = time.time()
            
            st.success(f"✅ Content generated successfully! (Took {end_time - start_time:.1f} seconds)")
            
            # Fetch the raw output from the 3rd task (index 2) which is the blog writer task
            blog_content = crew_instance.tasks[2].output.raw
            
            # Combine them so parse_output works exactly as expected
            final_text = blog_content + "\n\n" + str(result)
            blog_post, linkedin_post, twitter_post, instagram_post = parse_output(final_text)

            tab1, tab2, tab3, tab4 = st.tabs(["📝 Blog Post", "💼 LinkedIn", "🐦 Twitter Thread", "📸 Instagram"])
            
            with tab1:
                st.markdown(blog_post)
            with tab2:
                st.text_area("LinkedIn Post", linkedin_post, height=300)
            with tab3:
                st.text_area("Twitter Thread", twitter_post, height=300)
            with tab4:
                st.text_area("Instagram Caption", instagram_post, height=300)
            
            st.divider()
            
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    "📥 Download Blog (.md)", 
                    data=blog_post, 
                    file_name=f"{topic.replace(' ', '_')}_blog.md", 
                    mime="text/markdown"
                )
            with col2:
                st.download_button(
                    "📥 Download All (.txt)", 
                    data=final_text, 
                    file_name=f"{topic.replace(' ', '_')}_all_content.txt", 
                    mime="text/plain"
                )
                
        except Exception as e:
            st.error(f"Crew execution failed: {e}")
