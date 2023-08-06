"""
Test LLMFactory

Usage:
    pytest src/tests/test_llm_factory.py -v --log-cli-level INFO
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from llm_factory.llm_factory import LLMFactory
from langchain.chat_models import ChatOpenAI
import pytest

from dotenv import load_dotenv


load_dotenv(override=True)


@pytest.fixture
def llm_factory():
    return LLMFactory()


def test_build_llm(llm_factory):
    llm = llm_factory.build_llm(
        LLMFactory.LLM_OPENAI_CHAT_NAME, model_name="model_name", temperature=0.5, max_tokens=10)
    assert isinstance(llm, ChatOpenAI)
