# 🌾 AgroGPT: Intelligent Multilingual Agri-Advisory System
### *Bridging the Digital Divide with Voice-Enabled Generative AI for Agriculture*

![Build Status](https://img.shields.io/badge/Version-1.0.0-green.svg)
![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![React](https://img.shields.io/badge/React-18-blue.svg)
![Security](https://img.shields.io/badge/Security-API--Key--Auth-gold.svg)
![License](https://img.shields.io/badge/License-MIT-gray.svg)

---

## 🌟 Project Vision
**AgroGPT** is an enterprise-grade, multilingual AI advisor designed to empower farmers and agriculturists. In regions where literacy or technical barriers exist, AgroGPT provides a **voice-first, native-language interface** to access expert advice on crop management, pest control, and sustainable farming practices.

This system leverages state-of-the-art **Generative AI** and **ASR (Automatic Speech Recognition)** via the Sarvam AI platform to deliver high-accuracy, domain-specific intelligence.

---

## 🚀 Key Features

### 1. 🎤 Voice-First Interaction
Seamlessly transcribe regional dialects into actionable queries using advanced ASR models. Designed for accessibility in rural environments.

### 2. 🌍 Universal Multilingual Support
Conversational support for 6+ major languages:
- **English, Hindi, Bengali, Gujarati, Kannada, Punjabi.**

### 3. 🛡️ Enterprise Security & Scalability
- **API Key Guard:** Custom-built middleware for secure, authenticated access.
- **Rate Limiting:** Integrated `slowapi` to prevent abuse and ensure high availability.
- **Async Architecture:** Built on **FastAPI** for high-performance, asynchronous processing.

### 4. 📦 Cloud-Ready Deployment
- Full **Dockerization** for consistent environments.
- **GitHub Actions (CI/CD)** automated pipeline for Docker Hub deployment.

---

## 🛠️ Tech Stack

| Component | Technology |
| :--- | :--- |
| **Backend** | FastAPI (Python), SQLAlchemy, Pydantic |
| **Frontend** | React.js, Vite, Tailwind CSS, Axios |
| **AI/ML** | Sarvam AI (Text-to-Text & ASR), `saarika:v2.5` |
| **Database** | SQLite (Production-ready abstraction available) |
| **DevOps** | Docker, Docker Compose, GitHub Actions |

---

## 🏗️ System Architecture

```text
User Interface (React) <---> Secure Gateway (FastAPI) <---> Sarvam AI Engine
                                     |
                          +----------+----------+
                          |          |          |
                    Local Cache   Auth Mgr   Session DB
```

---

## ⚙️ Setup & Installation

### 1. Environment Configuration
Create a `.env` file in the root directory:
```env
SARVAM_API_KEY="your_sarvam_key"
MASTER_API_KEY="your_custom_secure_key"
```

### 2. Local Development (Classic)
**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --port 8000 --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### 3. Modern Launch (Recommended)
Launch the entire stack with one command:
```bash
python run.py
```

---

## 🐳 Dockerization & Deployment

To run in a containerized environment (Port 8000 & 5173):
```bash
docker-compose up --build -d
```

**CI/CD Pipeline:**
The project is configured to automatically push images to Docker Hub:
- Repository: `rashedulalbab1234/agrogpt`
- GitHub User: `rashedulalbab253`

---

## 🎓 Academic Significance
This project serves as a research foundation for:
1. **NLP in Low-Resource Languages:** Real-world application of cross-lingual knowledge transfer.
2. **HCI (Human-Computer Interaction):** Studying the impact of voice-based AI on rural technology adoption.
3. **Domain-Specific AI Alignment:** Implementing strict system prompts and safety guards for critical agricultural advice.

---

## 👨‍💻 Author
**Rashedul Albab**
- [GitHub](https://github.com/rashedulalbab253)
- [Docker Hub](https://hub.docker.com/u/rashedulalbab1234)

---

## 📜 License
Licensed under the MIT License.
