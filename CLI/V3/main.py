import pywhatkit as kit
import random
import time
import threading
import logging
import pyttsx3
from colorama import Fore, Style
from textblob import TextBlob
from transformers import pipeline
import openai


## Uses textblob and openai gpt2 (cuz im cheap) 

# Initialize Hugging Face pipelines for sentiment analysis and text generation.
sentiment_analyzer = pipeline("sentiment-analysis")
text_generator = pipeline("text-generation", model="gpt-2")

# Set OpenAI API key (replace with your own key)
openai.api_key = "YOUR_OPENAI_API_KEY"

# Global variables for threading persistent random messaging.
persistent_random_thread = None
random_stop_event = threading.Event()

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

def analyze_sentiment_hf(text):
    """Analyze sentiment using Hugging Face's Transformers."""
    result = sentiment_analyzer(text)[0]
    sentiment = result['label']  # e.g., POSITIVE or NEGATIVE
    score = result['score']
    return sentiment, score

def generate_dynamic_response_hf(reply_text):
    """Generate a contextually appropriate response using Hugging Face's GPT model."""
    sentiment, _ = analyze_sentiment_hf(reply_text)
    if sentiment == "POSITIVE":
        prompt = f"My mom said: '{reply_text}'. Respond warmly and lovingly."
    elif sentiment == "NEGATIVE":
        prompt = f"My mom said: '{reply_text}'. Respond with understanding and empathy."
    else:
        prompt = f"My mom said: '{reply_text}'. Respond neutrally and respectfully."
    
    response = text_generator(prompt, max_length=50, num_return_sequences=1)[0]["generated_text"]
    return response

def analyze_and_generate_openai(reply_text):
    """Analyze replies and generate dynamic responses using OpenAI's GPT."""
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"My mom said: '{reply_text}'. Analyze the sentiment and respond appropriately.",
        max_tokens=50,
        temperature=0.7
    )
    return response['choices'][0]['text'].strip()

def random_characters():
    """Generate a random string under 250 characters."""
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=random.randint(1, 250)))

def persist_random_messages(phone_number, duration, frequency_range, stop_event):
    """Send random characters repeatedly based on user input until duration expires or stop signal is set."""
    start_time = time.time()
    while time.time() - start_time < duration:
        if stop_event.is_set():
            print(f"{Fore.MAGENTA}Persistent random messaging stopped by user.{Style.RESET_ALL}")
            break
        message = random_characters()
        send_message(phone_number, message)
        sleep_time = random.randint(*frequency_range)
        print(f"Next message in {sleep_time} seconds...")
        time.sleep(sleep_time)
    print(f"{Fore.MAGENTA}Persistent random messaging finished or canceled.{Style.RESET_ALL}")

def display_message_with_sentiment(message):
    """Show the message alongside its sentiment in color."""
    sentiment, score = analyze_sentiment_hf(message)
    if sentiment == "POSITIVE":
        color = Fore.GREEN
    elif sentiment == "NEGATIVE":
        color = Fore.RED
    else:
        color = Fore.YELLOW
    print(f"{color}Message: {message} | Sentiment: {sentiment} ({score:.2f}){Style.RESET_ALL}")

def menu():
    """Display the enhanced menu."""
    options = [
        "1. Loving Quotes",
        "2. Understanding Remarks",
        "3. Express Anger",
        "4. Start Random Characters",
        "5. Apologetic Messages",
        "6. Encouraging Messages",
        "7. Funny/Lighthearted Messages",
        "8. Analyze Reply Sentiment & Suggest Response",
        "9. Stop Random Messaging",
        "10. Exit"
    ]
    for option in options:
        print(Fore.CYAN + option + Style.RESET_ALL)
    speak_text("Choose an option from the menu.")

def predefined_messages():
    """Return predefined messages organized by categories."""
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
    global persistent_random_thread, random_stop_event
    logging.basicConfig(filename="message_log.log", level=logging.INFO)
    
    # Ask for the recipient's phone number
    phone_number = input("Enter your mom's phone number (with country code, e.g., +1XXXXXXXXXX): ")
    messages = predefined_messages()

    while True:
        menu()
        choice = input("Select an option: ")

        if choice == "10":
            print("Exiting program.")
            speak_text("Exiting program now.")
            # If random messaging thread is active, signal it to stop.
            if persistent_random_thread and persistent_random_thread.is_alive():
                random_stop_event.set()
                persistent_random_thread.join()
            break

        elif choice in ["1", "2", "3", "5", "6", "7"]:
            # Predefined message sending options.
            hostility_level = int(choice)
            print(f"You selected option {hostility_level}.")
            for idx, msg in enumerate(messages[hostility_level], start=1):
                display_message_with_sentiment(msg)
            try:
                message_choice = int(input("Choose a message to send (e.g., 1, 2): "))
            except ValueError:
                print(f"{Fore.RED}Invalid input. Please enter a number.{Style.RESET_ALL}")
                continue

            if 1 <= message_choice <= len(messages[hostility_level]):
                message_to_send = messages[hostility_level][message_choice - 1]
                send_message(phone_number, message_to_send)
            else:
                print(Fore.RED + "Invalid choice, please try again." + Style.RESET_ALL)

        elif choice == "4":
            # Start persistent random messaging in a separate thread.
            try:
                duration = int(input("How long should this persist (in seconds)? "))
                min_frequency = int(input("Minimum frequency of messages (in seconds): "))
                max_frequency = int(input("Maximum frequency of messages (in seconds): "))
            except ValueError:
                print(f"{Fore.RED}Input must be an integer. Try again.{Style.RESET_ALL}")
                continue

            if persistent_random_thread and persistent_random_thread.is_alive():
                print(f"{Fore.MAGENTA}Random messaging is already running.{Style.RESET_ALL}")
            else:
                # Reset the event and start a new thread
                random_stop_event.clear()
                persistent_random_thread = threading.Thread(
                    target=persist_random_messages,
                    args=(phone_number, duration, (min_frequency, max_frequency), random_stop_event)
                )
                persistent_random_thread.start()
                print(f"{Fore.MAGENTA}Started persistent random messaging in a background thread.{Style.RESET_ALL}")

        elif choice == "9":
            # Stop the persistent random messaging if running.
            if persistent_random_thread and persistent_random_thread.is_alive():
                print("Stopping persistent random messaging...")
                random_stop_event.set()
                persistent_random_thread.join()
                print(f"{Fore.MAGENTA}Persistent random messaging stopped.{Style.RESET_ALL}")
            else:
                print(f"{Fore.MAGENTA}No persistent messaging is currently running.{Style.RESET_ALL}")

        elif choice == "8":
            # Analyze a reply and generate a dynamic response.
            reply = input("Enter your mom's reply: ")
            print("Analyzing sentiment using Hugging Face...")
            hf_response = generate_dynamic_response_hf(reply)
            print(Fore.GREEN + f"Hugging Face Response: {hf_response}" + Style.RESET_ALL)
            print("Analyzing sentiment using OpenAI...")
            openai_response = analyze_and_generate_openai(reply)
            print(Fore.BLUE + f"OpenAI Response: {openai_response}" + Style.RESET_ALL)
        else:
            print(Fore.RED + "Invalid option. Please select a valid menu item." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
