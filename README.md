# Instagram Bot

This is a Python-based Instagram bot designed to automate actions such as logging in and commenting on posts. The bot uses Selenium for web automation.

## Features

- Logs into Instagram with provided credentials.
- Automatically comments on recent posts based on predefined comments.
- Manages multiple accounts and handles login errors.

## Requirements

- Python 3.x
- Selenium
- Chrome WebDriver

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/instagram-bot-python.git
    cd instagram-bot-python
    ```

2. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Add your Instagram credentials and comments:

    - Create a `credentials.json` file in the root directory:

        ```json
        {
            "users": [
                {"username": "your_username1", "password": "your_password1"},
                {"username": "your_username2", "password": "your_password2"}
            ]
        }
        ```

    - Create a `comments.csv` file in the root directory with your comments, each comment on a new line.

## Usage

Run the bot with the following command:

```bash
python instabot.py
```

The bot will log in using the provided credentials and start commenting on recent posts.

