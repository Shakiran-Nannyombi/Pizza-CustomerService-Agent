# Artisan Pizza AI - Customer Service Agent

A premium, AI-powered customer service platform for a modern pizzeria. Featuring a high-performance static frontend and a modular Streamlit documentation/tool dashboard.

## 🚀 Live Demo
- **Frontend**: [Your GitHub Pages URL] (e.g., https://username.github.io/Pizza-CustomerService-Agent/)
- **Streamlit Dashboard**: [Your Streamlit Cloud URL]

## 🏗️ Project Structure
- **/frontend**: Modern multi-page application (HTML/Tailwind/JS)
  - `/css`: Centralized stylesheets
  - `/js`: Interactive cart and chatbot logic
  - `/assets`: Custom SVG logo and media
- **/streamlit**: Original modular application for documentation and dev tools
- **/api**: FastAPI backend serving the AI Agent and order management
- **/pizza_agent**: Core logic for the AI assistant and tools
- **/docs**: Technical documentation (Architecture, API, UI)

## 📦 Local Setup
1. **Clone & Install**:
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
   - Streamlit: http://localhost:8501

## 🌐 Deployment Instructions

### GitHub Pages (Frontend)
The project is pre-configured with a GitHub Action. To deploy:
1. Push your changes to the `main` branch.
2. In your GitHub Repo: **Settings → Pages**.
3. Set **Build and deployment → Source** to "GitHub Actions".
4. The site will automatically deploy from the `/frontend` directory.

### Streamlit Cloud
1. Connect your repository to [Streamlit Cloud](https://share.streamlit.io/).
2. Select your repository and the `main` branch.
3. Set **Main file path** to `streamlit/app.py`.
4. Add your `GROQ_API_KEY` to the **Secrets** section.

## 🛠️ Features
- **AI Agent**: LLaMA 3.1-powered assistant with 8 specialized tools.
- **Cart System**: Persistent local storage cart across all pages.
- **Interactive Chat**: Persistent history and specialized intents (Order, Call, Info).
- **Responsive Design**: Mobile-first, premium aesthetics with Lucide icons.
