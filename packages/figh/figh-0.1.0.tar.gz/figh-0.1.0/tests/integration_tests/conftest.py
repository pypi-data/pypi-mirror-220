import os

import pytest
from dotenv import load_dotenv


@pytest.fixture(scope="session")
def setup_test_env():
    load_dotenv()
