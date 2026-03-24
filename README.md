<p align="center">
  <img src="assets/banner.png" alt="Artisan Pizza AI Banner" width="100%">
</p>

<h1 align="center">Artisan Pizza AI</h1>

<p align="center">
  <b>The Future of Taste: Traditional Wood-Fired Excellence meets Artificial Intelligence</b>
</p>

<p align="center">
  <a href="https://shakiran-nannyombi.github.io/Pizza-CustomerService-Agent/">Live Frontend</a> •
  <a href="https://pizza-customerservice-agent.streamlit.app/">Live AI Dashboard</a> •
  <a href="#project-structure">Architecture</a> •
  <a href="#local-setup">Setup Guide</a>
</p>

---

Artisan Pizza AI is a premium, AI-driven platform designed to revolutionize the way you experience pizza. From our wood-fired kitchens in Kampala to our deep-learning taste recommendations, we engineer every bite for perfection.

## Project Structure
- **frontend/**: High-performance multi-page application
  - **css/**: Centralized professional branding
  - **js/**: Persistent cart and AI assistant logic
  - **assets/**: Custom SVG branding and media
- **streamlit/**: Modular dev tools and documentation dashboard
- **api/**: FastAPI backend powering the order management system
- **pizza_agent/**: Core LLaMA 3.1-powered intelligence and tools

## Key Features
- **AI Taste Assistant**: Personalized recommendations using advanced NLP.
- **Universal Persistence**: Conversations and carts stay with you across all pages.
- **Localized Experience**: Now serving Ugandan communities in Kampala, Entebbe, and Jinja.
- **Premium Interface**: Minimalist design with Lucide integration and custom notifications.

## Local Setup
1. **Clone and Install**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Configure**: Create a `.env` file with your `GROQ_API_KEY`.
3. **Launch**:
   ```bash
   python launch.py
   ```
   - Frontend: http://localhost:3000
   - API: http://localhost:8000
   - Streamlit Dashboard: http://localhost:8501

## Deployment Guide

### GitHub Pages (Frontend)
The project includes a GitHub Action for automated deployment.
1. Push to the `main` branch.
2. **CRITICAL**: In Repository Settings → Pages:
   - Under "Build and deployment" > **Source**, select **"GitHub Actions"**.
   - (Success depends on this being set to Actions, not "Deploy from a branch").

### Troubleshooting Deployment
If you see a `Get Pages site failed` error in GitHub Actions:
- Ensure **GitHub Actions** is selected as the source in **Settings > Pages**.
- Ensure the repository is **Public** (or you have a GitHub Pro/Team account for private Pages).
- Trigger a new push to `frontend/` to re-run the workflow.

### Streamlit Cloud (Dashboard)
1. Link your repo to Streamlit Cloud.
2. Set Main file path to `streamlit/app.py`.
3. Add your `GROQ_API_KEY` to the Secrets.

---

<p align="center">
  Built with precision in Uganda by Artisan AI Lab
</p>
