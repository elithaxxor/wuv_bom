# training_data.py

def get_predefined_messages():
    """
    Returns a dictionary containing predefined message categories and lists.
    This data is used for training/selecting messages to send.
    """
    return {
        1: { # Loving Quotes
            "name": "Loving Quotes",
            "messages": [
                "Mom, I love you to the moon and back.",
                "You are my rock and my guide. I love you!",
                "Thank you for always being there for me. You're the best!"
            ]
        },
        2: { # Understanding Remarks
            "name": "Understanding Remarks",
            "messages": [
                "I understand what you're saying, Mom.",
                "It’s okay to feel frustrated sometimes, we’ll get through it.",
                "I'm here, I’ll listen and try to understand better."
            ]
        },
        3: { # Express Anger (Calmly)
            "name": "Express Anger (Calmly)",
            "messages": [
                "Mom, you're testing my patience right now.",
                "I feel really upset, but we can talk about this calmly later.",
                "Let’s not argue. I need a little space to think."
            ]
        },
        5: { # Apologetic Messages
            "name": "Apologetic Messages",
            "messages": [
                "Mom, I'm sorry for earlier. I really appreciate you.",
                "I didn’t mean to upset you, I’ll try to do better.",
                "Please forgive me, I value everything you do for me."
            ]
        },
        6: { # Encouraging Messages
            "name": "Encouraging Messages",
            "messages": [
                "You’re doing an amazing job, Mom. Keep it up!",
                "I believe in you, you’re the strongest person I know.",
                "Don’t forget how incredible you are!"
            ]
        },
        7: { # Funny/Lighthearted Messages
            "name": "Funny/Lighthearted Messages",
            "messages": [
                "Mom, I heard coffee is life... shall we stock up?",
                "What do you call cheese that isn’t yours? Nacho cheese!",
                "Mom, why don’t scientists trust atoms? Because they make up everything!"
            ]
        }
        # Note: Category 4 (Random Characters) is handled separately in the main script.
    }

def get_nltk_responses():
    """
    Returns a dictionary of potential responses based on NLTK analysis triggers.
    """
    return {
        "question": [
            "That's a good question, Mom. Let me think about that.",
            "I'm not sure right now, but I can look into it.",
            "What do you think about that?",
            "Interesting point, Mom."
        ],
        "apology": [
            "It's okay, Mom. I understand.",
            "Thank you for saying that. I appreciate it.",
            "No worries at all. We're good.",
            "Apology accepted. Love you!"
        ],
        "gratitude": [
            "You're very welcome, Mom!",
            "I'm glad I could help.",
            "Anything for you!",
            "Happy to do it!"
        ],
        "strong_positive": [
            "That's wonderful to hear, Mom!",
            "I'm so glad you feel that way!",
            "Awesome!",
            "That makes me happy!"
        ],
        "strong_negative": [
            "Oh no, I'm sorry to hear that. Is there anything I can do?",
            "That sounds really tough. Let's talk about it?",
            "I understand your frustration. How can I help?",
            "Sending you a hug, Mom."
        ],
        "neutral": [
            "Got it, Mom.",
            "Okay, understood.",
            "Thanks for letting me know.",
            "Alright."
        ],
        "default": [
             "Okay, Mom.",
             "Understood.",
             "Got it."
         ]
    }
