import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

class Config:
    # =============================================================================
    # Gemini 配置
    # =============================================================================
    # Gemini API 密钥
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # Gemini LLM 模型名称
    # 可选: gemini-2.5-flash, gemini-2.5-flash-lite, gemini-3-flash-preview,
    #       gemini-3-pro-preview, gemini-3.1-pro-preview, gemini-flash-latest 等
    GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-flash")


    # =============================================================================
    # Zhipu AI 配置
    # =============================================================================
    # 智谱 API 密钥
    ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY")

    # 智谱 GLM 模型名称
    # 可选: glm-4.7-flash, glm-4.7, glm-4-plus, glm-z1-plus 等
    ZHIPU_MODEL_NAME = os.getenv("ZHIPU_MODEL_NAME", "glm-4.7-flash")

    # =============================================================================
    # 302.AI 配置
    # =============================================================================
    # 302.AI API 密钥
    # 302.AI 是一个 AI 模型聚合平台，提供 OpenAI 兼容格式的统一 API
    # 官方文档: https://302ai.apifox.cn/api-147522041
    # 价格: https://302.ai/price
    THIRTYTWO_API_KEY = os.getenv("THIRTYTWO_API_KEY")

    # 302.AI 模型名称
    # 302.AI 支持多种模型，包括 Gemini、GPT、Claude、智谱等
    # 常用 Gemini 模型（推荐）:
    #   - gemini-2.5-flash                    # 快速响应版（推荐）
    #   - gemini-2.5-pro                      # 专业版
    #   - gemini-3-pro-preview                # 第三代专业版预览
    #   - gemini-2.5-flash-preview-05-20      # Flash 预览版
    #   - gemini-2.5-flash-lite-preview-06-17 # Flash 轻量版
    #   - gemini-2.5-pro-preview-06-05        # Pro 预览版
    # 更多模型请参考: https://doc.302.ai/147522041e0
    THIRTYTWO_MODEL_NAME = os.getenv("THIRTYTWO_MODEL_NAME", "gemini-2.5-flash")

    # =============================================================================
    # 302.AI 图片生成配置
    # =============================================================================
    # Gemini 图片编辑 API 密钥（如不配置则使用 THIRTYTWO_API_KEY）
    THIRTYTWO_GEMINI_IMAGE_API_KEY = os.getenv("THIRTYTWO_GEMINI_IMAGE_API_KEY")

    # Gemini 图片编辑模型名称
    # 可用模型: gemini-3.1-flash-image-preview (Nano-Banana-2)
    # 文档: https://doc.302.ai/420136728e0
    THIRTYTWO_GEMINI_IMAGE_MODEL = os.getenv("THIRTYTWO_GEMINI_IMAGE_MODEL", "gemini-3.1-flash-image-preview")

    # Doubao 即梦 API 密钥（如不配置则使用 THIRTYTWO_API_KEY）
    THIRTYTWO_DOUBAO_API_KEY = os.getenv("THIRTYTWO_DOUBAO_API_KEY")

    # Doubao 即梦模型名称
    # 可用模型: doubao-seedream-5-0-260128
    # 文档: https://doc.302.ai/419295548e0
    THIRTYTWO_DOUBAO_MODEL = os.getenv("THIRTYTWO_DOUBAO_MODEL", "doubao-seedream-5-0-260128")

    # =============================================================================
    # Debug 模式
    # =============================================================================
    DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() in ("true", "1", "on")

# 导出配置实例或直接导出变量
config = Config()
