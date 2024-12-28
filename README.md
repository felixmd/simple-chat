# Simple Chat Interface

A flexible and extensible chat interface that supports multiple LLM providers including OpenAI's GPT models and DeepSeek. This project provides a clean implementation for integrating various chat models with rate limiting and configuration management.

## Features

- 🤖 Multi-model support (GPT-3.5, GPT-4, DeepSeek)
- 🔄 Built-in rate limiting
- ⚙️ Easy configuration management
- 🔑 Secure API key handling
- 💬 Clean chat interface

## Setup

1. Clone the repository:
```bash
git clone https://github.com/felixmd/simple-chat.git
cd simple_chat
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with your API keys:
```
OPENAI_API_KEY=your_openai_api_key
DEEPSEEK_API_KEY=your_deepseek_api_key
```

## Project Structure

```
simple_chat/
├── components/          # UI components
│   ├── chat_interface.py
│   └── sidebar.py
├── models/             # Data models
│   ├── conversation.py
│   ├── message.py
│   └── conversation_manager.py
├── services/          # Service layer
│   ├── api_client.py
│   └── rate_limiter.py
└── utils/            # Utility functions
    └── config.py
```

## Configuration

The project supports multiple chat models through the `config.py` file. Current supported models:
- ChatGPT (gpt-3.5-turbo)
- ChatGPT-O1 (gpt-4)
- DeepSeek

You can configure model-specific settings in `utils/config.py`.

## Usage

The chat interface provides a simple way to interact with different language models:

```python
from utils.config import create_api_client

# Initialize the client for a specific model
client = create_api_client("ChatGPT")

# Use the chat interface
# (Add specific usage examples based on your implementation)
```

## Rate Limiting

The service includes built-in rate limiting to prevent API abuse and manage costs. Rate limits are configurable per model in the rate limiter service.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Add your chosen license]

## Support

[Add support information/contact details] 