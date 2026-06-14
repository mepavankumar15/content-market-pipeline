# Content Marketing Pipeline ✍️

A multi-agent AI app built with **CrewAI** and **Streamlit** that automatically generates a full blog post and social media content (LinkedIn, Twitter/X, Instagram) based on a topic you provide.

Powered by **xAI Grok** via LiteLLM.

---

## Quick Start (Local)

```bash
# Clone the repo
git clone <your-repo-url>
cd content-pipeline

# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate
# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set your API key
cp .env.example .env
# Edit .env and paste your xAI API key

# Run the app
streamlit run main.py
```

---

## Deployment

### Option 1: Streamlit Cloud (Recommended — Free)

1. Push your code to a **GitHub** repository.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in.
3. Click **"New app"** → select your repo, branch, and `main.py`.
4. Go to **Advanced settings** → **Secrets** and add:
   ```toml
   XAI_API_KEY = "xai-your-key-here"
   ```
5. Click **Deploy**. Done!

### Option 2: Docker (Railway / Render / GCP Cloud Run)

```bash
# Build the image
docker build -t content-pipeline .

# Run locally
docker run -p 8501:8501 -e XAI_API_KEY="xai-your-key-here" content-pipeline
```

Then deploy to your platform of choice:

- **Railway**: Connect your GitHub repo → set `XAI_API_KEY` env var → deploy.
- **Render**: New Web Service → Docker → set `XAI_API_KEY` env var → deploy.
- **GCP Cloud Run**: `gcloud run deploy` with the image.

---

## Project Structure

```
content-pipeline/
├── main.py                  # Streamlit UI
├── crew.py                  # CrewAI crew setup (@CrewBase)
├── agents.py                # Agent definitions (4 agents)
├── tasks.py                 # Task definitions (4 tasks)
├── requirements.txt         # Pinned dependencies
├── Dockerfile               # Docker deployment
├── .streamlit/
│   └── config.toml          # Streamlit theme & server config
├── .env.example             # Template for API key
├── .gitignore
└── README.md
```

## How It Works

The pipeline runs 4 AI agents sequentially:

1. **Trend Researcher** — Analyzes the topic, finds 3 compelling angles, identifies the target audience.
2. **SEO Keyword Analyst** — Generates 5 SEO keywords, a blog title, and a meta description.
3. **Blog Writer** — Writes a full 800–1200 word blog post in Markdown.
4. **Social Media Repurposer** — Creates a LinkedIn post, 7-tweet Twitter/X thread, and Instagram caption.

---

## Environment Variables

| Variable       | Required | Description             |
|----------------|----------|-------------------------|
| `XAI_API_KEY`  | ✅       | Your xAI Grok API key   |

You can provide this via `.env`, Streamlit secrets, or the sidebar input.
