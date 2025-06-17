# Model Trainer 

! Concept !

## 📌 Overview

Model Trainer is a **web-based application** that allows users to **create, train, and evaluate machine learning models** via a user-friendly interface. It is designed for **educational purposes**, making it easy for students, researchers, and developers to experiment with machine learning workflows.

## 🛠 Tech Stack

### **Backend (`app/`)**

- **Python** (Flask)
- **Flask-SocketIO** (WebSockets for real-time communication)
- **SQLAlchemy** (Database ORM, if needed)
- **Celery + Redis** (Optional: for background task processing)

### **Frontend (`client/`)**

- **Vue.js** (Modern frontend framework)
- **Socket.IO Client** (Real-time updates)
- **Axios** (API communication)

---

## 🚀 Installation & Setup

### **1️⃣ Clone the Repository**

```bash
git clone https://github.com/nbursa/model-trainer.git
cd model-trainer
```

### **2️⃣ Backend Setup (`app/`)**

```bash
cd app
python -m venv venv  # Create virtual environment
source venv/bin/activate  # Activate it (Mac/Linux)
venv\Scripts\activate  # (Windows)

pip install -r requirements.txt  # Install dependencies
```

### **3️⃣ Frontend Setup (`client/`)**

```bash
cd ../client
npm ci  # Install dependencies
```

---

## 🏃 Running the Project

### **Run the Flask Backend (`app/`):**

```bash
cd app
python -m app.run  # Start Flask with Socket.IO support
```

The backend will start at: **http://localhost:5000**

### **Run the Vue Frontend (`client/`):**

```bash
cd client
npm run dev
```

The frontend will start at: **http://localhost:5173** (default Vite port)

---

## 🔄 API & WebSocket Usage

### **📌 API: Start Model Training**

Send a `POST` request to **`/train`** to start training a model.

```bash
curl -X POST http://localhost:5000/train -H "Content-Type: application/json" -d '{"model": "neural_network"}'
```

_Response:_

```json
{ "message": "Model training started" }
```

### **📌 WebSocket: Listen for Training Updates**

**Frontend (Vue.js) example:**

```javascript
import { io } from "socket.io-client";
const socket = io("http://localhost:5000");

socket.on("training_progress", (data) => {
  console.log("Training Update:", data);
});
```

**Backend (Flask) example:**

```python
from flask_socketio import SocketIO
socketio = SocketIO()

@socketio.on("start_training")
def handle_training(data):
    socketio.emit("training_progress", {"status": "50% completed"})
```

---

## 🚀 Planned Improvements

- ✅ Implement **User Authentication** (JWT-based login system)
- ✅ Optimize **Real-time Model Training Feedback**
- ✅ Add **Predefined ML Models** to simplify usage
- ✅ Improve **Frontend UI** with better visualizations

---

## 📢 Contributing

Pull requests are welcome! If you'd like to contribute, please **open an issue first** to discuss the changes.

---

## 📜 License

MIT License. See [LICENSE](LICENSE) for details.
