import pywhatkit
from datetime import datetime, timedelta
import random
import string
import time
import nltk
from nltk.stem import WordNetLemmatizer
from train import train_model
import logging
import sqlite3
import pickle

# Set up logging
logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(message)s', level=logging.INFO)

# Initialize NLTK
nltk.download('wordnet')
nltk.download('omw-1.4')
lemmatizer = WordNetLemmatizer()

# Load the trained model
with open("trained_model.pkl", "rb") as f:
    model = pickle.load(f)

# Define a dictionary with hostility levels and corresponding messages
hostility_levels = {
    1: ["I love you", "You mean everything to me", "You're the best thing that's ever happened to me"],
    2: ["I'm sorry if I upset you", "I understand why you're upset", "Let's talk about what's bothering you"],
    3: ["I'm so angry with you right now", "How could you do that?", "I need some space"]
}

# Get user input for phone number
while True:
    mom_number = input("Enter the phone number (e.g. +1234567890): ")
    if mom_number.startswith('+') and len(mom_number) == 12 and mom_number[1:].isdigit():
        break
    print("Invalid phone number. Please try again.")

# Create a database connection
conn = sqlite3.connect('messages.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE IF NOT EXISTS messages
             (date text, message text, response text)''')

try:
    while True:
        # Get user input for hostility level
        print("Select a hostility level:")
        print("1. Loving")
        print("2. Understanding")
        print("3. Angry")
        print("4. Random characters")
        hostility_level = int(input("Enter the number of your chosen hostility level: "))

        if hostility_level == 4:
            # Get user input for duration and frequency
            duration_minutes = int(input("Enter the duration in minutes: "))
            frequency_minutes = int(input("Enter the frequency in minutes: "))

            # Send random characters at the specified frequency for the specified duration
            end_time = datetime.now() + timedelta(minutes=duration_minutes)
            while datetime.now() < end_time:
                message = ''.join(random.choice(string.ascii_letters) for _ in range(random.randint(1, 250)))
                pywhatkit.sendwhatmsg(mom_number, message, datetime.now().hour, datetime.now().minute)
                logging.info(f"Sent message: {message}")
                print(f"Sent message: {message}")
                time.sleep(frequency_minutes * 60 + random.randint(1, 60))  # Add a random delay to avoid sending at the same time

        else:
            # Get a random message from the selected hostility level
            message = random.choice(hostility_levels[hostility_level])

            # Get user input for time and date
            date_str = input("Enter the date (YYYY-MM-DD): ")
            time_str = input("Enter the time (HH:MM): ")

            # Parse the input date and time
            date_time = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")

            # Send the WhatsApp message
            pywhatkit.sendwhatmsg(mom_number, message, date_time.hour, date_time.minute)
            logging.info(f"Sent message: {message}")
            print(f"Sent message: {message}")

            # Wait for a response and respond using the trained model
            response = input("Enter the response from WhatsApp: ")
            response = lemmatizer.lemmatize(response)
            predicted_response = model.predict([response])
            logging.info(f"Received response: {response}, Predicted response: {predicted_response}")
            print(f"Received response: {response}, Predicted response: {predicted_response}")

            # Send the predicted response back to the user
            pywhatkit.sendwhatmsg(mom_number, predicted_response, datetime.now().hour, datetime.now().minute)
            logging.info(f"Sent response: {predicted_response}")
            print(f"Sent response: {predicted_response}")

            # Save the message and response to the database
            c.execute("INSERT INTO messages VALUES (?, ?, ?)", (date_str, message, response))
            conn.commit()

except KeyboardInterrupt:
    print("\nExiting program...")
    conn.close()
