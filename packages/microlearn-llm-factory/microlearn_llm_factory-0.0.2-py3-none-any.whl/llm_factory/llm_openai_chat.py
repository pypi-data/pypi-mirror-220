"""
LLM wrapper for OpenAI chat model.
"""

from langchain.chat_models import ChatOpenAI

from llm_factory.llm_base import LLMBase


class LLMOpenAIChat(LLMBase):
    """
    LLM wrapper for OpenAI chat model.
    """

    def _validate_args(self, **kwargs):
        assert "model_name" in kwargs, "'model_name' must be provided"
        assert "temperature" in kwargs, "'temperature' must be provided"
        assert "max_tokens" in kwargs, "'max_tokens' must be provided"
        if "verbose" in kwargs:
            assert isinstance(kwargs["verbose"],
                              bool), "'verbose' must be a boolean"

    def _build_llm(self, **kwargs):
        llm = ChatOpenAI(
            model=kwargs["model_name"],
            temperature=kwargs["temperature"],
            max_tokens=kwargs["max_tokens"],
            verbose=kwargs.get("verbose", False),
        )
        return llm
