from langchain.schema import BaseMessage
import json

def normalize_response_text(raw_response) -> str:
    """
    Normalize the raw LLM response into a string for parsing.
    Handles BaseMessage, dict, list, and plain string cases.
    """

    # 1. BaseMessage case
    if isinstance(raw_response, BaseMessage):
        return str(raw_response.content)

    # 2. Has .content attribute (some LLM SDKs wrap messages like this)
    if hasattr(raw_response, "content"):
        return str(raw_response.content)

    # 3. Dict → JSON string
    if isinstance(raw_response, dict):
        return json.dumps(raw_response)

    # 4. List → join items (or JSON dump if complex types)
    if isinstance(raw_response, list):
        if all(isinstance(item, str) for item in raw_response):
            return "\n".join(raw_response)
        return json.dumps(raw_response)

    # 5. Already string
    if isinstance(raw_response, str):
        return raw_response

    # 6. Fallback
    return str(raw_response)
