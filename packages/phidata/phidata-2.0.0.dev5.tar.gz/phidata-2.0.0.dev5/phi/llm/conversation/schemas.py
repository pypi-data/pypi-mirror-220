from typing import Optional, Any
from pydantic import BaseModel


class Message(BaseModel):
    """
    Message class for holding LLM messages.
    """

    # The role of the messages author.
    # One of system, user, assistant, or function.
    role: str
    # The contents of the message. content is required for all messages,
    # and may be null for assistant messages with function calls.
    content: str
    # The name of the author of this message. name is required if role is function,
    # and it should be the name of the function whose response is in the content.
    # May contain a-z, A-Z, 0-9, and underscores, with a maximum length of 64 characters.
    name: Optional[str] = None
    # The name and arguments of a function that should be called, as generated by the model.
    function_call: Optional[Any] = None
