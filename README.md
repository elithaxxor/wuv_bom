# Multi-Modular WhatsApp Messenger Tool using NLTK + LLM

A comparative overview of three versions of a WhatsApp Messenger tool showcasing evolving NLP capabilities.

## Overview

This project demonstrates the progression of a WhatsApp Messenger tool through three distinct versions, each implementing different Natural Language Processing (NLP) approaches for message analysis and response generation:

1. **V1**: Rule-based sentiment analysis with NLTK VADER
2. **V2**: Custom classification using Multinomial Naive Bayes
3. **V3**: Advanced NLP with Transformers and OpenAI GPT

## Version Details

### Version 1: NLTK VADER Sentiment Analysis

#### Features
- Sentiment analysis using NLTK's VADER lexicon
- Compound sentiment scoring (-1 to +1 intensity)
- Predefined response categories (loving, apologetic, funny, etc.)
- Dual logging system:
  - SQLite database storage
  - File-based logging
- CLI interface with:
  - Color-coded outputs (via Colorama)
  - Optional text-to-speech prompts

#### Technologies
- `nltk` VADER
- `sqlite3` for database logging
- `colorama` for CLI styling

---

### Version 2: Multinomial Naive Bayes Classifier

#### Features
- Custom hostility level classification (low/medium/high)
- Trainable model using labeled datasets
- Automated response generation based on detected hostility
- Two-phase architecture:
  1. **Training Mode**: Builds classification model
  2. **Chatbot Mode**: Implements trained model

#### Technologies
- Scikit-learn's `MultinomialNB`
- `pickle` for model serialization
- Customizable training data format

---

### Version 3: Advanced NLP with Transformers and OpenAI

#### Features
- Hybrid NLP pipeline:
  - Sentiment analysis via Hugging Face Transformers
  - Contextual response generation using OpenAI GPT
- Dynamic response adaptation based on message sentiment
- Background threading for concurrent operations
- Enhanced conversational flow:
  - Empathetic responses to negative messages
  - Context-aware positive reinforcements

#### Technologies
- `transformers` library (Hugging Face)
- OpenAI GPT API
- Concurrent threading
- Advanced prompt engineering

## Key Differences

| Aspect                | V1                          | V2                          | V3                          |
|-----------------------|-----------------------------|-----------------------------|-----------------------------|
| **Analysis Approach** | Rule-based (VADER)          | Statistical (Naive Bayes)   | Neural (Transformers/GPT)   |
| **Classification**    | Positive/Neutral/Negative   | Custom Hostility Levels     | Contextual Sentiment        |
| **Response Generation** | Predefined Templates      | Model-Based Suggestions     | Dynamic GPT Generation      |
| **Technical Stack**   | NLTK + SQLite               | Scikit-learn + Pickle       | Transformers + OpenAI API   |
| **User Experience**   | Basic CLI Interactions      | Trainable Classifier        | Threaded Conversational AI  |

## Getting Started

1. Clone repository:
   ```bash
   git clone https://github.com/yourusername/whatsapp-messenger-evolution.git

	1.	Install requirements for each version:
pip install -r v1/requirements.txt
pip install -r v2/requirements.txt
pip install -r v3/requirements.txt

	2.	Obtain API keys (for V3):
	•	Hugging Face Hub token
	•	OpenAI API key

Usage

	•	V1: Run python v1/main.py for sentiment-based chatting
	•	V2: First train model with python v2/train.py, then run python v2/chat.py
	•	V3: Set API keys in .env, then execute python v3/main.py

Evolution Summary

VersionStrengthIdeal Use CaseV1Simple & ReliableBasic Sentiment MonitoringV2Customizable ClassifierDomain-Specific ModerationV3Contextual UnderstandingHuman-Like Conversational AI	Note: Each version requires progressively more computational resources, with V3 needing GPU acceleration for optimal performance.


This professional README structure provides clear technical documentation while highlighting the evolutionary progression between versions. It uses standardized markdown formatting with comparative tables and technology badges for quick scanning.
