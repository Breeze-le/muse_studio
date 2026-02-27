import logging
import os
from datetime import datetime


def get_project_root():
    """获取项目根目录的绝对路径"""
    # 当前文件是 src/backend/utils.py
    # 向上三级到达项目根目录
    current_file = os.path.abspath(__file__)
    return os.path.dirname(os.path.dirname(os.path.dirname(current_file)))


def setup_logging(name="muse_studio", log_dir=None):
    """配置日志，同时输出到控制台和文件

    Args:
        name: logger 名称
        log_dir: 日志目录路径，默认为项目根目录下的 logs 文件夹
    """
    # 默认使用项目根目录下的 logs 文件夹
    if log_dir is None:
        project_root = get_project_root()
        log_dir = os.path.join(project_root, "logs")

    # 确保日志目录存在
    os.makedirs(log_dir, exist_ok=True)

    # 生成日志文件名（带时间戳）
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"app_{timestamp}.log")

    # 配置日志格式
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 创建 logger
    logger = logging.getLogger(name)

    # 避免重复配置：如果已经有 handlers 且已设置过 level，直接返回
    if logger.handlers and logger.level != logging.NOTSET:
        return logger

    # 设置日志级别为 DEBUG（捕获所有级别的日志）
    logger.setLevel(logging.DEBUG)

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # 文件处理器
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # 添加处理器
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


logger = setup_logging()
