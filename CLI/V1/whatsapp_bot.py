import pywhatkit as kit
import random, time, sys, os, logging 
from datetime import datetime
import pyttsx3
from colorama import Fore, Style, init as colorama_init
import sqlite3 # Import SQLite library

# --- NLTK Imports ---
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize

# --- Custom Module Import ---
from training_data import get_predefined_messages, get_nltk_responses

# --- Initialize Colorama ---
colorama_init(autoreset=True)

# --- Constants ---
DB_NAME = 'chat_log.db' # Define database name centrally

# --- NLTK Data Download ---
def download_nltk_data():
    """Downloads necessary NLTK data if not already present."""
    required_data = [('sentiment/vader_lexicon.zip', 'vader_lexicon'),
                     ('tokenizers/punkt', 'punkt')]
    for path, pkg_id in required_data:
        try:
            nltk.data.find(path)
            logging.info(f"NLTK data '{pkg_id}' found.")
            # print(f"{Fore.GREEN}NLTK data '{pkg_id}' found.{Style.RESET_ALL}") # Less verbose console
        except LookupError:
            print(f"{Fore.YELLOW}NLTK data '{pkg_id}' not found. Downloading...{Style.RESET_ALL}")
            logging.warning(f"NLTK data '{pkg_id}' not found. Attempting download.")
            try:
                nltk.download(pkg_id)
                print(f"{Fore.GREEN}Successfully downloaded '{pkg_id}'.{Style.RESET_ALL}")
                logging.info(f"Successfully downloaded NLTK data '{pkg_id}'.")
            except Exception as e:
                print(f"{Fore.RED}Error downloading NLTK data '{pkg_id}': {e}{Style.RESET_ALL}")
                logging.error(f"Error downloading NLTK data '{pkg_id}': {e}", exc_info=True)
                print(f"{Fore.RED}Please ensure you have an internet connection and try running the script again.{Style.RESET_ALL}")
                exit()

# --- Global NLTK Analyzer ---
try:
    analyzer = SentimentIntensityAnalyzer()
except LookupError:
    print(f"{Fore.YELLOW}VADER lexicon not found initially. Attempting download...{Style.RESET_ALL}")
    download_nltk_data()
    analyzer = SentimentIntensityAnalyzer()

# --- Database Functions ---
def init_db(db_path=DB_NAME):
    """Initializes the SQLite database and creates the interactions table if it doesn't exist."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                interaction_type TEXT NOT NULL CHECK(interaction_type IN ('SENT', 'RECEIVED_REPLY', 'RANDOM_SENT', 'ERROR')),
                phone_number TEXT,
                message_content TEXT,
                sentiment_label TEXT,
                sentiment_score REAL,
                suggested_response TEXT,
                error_details TEXT
            )
        ''')
        conn.commit()
        logging.info(f"Database '{db_path}' initialized successfully. Table 'interactions' ready.")
        print(f"{Fore.GREEN}Database '{db_path}' initialized successfully.{Style.RESET_ALL}")
    except sqlite3.Error as e:
        logging.error(f"Database Error during initialization: {e}", exc_info=True)
        print(f"{Fore.RED}Database Error during initialization: {e}{Style.RESET_ALL}")
    finally:
        if conn:
            conn.close()

def log_interaction_to_db(conn, interaction_data):
    """Logs a single interaction record to the database."""
    sql = ''' INSERT INTO interactions(timestamp, interaction_type, phone_number, message_content, sentiment_label, sentiment_score, suggested_response, error_details)
              VALUES(datetime('now', 'localtime'),?,?,?,?,?,?,?) '''
    try:
        cursor = conn.cursor()
        # Ensure all potential keys exist, defaulting to None if not present
        data_tuple = (
            interaction_data.get('type'),
            interaction_data.get('phone'),
            interaction_data.get('content'),
            interaction_data.get('sentiment'),
            interaction_data.get('score'),
            interaction_data.get('suggestion'),
            interaction_data.get('error')
        )
        cursor.execute(sql, data_tuple)
        conn.commit()
        logging.info(f"Logged interaction (Type: {interaction_data.get('type')}) to database.")
        # print(f"DEBUG: Logged interaction to DB: {interaction_data.get('type')}") # Optional debug print
    except sqlite3.Error as e:
        logging.error(f"Database Error logging interaction: {e} - Data: {interaction_data}", exc_info=True)
        print(f"{Fore.RED}Database Error logging interaction: {e}{Style.RESET_ALL}")

# --- Core Functions (Modified for DB Logging) ---

def send_message(conn, phone_number, message): # Added conn parameter
    """Send a WhatsApp message and log it to the database."""
    success = False
    error_info = None
    try:
        # Increased wait_time slightly for more reliability
        kit.sendwhatmsg_instantly(phone_number, message, wait_time=10, tab_close=True, close_time=3)
        log_entry = {
            "type": "SENT",
            "phone": phone_number,
            "content": message
        }
        log_interaction_to_db(conn, log_entry)
        logging.info(f"Message sent successfully via pywhatkit: {message}")
        print(f"{Fore.GREEN}Message sent: {message}{Style.RESET_ALL}")
        success = True
        time.sleep(5) # Small delay after sending
    except Exception as e:
        error_info = str(e)
        logging.error(f"Failed to send message via pywhatkit: {e}", exc_info=True)
        print(f"{Fore.RED}Failed to send message: {e}{Style.RESET_ALL}")
        # Log error to DB
        log_entry = {
            "type": "ERROR",
            "phone": phone_number,
            "content": f"Failed to send: {message}",
            "error": error_info
        }
        log_interaction_to_db(conn, log_entry)
    return success

def speak_text(text):
    """Convert text to speech."""
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        engine.stop() # Explicitly stop engine
    except Exception as e:
        print(f"{Fore.YELLOW}Could not initialize/run text-to-speech: {e}{Style.RESET_ALL}")
        logging.warning(f"Text-to-speech error: {e}", exc_info=True)


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

def suggest_response_nltk(reply_text):
    """Provide a dynamic response suggestion based on NLTK analysis of the reply."""
    sentiment, score = analyze_sentiment_nltk(reply_text)
    try:
        tokens = word_tokenize(reply_text.lower())
    except Exception as e:
        logging.warning(f"Could not tokenize reply for suggestion: {e}")
        tokens = reply_text.lower().split() # Fallback basic split

    responses = get_nltk_responses() # Load potential responses

    # Basic Keyword/Structure Checks
    if '?' in reply_text:
        return random.choice(responses["question"])
    if any(word in tokens for word in ['sorry', 'apologies', 'apologize', 'my bad']):
         return random.choice(responses["apology"])
    if any(word in tokens for word in ['thank you', 'thanks', 'appreciate it', 'grateful']):
         return random.choice(responses["gratitude"])

    # Sentiment-Based Checks
    if sentiment == "Positive" and score > 0.6: # Strong positive
        return random.choice(responses["strong_positive"])
    elif sentiment == "Negative" and score < -0.6: # Strong negative
        return random.choice(responses["strong_negative"])
    elif sentiment == "Neutral":
         return random.choice(responses["neutral"])
    else: # General positive/negative or fallback
        return random.choice(responses["default"])


def random_characters():
    """Generate a random string under 250 characters."""
    # Adjusted characters slightly
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,!?'
    return ''.join(random.choices(chars, k=random.randint(20, 150)))

def persist_random_messages(conn, phone_number, duration, frequency_range): # Added conn parameter
    """Send random characters repeatedly and log each to DB."""
    start_time = time.time()
    end_time = start_time + duration
    print(f"{Fore.CYAN}Starting random message persistence for {duration} seconds... Press Ctrl+C to stop early.{Style.RESET_ALL}")
    logging.info(f"Starting random message persistence: Duration={duration}s, Freq={frequency_range}s")
    try:
        while time.time() < end_time:
            message = random_characters()
            # Try to send message, log success/failure inside send_message
            if send_message(conn, phone_number, message): # send_message now handles its own DB logging
                pass # Logging done inside send_message
            else:
                print(f"{Fore.YELLOW}Skipping sleep due to send failure.{Style.RESET_ALL}")
                continue # Don't sleep if send failed

            # Check remaining time
            time_left = end_time - time.time()
            if time_left <= 0:
                break
            # Calculate sleep time, ensuring it doesn't exceed remaining duration
            sleep_time = random.randint(*frequency_range)
            actual_sleep = min(sleep_time, time_left)
            print(f"Next random message in {actual_sleep:.1f} seconds...")
            time.sleep(actual_sleep)
        print(f"{Fore.GREEN}Random message persistence finished.{Style.RESET_ALL}")
        logging.info("Random message persistence finished.")
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Random message persistence stopped by user.{Style.RESET_ALL}")
        logging.info("Random message persistence stopped by user.")

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
    # speak_text("Choose an option from the menu.") # Can be noisy

def main():
    """Main CLI for sending WhatsApp messages with DB logging."""
    # --- Setup Logging ---
    logging.basicConfig(filename="message_log.log", level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    logging.info("Application Started")
    print(f"{Fore.YELLOW}Starting WhatsApp Messenger Bot... Check 'message_log.log' for detailed logs.{Style.RESET_ALL}")

    # --- Download NLTK Data ---
    download_nltk_data()

    # --- Initialize Database ---
    init_db(DB_NAME) # Create DB and table if they don't exist

    # --- Load Predefined Messages ---
    messages_data = get_predefined_messages()

    # --- Get Phone Number ---
    while True:
        phone_number = input("Enter recipient's phone number (with country code, e.g., +12125551212): ")
        if phone_number.startswith('+') and phone_number[1:].isdigit() and len(phone_number) > 10:
             logging.info(f"Using phone number: {phone_number}")
             break
        else:
             print(f"{Fore.RED}Invalid format. Please use international format like +1XXXXXXXXXX.{Style.RESET_ALL}")
             logging.warning(f"Invalid phone number format entered: {phone_number}")

    # --- Database Connection ---
    conn = None # Initialize conn
    try:
        conn = sqlite3.connect(DB_NAME)
        logging.info(f"Successfully connected to database '{DB_NAME}'.")
        print(f"{Fore.GREEN}Database connection successful.{Style.RESET_ALL}")

        # --- Main Application Loop ---
        while True:
            menu(messages_data) # Pass loaded data to menu
            choice = input("Select an option: ")
            logging.info(f"User selected menu option: {choice}")

            if choice == "9":
                print("Exiting program.")
                speak_text("Exiting program now.")
                logging.info("User chose to exit.")
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
                        message_choice_str = input(f"Choose message number (1-{len(available_messages)}) or 'b' to go back: ")
                        if message_choice_str.lower() == 'b':
                            logging.info("User chose to go back from message selection.")
                            break
                        message_choice = int(message_choice_str)
                        if 1 <= message_choice <= len(available_messages):
                            message_to_send = available_messages[message_choice - 1]
                            print(f"{Fore.YELLOW}Preparing to send: {message_to_send}{Style.RESET_ALL}")
                            logging.info(f"User chose message {message_choice} from category {category_key}: '{message_to_send}'")
                            send_message(conn, phone_number, message_to_send) # Pass conn
                            break # Exit message choice loop after attempting send
                        else:
                            print(Fore.RED + f"Invalid choice. Please enter a number between 1 and {len(available_messages)} or 'b'." + Style.RESET_ALL)
                            logging.warning(f"Invalid message choice entered: {message_choice_str}")
                    except ValueError:
                         print(Fore.RED + "Invalid input. Please enter a number or 'b'." + Style.RESET_ALL)
                         logging.warning(f"Invalid input type for message choice: {message_choice_str}")

            elif choice == "4":
                print(Fore.CYAN + "You selected Random Characters." + Style.RESET_ALL)
                try:
                    duration = int(input("How long should this persist (in seconds)? "))
                    min_frequency = int(input("Minimum time between messages (in seconds): "))
                    max_frequency = int(input("Maximum time between messages (in seconds): "))
                    if min_frequency <= 0 or max_frequency <= 0 or max_frequency < min_frequency or duration <= 0:
                        print(f"{Fore.RED}Invalid time values. Please enter positive numbers, max frequency >= min frequency.{Style.RESET_ALL}")
                        logging.warning(f"Invalid parameters for random persistence: dur={duration}, minf={min_frequency}, maxf={max_frequency}")
                        continue
                    logging.info(f"Starting random message persistence requested by user: dur={duration}, minf={min_frequency}, maxf={max_frequency}")
                    persist_random_messages(conn, phone_number, duration, (min_frequency, max_frequency)) # Pass conn
                except ValueError:
                    print(f"{Fore.RED}Invalid input. Please enter numbers for duration and frequency.{Style.RESET_ALL}")
                    logging.warning("Invalid input type for random persistence parameters.")

            elif choice == "8":
                print(Fore.CYAN + "You selected Analyze Reply & Suggest NLTK Response." + Style.RESET_ALL)
                reply = input("Enter the reply message received: ")
                logging.info(f"User entered reply for analysis: '{reply}'")
                if not reply:
                    print(f"{Fore.YELLOW}No reply entered.{Style.RESET_ALL}")
                    logging.warning("User submitted empty reply for analysis.")
                    continue

                sentiment, score = analyze_sentiment_nltk(reply) # Use NLTK version
                suggestion = suggest_response_nltk(reply) # Use NLTK version

                # Determine color based on sentiment
                if sentiment == "Positive": color = Fore.GREEN
                elif sentiment == "Negative": color = Fore.RED
                else: color = Fore.YELLOW # Neutral

                print(f"Reply Sentiment: {color}{sentiment} (Score: {score:.2f}){Style.RESET_ALL}")
                print(f"Suggested NLTK-based Response: {Fore.GREEN}{suggestion}{Style.RESET_ALL}")
                # speak_text(f"The reply sentiment is {sentiment}. A suggested response is: {suggestion}") # Optional TTS

                # Log this interaction to DB
                log_entry = {
                    "type": "RECEIVED_REPLY",
                    "phone": phone_number, # Assuming reply is from the main recipient
                    "content": reply,
                    "sentiment": sentiment,
                    "score": score,
                    "suggestion": suggestion
                }
                log_interaction_to_db(conn, log_entry)

            else:
                print(Fore.RED + "Invalid option. Please select a valid menu item." + Style.RESET_ALL)
                # speak_text("Invalid option chosen.") # Optional TTS
                logging.warning(f"Invalid menu option entered: {choice}")

    except sqlite3.Error as e:
        # Catch DB errors during the main loop if connection fails later
        print(f"{Fore.RED}\n--- CRITICAL DATABASE ERROR --- \n{e}\nExiting program.{Style.RESET_ALL}")
        logging.critical(f"Critical database error encountered in main loop: {e}", exc_info=True)
    except Exception as e:
        # Catch any other unexpected errors
        print(f"{Fore.RED}\n--- UNEXPECTED ERROR --- \n{e}\nExiting program.{Style.RESET_ALL}")
        logging.critical(f"An unexpected error occurred in the main loop: {e}", exc_info=True)
    finally:
        # --- Close Database Connection ---
        if conn:
            conn.close()
            logging.info("Database connection closed.")
            print(f"{Fore.YELLOW}Database connection closed.{Style.RESET_ALL}")
        logging.info("Application Ended")

if __name__ == "__main__":
    main()
