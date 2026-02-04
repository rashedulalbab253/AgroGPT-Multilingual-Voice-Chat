# 🌾 Multilingual Assistance Chatbot

A secure multilingual chatbot system designed to assist people in their native language. The project consists of a **FastAPI backend** for chat generation and translation, and a **React frontend** chat widget for user interaction. The backend leverages the **Sarvam AI platform** and is secured using a custom **API key**.

---

## 💻 Prerequisites

To run this project locally, ensure the following tools are installed:

- **Python 3.9+** (for FastAPI backend)
- **Node.js & npm** (for React frontend)
- **Postman** (for API testing)
- **Sarvam AI API Key** (`SARVAM_API_KEY`)

---

## 🚀 1. Backend Setup (FastAPI)

The backend handles chat logic, conversation history, translations, and enforces API key authentication.

### 1.1 Directory Setup

Navigate to your project root:

```bash
 cd backend
```

### 1.2 Environment Configuration

Create a `.env` file inside the directory:

```env
SARVAM_API_KEY="your-sarvam-ai-key-here"
MASTER_API_KEY="my-secret-master-key-12345"
```

⚠️ **Important:** Replace the placeholder values with your actual API keys.

### 1.3 Install Dependencies

```bash
pip install fastapi uvicorn python-dotenv sarvamai requests pydantic
```

### 1.4 Run the Server

```bash
uvicorn test:app --reload --port 8000
```



---

## 🎨 2. Frontend Setup (React)

The frontend is a single Streamlit web page that communicates with the FastAPI backend.

### 2.1 API Key Injection

Ensure the **hardcoded `MASTER_API_KEY`** in your React file matches the backend’s `.env` file.

In `Chatbot.jsx`:

```javascript
// --- API & LANGUAGE CONFIGURATION ---
const FASTAPI_API_URL = "http://127.0.0.1:8000/chat";
const MASTER_API_KEY = "my-secret-master-key-12345"; // must match backend
```

### 2.2 Run the Frontend

If integrated into a React app, start the development server:

```bash
npm start
# or
yarn start
```

---

## 🧪 3. API Testing with Postman

All requests require the `X-API-Key` header.

### 3.1 Unauthorized Test (Expected Failure)

**Request:**

- **Method:** POST
- **URL:** `http://127.0.0.1:8000/chat`
- **Headers:** `Content-Type: application/json`
- **Body:**

```json
{
  "messages": [{ "role": "user", "content": "Hello" }],
  "target_language": "English"
}
```

**Expected Result:**

```json
{ "detail": "Not authenticated" }
```

or

```json
{ "detail": "API Key header is missing" }
```

### 3.2 Authorized Chat Test (Expected Success)

**Request:**

- **Method:** POST
- **URL:** `http://127.0.0.1:8000/chat`
- **Headers:**

  - `Content-Type: application/json`
  - `X-API-Key: my-secret-master-key-12345`

- **Body:**

```json
{
  "messages": [
    { "role": "user", "content": "What fertilizer should I use for rice?" }
  ],
  "target_language": "Kannada"
}
```

**Expected Result:**

```json
{
  "reply": "<Translated response in Kannada>"
}
```

---

## 📌 Project Highlights

- 🔒 Secure backend with API key authentication
- 🌍 Multilingual translation powered by **Sarvam AI**
- 🧑‍🌾 Farmer-friendly chatbot interface
- ⚡ Built with **FastAPI** + **React**

---

## 📜 License

This project is licensed under the MIT License.
