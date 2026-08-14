"""Test configuration and fixtures for py_lead_generation."""

import pytest


@pytest.fixture
def sample_location() -> str:
    """Return a sample location for testing."""
    return "San Francisco, CA"


@pytest.fixture
def sample_query() -> str:
    """Return a sample search query for testing."""
    return "restaurants"
