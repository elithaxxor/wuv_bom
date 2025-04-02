#### NLTK + OPENAI 
```markdown
# WhatsApp Messaging CLI Tool

This CLI tool allows you to send WhatsApp messages, generate dynamic responses, and perform sentiment analysis. The script is designed for sending messages to your mom with various predefined categories and features persistent random message sending.

## Features

- **Send WhatsApp Messages**: Instantly send messages via WhatsApp.
- **Text-to-Speech**: Convert text to speech using `pyttsx3`.
- **Sentiment Analysis**: Analyze sentiment using Hugging Face's Transformers.
- **Dynamic Response Generation**: Generate responses using Hugging Face's GPT-2 model and OpenAI's GPT-3.
- **Persistent Random Messaging**: Continuously send random characters for a specified duration.
- **Predefined Message Categories**: Choose from loving, understanding, apologetic, encouraging, funny, and more.

## Setup

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/elithaxxor/wuv_bom
    cd wuv_bom/CLI/V3
    ```

2. **Install Requirements**:
    Create a `requirements.txt` file with the following content:
    ```
    pywhatkit
    textblob
    pyttsx3
    colorama
    transformers
    openai
    ```
    Then install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set OpenAI API Key**:
    Replace `"YOUR_OPENAI_API_KEY"` in the script with your actual OpenAI API key:
    ```python
    openai.api_key = "YOUR_OPENAI_API_KEY"
    ```

## Usage

Run the script:
```bash
python main.py
```

Follow the on-screen menu to choose options for sending messages, generating responses, or starting/stopping random messaging.

### Menu Options

1. **Loving Quotes**
2. **Understanding Remarks**
3. **Express Anger**
4. **Start Random Characters**
5. **Apologetic Messages**
6. **Encouraging Messages**
7. **Funny/Lighthearted Messages**
8. **Analyze Reply Sentiment & Suggest Response**
9. **Stop Random Messaging**
10. **Exit**

### Example

1. Enter your mom's phone number with the country code (e.g., `+1XXXXXXXXXX`).
2. Choose an option from the menu (e.g., **1. Loving Quotes**).
3. Select a predefined message to send.
4. Follow prompts for any additional input (e.g., duration for random messaging).

## Notes

- Ensure you have `Google Chrome` installed as `pywhatkit` uses it to send WhatsApp messages.
- The tool logs all messages to `message_log.log`.

## License

This project is licensed under the MIT License.
```

Feel free to customize the `README.md` further to suit your needs.
