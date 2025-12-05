
import os
from openai import OpenAI
from dotenv import load_dotenv
import anthropic

load_dotenv()

# OpenAI
openai_client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Claude (Anthropic)
claude_client = anthropic.Anthropic(
    api_key=os.environ.get("CLAUDE_API_KEY"),
)
