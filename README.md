# Panaversity Gemini AI Assistant

This project is an AI chatbot assistant built with [Chainlit](https://www.chainlit.io/) and Google's Gemini API, designed to provide helpful responses to user queries in a conversational interface.

## Features
- Uses Gemini API via OpenAI-compatible endpoints
- Maintains chat history for context-aware conversations
- Real-time streaming of assistant responses
- Modular agent and configuration setup

## Requirements
- Python 3.8+
- Gemini API key (see below)

## Setup

1. **Clone the repository:**
   ```sh
   git clone https://github.com/mkrashid2003/chatbot.git
   cd chatbot
   ```

2. **Install dependencies:**
   ```sh
   uv pip install -r requirements.txt
   # or, if using pyproject.toml:
   uv pip install .
   ```

3. **Set up your environment:**
   - Copy `.env.example` to `.env` and add your Gemini API key:
     ```env
     GEMINI_API_KEY=your_gemini_api_key_here
     ```

4. **Run the chatbot:**
   ```sh
   chainlit run main.py
   ```
   Then open the provided local URL in your browser.

## File Structure
- `main.py` — Main application logic and Chainlit callbacks
- `pyproject.toml` — Project dependencies and metadata
- `.env` — Environment variables (not committed)
- `.chainlit/` — Chainlit configuration and translations

## Usage
- Start the app and interact with the assistant in your browser.
- The assistant will respond using the Gemini API and maintain context throughout the conversation.

## License
MIT License

---

**Note:** Ensure your Gemini API key is valid and has access to the Gemini endpoints. For more information, see the [Gemini API documentation](https://ai.google.dev/gemini-api/docs/openai).
