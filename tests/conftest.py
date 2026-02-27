import logging
import os

import pytest

from src.backend.logger import logger


def pytest_runtest_setup(item):
    """测试开始前的钩子"""
    logger.info(f"[TEST START] {item.nodeid}")


def pytest_runtest_call(item):
    """测试执行中的钩子"""
    logger.debug(f"[TEST RUNNING] {item.nodeid}")


def pytest_runtest_teardown(item, nextitem):
    """测试结束后的钩子"""
    logger.info(f"[TEST END] {item.nodeid}")


def pytest_runtest_logreport(report):
    """测试结果报告钩子"""
    if report.when == "call":
        if report.passed:
            logger.info(f"[TEST PASSED] {report.nodeid}")
        elif report.failed:
            logger.error(f"[TEST FAILED] {report.nodeid}")
            if report.longrepr:
                logger.error(f"Failure details: {report.longrepr}")
        elif report.skipped:
            logger.warning(f"[TEST SKIPPED] {report.nodeid}")


@pytest.fixture(autouse=True)
def test_logger(request):
    """为每个测试提供日志功能"""
    test_name = request.node.name
    logger.debug(f"Starting test: {test_name}")
    yield
    logger.debug(f"Finished test: {test_name}")
