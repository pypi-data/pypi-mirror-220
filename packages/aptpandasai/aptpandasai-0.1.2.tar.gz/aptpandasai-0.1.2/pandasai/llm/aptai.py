""" Starcoder LLM
This module is to run the StartCoder API hosted and maintained by HuggingFace.co.
To generate HF_TOKEN go to https://huggingface.co/settings/tokens after creating Account
on the platform.

Example:
    Use below example to call Starcoder Model

    >>> from pandasai.llm.starcoder import Starcoder
"""


import os
from typing import Optional

from dotenv import load_dotenv

from ..exceptions import APIKeyNotFoundError
from .base import HuggingFaceLLM

load_dotenv()


class Starcoder(HuggingFaceLLM):

    """AptAI LLM API

    """

    api_token: str
    _api_url: str = "https://api.apttechsols.com/api/service/llm/v3"
    _max_retries: int = 5

    def __init__(self, api_token: Optional[str] = None):
        """
        __init__ method of AptAI Class
        Args:
            api_token (str): API token from AptAI platform
        """

        self.api_token = api_token or os.getenv("APT_API_KEY") or None
        if self.api_token is None:
            raise APIKeyNotFoundError("APT Hub API key is required")

    @property
    def type(self) -> str:
        return "aptai"
