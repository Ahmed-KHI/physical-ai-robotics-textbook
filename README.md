# Physical AI & Humanoid Robotics Textbook 🤖

An AI-native interactive textbook for learning Physical AI and Humanoid Robotics, built with Docusaurus and featuring an intelligent RAG-powered chatbot.

## 🌐 Live Demo

**🔗 Live Site**: https://physical-ai-robotics-textbook.vercel.app  
**🔐 Demo Account**: `teacher@giaic.com` / `teacher123`  
**🎥 Demo Video**: [Coming Soon]

## 🎯 Hackathon Project Features

This project includes **ALL bonus features** for maximum points (300/300):

### ✅ Core Requirements (100 points)
- [x] **Book Creation**: Comprehensive 13-week textbook using Docusaurus
- [x] **RAG Chatbot**: OpenAI GPT-3.5-turbo + Qdrant vector database + LangChain
- [x] **Text Selection Query**: Ask questions about selected text
- [x] **Live Deployment**: Frontend on Vercel, Backend on Render
- [x] **💰 Cost-Optimized**: Uses GPT-3.5-turbo (20x cheaper than GPT-4)

### ⭐ Bonus Features (+200 points)
- [x] **+50 pts**: User Authentication - Better-Auth with email/password, user profiling (experience level, robotics background, hardware access)
- [x] **+50 pts**: Adaptive Learning - AI-powered content personalization based on user's skill level and background
- [x] **+50 pts**: Urdu Translation - One-click translation of any page content to Urdu using OpenAI
- [x] **+50 pts**: Mobile Responsive - Fully responsive design optimized for mobile, tablet, and desktop

## 🏗️ Architecture

```
Frontend (Vercel)         Backend (Render)           AI Services
─────────────────         ────────────────           ────────────
Docusaurus/React    →     FastAPI + LangChain   →   OpenAI GPT-3.5
Better-Auth Client  →     Better-Auth Server    →   Qdrant Cloud
Static Site Gen     →     REST API Endpoints    →   Neon Postgres
```

## 🚀 Quick Start (Local Development)

**⚡ Fast Setup**: See [SETUP.md](./SETUP.md) for detailed step-by-step guide.

### 1. Clone Repository

```bash
git clone https://github.com/Ahmed-KHI/physical-ai-robotics-textbook.git
cd physical-ai-robotics-textbook
```

### 2. Install Dependencies

```bash
# Frontend
npm install

# Backend
cd backend
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create `backend/.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
QDRANT_URL=your_qdrant_cloud_url
QDRANT_API_KEY=your_qdrant_api_key
DATABASE_URL=your_neon_postgres_url
JWT_SECRET_KEY=your_random_secret_key
```

**Get API Keys:**
- OpenAI: https://platform.openai.com/api-keys
- Qdrant Cloud: https://cloud.qdrant.io/ (free tier)
- Neon Postgres: https://neon.tech/ (free tier)

### 4. Index Book Content

```bash
cd backend
python index_content.py
```

### 5. Start Development Servers

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
npm start
```

Visit `http://localhost:3000`

## 💡 Key Features

### 🤖 RAG-Powered Chatbot
- **Contextual Understanding**: Answers questions based on entire textbook content
- **Text Selection Query**: Select any text and ask specific questions about it
- **Conversation Memory**: Maintains context across multiple questions
- **Source Citations**: References specific modules and topics

### 👤 User Authentication & Profiling
- **Better-Auth Integration**: Secure email/password authentication
- **User Profiles**: Track programming experience, robotics background, hardware access
- **Personalized Dashboard**: Custom learning path for each user

### 🎯 Adaptive Learning
- **AI-Powered Personalization**: Content difficulty adapts to user's skill level
- **Smart Recommendations**: Suggests relevant topics based on background
- **Progress Tracking**: Monitors learning journey

### 🌐 Urdu Translation
- **One-Click Translation**: Translate any page to Urdu instantly
- **Context-Aware**: Maintains technical accuracy in translations
- **Toggle Feature**: Switch between English and Urdu seamlessly

### 📱 Mobile Responsive
- **Optimized UI**: Perfect display on all screen sizes
- **Touch-Friendly**: Mobile-optimized controls and navigation
- **Progressive Web App**: Fast loading on all devices

## 📚 Course Structure

- **Module 1**: ROS 2 Fundamentals (Weeks 1-5)
- **Module 2**: Gazebo & Unity Simulation (Weeks 6-7)
- **Module 3**: NVIDIA Isaac Platform (Weeks 8-10)
- **Module 4**: Vision-Language-Action (Weeks 11-13)

## 🚀 Deployment

### Production URLs
- **Frontend**: https://physical-ai-robotics-textbook.vercel.app (Vercel)
- **Backend API**: https://physical-ai-robotics-textbook.onrender.com (Render)

### Deploy Your Own

**Frontend (Vercel):**
1. Fork this repository
2. Connect to Vercel
3. Deploy automatically from main branch

**Backend (Render):**
1. Create new Web Service on Render
2. Connect your GitHub repository
3. Set environment variables
4. Deploy from `backend/` directory

## 📝 Tech Stack

### Frontend
- **Framework**: Docusaurus 3.9.2
- **UI**: React 19.0.0, TypeScript 5.6.2
- **Styling**: CSS Modules, Custom CSS
- **Auth**: Better-Auth 1.4.5
- **Deployment**: Vercel

### Backend
- **Framework**: FastAPI 0.115.6
- **AI/ML**: OpenAI GPT-3.5-turbo, LangChain 0.3.14
- **Vector DB**: Qdrant Cloud (1.12.1)
- **Database**: Neon Serverless Postgres
- **Auth**: Better-Auth, JWT
- **Deployment**: Render

### DevOps
- **Version Control**: Git + GitHub
- **CI/CD**: Automatic deployment via Vercel & Render
- **Monitoring**: Built-in platform monitoring

## 📹 Demo Video

🎥 **Coming Soon**: 90-second walkthrough of all features

**Demo Contents:**
1. Homepage & Navigation (10s)
2. RAG Chatbot with text selection (20s)
3. User Authentication (15s)
4. Adaptive Learning personalization (20s)
5. Urdu translation (15s)
6. Mobile responsive design (10s)

## 🏆 Hackathon Submission Checklist

- [x] ✅ Public GitHub repository
- [x] ✅ Live deployment (Vercel + Render)
- [x] ✅ Comprehensive README
- [x] ✅ All core features implemented
- [x] ✅ All bonus features implemented
- [ ] 🎥 Demo video (in progress)
- [ ] 📝 Submission form completed

**Total Points**: 300/300 (Core: 100 + Bonus: 200)  

## 📄 License

This project is created for educational purposes as part of GIAIC Hackathon.

## 🤝 Contributing

This is a hackathon submission project. For suggestions or improvements, please open an issue.

## 📧 Contact

**Author**: Mirza Muhammad Ahmed  
**GIAIC ID**: 00263838  
**GitHub**: [@Ahmed-KHI](https://github.com/Ahmed-KHI)  
**Project**: [physical-ai-robotics-textbook](https://github.com/Ahmed-KHI/physical-ai-robotics-textbook)

---

<div align="center">

**🏆 Built for GIAIC AI Hackathon | December 2025**

[Live Demo](https://physical-ai-robotics-textbook.vercel.app) • [Documentation](./SETUP.md) • [Report Issue](https://github.com/Ahmed-KHI/physical-ai-robotics-textbook/issues)

Made with ❤️ by Mirza Muhammad Ahmed

</div>
