# 🎥 Telegram YouTube Research Assistant Bot

A Telegram bot that:

- Extracts YouTube transcripts (Hindi & English)
- Splits long transcripts into chunks
- Generates transcript preview
- Supports question-answering over the video
- Automatically handles Telegram message length limits

---

## 🚀 Features

✔ YouTube transcript extraction using `yt-dlp`  
✔ Hindi & English subtitle support  
✔ Transcript chunking system  
✔ Lightweight TF-based retrieval for Q&A  
✔ Automatic Telegram message splitting  
✔ Clean modular project structure  

---

## 🛠 Tech Stack

- Python
- python-telegram-bot
- yt-dlp
- dotenv
- Basic retrieval logic (TF-based ranking)

---

## 📂 Project Structure

```
Telegram_YouTube_Summarizer/
│
├── src/
│   ├── bot.py
│   └── core/
│       ├── youtube_utils.py
│       ├── chunking.py
│       └── assistant.py
│
├── requirements.txt
├── .gitignore
├── .env.example
└── README.md
```

---

## 📸 Screenshots

### 🔹 Bot Summary Output

![Summary Screenshot](https://github.com/ishitachitranshi/Telegram_YouTube_Summarizer/blob/main/bot-summary.png.png)

---

### 🔹 Question Answering Example

![QA Screenshot](https://github.com/ishitachitranshi/Telegram_YouTube_Summarizer/blob/main/bot-summary.png.png)

---


## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone https://github.com/ishitachitranshi/Telegram_YouTube_Summarizer.git
cd Telegram_YouTube_Summarizer
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Create .env File

Create a file named `.env` in the root directory:

```
TELEGRAM_TOKEN=your_bot_token_here
```

---

### 5️⃣ Run Bot

```bash
python -m src.bot
```

---

## 💬 How to Use

1. Open your Telegram bot.
2. Send any YouTube link.
3. The bot will:
   - Fetch transcript
   - Provide preview
4. Ask questions like:
   - “What is eligibility?”
   - “Summarize in 5 points”
   - “What are exam dates?”

---

## 📌 Example Flow

User:
```
https://youtu.be/Kp3cEC8sU1I
```

Bot:
```
Transcript fetched.
Preview...
```

User:
```
What is the eligibility criteria?
```

Bot:
```
[01:00] Eligibility criteria...
```

---

## 🔐 Security Note

Sensitive files are excluded via `.gitignore`:

- `.env`
- `.venv`
- `*.json3`
- `*.vtt`

---

## 👩‍💻 Author

**Ishita Chitranshi**

Built as part of internship assignment.
