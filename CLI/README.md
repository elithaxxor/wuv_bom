#### v1
```markdown
# 📱 Python WhatsApp Messenger & Reply Assistant (v1.4) 🚀

![Python Versions](https://img.shields.io/badge/python-3.7%2B-blue) ![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-green) ![License](https://img.shields.io/badge/license-MIT-orange)  
📖 *Automate WhatsApp messages, perform sentiment analysis with NLP, log interactions, and streamline communication—all from your command line!*

---

⚠️ **Disclaimer:**  
Using automated tools on WhatsApp **may violate their Terms of Service**, leading to account suspension. This project is **for educational purposes only**, showcasing Python’s capabilities in automation, NLP, and database logging. **Use responsibly and at your own risk.**

---

## ✨ Key Features

**1. 📤 Versatile WhatsApp Messaging:**  
   - Send predefined messages from categories like ❤️ Loving, 😡 Anger, 🫂 Understanding, 📜 Apology, 💪 Encouragement, and 😄 Funny.  
   - Fire random character strings persistently for specified durations and intervals (fun in moderation!).

**2. 🤖 Intelligent Reply Analysis (Sentiment Analysis):**  
   - Detects the **sentiment** (`Positive`, `Negative`, `Neutral`) of WhatsApp replies using **NLTK VADER** (Valence Aware Dictionary and sEntiment Reasoner), specialized for chat-like text.  
   - Generates a **compound sentiment score** (-1 to +1) indicating reply intensity.  
   - 🎯 **Suggests responses** tailored to detected sentiment and keyword patterns (e.g., apologies, gratitude).

**3. 🧾 Robust Logging:**  
   - 🗃️ **Database Logging:** Every interaction is securely stored in an SQLite database (`chat_log.db`) with metadata (e.g., timestamps, messages, sentiment score).  
   - 📝 **File-Based Logging:** Text logs (`message_log.log`) track workflow, warnings, errors, database actions, and more.

**4. 🎨 User-Friendly CLI:**  
   - Interactive **menu system** with clear options.  
   - 🌈 **Colored outputs** (via `colorama`) enhance readability.  
   - Optional **text-to-speech prompts** (using `pyttsx3`) for an immersive experience.

---

## 🛠️ Prerequisites

| Requirement          | Notes                                                                                           |
|-----------------------|------------------------------------------------------------------------------------------------|
| 🐍 **Python**         | Version 3.7+, [Download Python](https://www.python.org/downloads/).                            |
| 📦 **pip**            | Python package installer (default with Python).                                                |
| 💻 **Operating System** | Compatible with Windows, macOS, and Linux.                                                    |
| 🌐 **WhatsApp Web**   | An active WhatsApp account and **web.whatsapp.com** session in your default browser are required.|

---

## 📂 File Structure

```plaintext
📦 Project Directory
├── 📜 whatsapp_bot.py        # Main Python script (bot logic).  
├── 📜 training_data.py       # Stores predefined messages and sentiment-based suggestions.  
├── 📦 chat_log.db            # SQLite database. Automatically created/updated during use.  
├── 📜 message_log.log        # Detailed file log documenting interactions.  
└── 📜 README.md              # This documentation file.
```
#### v2
```
⸻

🤖 WhatsApp Chatbot using NLTK and PyWhatKit

A simple yet effective chatbot that uses Natural Language Processing to classify message hostility and respond intelligently over WhatsApp.

⸻

📚 Table of Contents
	•	Introduction
	•	Methodology
	•	Program Overview
	•	Features
	•	Room for Improvement
	•	Requirements
	•	Installation
	•	Usage

⸻

🚀 Introduction

This project demonstrates the use of NLTK and PyWhatKit to build a basic yet functional WhatsApp chatbot. It is trained on a labeled dataset of text messages and classifies incoming messages by hostility level to generate context-aware responses.

⸻

🧠 Methodology

The chatbot leverages Natural Language Toolkit (NLTK) for text preprocessing and classification using a Multinomial Naive Bayes model.

Why Multinomial Naive Bayes?

We evaluated VADER, a popular sentiment analysis tool in NLTK, but opted for Multinomial Naive Bayes for the following reasons:
	•	📈 Custom Classification vs. Predefined Sentiment: VADER is rule-based and designed for general sentiment polarity (positive, neutral, negative). Our use case demanded custom hostility levels, which Naive Bayes can be trained for directly.
	•	🧠 Learned Behavior: Naive Bayes learns from data, adapting to specific language patterns in your dataset. VADER uses a fixed lexicon, limiting adaptability.
	•	🧪 Higher Granularity: Multinomial Naive Bayes allows multi-class classification (e.g., low, medium, high hostility) rather than simple positive/negative/neutral outputs.
	•	🧾 Bag-of-Words Suitability: Texts are converted into frequency vectors (bag-of-words), a format Naive Bayes handles naturally and efficiently.

In summary, VADER is great for general sentiment, but Multinomial Naive Bayes is better for custom, multi-label classification tasks like hostility detection.

⸻

🧩 Program Overview

The application consists of two main parts:
	1.	Training
A Multinomial Naive Bayes model is trained on pre-labeled text messages.
	2.	Chatbot
The trained model classifies incoming messages and generates responses accordingly, using PyWhatKit to interface with WhatsApp.

⸻

✨ Features
	•	🔍 Hostility Detection: Predicts hostility level from incoming text.
	•	💬 Smart Responses: Generates appropriate replies based on detected hostility.
	•	📱 WhatsApp Integration: Uses PyWhatKit to send/receive messages via WhatsApp Web.
	•	💾 SQLite Database: Logs all conversations for recordkeeping and improvement.

⸻

🛠️ Room for Improvement
	•	🔧 Model Accuracy: Improve accuracy by expanding the dataset and tuning hyperparameters.
	•	🧠 Advanced NLP: Consider integrating libraries like spaCy or Transformers.
	•	🏗️ More Features: Add sentiment analysis, entity recognition, or conversation threading.

⸻

📦 Requirements
	•	Python 3.x
	•	nltk
	•	pywhatkit
	•	SQLite3

⸻

🧪 Installation
	1.	Install dependencies:

pip install nltk pywhatkit


	2.	Download NLTK data:

python -m nltk.downloader all

⸻

▶️ Usage
	1.	Run the main script:

python main.py


	2.	Train and Chat:
	•	Follow prompts to train the model.
	•	Begin chatting via WhatsApp.
	•	Responses and messages are logged automatically.
```
