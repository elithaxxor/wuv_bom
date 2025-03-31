import pywhatkit as kit
import random
import time
from datetime import datetime
import logging
from textblob import TextBlob
import pyttsx3
from colorama import Fore, Style

def send_message(phone_number, message):
    """Send a WhatsApp message to the given phone number."""
    try:
        kit.sendwhatmsg_instantly(phone_number, message, wait_time=5, tab_close=True)
        logging.info(f"Message sent: {message}")
        print(f"{Fore.GREEN}Message sent: {message}{Style.RESET_ALL}")
    except Exception as e:
        logging.error(f"Failed to send message: {e}")
        print(f"{Fore.RED}Failed to send message: {e}{Style.RESET_ALL}")

def speak_text(text):
    """Convert text to speech."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def analyze_sentiment(text):
    """Analyze the sentiment of a given text using TextBlob."""
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return "Positive"
    elif analysis.sentiment.polarity < 0:
        return "Negative"
    else:
        return "Neutral"

def suggest_response(reply_text):
    """Provide a dynamic response suggestion based on sentiment analysis of the reply."""
    sentiment = analyze_sentiment(reply_text)
    if sentiment == "Positive":
        return "Thank you, Mom. I appreciate your kindness!"
    elif sentiment == "Negative":
        return "I understand your frustration. Let’s talk about it calmly."
    else:
        return "Got it, Mom. Let me know how I can help."

def random_characters():
    """Generate a random string under 250 characters."""
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=random.randint(1, 250)))

def persist_random_messages(phone_number, duration, frequency_range):
    """Send random characters repeatedly based on user-defined duration and frequency."""
    start_time = time.time()
    while time.time() - start_time < duration:
        message = random_characters()
        send_message(phone_number, message)
        sleep_time = random.randint(*frequency_range)
        print(f"Next message in {sleep_time} seconds...")
        time.sleep(sleep_time)

def display_message_with_sentiment(message):
    """Show the message alongside its sentiment in color."""
    sentiment = analyze_sentiment(message)
    if sentiment == "Positive":
        color = Fore.GREEN
    elif sentiment == "Negative":
        color = Fore.RED
    else:
        color = Fore.YELLOW
    print(f"{color}Message: {message} | Sentiment: {sentiment}{Style.RESET_ALL}")

def menu():
    """Display the enhanced hostility menu."""
    options = [
        "1. Loving Quotes",
        "2. Understanding Remarks",
        "3. Express Anger",
        "4. Random Characters",
        "5. Apologetic Messages",
        "6. Encouraging Messages",
        "7. Funny/Lighthearted Messages",
        "8. Analyze Reply Sentiment & Suggest Response",
        "9. Exit"
    ]
    for option in options:
        print(Fore.CYAN + option + Style.RESET_ALL)
    speak_text("Choose an option from the menu.")

def predefined_messages():
    """Data structure for predefined messages."""
    return {
        1: [
            "Mom, I love you to the moon and back.",
            "You are my rock and my guide. I love you!",
            "Thank you for always being there for me. You're the best!"
        ],
        2: [
            "I understand what you're saying, Mom.",
            "It’s okay to feel frustrated sometimes, we’ll get through it.",
            "I'm here, I’ll listen and try to understand better."
        ],
        3: [
            "Mom, you're testing my patience right now.",
            "I feel really upset, but we can talk about this calmly later.",
            "Let’s not argue. I need a little space to think."
        ],
        5: [
            "Mom, I'm sorry for earlier. I really appreciate you.",
            "I didn’t mean to upset you, I’ll try to do better.",
            "Please forgive me, I value everything you do for me."
        ],
        6: [
            "You’re doing an amazing job, Mom. Keep it up!",
            "I believe in you, you’re the strongest person I know.",
            "Don’t forget how incredible you are!"
        ],
        7: [
            "Mom, I heard coffee is life... shall we stock up?",
            "What do you call cheese that isn’t yours? Nacho cheese!",
            "Mom, why don’t scientists trust atoms? Because they make up everything!"
        ]
    }

def main():
    """Main CLI for sending WhatsApp messages."""
    logging.basicConfig(filename="message_log.log", level=logging.INFO)
    # Input the phone number of your mom (ensure it's in international format)
    phone_number = input("Enter your mom's phone number (with country code, e.g., +1XXXXXXXXXX): ")

    messages = predefined_messages()

    while True:
        menu()
        choice = input("Select an option: ")

        if choice == "9":
            print("Exiting program.")
            speak_text("Exiting program now.")
            break
        elif choice in ["1", "2", "3", "5", "6", "7"]:
            hostility_level = int(choice)
            print(f"You selected option {hostility_level}.")
            print("\nAvailable messages:")
            for idx, msg in enumerate(messages[hostility_level], start=1):
                display_message_with_sentiment(msg)
            
            message_choice = int(input("Choose a message to send (e.g., 1, 2): "))
            if 1 <= message_choice <= len(messages[hostility_level]):
                message_to_send = messages[hostility_level][message_choice - 1]
                send_message(phone_number, message_to_send)
            else:
                print(Fore.RED + "Invalid choice, please try again." + Style.RESET_ALL)
        elif choice == "4":
            print(Fore.CYAN + "You selected random characters." + Style.RESET_ALL)
            duration = int(input("How long should this persist (in seconds)? "))
            min_frequency = int(input("Minimum frequency of messages (in seconds): "))
            max_frequency = int(input("Maximum frequency of messages (in seconds): "))
            persist_random_messages(phone_number, duration, (min_frequency, max_frequency))
        elif choice == "8":
            print(Fore.CYAN + "You selected Analyze Reply Sentiment & Suggest Response." + Style.RESET_ALL)
            reply = input("Enter your mom's reply: ")
            sentiment = analyze_sentiment(reply)
            suggestion = suggest_response(reply)
            print(f"Reply Sentiment: {Fore.MAGENTA}{sentiment}{Style.RESET_ALL}")
            print(f"Suggested Response: {Fore.GREEN}{suggestion}{Style.RESET_ALL}")
        else:
            print(Fore.RED + "Invalid option. Please select a valid menu item." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
