import pywhatkit as kit
import random
import time
from datetime import datetime
import logging
# Removed TextBlob import
# import textblob import TextBlob
import pyttsx3
from colorama import Fore, Style, init as colorama_init

# --- NLTK Imports ---
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize

# --- Custom Module Import ---
from training_data import get_predefined_messages, get_nltk_responses # Import functions from the new file

# --- Initialize Colorama ---
colorama_init(autoreset=True)

# --- NLTK Data Download ---
def download_nltk_data():
    """Downloads necessary NLTK data if not already present."""
    required_data = [('sentiment/vader_lexicon.zip', 'vader_lexicon'),
                     ('tokenizers/punkt', 'punkt')]
    for path, pkg_id in required_data:
        try:
            nltk.data.find(path)
            print(f"{Fore.GREEN}NLTK data '{pkg_id}' found.{Style.RESET_ALL}")
        except LookupError:
            print(f"{Fore.YELLOW}NLTK data '{pkg_id}' not found. Downloading...{Style.RESET_ALL}")
            try:
                nltk.download(pkg_id)
                print(f"{Fore.GREEN}Successfully downloaded '{pkg_id}'.{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}Error downloading NLTK data '{pkg_id}': {e}{Style.RESET_ALL}")
                print(f"{Fore.RED}Please ensure you have an internet connection and try running the script again.{Style.RESET_ALL}")
                exit() # Exit if essential data can't be downloaded

# --- Global NLTK Analyzer ---
# Initialize VADER once
try:
    analyzer = SentimentIntensityAnalyzer()
except LookupError:
    print(f"{Fore.YELLOW}VADER lexicon not found initially. Attempting download...{Style.RESET_ALL}")
    download_nltk_data() # Make sure VADER is downloaded
    analyzer = SentimentIntensityAnalyzer() # Try initializing again

# --- Existing Functions (Modified where needed) ---

def send_message(phone_number, message):
    """Send a WhatsApp message to the given phone number."""
    try:
        # Increased wait_time slightly for more reliability
        kit.sendwhatmsg_instantly(phone_number, message, wait_time=10, tab_close=True, close_time=3)
        logging.info(f"Message sent: {message}")
        print(f"{Fore.GREEN}Message sent: {message}{Style.RESET_ALL}")
        # Add a small delay after sending
        time.sleep(5)
    except Exception as e:
        logging.error(f"Failed to send message: {e}")
        print(f"{Fore.RED}Failed to send message: {e}{Style.RESET_ALL}")
        # Consider adding more specific error handling if needed

def speak_text(text):
    """Convert text to speech."""
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"{Fore.YELLOW}Could not initialize text-to-speech: {e}{Style.RESET_ALL}")


# Modified to use NLTK VADER
def analyze_sentiment_nltk(text):
    """Analyze the sentiment of a given text using NLTK VADER."""
    vs = analyzer.polarity_scores(text)
    compound_score = vs['compound']
    if compound_score >= 0.05:
        return "Positive", compound_score
    elif compound_score <= -0.05:
        return "Negative", compound_score
    else:
        return "Neutral", compound_score

# Heavily modified to use NLTK and response dictionary
def suggest_response_nltk(reply_text):
    """Provide a dynamic response suggestion based on NLTK analysis of the reply."""
    sentiment, score = analyze_sentiment_nltk(reply_text)
    tokens = word_tokenize(reply_text.lower())
    responses = get_nltk_responses() # Load potential responses

    # Basic Keyword/Structure Checks
    if '?' in reply_text:
        return random.choice(responses["question"])
    if any(word in tokens for word in ['sorry', 'apologies', 'apologize', 'my bad']):
         return random.choice(responses["apology"])
    if any(word in tokens for word in ['thank you', 'thanks', 'appreciate it']):
         return random.choice(responses["gratitude"])

    # Sentiment-Based Checks
    if sentiment == "Positive" and score > 0.6: # Strong positive
        return random.choice(responses["strong_positive"])
    elif sentiment == "Negative" and score < -0.6: # Strong negative
        return random.choice(responses["strong_negative"])
    elif sentiment == "Neutral":
         return random.choice(responses["neutral"])
    else: # General positive/negative or fallback
        # You could add more specific responses for mild positive/negative here if desired
        return random.choice(responses["default"])


def random_characters():
    """Generate a random string under 250 characters."""
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+ ', k=random.randint(50, 200))) # Increased min length slightly

def persist_random_messages(phone_number, duration, frequency_range):
    """Send random characters repeatedly based on user-defined duration and frequency."""
    start_time = time.time()
    end_time = start_time + duration
    print(f"{Fore.CYAN}Starting random message persistence for {duration} seconds... Press Ctrl+C to stop early.{Style.RESET_ALL}")
    try:
        while time.time() < end_time:
            message = random_characters()
            send_message(phone_number, message)
            # Check remaining time
            time_left = end_time - time.time()
            if time_left <= 0:
                break
            # Calculate sleep time, ensuring it doesn't exceed remaining duration
            sleep_time = random.randint(*frequency_range)
            actual_sleep = min(sleep_time, time_left)
            print(f"Next message in {actual_sleep:.1f} seconds...")
            time.sleep(actual_sleep)
        print(f"{Fore.GREEN}Random message persistence finished.{Style.RESET_ALL}")
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Random message persistence stopped by user.{Style.RESET_ALL}")

def display_message_with_sentiment(message):
    """Show the message alongside its NLTK VADER sentiment in color."""
    sentiment, score = analyze_sentiment_nltk(message)
    if sentiment == "Positive":
        color = Fore.GREEN
    elif sentiment == "Negative":
        color = Fore.RED
    else: # Neutral
        color = Fore.YELLOW
    # Display score along with sentiment label
    print(f"{color}Message: {message} | Sentiment: {sentiment} (Score: {score:.2f}){Style.RESET_ALL}")

def menu(message_options):
    """Display the enhanced menu using names from the training data."""
    print(f"\n{Fore.MAGENTA}--- WhatsApp Message Menu ---{Style.RESET_ALL}")
    options = []
    # Dynamically build menu from loaded message categories
    for key, data in message_options.items():
        options.append(f"{key}. {data['name']}")

    # Add the fixed options
    options.extend([
        "4. Random Characters",
        "8. Analyze Reply & Suggest NLTK Response",
        "9. Exit"
    ])

    for option in options:
        print(Fore.CYAN + option + Style.RESET_ALL)
    speak_text("Choose an option from the menu.")

# Removed predefined_messages function, data is now in training_data.py

def main():
    """Main CLI for sending WhatsApp messages."""
    logging.basicConfig(filename="message_log.log", level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    print(f"{Fore.YELLOW}Starting WhatsApp Messenger Bot...{Style.RESET_ALL}")
    # --- Download NLTK Data ---
    download_nltk_data()

    # Load predefined messages from the external file
    messages_data = get_predefined_messages()

    # Input the phone number (add validation if desired)
    while True:
        phone_number = input("Enter your mom's phone number (with country code, e.g., +12125551212): ")
        # Basic check for '+' and digits
        if phone_number.startswith('+') and phone_number[1:].isdigit() and len(phone_number) > 10:
             break
        else:
             print(f"{Fore.RED}Invalid format. Please use international format like +1XXXXXXXXXX.{Style.RESET_ALL}")


    while True:
        menu(messages_data) # Pass loaded data to menu
        choice = input("Select an option: ")

        if choice == "9":
            print("Exiting program.")
            speak_text("Exiting program now.")
            break
        elif choice.isdigit() and int(choice) in messages_data: # Handle predefined message categories
            category_key = int(choice)
            category_data = messages_data[category_key]
            category_name = category_data["name"]
            available_messages = category_data["messages"]

            print(f"\nYou selected {category_key}. {category_name}.")
            print("Available messages:")
            for idx, msg in enumerate(available_messages, start=1):
                print(f"{Fore.BLUE}{idx}:{Style.RESET_ALL}", end=" ")
                display_message_with_sentiment(msg) # Show with sentiment

            while True:
                try:
                    message_choice_str = input(f"Choose a message number (1-{len(available_messages)}) or 'b' to go back: ")
                    if message_choice_str.lower() == 'b':
                        break
                    message_choice = int(message_choice_str)
                    if 1 <= message_choice <= len(available_messages):
                        message_to_send = available_messages[message_choice - 1]
                        print(f"{Fore.YELLOW}Preparing to send: {message_to_send}{Style.RESET_ALL}")
                        send_message(phone_number, message_to_send)
                        break # Exit message choice loop after sending
                    else:
                        print(Fore.RED + f"Invalid choice. Please enter a number between 1 and {len(available_messages)} or 'b'." + Style.RESET_ALL)
                except ValueError:
                     print(Fore.RED + "Invalid input. Please enter a number or 'b'." + Style.RESET_ALL)

        elif choice == "4":
            print(Fore.CYAN + "You selected Random Characters." + Style.RESET_ALL)
            try:
                duration = int(input("How long should this persist (in seconds)? "))
                min_frequency = int(input("Minimum time between messages (in seconds): "))
                max_frequency = int(input("Maximum time between messages (in seconds): "))
                if min_frequency <= 0 or max_frequency <= 0 or max_frequency < min_frequency or duration <= 0:
                    print(f"{Fore.RED}Invalid time values. Please enter positive numbers, max frequency >= min frequency.{Style.RESET_ALL}")
                    continue
                persist_random_messages(phone_number, duration, (min_frequency, max_frequency))
            except ValueError:
                print(f"{Fore.RED}Invalid input. Please enter numbers for duration and frequency.{Style.RESET_ALL}")

        elif choice == "8":
            print(Fore.CYAN + "You selected Analyze Reply & Suggest NLTK Response." + Style.RESET_ALL)
            reply = input("Enter your mom's reply message: ")
            if not reply:
                print(f"{Fore.YELLOW}No reply entered.{Style.RESET_ALL}")
                continue

            sentiment, score = analyze_sentiment_nltk(reply) # Use NLTK version
            suggestion = suggest_response_nltk(reply) # Use NLTK version

            # Determine color based on sentiment
            if sentiment == "Positive":
                color = Fore.GREEN
            elif sentiment == "Negative":
                color = Fore.RED
            else: # Neutral
                color = Fore.YELLOW

            print(f"Reply Sentiment: {color}{sentiment} (Score: {score:.2f}){Style.RESET_ALL}")
            print(f"Suggested NLTK-based Response: {Fore.GREEN}{suggestion}{Style.RESET_ALL}")
            speak_text(f"The reply sentiment is {sentiment}. A suggested response is: {suggestion}")


        else:
            print(Fore.RED + "Invalid option. Please select a valid menu item." + Style.RESET_ALL)
            speak_text("Invalid option chosen.")

if __name__ == "__main__":
    main()
