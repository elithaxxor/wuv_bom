####### Simple Multinomial Naive Bayes classifier for predicting responses on WhatsApp

```markdown
⸻

🤖 WhatsApp Chatbot using NLTK (Multinomial Naive Bayes Classifyer / TD-IDF) and PyWhatKit

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
```
