# Project Technical Report: AgroGPT
## Intelligent Multilingual Agri-Advisory System
**Prepared by:** Rashedul Albab  
**Date:** February 5, 2026  
**Subject:** Technical Documentation and Architectural Overview

---

## 1. Executive Summary
AgroGPT is a specialized Generative AI solution designed for the agricultural sector. It addresses the "Knowledge Gap" in rural farming by providing a voice-enabled, multilingual interface. The system allows users to interact in their native languages (Bengali, Hindi, etc.) using speech or text to receive expert-curated agricultural advice.

---

## 2. Problem Statement
Farmers in developing regions often lack access to immediate, expert agricultural advice due to:
1.  **Language Barriers:** Most advanced AI and agricultural databases are in English.
2.  **Literacy Challenges:** Difficulty in typing complex queries on mobile devices.
3.  **Latency:** Inefficient distribution of regional agricultural updates.

AgroGPT solves these by utilizing **Automatic Speech Recognition (ASR)** and **Neural Machine Translation (NMT)** to make expert knowledge accessible via simple voice commands.

---

## 3. System Architecture
The system follows a **Decoupled Micro-service Architecture** to ensure independent scalability of the frontend and backend.

### 3.1 Architecture Diagram (Conceptual)
```text
[ Client Layer ]          [ Application Layer ]          [ AI Engine Layer ]
+--------------+          +-------------------+          +-----------------+
|  React Web   | <------> |  FastAPI Backend  | <------> |   Sarvam AI API |
|   (Vite)     | (HTTPS)  |  (Uvicorn/Py3.9)  | (REST)   | (ASR & GenChat) |
+--------------+          +---------+---------+          +-----------------+
                                    |
                          +---------+---------+
                          |  Security & Core  |
                          | - API Auth Guard  |
                          | - SQLite Sync     |
                          | - Rate Limiter    |
                          +-------------------+
```

### 3.2 Component Analysis
-   **Frontend (React/Vite):** A lightweight, responsive SPA (Single Page Application) that handles audio recording via the Web MediaStreams API and converts it to Blobs for backend processing.
-   **Backend (FastAPI):** An asynchronous Python framework chosen for its high concurrency performance. It acts as the middleware that orchestrates authentication, logging, and external AI calls.
-   **Intelligence Layer (Sarvam AI):**
    -   **Models:** `saarika:v2.5` for high-fidelity Indic ASR.
    -   **Role:** Handles the complex translation and domain-specific response generation.

---

## 4. Technical Implementation Details

### 4.1 Speech-to-Text Pipeline
1.  Frontend captures PCM/WebM audio data.
2.  Data is transmitted as `multipart/form-data` to the `/transcribe` endpoint.
3.  Backend utilizes the `sarvamai` SDK to convert audio to text using the regional language code (e.g., `bn-IN` for Bengali).

### 4.2 Security Protocol
-   **X-API-Key Middleware:** A custom security layer validates every request against a Master API Key stored in environmental variables. 
-   **Rate Limiting:** Implemented at the router level using `slowapi` (Fixed Window strategy) to protect the backend from DoS attacks and manage API costs.

### 4.3 DevOps & Containerization
-   **Environment Isolation:** Using Docker to ensure "It works on my machine" translates to "It works in production."
-   **CI/CD:** GitHub Actions workflow automates the build process:
    -   Linting/Verification.
    -   Multi-platform Docker build.
    -   Automated push to Docker Hub (`rashedulalbab1234`).

---

## 5. Deployment Strategy
-   **Container Orchestration:** Managed via `docker-compose` for local development.
-   **Production Path:** Designed for deployment on AWS ECS or DigitalOcean App Platform using the established Docker images.

---

## 6. Future Scope (Applied Research)
For a PhD or Advanced Research track, the project can be extended through:
1.  **RAG (Retrieval-Augmented Generation):** Connecting the bot to local government agricultural PDF databases for verified local advice.
2.  **Offline-First ASR:** Implementing edge-device transcription for areas with zero internet connectivity.
3.  **Crop Disease Vision:** Using Computer Vision (CNNs) to diagnose plant health via photos uploaded in the chat.

---

## 7. Conclusion
AgroGPT demonstrates a successful fusion of modern software engineering principles and cutting-edge artificial intelligence. By focusing on accessibility and security, it provides a stable foundation for a scalable agricultural tech product.
