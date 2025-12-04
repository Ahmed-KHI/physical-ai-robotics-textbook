# Physical AI & Humanoid Robotics Textbook 🤖

An AI-native interactive textbook for learning Physical AI and Humanoid Robotics, built with Docusaurus and featuring an intelligent RAG-powered chatbot.

## 🎯 Hackathon Project Features

This project includes **ALL bonus features** for maximum points (300/300):

### ✅ Core Requirements (100 points)
- [x] **Book Creation**: Comprehensive textbook using Docusaurus
- [x] **RAG Chatbot**: OpenAI GPT-3.5-turbo + Qdrant vector database
- [x] **Text Selection Query**: Ask questions about selected text
- [x] **Deployed to GitHub Pages**
- [x] **💰 Cost-Optimized**: Uses GPT-3.5-turbo (20x cheaper than GPT-4)

### ⭐ Bonus Features (+200 points)
- [x] **+50 pts**: Claude Code Subagents & Agent Skills
- [x] **+50 pts**: Better-Auth authentication with user profiling
- [x] **+50 pts**: Content personalization based on user level (GPT-3.5)
- [x] **+50 pts**: Urdu translation feature (GPT-3.5)

## 🚀 Quick Start

**⚡ Fast Setup**: See [SETUP.md](./SETUP.md) for detailed step-by-step guide.

### 1. Install Dependencies

```bash
# Frontend
npm install

# Backend
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment Variables

```bash
cd backend
cp .env.example .env
# Edit .env with your API keys:
# - OPENAI_API_KEY (required)
# - QDRANT_URL (required)
# - QDRANT_API_KEY (required)
# - DATABASE_URL (required)
```

**Get API Keys:**
- OpenAI: https://platform.openai.com/api-keys
- Qdrant Cloud: https://cloud.qdrant.io/ (free tier)
- Neon Postgres: https://neon.tech/ (free tier)

### 3. Index Book Content

```bash
cd backend
python index_content.py
```

This indexes all textbook content to Qdrant for the RAG chatbot.

### 4. Start Servers

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
npm start

# Initialize database & start server
python database.py
python main.py
```

API available at `http://localhost:8000`

## 🗝️ Required API Keys

1. **OpenAI**: https://platform.openai.com/ ($5 free credit)
2. **Qdrant Cloud**: https://cloud.qdrant.io/ (Free 1GB tier)
3. **Neon Postgres**: https://neon.tech/ (Free tier)

## 💡 Key Features

- 💬 **AI Chatbot**: Context-aware RAG chatbot on every page
- 🎯 **Personalization**: Content adapts to user skill level
- 🌐 **Translation**: One-click Urdu translation
- 📱 **Responsive**: Works on all devices
- 🚀 **Fast**: Static site generation for performance

## 📚 Course Structure

- **Module 1**: ROS 2 Fundamentals (Weeks 1-5)
- **Module 2**: Gazebo & Unity Simulation (Weeks 6-7)
- **Module 3**: NVIDIA Isaac Platform (Weeks 8-10)
- **Module 4**: Vision-Language-Action (Weeks 11-13)

## 🚀 Deployment

```bash
# Build for production
npm run build

# Deploy to GitHub Pages
npm run deploy
```

## 📝 Tech Stack

**Frontend**: Docusaurus, React, TypeScript  
**Backend**: FastAPI, OpenAI, Qdrant, Neon Postgres, LangChain  
**Auth**: Better-Auth  

## 📹 Demo Video

90-second demo showcasing all features (required for submission)

## 🏆 Hackathon Submission

✅ Public GitHub repo  
✅ Deployed to GitHub Pages  
✅ Demo video created  
✅ All features implemented  

---

**Author**: Mirza Muhammad Ahmed  
**GIAIC ID**: 00263838  
**GitHub**: [@Ahmed-KHI](https://github.com/Ahmed-KHI)  

Built with ❤️ for GIAIC AI Hackathon | December 2025
