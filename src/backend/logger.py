import logging
import os
from datetime import datetime


def get_project_root():
    """获取项目根目录的绝对路径"""
    # 当前文件是 src/backend/logger.py
    # 向上三级到达项目根目录
    current_file = os.path.abspath(__file__)
    return os.path.dirname(os.path.dirname(os.path.dirname(current_file)))


def setup_logging(name="muse_studio", log_dir=None, debug_mode=None):
    """配置日志，同时输出到控制台和文件

    Args:
        name: logger 名称
        log_dir: 日志目录路径，默认为项目根目录下的 logs 文件夹
        debug_mode: 是否启用 debug 模式，控制台输出 DEBUG 级别日志
    """
    # 延迟导入 config 避免循环依赖
    if debug_mode is None:
        from src.backend.config import config
        debug_mode = config.DEBUG_MODE

    # 默认使用项目根目录下的 logs 文件夹
    if log_dir is None:
        project_root = get_project_root()
        log_dir = os.path.join(project_root, "logs")

    # 确保日志目录存在
    os.makedirs(log_dir, exist_ok=True)

    # 使用日期作为日志文件名，一天一个文件
    date_str = datetime.now().strftime("%Y%m%d")
    log_file = os.path.join(log_dir, f"app_{date_str}.log")

    # 配置日志格式
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 创建 logger
    logger = logging.getLogger(name)

    # 避免重复配置：如果已经有 handlers，直接返回
    if logger.handlers:
        return logger

    # 设置日志级别为 DEBUG（捕获所有级别的日志）
    logger.setLevel(logging.DEBUG)

    # 控制台处理器 - 根据 DEBUG_MODE 决定日志级别
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if debug_mode else logging.INFO)
    console_handler.setFormatter(formatter)

    # 文件处理器 - 使用追加模式
    file_handler = logging.FileHandler(log_file, encoding="utf-8", mode="a")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # 添加处理器
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


logger = setup_logging()
