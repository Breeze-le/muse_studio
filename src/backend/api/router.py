"""
Provider API 路由

提供统一的 RESTful API 端点来访问 LLM/Image/Video Provider。
API 入参根据各 Provider 的 ParamSpec.exposed 动态决定。
"""

import os
import time
import uuid
from typing import Any

from fastapi import APIRouter, Body, File, UploadFile
from pydantic import BaseModel, Field

from src.backend.services.provider_service import (
    ImageService,
    LLMService,
    VideoService,
)


# =============================================================================
# 请求/响应模型
# =============================================================================


class LLMGenerateRequest(BaseModel):
    """LLM 生成请求

    参数根据各 Provider 的 ParamSpec.exposed 动态决定：
    - zhipu: thinking_enabled
    - gemini: thinking_level
    - thirtytwo: 无暴露参数
    """

    vendor: str = Field(
        ...,
        description="厂商名称 (zhipu, gemini, thirtytwo)",
        examples=["zhipu"],
    )
    prompt: str = Field(
        ...,
        description="输入提示词",
        examples=["请写一首关于春天的诗"],
    )
    parameters: dict[str, Any] = Field(
        default_factory=dict,
        description="厂商特定参数，需根据 Provider 的 exposed_params 提供",
    )


class ImageGenerateRequest(BaseModel):
    """Image 生成请求

    参数根据各 Provider 的 ParamSpec.exposed 动态决定：
    - thirtytwo_nano_banana: images, resolution, aspect_ratio
    - thirtytwo_seedream: image, aspect_ratio
    """

    vendor: str = Field(
        ...,
        description="厂商名称 (thirtytwo_nano_banana, thirtytwo_seedream)",
        examples=["thirtytwo_nano_banana"],
    )
    prompt: str = Field(
        ...,
        description="图片描述提示词",
        examples=["一只可爱的橘猫，坐在窗台上"],
    )
    parameters: dict[str, Any] = Field(
        default_factory=dict,
        description="厂商特定参数，需根据 Provider 的 exposed_params 提供",
    )


class VideoGenerateRequest(BaseModel):
    """Video 生成请求

    参数根据各 Provider 的 ParamSpec.exposed 动态决定：
    - thirtytwo_kling: images, model_name, mode, aspect_ratio, duration
    """

    vendor: str = Field(
        ...,
        description="厂商名称 (thirtytwo_kling)",
        examples=["thirtytwo_kling"],
    )
    prompt: str = Field(
        ...,
        description="视频描述提示词",
        examples=["让画面中的云朵缓缓移动"],
    )
    parameters: dict[str, Any] = Field(
        default_factory=dict,
        description="厂商特定参数，需根据 Provider 的 exposed_params 提供",
    )


class GenerateResponse(BaseModel):
    """统一生成响应"""

    success: bool = Field(..., description="是否成功")
    content: Any | None = Field(None, description="生成内容")
    format: str | None = Field(None, description="内容格式")
    error: str | None = Field(None, description="错误信息")
    vendor: str = Field(..., description="使用的厂商")
    model: str | None = Field(None, description="使用的模型")


class ProviderInfo(BaseModel):
    """Provider 信息"""

    vendor: str = Field(..., description="厂商名称")
    model: str = Field(..., description="模型名称")
    available: bool = Field(..., description="是否可用")
    info: dict[str, Any] = Field(..., description="Provider 详细信息")


class ProvidersListResponse(BaseModel):
    """Provider 列表响应"""

    llm: list[ProviderInfo] = Field(default_factory=list, description="LLM Provider 列表")
    image: list[ProviderInfo] = Field(default_factory=list, description="Image Provider 列表")
    video: list[ProviderInfo] = Field(default_factory=list, description="Video Provider 列表")


# =============================================================================
# 路由定义
# =============================================================================

router = APIRouter(
    prefix="/api/v1",
    tags=["providers"],
)


# -----------------------------------------------------------------------------
# LLM 端点
# -----------------------------------------------------------------------------

@router.post("/llm/generate", response_model=GenerateResponse)
async def generate_llm(request: LLMGenerateRequest) -> dict[str, Any]:
    """LLM 文本生成

    调用指定厂商的 LLM 模型生成文本内容。

    ### 参数说明

    通过 `GET /api/v1/llm/providers` 查看每个厂商的 `info.exposed_params`，
    仅可传入暴露的参数，未暴露的参数将被忽略。

    ### 各厂商暴露参数

    | 厂商 | 暴露参数 |
    |------|----------|
    | zhipu | thinking_enabled |
    | gemini | thinking_level |
    | thirtytwo | 无暴露参数 |

    ### 请求示例

    ```json
    {
      "vendor": "zhipu",
      "prompt": "请写一首关于春天的诗",
      "parameters": {
        "thinking_enabled": true
      }
    }
    ```
    """
    result = LLMService.generate(
        vendor=request.vendor,
        prompt=request.prompt,
        **request.parameters,
    )

    return result


@router.get("/llm/providers", response_model=list[ProviderInfo])
async def list_llm_providers() -> list[dict[str, Any]]:
    """获取所有 LLM Provider 信息

    返回所有已注册的 LLM Provider 及其状态。

    响应中的 `info.exposed_params` 列表包含该 Provider 允许通过 API 传入的参数。
    """
    return LLMService.get_providers()


# -----------------------------------------------------------------------------
# Image 端点
# -----------------------------------------------------------------------------

@router.post("/image/generate", response_model=GenerateResponse)
async def generate_image(request: ImageGenerateRequest) -> dict[str, Any]:
    """Image 图片生成

    调用指定厂商的图像模型生成图片。

    ### 参数说明

    通过 `GET /api/v1/image/providers` 查看每个厂商的 `info.exposed_params`，
    仅可传入暴露的参数，未暴露的参数将被忽略。

    ### 各厂商暴露参数

    | 厂商 | 暴露参数 |
    |------|----------|
    | thirtytwo_nano_banana | images, resolution, aspect_ratio |
    | thirtytwo_seedream | image, aspect_ratio |

    ### 请求示例

    ```json
    {
      "vendor": "thirtytwo_nano_banana",
      "prompt": "一只可爱的橘猫",
      "parameters": {
        "resolution": "2k",
        "aspect_ratio": "16:9"
      }
    }
    ```
    """
    result = ImageService.generate(
        vendor=request.vendor,
        prompt=request.prompt,
        return_format="base64",
        **request.parameters,
    )

    return result


@router.get("/image/providers", response_model=list[ProviderInfo])
async def list_image_providers() -> list[dict[str, Any]]:
    """获取所有 Image Provider 信息

    返回所有已注册的 Image Provider 及其状态。

    响应中的 `info.exposed_params` 列表包含该 Provider 允许通过 API 传入的参数。
    """
    return ImageService.get_providers()


# -----------------------------------------------------------------------------
# Video 端点
# -----------------------------------------------------------------------------

@router.post("/video/generate", response_model=GenerateResponse)
async def generate_video(request: VideoGenerateRequest) -> dict[str, Any]:
    """Video 视频生成

    调用指定厂商的视频模型生成视频。

    ### 参数说明

    通过 `GET /api/v1/video/providers` 查看每个厂商的 `info.exposed_params`，
    仅可传入暴露的参数，未暴露的参数将被忽略。

    ### 各厂商暴露参数

    | 厂商 | 暴露参数 |
    |------|----------|
    | thirtytwo_kling | images, model_name, mode, aspect_ratio, duration |

    ### 请求示例

    ```json
    {
      "vendor": "thirtytwo_kling",
      "prompt": "让画面中的云朵缓缓移动",
      "parameters": {
        "aspect_ratio": "16:9",
        "duration": 5
      }
    }
    ```
    """
    result = VideoService.generate(
        vendor=request.vendor,
        prompt=request.prompt,
        return_format="base64",
        **request.parameters,
    )

    return result


@router.get("/video/providers", response_model=list[ProviderInfo])
async def list_video_providers() -> list[dict[str, Any]]:
    """获取所有 Video Provider 信息

    返回所有已注册的 Video Provider 及其状态。

    响应中的 `info.exposed_params` 列表包含该 Provider 允许通过 API 传入的参数。
    """
    return VideoService.get_providers()


# -----------------------------------------------------------------------------
# 图片上传端点
# -----------------------------------------------------------------------------

@router.post("/upload/image")
async def upload_image(file: UploadFile = File(...)) -> dict[str, Any]:
    """上传图片到 OSS，返回永久 URL

    接收 multipart/form-data 格式的图片文件，上传至阿里云 OSS，
    返回可公开访问的永久 URL。用于将画布选中图片转为 URL 传给 AI Provider。
    """
    from src.backend.utils import BucketCommand, DEFAULT_OSS_CONFIG

    try:
        oss_client = BucketCommand.from_str_config(DEFAULT_OSS_CONFIG)
        if not oss_client:
            return {"success": False, "error": "OSS 未配置，请检查环境变量"}

        file_bytes = await file.read()
        ext = os.path.splitext(file.filename or "image.png")[1].lstrip(".")
        if not ext:
            ext = "png"

        remote_filename = f"upload_{int(time.time())}_{uuid.uuid4()}.{ext}"
        url = oss_client.upload_file_bytes(file_bytes, remote_filename)

        return {"success": True, "url": url}
    except Exception as e:
        return {"success": False, "error": str(e)}


# -----------------------------------------------------------------------------
# 统一端点
# -----------------------------------------------------------------------------

@router.get("/providers", response_model=ProvidersListResponse)
async def list_all_providers() -> dict[str, Any]:
    """获取所有 Provider 信息

    返回所有已注册的 Provider（LLM/Image/Video）及其状态。

    响应中的 `info.exposed_params` 列表包含每个 Provider 允许通过 API 传入的参数。
    """
    from src.backend.services.provider_service import ProviderRegistry

    return ProviderRegistry.list_all_providers()
