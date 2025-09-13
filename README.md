# Finance RAG Chatbot 🚀

An AI-powered financial assistant with RAG (Retrieval-Augmented Generation) capabilities, featuring real-time news analysis, stock recommendations, and market insights.

## ✨ Features

- **🤖 AI Chat Interface**: ChatGPT-like interface for financial queries
- **📰 Real-time News**: Latest financial news with sentiment analysis
- **📈 Stock Analysis**: AI-powered stock recommendations and analysis
- **📊 Market Overview**: Real-time market indices and sector performance
- **🎨 Modern UI**: Beautiful ChatGPT-inspired dark theme
- **📱 Responsive Design**: Works on desktop and mobile devices

## 🛠️ Tech Stack

### Backend
- **Python 3.10+**
- **FastAPI** - Modern web framework
- **LangChain** - RAG implementation
- **OpenAI GPT-3.5** - Language model
- **ChromaDB** - Vector database
- **BeautifulSoup4** - Web scraping
- **YFinance** - Stock data
- **NewsAPI** - Financial news

### Frontend
- **React 18** - UI framework
- **Tailwind CSS** - Styling
- **Framer Motion** - Animations
- **React Query** - Data fetching
- **Lucide React** - Icons
- **React Router** - Navigation

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 16+
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/finance-rag-chatbot.git
   cd finance-rag-chatbot
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

4. **Environment Configuration**
   ```bash
   # Create .env file in backend directory
   cp .env.example .env
   # Add your OpenAI API key
   echo "OPENAI_API_KEY=your_api_key_here" >> .env
   ```

5. **Start the Application**
   ```bash
   # Terminal 1 - Backend
   cd backend
   source venv/bin/activate
   python simple_server.py
   
   # Terminal 2 - Frontend
   cd frontend
   npm start
   ```

6. **Access the Application**
   - Frontend: http://localhost:3001
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## 📁 Project Structure

```
finance-rag-chatbot/
├── backend/
│   ├── main.py                 # Full RAG backend
│   ├── simple_server.py        # Simple mock backend
│   ├── requirements.txt        # Python dependencies
│   ├── config.py              # Configuration
│   ├── services/              # Business logic
│   ├── routers/               # API routes
│   └── models/                # Data models
├── frontend/
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── hooks/            # Custom hooks
│   │   ├── api/              # API clients
│   │   ├── utils/            # Utilities
│   │   └── styles/           # CSS styles
│   ├── package.json          # Node dependencies
│   └── tailwind.config.js    # Tailwind config
├── README.md
└── .gitignore
```

## 🎯 Features Breakdown

### Chat Interface
- AI-powered financial assistant
- Context-aware responses
- Source citations
- Quick action buttons

### News Dashboard
- Real-time financial news
- Sentiment analysis
- Category filtering
- Search functionality

### Stock Analysis
- Stock recommendations
- Technical indicators
- AI-powered insights
- Interactive charts

### Market Overview
- Major market indices
- Sector performance
- Market sentiment
- Real-time data

## 🔧 Configuration

### Environment Variables
```bash
# Backend (.env)
OPENAI_API_KEY=your_openai_api_key
NEWS_API_KEY=your_news_api_key
DATABASE_URL=your_database_url

# Frontend (.env)
REACT_APP_API_URL=http://localhost:8000
```

### API Keys Required
- **OpenAI API**: For AI chat functionality
- **NewsAPI**: For financial news (optional)
- **YFinance**: For stock data (free)

## 🚀 Deployment

### Backend Deployment
```bash
# Using Docker
docker build -t finance-rag-backend .
docker run -p 8000:8000 finance-rag-backend

# Using Heroku
heroku create your-app-name
git push heroku main
```

### Frontend Deployment
```bash
# Build for production
npm run build

# Deploy to Vercel/Netlify
# Upload the build folder
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for GPT models
- LangChain for RAG framework
- Tailwind CSS for styling
- React team for the amazing framework


## 🔮 Roadmap

- [ ] Real-time WebSocket chat
- [ ] Portfolio tracking
- [ ] Advanced charting
- [ ] Mobile app
- [ ] Multi-language support
- [ ] Advanced RAG features

---

<img width="1428" height="775" alt="Screenshot 2025-09-12 at 20 36 54" src="https://github.com/user-attachments/assets/31280df2-0276-410c-86c8-41265878da90" />

<img width="1433" height="772" alt="Screenshot 2025-09-12 at 20 37 08" src="https://github.com/user-attachments/assets/421ec9e7-cc7b-480d-b481-c6b6cd67e122" />

<img width="1243" height="773" alt="Screenshot 2025-09-12 at 20 37 12" src="https://github.com/user-attachments/assets/03e24a69-21c2-48c4-8e7b-ed6450311525" />

<img width="1420" height="760" alt="Screenshot 2025-09-12 at 20 37 38" src="https://github.com/user-attachments/assets/d56397ae-ce74-416d-bac2-4b6d95fb9281" />




