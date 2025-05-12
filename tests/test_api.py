import os
from src.main import get_chat_response

def test_get_chat_response():
    # Skip if no API key (to avoid running on CI without key)
    if not os.getenv("OPENAI_API_KEY"):
        return
    response = get_chat_response("Hello, world!")
    assert isinstance(response, str)
    assert len(response) > 0