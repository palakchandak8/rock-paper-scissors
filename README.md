# 🪨 Rock Paper Scissors - Hand Gesture Game ✂️

A real-time hand gesture recognition game using Python MediaPipe backend and HTML/CSS/JS frontend.

## 🎮 Features

- Real-time hand gesture detection (both left and right hands)
- Beautiful web-based UI with live webcam feed
- Visual hand tracking landmarks (dots and lines)
- Auto-rematch system for continuous gameplay
- Score tracking

## 🎯 How to Play

1. Show your hand gesture to the camera:
   - ✊ **Rock**: Closed fist (0 fingers)
   - ✋ **Paper**: Open hand (5 fingers)
   - ✌️ **Scissors**: Two fingers up

2. Press **Start Game** to begin
3. Game automatically continues with countdown and rematches
4. Press **Reset** to stop and clear scores

## 📦 Project Versions

### Web Version (Main - Recommended)
- Modern web interface with beautiful UI
- Works on any device with a browser
- Backend API with Flask
- Auto-rematch system
- Located in: `frontend/` and `backend/`

### Desktop Version (Legacy)
- OpenCV window interface
- For local development/testing
- Located in: `examples/rps-opencv.py`
- [See examples/README.md for usage](examples/README.md)

## 🛠️ Tech Stack

**Backend:**
- Python Flask
- MediaPipe (Hand tracking)
- OpenCV
- Flask-CORS

**Frontend:**
- HTML5 Canvas
- CSS3 (Grid background, animations)
- Vanilla JavaScript (Fetch API)

## 🚀 Local Development

### Prerequisites
- Python 3.8+
- Webcam
- Modern web browser

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/rock-paper-scissors.git
cd rock-paper-scissors
```

2. **Install Python dependencies**
```bash
cd backend
pip install -r requirements.txt
```

3. **Run the backend server**
```bash
python app.py
```
Server runs on `http://localhost:5000`

4. **Open the frontend**
- Option 1: Use Live Server in VS Code
- Option 2: Open `frontend/index.html` directly in browser

5. **Allow camera permissions** when prompted

## 📁 Project Structure
```
rock-paper-scissors/
├── backend/
│   ├── app.py              # Flask API server
│   ├── requirements.txt    # Python dependencies
│   └── Procfile           # Deployment config
├── examples/
│   ├── rps-opencv.py      # Desktop OpenCV version
│   └── README.md          # Desktop version docs
├── frontend/
│   └── index.html         # Web interface
├── .gitignore
└── README.md
```

## 🌐 Deployment

### Backend Deployment (Railway/Render)
1. Push to GitHub
2. Connect repository to Railway/Render
3. Set root directory: `backend`
4. Set start command: `gunicorn app:app`
5. Update `BACKEND_URL` in frontend

### Frontend Deployment (GitHub Pages)
1. Enable GitHub Pages in repository settings
2. Deploy from `main` branch
3. Site will be live at: `https://YOUR_USERNAME.github.io/rock-paper-scissors/`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.

## 👏 Acknowledgments

- MediaPipe by Google for hand tracking
- Flask for backend API
- Inspiration from classic Rock Paper Scissors game

---

Made with ❤️ using Python & JavaScript