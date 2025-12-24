🎨 PicBot — AI Image Generator

**Dream It. Create It. Own It.**

PicBot is a **full-stack AI image generation web application** built with **Flask**, **LangChain**, and **free AI image APIs**. It transforms text prompts into stunning visuals with a modern, animated UI — all bundled into a **single Python file** for easy deployment.

---

## ✨ Features

* 🖼️ **AI Image Generation**

  * Uses **Pollinations AI (FLUX model)** — completely free, no API key required
  * Automatic fallback to **DeepAI** if the primary service fails

* 🧠 **Prompt Enhancement with LangChain**

  * Enhances user prompts using a Hugging Face LLM
  * Gracefully falls back if no API key is provided

* ⚡ **Modern, Animated UI**

  * Built with **Tailwind CSS**
  * Glassmorphism, gradients, animations, and responsive layout

* 🔁 **Prompt Suggestions**

  * Randomized trending prompts for inspiration

* 🕒 **Image History**

  * View, reuse, and download recently generated images

* 🌍 **CORS Enabled API**

  * Ready for frontend extensions or integrations

* 📦 **Single-File Application**

  * Backend + frontend HTML auto-generated at runtime

---

## 🧱 Tech Stack

### Backend

* Python 3.9+
* Flask
* Flask-CORS
* LangChain
* Hugging Face Hub
* Requests
* Pillow
* python-dotenv

### Frontend

* HTML5
* Tailwind CSS (CDN)
* Vanilla JavaScript

---

## 🚀 Quick Start

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/picbot.git
cd picbot
```

---

### 2️⃣ Create a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

**Required packages:**

```txt
flask
flask-cors
langchain
langchain-huggingface
huggingface-hub
python-dotenv
requests
pillow
```

---

### 4️⃣ Configure Environment Variables (Optional)

Create a `.env` file:

```env
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
PORT=5000
```

> 🔹 **Note:**
>
> * The app works **without** a Hugging Face API key
> * Prompt enhancement will be disabled if the key is missing

---

### 5️⃣ Run the Application

```bash
python app.py
```

Then open your browser:

```
http://localhost:5000
```

---

## 📡 API Endpoints

### 🔹 Generate Image

**POST** `/api/generate-image`

```json
{
  "prompt": "A futuristic cyberpunk city at sunset"
}
```

**Response**

```json
{
  "image": "data:image/png;base64,...",
  "prompt": "A futuristic cyberpunk city at sunset"
}
```

---

### 🔹 Enhance Prompt

**POST** `/api/enhance-prompt`

```json
{
  "prompt": "A dragon flying"
}
```

**Response**

```json
{
  "enhanced": "A majestic ancient dragon soaring through stormy skies..."
}
```

---

### 🔹 Prompt Suggestions

**GET** `/api/suggestions`

---

### 🔹 Health Check

**GET** `/api/health`

```json
{
  "status": "OK",
  "api_key_configured": true,
  "langchain_available": true
}
```

---

## 🖌️ UI Highlights

* Gradient animated backgrounds
* Glassmorphic cards
* Keyboard shortcuts:

  * **Ctrl + Enter** → Generate image
  * **Ctrl + E** → Enhance prompt
  * **Ctrl + M** → Magic prompt

---

## 🧠 How It Works

1. User enters a prompt
2. (Optional) Prompt is enhanced using LangChain + Hugging Face
3. Image is generated via **Pollinations AI**
4. Result is returned as a Base64 image
5. Frontend renders and stores history locally

---

## 🔒 Security Notes

* Never commit your `.env` file
* Hugging Face API key is optional
* Image generation uses public, rate-free APIs

---

## 🛠️ Deployment

The app is ready for deployment on:

* **Render**
* **Railway**
* **Fly.io**
* **Heroku**
* **Docker**

Uses:

```bash
PORT environment variable
0.0.0.0 binding
```

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 🌟 Credits

* **Pollinations AI** — Free image generation
* **DeepAI** — Backup image generation
* **Hugging Face** — Text generation
* **LangChain** — Prompt orchestration
* **Tailwind CSS** — UI styling

---

## 💡 Future Enhancements

* User authentication
* Image upscaling
* Prompt presets & styles
* Image gallery export
* Stable Diffusion local support

---

### 🚀 Built with passion, creativity, and AI

**PicBot — Turn imagination into reality.**
