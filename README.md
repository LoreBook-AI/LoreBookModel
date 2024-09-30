# LorebookModel

This project implements a mystical storyteller for Dungeons and Dragons, using the Anthropic API to generate responses based on the Realm of Aethoria. The system maintains conversation context across messages to reduce token usage.

## Features

- Utilizes the Anthropic API for generating story responses.
- Maintains conversation history for each connection to optimize token usage.
- Provides a web interface for interacting with the storyteller.

## Requirements

- Python 3.8+
- `websockets` library
- `dotenv` library
- `flask` library
- Anthropic API key

## Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/LorebookModel.git
    cd LorebookModel
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Create a `.env` file and add your Anthropic API key:**

    ```
    API_KEY=your_anthropic_api_key
    ```

## Running the Server

1. **Start the WebSocket server:**

    ```bash
    python getLore.py
    ```

2. **Start the Flask web server:**

    ```bash
    python client.py
    ```

3. **Access the web interface:**

    Open your browser and go to `http://localhost:5000`.

## File Structure

- `getLore.py`: Handles the WebSocket server and interactions with the Anthropic API.
- `client.py`: Implements the Flask web server for user interaction.
- `templates/index.html`: HTML template for the web interface.

## Code Overview

### `getLore.py`

This script handles the WebSocket server, manages conversation history, and interacts with the Anthropic API.

- **Global Variables:**
  - `api_key`: Loaded from the `.env` file.
  - `client`: Anthropic client initialized with the API key.
  - `lore_context`: The initial context for the storyteller.
  - `conversation_histories`: Dictionary to store conversation history for each WebSocket connection.

- **Functions:**
  - `anthropic_request(prompt_text, websocket)`: Sends a message to the Anthropic API and maintains conversation history.
  - `handler(websocket, path)`: Handles incoming WebSocket messages and sends responses back.

### `client.py`

This script implements a Flask web server for user interaction.

- **Functions:**
  - `get_websocket()`: Ensures an active WebSocket connection.
  - `send_message(prompt_text)`: Sends a message via WebSocket and receives the response.
  - `index()`: Handles GET and POST requests to the web interface.

## Notes

- Conversation histories are cleaned up when a WebSocket connection is closed to avoid memory leaks.
- The initial context and system messages are sent only once per WebSocket connection, reducing token usage.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
