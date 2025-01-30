# Telegram AI Chatbot

![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue.svg) ![Python](https://img.shields.io/badge/Python-3.9%2B-brightgreen.svg) ![AI-Powered](https://img.shields.io/badge/AI-Powered-orange.svg)

## 📌 Overview
This AI-powered Telegram bot provides intelligent responses, image and document analysis, and web search capabilities. It integrates with Google Gemini AI to enhance user interactions with AI-generated insights. 

## 🎥 Demo
🔗 [Watch the Demo Video](https://drive.google.com/file/d/1eymhELh6P0YVlp59VMmaHD9EEeOhyGCc/view?usp=drive_link) 

## ✨ Features
- **User Registration:** Secure user registration with phone number verification.
- **AI Chat:** Engage with Google Gemini AI for intelligent responses.
- **Image & Document Analysis:** Analyze images and extract insights from PDFs.
- **Web Search:** AI-powered web search summarization.
- **Error Handling:** Robust error handling for smooth user experience.

## 🏗️ Project Structure
```
📂 telegram-ai-chatbot
├── 📂 handlers
│   ├── registration.py   # Handles user registration
│   ├── chat.py          # AI chat response handler
│   ├── image_analysis.py # Image and PDF analysis
│   ├── web_search.py     # AI-powered web search
│   ├── error_handler.py  # Error handling
├── config.py            # API keys and configurations
├── database.py          # MongoDB connection
├── main.py               # Main bot execution
├── requirements.txt     # Required dependencies
├── README.md            # Project documentation
```

## 🔧 Installation & Setup
### 1️⃣ Prerequisites
- Python 3.9+
- MongoDB
- Telegram Bot API Token
- Google Gemini API Key

### 2️⃣ Clone the Repository
```bash
git clone https://github.com/abhaykashyap31/Telegram-AI-bot.git
cd telegram-ai-chatbot
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables
Create a `.env` file in the root directory:
```ini
BOT_API_KEY=your-telegram-bot-token
BOT_NAME=your-bot-username
MONGO_URL=your-mongodb-connection-string
GEMINI_API_KEY=your-gemini-api-key
```

### 5️⃣ Run the Bot
```bash
python bot.py
```

## 🤖 AI Models Used
### 🔹 Google Gemini AI
- **Natural Language Processing (NLP):** Used to generate intelligent responses for user queries.
- **Vision Model:** Analyzes images and documents to provide AI-driven insights.
- **Search Summarization:** AI-based summarization of web search results.

## 📚 Acknowledgments & External Sources
- [Google Gemini AI](https://ai.google.dev/) - For AI-powered responses and image analysis.
- [Python Telegram Bot Library](https://python-telegram-bot.readthedocs.io/) - For seamless bot integration.
- [PyMuPDF](https://pymupdf.readthedocs.io/) - For PDF text extraction.
- [Pillow](https://pillow.readthedocs.io/) - For image processing.

## 🚀 Future Enhancements
- ✅ Implement voice-to-text AI chat.
- ✅ Add more document formats for analysis.
- ✅ Enhance chatbot memory for context retention.

## 📩 Contact & Support
For any issues or feature requests, feel free to raise an issue or contact [your email/contact info].

---
© 2025 Telegram AI Chatbot | Built with ❤️ using Python & AI
