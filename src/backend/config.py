import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

class Config:
    # Gemini 配置
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "gemini-3.1-pro-preview")

    # OpenAI 配置（预留）
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "gpt-4o")

    # Anthropic 配置（预留）
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    ANTHROPIC_MODEL_NAME = os.getenv("ANTHROPIC_MODEL_NAME", "claude-sonnet-4-20250514")

    # Zhipu AI 配置
    ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY")
    ZHIPU_MODEL_NAME = os.getenv("ZHIPU_MODEL_NAME", "glm-4.7")

# 导出配置实例或直接导出变量
config = Config()
