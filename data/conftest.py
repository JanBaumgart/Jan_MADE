import pytest

def pytest_configure(config):
    config.addinivalue_line("markers", "dependency: mark a test as a dependency")
